#!/usr/bin/env python3
"""Read-only structural audit for lecture PPTX packages.

This checker validates package integrity, relationships, slide/notes mapping,
note hygiene, and file stability. It does not render slides or validate facts.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import math
import os
import posixpath
import re
import sys
import tempfile
import unicodedata
import zipfile
from collections import Counter
from contextlib import ExitStack
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET


PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
OFFICE_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
MC_NS = "http://schemas.openxmlformats.org/markup-compatibility/2006"
P14_NS = "http://schemas.microsoft.com/office/powerpoint/2010/main"
VML_OFFICE_NS = "urn:schemas-microsoft-com:office:office"
VML_NS = "urn:schemas-microsoft-com:vml"
CHART_NS = "http://schemas.openxmlformats.org/drawingml/2006/chart"
DIAGRAM_NS = "http://schemas.openxmlformats.org/drawingml/2006/diagram"
A14_NS = "http://schemas.microsoft.com/office/drawing/2010/main"
SVG_NS = "http://schemas.microsoft.com/office/drawing/2016/SVG/main"
WEBEXT_NS = "http://schemas.microsoft.com/office/webextensions/taskpanes/2010/11"

NS = {"p": P_NS, "a": A_NS, "r": OFFICE_REL_NS}
SLIDE_RE = re.compile(r"^ppt/slides/slide(\d+)\.xml$")
NOTE_RE = re.compile(r"^ppt/notesSlides/notesSlide(\d+)\.xml$")
URL_RE = re.compile(r"https?://|www\.", re.IGNORECASE)
DOI_RE = re.compile(r"\bdoi\s*:|\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
TIME_RE = re.compile(
    r"(?mi)^\s*(?:"
    r"\[(?:(?:시간|time)[^\]]*|\d{1,2}:\d{2}|\d+(?:\.\d+)?\s*(?:초|분|시간|min(?:ute)?s?|sec(?:ond)?s?|hours?))\]"
    r"|(?:배정\s*)?시간\s*:\s*\d+(?:\.\d+)?\s*(?:초|분|시간)"
    r"|time\s*:\s*\d+(?:\.\d+)?\s*(?:s(?:ec(?:ond)?s?)?|m(?:in(?:ute)?s?)?|h(?:ours?)?)"
    r"|\d{1,2}:\d{2}\s*[–—-]\s*\d{1,2}:\d{2}"
    r")\s*$"
)
SOURCE_LINE_RE = re.compile(r"(?mi)^\s*(?:출처|source|참고)\s*:")
PRODUCTION_RE = re.compile(
    r"(?:강의자\s*(?:종합|재구성)|자체\s*구성|수업용\s*프레임|제작\s*메모|"
    r"^\s*(?:도입|설명|전환|마무리)\s*:)",
    re.IGNORECASE | re.MULTILINE,
)
AUDIO_EXTENSIONS = {".aac", ".aif", ".aiff", ".m4a", ".mid", ".midi", ".mp3", ".oga", ".wav", ".wma"}
VIDEO_EXTENSIONS = {".avi", ".m4v", ".mov", ".mp4", ".mpeg", ".mpg", ".ogv", ".wmv"}
STRICT_OOXML_PREFIX = "http://purl.oclc.org/ooxml/"
PATH_CONTEXT_KEYS = {"path", "added", "removed", "baseline_path", "baseline_file", "file", "output"}
WEB_URI_SPAN_RE = re.compile(r"(?i)\b(?:https?://|mailto:)[^\s<>\"'\]\[{}]+")
POSIX_PATH_TOKEN_RE = re.compile(
    r"(?P<prefix>^|[\s\"'=:(\[<{,;])(?P<path>/(?!/)[^\s\"'<>|,;\])}?#&]+)"
)
LOCAL_PATH_TOKEN_RE = re.compile(
    r"(?i)(?<![A-Z0-9_.-])(?P<path>"
    r"file:(?://)?[^\s,;\]\[{}()?#&]+|"
    r"[A-Z]:[\\/][^\s,;\]\[{}()?#&]+|"
    r"\\\\[^\s,;\]\[{}()?#&]+)"
)
PRIVATE_FILENAME_RE = re.compile(
    r"(?i)(?P<prefix>^|[\s\"'=:\\/(\[{<])"
    r"(?P<path>[^\\/:*?\"<>|\r\n]*[\w-]\."
    r"(?:pptx|pptm|json|csv|md|ya?ml|xlsx|docx|pdf)\b"
    r")"
)
TRAVERSAL_PATH_TOKEN_RE = re.compile(
    r"(?P<path>(?:^|[\\/])\.\.(?:[\\/][^\s,;\]\[{}()?#&]*)?)"
)

REL_OFFICE_DOCUMENT = f"{OFFICE_REL_NS}/officeDocument"
REL_SLIDE = f"{OFFICE_REL_NS}/slide"
REL_NOTES_SLIDE = f"{OFFICE_REL_NS}/notesSlide"
REL_SLIDE_LAYOUT = f"{OFFICE_REL_NS}/slideLayout"
REL_SLIDE_MASTER = f"{OFFICE_REL_NS}/slideMaster"
REL_NOTES_MASTER = f"{OFFICE_REL_NS}/notesMaster"
REL_HANDOUT_MASTER = f"{OFFICE_REL_NS}/handoutMaster"
REL_THEME = f"{OFFICE_REL_NS}/theme"
REL_THEME_OVERRIDE = f"{OFFICE_REL_NS}/themeOverride"
REL_HYPERLINK = f"{OFFICE_REL_NS}/hyperlink"
REL_IMAGE = f"{OFFICE_REL_NS}/image"
REL_AUDIO = f"{OFFICE_REL_NS}/audio"
REL_VIDEO = f"{OFFICE_REL_NS}/video"
REL_MEDIA = "http://schemas.microsoft.com/office/2007/relationships/media"
REL_HD_PHOTO = "http://schemas.microsoft.com/office/2007/relationships/hdphoto"
REL_VML_DRAWING = f"{OFFICE_REL_NS}/vmlDrawing"
REL_CHART = f"{OFFICE_REL_NS}/chart"
REL_FONT = f"{OFFICE_REL_NS}/font"
REL_OLE_OBJECT = f"{OFFICE_REL_NS}/oleObject"
REL_PACKAGE = f"{OFFICE_REL_NS}/package"
REL_CONTROL = f"{OFFICE_REL_NS}/control"
REL_CONTENT_PART = f"{OFFICE_REL_NS}/contentPart"
REL_DIAGRAM_DATA = f"{OFFICE_REL_NS}/diagramData"
REL_DIAGRAM_LAYOUT = f"{OFFICE_REL_NS}/diagramLayout"
REL_DIAGRAM_QUICK_STYLE = f"{OFFICE_REL_NS}/diagramQuickStyle"
REL_DIAGRAM_COLORS = f"{OFFICE_REL_NS}/diagramColors"
REL_WEB_EXTENSION = "http://schemas.microsoft.com/office/2011/relationships/webextension"
SOURCE_EXEMPTION_TYPES = {
    "navigation",
    "activity",
    "instructor_synthesis",
    "original_course_instruction",
}

MAX_JSON_BYTES = 16 * 1024 * 1024


def is_xml_ncname(value: Any) -> bool:
    """Return whether ``value`` is an XML NCName without a namespace colon."""
    if not isinstance(value, str) or not value or ":" in value:
        return False

    def start(character: str) -> bool:
        code = ord(character)
        return (
            character == "_"
            or 0x41 <= code <= 0x5A
            or 0x61 <= code <= 0x7A
            or 0xC0 <= code <= 0xD6
            or 0xD8 <= code <= 0xF6
            or 0xF8 <= code <= 0x2FF
            or 0x370 <= code <= 0x37D
            or 0x37F <= code <= 0x1FFF
            or 0x200C <= code <= 0x200D
            or 0x2070 <= code <= 0x218F
            or 0x2C00 <= code <= 0x2FEF
            or 0x3001 <= code <= 0xD7FF
            or 0xF900 <= code <= 0xFDCF
            or 0xFDF0 <= code <= 0xFFFD
            or 0x10000 <= code <= 0xEFFFF
        )

    def continuation(character: str) -> bool:
        code = ord(character)
        return (
            start(character)
            or character in {"-", "."}
            or 0x30 <= code <= 0x39
            or code == 0xB7
            or 0x300 <= code <= 0x36F
            or 0x203F <= code <= 0x2040
        )

    return start(value[0]) and all(continuation(character) for character in value[1:])


@dataclass(frozen=True)
class PackageSnapshot:
    members: set[str]
    xml_payloads: dict[str, bytes]
    member_hashes: dict[str, str]
    sha256: str | None
    size: int
    mtime_ns: int
    usable: bool

    def __iter__(self):
        # Preserve the historical three-value unpacking API for callers that
        # only need package members. New callers should also bind ``sha256``.
        yield self.members
        yield self.xml_payloads
        yield self.member_hashes


def _reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate_json_key: {key}")
        result[key] = value
    return result


def strict_json_loads(payload: bytes) -> Any:
    """Decode one bounded UTF-8 JSON snapshot with no ambiguous scalars."""
    try:
        text_payload = payload.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("JSON must be UTF-8 (optional BOM is allowed)") from exc
    def finite_float(value: str) -> float:
        parsed = float(value)
        if not math.isfinite(parsed):
            raise ValueError(f"nonfinite_json_number: {value}")
        return parsed

    try:
        return json.loads(
            text_payload,
            object_pairs_hook=_reject_duplicate_json_keys,
            parse_float=finite_float,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ValueError(f"nonfinite_json_number: {value}")
            ),
        )
    except RecursionError as exc:
        raise ValueError("json_nesting_limit_exceeded") from exc


def read_json_snapshot(path: Path, *, max_bytes: int = MAX_JSON_BYTES) -> tuple[Any, tuple[int, int, str]]:
    """Read, hash, and parse the exact same JSON bytes from one open handle."""
    resolved = path.expanduser().resolve()
    with resolved.open("rb") as handle:
        before = os.fstat(handle.fileno())
        if before.st_size > max_bytes:
            raise ValueError("json_file_size_limit_exceeded")
        payload = handle.read(max_bytes + 1)
        if len(payload) > max_bytes:
            raise ValueError("json_file_size_limit_exceeded")
        after = os.fstat(handle.fileno())
    path_after = resolved.stat()
    identity_before = (getattr(before, "st_dev", None), getattr(before, "st_ino", None))
    identity_after = (getattr(path_after, "st_dev", None), getattr(path_after, "st_ino", None))
    if (
        (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns)
        or (before.st_size, before.st_mtime_ns) != (path_after.st_size, path_after.st_mtime_ns)
        or (all(value is not None for value in (*identity_before, *identity_after)) and identity_before != identity_after)
    ):
        raise ValueError("json_input_drift_during_read")
    digest = hashlib.sha256(payload).hexdigest()
    return strict_json_loads(payload), (before.st_size, before.st_mtime_ns, digest)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def discover(inputs: Iterable[str], excludes: Iterable[str]) -> list[Path]:
    patterns = [re.compile(pattern, re.IGNORECASE) for pattern in excludes]
    found: list[Path] = []
    for raw in inputs:
        path = Path(raw).expanduser().resolve()
        if path.is_file() and path.suffix.lower() == ".pptx":
            found.append(path)
        elif path.is_dir():
            for candidate in path.rglob("*"):
                resolved = candidate.resolve()
                if (
                    not candidate.name.startswith("~$")
                    and candidate.is_file()
                    and candidate.suffix.casefold() == ".pptx"
                    and not any(pattern.search(str(resolved)) for pattern in patterns)
                ):
                    found.append(resolved)
        else:
            raise FileNotFoundError(f"PPTX file or directory not found: {path}")
    unique = {os.path.normcase(str(p)): p for p in found}
    return sorted(unique.values(), key=lambda p: str(p).casefold())


PERCENT_ESCAPE_RE = re.compile(r"%([0-9A-Fa-f]{2})")
OPC_PCHAR_RE = re.compile(r"^(?:[A-Za-z0-9._~!$&'()*+,;=:@-]|%[0-9A-Fa-f]{2})+$")
UNRESERVED_URI_BYTES = frozenset(
    b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
)


def _safe_percent_encoding(value: str) -> bool:
    """Reject ambiguous or structure-changing percent escapes.

    OPC part names are URI paths.  Encoded unreserved characters create URI
    aliases, while encoded separators, percent signs, and dot segments can
    change path structure after a consumer decodes them.
    """
    cursor = 0
    while cursor < len(value):
        if value[cursor] != "%":
            cursor += 1
            continue
        match = PERCENT_ESCAPE_RE.match(value, cursor)
        if match is None:
            return False
        decoded = int(match.group(1), 16)
        if (
            decoded in UNRESERVED_URI_BYTES
            or decoded < 0x20
            or decoded == 0x7F
            or decoded in {0x2F, 0x5C, 0x25, 0x3A, 0x3F, 0x23}
        ):
            return False
        cursor = match.end()
    return True


def canonical_opc_part_key(name: str, *, allow_directory: bool = False) -> str | None:
    """Return a canonical archive-part key, or ``None`` when OPC-unsafe."""
    if not isinstance(name, str) or not name or "\\" in name:
        return None
    is_directory = name.endswith("/")
    if is_directory:
        if not allow_directory:
            return None
        name = name[:-1]
    if (
        not name
        or name.startswith("/")
        or "?" in name
        or "#" in name
        or any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in name)
        or not _safe_percent_encoding(name)
    ):
        return None
    segments = name.split("/")
    if any(
        segment in {"", ".", ".."}
        or segment.endswith(".")
        or OPC_PCHAR_RE.fullmatch(segment) is None
        for segment in segments
    ):
        return None
    normalized = unicodedata.normalize("NFC", name)
    normalized = PERCENT_ESCAPE_RE.sub(lambda match: f"%{match.group(1).upper()}", normalized)
    try:
        normalized = unicodedata.normalize("NFC", unquote(normalized, errors="strict"))
    except UnicodeDecodeError:
        return None
    if any(ord(char) < 32 or ord(char) == 127 for char in normalized):
        return None
    if any(segment in {"", ".", ".."} or segment.endswith(".") for segment in normalized.split("/")):
        return None
    return normalized + ("/" if is_directory else "")


def safe_member_name(name: str) -> bool:
    return name == "[Content_Types].xml" or canonical_opc_part_key(name, allow_directory=True) is not None


def safe_internal_relationship_target(source_part: str, target: str) -> tuple[bool, str]:
    """Validate an internal OPC URI reference and return its resolved part."""
    if (
        not isinstance(target, str)
        or not target
        or "\\" in target
        or "?" in target
        or "#" in target
        or target.startswith("//")
        or any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in target)
        or not _safe_percent_encoding(target)
    ):
        return False, target
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        return False, target
    path_text = target[1:] if target.startswith("/") else target
    if any(
        segment in {"", "."}
        or (segment != ".." and (segment.endswith(".") or OPC_PCHAR_RE.fullmatch(segment) is None))
        for segment in path_text.split("/")
    ):
        return False, target
    resolved = resolve_target(source_part, target)
    return canonical_opc_part_key(resolved) is not None, resolved


def relationship_source_part(rel_part: str) -> str | None:
    if rel_part == "_rels/.rels":
        return ""
    path = PurePosixPath(rel_part)
    if path.parent.name != "_rels" or not path.name.endswith(".rels"):
        return None
    return str(path.parent.parent / path.name[:-5])


def companion_relationship_part(source_part: str) -> str:
    if not source_part:
        return "_rels/.rels"
    path = PurePosixPath(source_part)
    return str(path.parent / "_rels" / f"{path.name}.rels")


def resolve_target(source_part: str, target: str) -> str:
    target = target.replace("\\", "/")
    if target.startswith("/"):
        return posixpath.normpath(target.lstrip("/"))
    base = posixpath.dirname(source_part)
    return posixpath.normpath(posixpath.join(base, target))


def repeatedly_unquote(value: str, rounds: int = 32) -> str:
    decoded = value
    for _ in range(rounds):
        next_value = unquote(decoded)
        if next_value == decoded:
            return decoded
        decoded = next_value
    # Excessively nested encodings are not safe to reproduce in reports.
    return "[redacted-local-path]" if PERCENT_ESCAPE_RE.search(decoded) else decoded


def is_external_file_target(target: str) -> bool:
    decoded = repeatedly_unquote(target.strip())
    if not decoded or any(ord(char) < 32 for char in decoded) or "\\" in decoded:
        return True
    if re.match(r"(?i)^[A-Z]:[\\/]", decoded):
        return True
    parsed = urlsplit(decoded)
    scheme = parsed.scheme.lower()
    if scheme in {"http", "https"}:
        return not (
            decoded.lower().startswith(f"{scheme}://")
            and bool(parsed.hostname)
            and not parsed.username
            and not parsed.password
        )
    if scheme == "mailto":
        address = parsed.path
        return not address or "@" not in address or any(char.isspace() for char in address)
    if scheme == "tel":
        return not bool(re.fullmatch(r"[+0-9(). -]+", parsed.path or ""))
    if decoded.startswith("//"):
        return True
    if scheme in {"file", "smb", "nfs"}:
        return True
    if decoded.startswith("\\\\"):
        return True
    if decoded.startswith("/") and not decoded.startswith("//"):
        return True
    # TargetMode=External with no recognized network scheme is a file-like
    # relative/unknown reference and is rejected fail-closed.
    return True


def _redact_plain_text_span(value: str) -> tuple[str, bool]:
    """Redact one non-URI span, decoding only when a path is actually found."""
    decoded = repeatedly_unquote(value)
    if decoded == "[redacted-local-path]":
        return decoded, True
    cleaned = LOCAL_PATH_TOKEN_RE.sub("[redacted-local-path]", decoded)
    cleaned = POSIX_PATH_TOKEN_RE.sub(
        lambda match: f"{match.group('prefix')}[redacted-local-path]", cleaned
    )
    cleaned = TRAVERSAL_PATH_TOKEN_RE.sub("[redacted-local-path]", cleaned)
    cleaned = PRIVATE_FILENAME_RE.sub(
        lambda match: f"{match.group('prefix')}[redacted-local-path]", cleaned
    )
    return (cleaned, True) if cleaned != decoded else (value, False)


def _ascii_unquote_with_origins(
    value: str, rounds: int = 32
) -> tuple[str, list[tuple[int, int]], bool]:
    """Decode nested ASCII percent escapes while retaining source offsets."""
    characters = list(value)
    origins = [(index, index + 1) for index in range(len(value))]
    for _ in range(rounds):
        next_characters: list[str] = []
        next_origins: list[tuple[int, int]] = []
        changed = False
        index = 0
        while index < len(characters):
            if (
                index + 2 < len(characters)
                and characters[index] == "%"
                and re.fullmatch(r"[0-9A-Fa-f]{2}", "".join(characters[index + 1 : index + 3]))
            ):
                byte = int("".join(characters[index + 1 : index + 3]), 16)
                if byte < 128:
                    next_characters.append(chr(byte))
                    next_origins.append((origins[index][0], origins[index + 2][1]))
                    index += 3
                    changed = True
                    continue
            next_characters.append(characters[index])
            next_origins.append(origins[index])
            index += 1
        characters, origins = next_characters, next_origins
        if not changed:
            return "".join(characters), origins, False
    saturated = any(
        characters[index] == "%"
        and index + 2 < len(characters)
        and re.fullmatch(r"[0-9A-Fa-f]{2}", "".join(characters[index + 1 : index + 3]))
        and int("".join(characters[index + 1 : index + 3]), 16) < 128
        for index in range(len(characters))
    )
    return "".join(characters), origins, saturated


def _merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    merged: list[tuple[int, int]] = []
    for start, end in sorted(intervals):
        if not merged or start > merged[-1][1]:
            merged.append((start, end))
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
    return merged


def _redact_uri_component(
    value: str,
    *,
    allow_absolute_posix: bool,
    allow_encoded_absolute_posix: bool = False,
) -> tuple[str, bool]:
    """Redact path tokens in a URI component without rewriting safe source bytes."""
    decoded, origins, saturated = _ascii_unquote_with_origins(value)
    if saturated:
        return "[redacted-local-path]", True
    decoded_intervals: list[tuple[int, int]] = []
    decoded_intervals.extend(match.span("path") for match in LOCAL_PATH_TOKEN_RE.finditer(decoded))
    decoded_intervals.extend(
        match.span("path") for match in TRAVERSAL_PATH_TOKEN_RE.finditer(decoded)
    )
    decoded_intervals.extend(match.span("path") for match in PRIVATE_FILENAME_RE.finditer(decoded))
    if allow_absolute_posix:
        decoded_intervals.extend(match.span("path") for match in POSIX_PATH_TOKEN_RE.finditer(decoded))
    if allow_encoded_absolute_posix:
        for index, character in enumerate(decoded):
            if character != "/":
                continue
            raw_start, raw_end = origins[index]
            if (
                raw_start >= raw_end
                or not value[raw_start:raw_end].startswith("%")
                or (raw_start > 0 and value[raw_start - 1] not in "/=:;,(")
            ):
                continue
            candidate = re.match(r"/(?!/)[^\s,;\]\[{}()?#&]+", decoded[index:])
            if candidate is not None:
                decoded_intervals.append((index, index + candidate.end()))
    if not decoded_intervals:
        return value, False

    raw_intervals: list[tuple[int, int]] = []
    for start, end in decoded_intervals:
        if start < end:
            raw_intervals.append((origins[start][0], origins[end - 1][1]))
    cleaned: list[str] = []
    cursor = 0
    for start, end in _merge_intervals(raw_intervals):
        cleaned.append(value[cursor:start])
        cleaned.append("[redacted-local-path]")
        cursor = end
    cleaned.append(value[cursor:])
    return "".join(cleaned), True


def _redact_uri_span(value: str) -> tuple[str, bool]:
    """Preserve a URI byte-for-byte except for sensitive component substrings."""
    fragment_at = value.find("#")
    before_fragment = value if fragment_at < 0 else value[:fragment_at]
    fragment = "" if fragment_at < 0 else value[fragment_at + 1 :]
    query_at = before_fragment.find("?")
    base = before_fragment if query_at < 0 else before_fragment[:query_at]
    query = "" if query_at < 0 else before_fragment[query_at + 1 :]

    clean_base, base_changed = _redact_uri_component(
        base,
        allow_absolute_posix=False,
        allow_encoded_absolute_posix=True,
    )
    clean_query, query_changed = _redact_uri_component(query, allow_absolute_posix=True)
    clean_fragment, fragment_changed = _redact_uri_component(
        fragment, allow_absolute_posix=True
    )
    result = clean_base
    if query_at >= 0:
        result += f"?{clean_query}"
    if fragment_at >= 0:
        result += f"#{clean_fragment}"
    return result, base_changed or query_changed or fragment_changed


def _redact_report_text(value: str) -> tuple[str, bool]:
    """Redact URI and non-URI spans independently without placeholder collisions."""
    cleaned: list[str] = []
    changed = False
    cursor = 0
    for match in WEB_URI_SPAN_RE.finditer(value):
        plain, plain_changed = _redact_plain_text_span(value[cursor : match.start()])
        uri, uri_changed = _redact_uri_span(match.group(0))
        cleaned.extend((plain, uri))
        changed = changed or plain_changed or uri_changed
        cursor = match.end()
    plain, plain_changed = _redact_plain_text_span(value[cursor:])
    cleaned.append(plain)
    changed = changed or plain_changed
    return "".join(cleaned), changed


def redact_report_value(value: Any, context_key: str | None = None) -> tuple[Any, int]:
    """Redact local-path-bearing strings recursively before report emission."""
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        count = 0
        for key, item in value.items():
            cleaned, item_count = redact_report_value(item, key)
            result[key] = cleaned
            count += item_count
        return result, count
    if isinstance(value, list):
        result_list: list[Any] = []
        count = 0
        for item in value:
            cleaned, item_count = redact_report_value(item, context_key)
            result_list.append(cleaned)
            count += item_count
        return result_list, count
    if isinstance(value, tuple):
        cleaned, count = redact_report_value(list(value), context_key)
        return cleaned, count
    if isinstance(value, str):
        if context_key in PATH_CONTEXT_KEYS:
            return "[redacted-local-path]", 1
        cleaned, changed = _redact_report_text(value)
        if changed:
            return cleaned, 1
    return value, 0


def emit_json(payload: dict[str, Any], redact_paths: bool) -> str:
    if redact_paths:
        cleaned, redacted_count = redact_report_value(payload)
        assert isinstance(cleaned, dict)
        cleaned["redaction_applied"] = True
        cleaned["redacted_field_count"] = redacted_count
        payload = cleaned
    else:
        payload = dict(payload)
        payload["redaction_applied"] = False
        payload["redacted_field_count"] = 0
    return json.dumps(payload, ensure_ascii=False, indent=2)


def parse_xml(name: str, payload: bytes, errors: list[dict[str, Any]]) -> ET.Element | None:
    try:
        pending_namespaces: list[tuple[str, str]] = []
        scopes: list[dict[str, str]] = [
            {"xml": "http://www.w3.org/XML/1998/namespace"}
        ]
        namespace_scope_by_element: dict[int, dict[str, str]] = {}
        parser = ET.iterparse(io.BytesIO(payload), events=("start-ns", "start", "end"))
        for event, item in parser:
            if event == "start-ns":
                prefix, uri = item
                pending_namespaces.append((prefix or "", uri))
            elif event == "start":
                scope = dict(scopes[-1])
                scope.update(pending_namespaces)
                pending_namespaces.clear()
                namespace_scope_by_element[id(item)] = scope
                scopes.append(scope)
            else:
                scopes.pop()
        root = parser.root
    except ET.ParseError as exc:
        errors.append({"code": "xml_parse_error", "part": name, "detail": str(exc)})
        return None
    for alternate in root.iter(f"{{{MC_NS}}}AlternateContent"):
        children = list(alternate)
        choice_tag = f"{{{MC_NS}}}Choice"
        fallback_tag = f"{{{MC_NS}}}Fallback"
        choices = [child for child in children if child.tag == choice_tag]
        fallbacks = [child for child in children if child.tag == fallback_tag]
        if any(child.tag not in {choice_tag, fallback_tag} for child in children):
            errors.append({"code": "alternatecontent_child_invalid", "part": name})
        if not choices:
            errors.append({"code": "alternatecontent_choice_missing", "part": name})
        if len(fallbacks) > 1 or (fallbacks and children[-1].tag != fallback_tag):
            errors.append({"code": "alternatecontent_fallback_invalid", "part": name})
        for choice in choices:
            requires = (choice.get("Requires") or "").strip()
            if not requires:
                errors.append({"code": "alternatecontent_choice_requires_missing", "part": name})
                continue
            tokens = requires.split()
            scope = namespace_scope_by_element.get(id(choice), {})
            if (
                len(tokens) != len(set(tokens))
                or any(not is_xml_ncname(token) or token not in scope for token in tokens)
            ):
                errors.append(
                    {
                        "code": "alternatecontent_choice_requires_invalid",
                        "part": name,
                        "requires": requires,
                    }
                )
        if any(not list(branch) for branch in [*choices, *fallbacks]):
            errors.append({"code": "alternatecontent_empty_branch", "part": name})
    return root


def strict_ooxml_parts(
    roots: dict[str, ET.Element], payloads: dict[str, bytes] | None = None
) -> list[str]:
    strict: list[str] = []
    needle = STRICT_OOXML_PREFIX.encode("ascii")
    if payloads:
        strict.extend(name for name, payload in payloads.items() if needle in payload)
    for name, root in roots.items():
        if any(
            str(element.tag).startswith(f"{{{STRICT_OOXML_PREFIX}")
            for element in root.iter()
        ) or any(
            attribute.startswith(f"{{{STRICT_OOXML_PREFIX}")
            or (isinstance(value, str) and STRICT_OOXML_PREFIX in value)
            for element in root.iter()
            for attribute, value in element.attrib.items()
        ):
            strict.append(name)
    return sorted(set(strict))


def read_members(
    path: Path, errors: list[dict[str, Any]], args: argparse.Namespace
) -> PackageSnapshot:
    size = 0
    mtime_ns = 0
    try:
        with ExitStack() as resources:
            package_handle = resources.enter_context(path.open("rb"))
            snapshot_handle = resources.enter_context(
                tempfile.SpooledTemporaryFile(max_size=64 * 1024 * 1024, mode="w+b")
            )
            opened = os.fstat(package_handle.fileno())
            size, mtime_ns = opened.st_size, opened.st_mtime_ns
            max_package = getattr(args, "max_package_mb", 1024) * 1024 * 1024
            if size > max_package:
                errors.append(
                    {"code": "package_file_size_limit_exceeded", "bytes": size, "limit": max_package}
                )
                return PackageSnapshot(set(), {}, {}, None, size, mtime_ns, False)
            package_digest = hashlib.sha256()
            copied_bytes = 0
            for block in iter(lambda: package_handle.read(1024 * 1024), b""):
                copied_bytes += len(block)
                if copied_bytes > max_package:
                    errors.append(
                        {
                            "code": "package_file_size_limit_exceeded",
                            "bytes": copied_bytes,
                            "limit": max_package,
                        }
                    )
                    return PackageSnapshot(set(), {}, {}, None, size, mtime_ns, False)
                package_digest.update(block)
                snapshot_handle.write(block)
            if copied_bytes != opened.st_size:
                errors.append({"code": "input_drift_during_package_snapshot"})
                return PackageSnapshot(set(), {}, {}, None, size, mtime_ns, False)
            package_sha = package_digest.hexdigest()
            snapshot_handle.flush()
            snapshot_handle.seek(0)
            archive = zipfile.ZipFile(snapshot_handle)
            with archive:
                infos = archive.infolist()
                names = [item.filename for item in infos]
                duplicates = sorted(name for name, count in Counter(names).items() if count > 1)
                if duplicates:
                    errors.append({"code": "duplicate_zip_members", "members": duplicates})
                unsafe = sorted(name for name in names if not safe_member_name(name))
                if unsafe:
                    errors.append({"code": "unsafe_zip_members", "members": unsafe})
                canonical_names: dict[str, str] = {}
                aliases: list[dict[str, str]] = []
                for item in infos:
                    if item.is_dir():
                        continue
                    canonical = canonical_opc_part_key(item.filename)
                    if canonical is None:
                        continue
                    canonical_lookup = canonical.casefold()
                    previous = canonical_names.get(canonical_lookup)
                    if previous is not None and previous != item.filename:
                        aliases.append(
                            {"canonical": canonical, "first": previous, "second": item.filename}
                        )
                    canonical_names[canonical_lookup] = item.filename
                if aliases:
                    errors.append({"code": "duplicate_canonical_part_name", "members": aliases[:20]})
                if duplicates or unsafe or aliases:
                    return PackageSnapshot(set(), {}, {}, package_sha, size, mtime_ns, False)
                if len(infos) > args.max_members:
                    errors.append(
                        {
                            "code": "zip_member_limit_exceeded",
                            "count": len(infos),
                            "limit": args.max_members,
                        }
                    )
                    return PackageSnapshot(set(), {}, {}, package_sha, size, mtime_ns, False)
                total_uncompressed = sum(item.file_size for item in infos)
                max_uncompressed = args.max_uncompressed_mb * 1024 * 1024
                if total_uncompressed > max_uncompressed:
                    errors.append(
                        {
                            "code": "zip_uncompressed_limit_exceeded",
                            "bytes": total_uncompressed,
                            "limit": max_uncompressed,
                        }
                    )
                    return PackageSnapshot(set(), {}, {}, package_sha, size, mtime_ns, False)
                suspicious_ratios = []
                for item in infos:
                    if item.file_size <= 0:
                        continue
                    ratio = item.file_size / max(item.compress_size, 1)
                    if ratio > args.max_compression_ratio:
                        suspicious_ratios.append({"member": item.filename, "ratio": round(ratio, 2)})
                if suspicious_ratios:
                    errors.append(
                        {
                            "code": "zip_compression_ratio_limit_exceeded",
                            "limit": args.max_compression_ratio,
                            "members": suspicious_ratios[:20],
                        }
                    )
                    return PackageSnapshot(set(), {}, {}, package_sha, size, mtime_ns, False)
                xml_limit = args.max_xml_mb * 1024 * 1024
                oversized_xml = [
                    {"member": item.filename, "bytes": item.file_size}
                    for item in infos
                    if (
                        item.filename.lower().endswith(".xml")
                        or item.filename.lower().endswith(".rels")
                        or item.filename.lower().endswith(".vml")
                    )
                    and item.file_size > xml_limit
                ]
                if oversized_xml:
                    errors.append(
                        {
                            "code": "xml_part_size_limit_exceeded",
                            "limit": xml_limit,
                            "members": oversized_xml[:20],
                        }
                    )
                    return PackageSnapshot(set(), {}, {}, package_sha, size, mtime_ns, False)
                xml_payloads: dict[str, bytes] = {}
                member_hashes: dict[str, str] = {}
                for item in infos:
                    digest = hashlib.sha256()
                    lowered_name = item.filename.lower()
                    capture_xml = lowered_name.endswith((".xml", ".rels", ".vml"))
                    captured = bytearray() if capture_xml else None
                    with archive.open(item) as member:
                        for block in iter(lambda: member.read(1024 * 1024), b""):
                            digest.update(block)
                            if captured is not None:
                                captured.extend(block)
                    member_hashes[item.filename] = digest.hexdigest()
                    if captured is not None:
                        xml_payloads[item.filename] = bytes(captured)
            closed = os.fstat(package_handle.fileno())
            path_after = path.stat()
            opened_identity = (getattr(opened, "st_dev", None), getattr(opened, "st_ino", None))
            path_identity = (getattr(path_after, "st_dev", None), getattr(path_after, "st_ino", None))
            if (
                (opened.st_size, opened.st_mtime_ns) != (closed.st_size, closed.st_mtime_ns)
                or (opened.st_size, opened.st_mtime_ns) != (path_after.st_size, path_after.st_mtime_ns)
                or (all(value is not None for value in (*opened_identity, *path_identity)) and opened_identity != path_identity)
            ):
                errors.append({"code": "input_drift_during_package_snapshot"})
                return PackageSnapshot(set(), {}, {}, package_sha, size, mtime_ns, False)
            return PackageSnapshot(set(names), xml_payloads, member_hashes, package_sha, size, mtime_ns, True)
    except (OSError, RuntimeError, NotImplementedError, zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
        errors.append({"code": "pptx_open_failure", "detail": str(exc)})
        return PackageSnapshot(set(), {}, {}, None, size, mtime_ns, False)


def validate_content_types(
    members: set[str], roots: dict[str, ET.Element], errors: list[dict[str, Any]]
) -> None:
    name = "[Content_Types].xml"
    root = roots.get(name)
    if root is None:
        errors.append({"code": "content_types_missing"})
        return
    if root.tag != f"{{{CT_NS}}}Types":
        errors.append({"code": "content_types_root_invalid", "tag": root.tag})

    defaults: dict[str, str] = {}
    overrides: dict[str, str] = {}
    default_keys: set[str] = set()
    override_keys: set[str] = set()
    for element in root:
        if element.tag == f"{{{CT_NS}}}Default":
            extension = (element.get("Extension") or "").lower()
            content_type = element.get("ContentType") or ""
            key = extension.casefold()
            if not extension or key in default_keys:
                errors.append({"code": "content_type_default_duplicate_or_empty", "extension": extension})
            if not content_type:
                errors.append({"code": "content_type_value_empty", "extension": extension})
            default_keys.add(key)
            defaults[extension] = content_type
        elif element.tag == f"{{{CT_NS}}}Override":
            raw_part = element.get("PartName") or ""
            part = raw_part[1:] if raw_part.startswith("/") and not raw_part.startswith("//") else ""
            content_type = element.get("ContentType") or ""
            canonical = canonical_opc_part_key(part) if part else None
            key = canonical.casefold() if canonical is not None else ""
            if canonical is None:
                errors.append(
                    {"code": "content_type_override_part_name_invalid", "part": raw_part}
                )
            if not part or not key or key in override_keys:
                errors.append({"code": "content_type_override_duplicate_or_empty", "part": part})
            if not content_type:
                errors.append({"code": "content_type_value_empty", "part": part})
            if part and part not in members:
                errors.append({"code": "content_type_orphan_override", "part": part})
            override_keys.add(key)
            overrides[part] = content_type
        else:
            errors.append({"code": "content_type_child_invalid", "tag": str(element.tag)})

    for member in members:
        if member == name or member.endswith("/"):
            continue
        # OPC relationship parts such as `_rels/.rels` have a dotfile-style
        # basename, so PurePosixPath reports no suffix even though the package
        # content-type extension is `rels`.
        extension = "rels" if member.endswith(".rels") else PurePosixPath(member).suffix.lower().lstrip(".")
        if member not in overrides and extension not in defaults:
            errors.append({"code": "content_type_uncovered_member", "member": member})

    expected_types = {
        "ppt/presentation.xml": "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml",
    }
    for member in members:
        if member.endswith(".rels"):
            expected_types[member] = "application/vnd.openxmlformats-package.relationships+xml"
        elif SLIDE_RE.fullmatch(member):
            expected_types[member] = "application/vnd.openxmlformats-officedocument.presentationml.slide+xml"
        elif NOTE_RE.fullmatch(member):
            expected_types[member] = "application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"
        elif re.fullmatch(r"ppt/slideLayouts/slideLayout\d+\.xml", member):
            expected_types[member] = "application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"
        elif re.fullmatch(r"ppt/slideMasters/slideMaster\d+\.xml", member):
            expected_types[member] = "application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"
        elif re.fullmatch(r"ppt/notesMasters/notesMaster\d+\.xml", member):
            expected_types[member] = "application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml"
        elif re.fullmatch(r"ppt/handoutMasters/handoutMaster\d+\.xml", member):
            expected_types[member] = "application/vnd.openxmlformats-officedocument.presentationml.handoutMaster+xml"
        elif re.fullmatch(r"ppt/theme/theme\d+\.xml", member):
            expected_types[member] = "application/vnd.openxmlformats-officedocument.theme+xml"
        elif re.fullmatch(r"ppt/theme/themeOverride\d+\.xml", member):
            expected_types[member] = "application/vnd.openxmlformats-officedocument.themeOverride+xml"
    for part, expected in expected_types.items():
        extension = "rels" if part.endswith(".rels") else PurePosixPath(part).suffix.lower().lstrip(".")
        actual = overrides.get(part, defaults.get(extension))
        if part in members and actual != expected:
            errors.append(
                {
                    "code": "core_content_type_mismatch",
                    "part": part,
                    "expected": expected,
                    "actual": actual,
                }
            )


def opc_part_role(part: str) -> str:
    if part == "":
        return "package"
    patterns = (
        (r"ppt/presentation\.xml", "presentation"),
        (r"ppt/slides/slide\d+\.xml", "slide"),
        (r"ppt/notesSlides/notesSlide\d+\.xml", "notesSlide"),
        (r"ppt/slideLayouts/slideLayout\d+\.xml", "slideLayout"),
        (r"ppt/slideMasters/slideMaster\d+\.xml", "slideMaster"),
        (r"ppt/notesMasters/notesMaster\d+\.xml", "notesMaster"),
        (r"ppt/handoutMasters/handoutMaster\d+\.xml", "handoutMaster"),
        (r"ppt/theme/theme\d+\.xml", "theme"),
        (r"ppt/theme/themeOverride\d+\.xml", "themeOverride"),
        (r"ppt/drawings/[^/]+\.vml", "vmlDrawing"),
    )
    for pattern, role in patterns:
        if re.fullmatch(pattern, part):
            return role
    if part.startswith("ppt/media/"):
        return "media"
    return "other"


def relationship_role_is_valid(source: str, rel_type: str, target: str) -> bool:
    """Validate source/target roles for relationships used by ownership logic."""
    source_role = opc_part_role(source)
    target_role = opc_part_role(target)
    allowed_pairs: dict[str, set[tuple[str, str]]] = {
        REL_OFFICE_DOCUMENT: {("package", "presentation")},
        REL_NOTES_SLIDE: {("slide", "notesSlide")},
        REL_SLIDE_LAYOUT: {
            ("slide", "slideLayout"),
            ("slideMaster", "slideLayout"),
        },
        REL_SLIDE_MASTER: {
            ("presentation", "slideMaster"),
            ("slideLayout", "slideMaster"),
        },
        REL_NOTES_MASTER: {
            ("presentation", "notesMaster"),
            ("notesSlide", "notesMaster"),
        },
        REL_HANDOUT_MASTER: {("presentation", "handoutMaster")},
        REL_THEME: {
            ("presentation", "theme"),
            ("slideMaster", "theme"),
            ("notesMaster", "theme"),
            ("handoutMaster", "theme"),
        },
        REL_THEME_OVERRIDE: {
            ("slide", "themeOverride"),
            ("slideLayout", "themeOverride"),
        },
        REL_VML_DRAWING: {
            ("slide", "vmlDrawing"),
            ("notesSlide", "vmlDrawing"),
            ("slideLayout", "vmlDrawing"),
            ("slideMaster", "vmlDrawing"),
            ("notesMaster", "vmlDrawing"),
            ("handoutMaster", "vmlDrawing"),
        },
    }
    if rel_type == REL_SLIDE:
        return target_role == "slide" and source_role in {
            "presentation",
            "slide",
            "notesSlide",
        }
    if rel_type in {REL_IMAGE, REL_AUDIO, REL_VIDEO, REL_MEDIA, REL_HD_PHOTO}:
        return source_role not in {"package", "media"} and target_role == "media"
    pairs = allowed_pairs.get(rel_type)
    # Unknown relationship types may extend the package through ordinary
    # parts, but must not impersonate a typed structural or media edge.
    return target_role == "other" if pairs is None else (source_role, target_role) in pairs


def external_relationship_role_is_valid(source: str, rel_type: str) -> bool:
    """Reject external bindings for package-only roles and invalid media sources."""
    if rel_type in {
        REL_OFFICE_DOCUMENT,
        REL_SLIDE,
        REL_NOTES_SLIDE,
        REL_SLIDE_LAYOUT,
        REL_SLIDE_MASTER,
        REL_NOTES_MASTER,
        REL_HANDOUT_MASTER,
        REL_THEME,
        REL_THEME_OVERRIDE,
        REL_VML_DRAWING,
    }:
        return False
    if rel_type in {REL_IMAGE, REL_AUDIO, REL_VIDEO, REL_MEDIA, REL_HD_PHOTO}:
        return opc_part_role(source) not in {"package", "media"}
    return True


RID = f"{{{OFFICE_REL_NS}}}id"
REMBED = f"{{{OFFICE_REL_NS}}}embed"
RLINK = f"{{{OFFICE_REL_NS}}}link"
RELATIONSHIP_REFERENCE_SCHEMA: dict[tuple[str, str], frozenset[str]] = {
    (f"{{{P_NS}}}sldId", RID): frozenset({REL_SLIDE}),
    (f"{{{P_NS}}}sldMasterId", RID): frozenset({REL_SLIDE_MASTER}),
    (f"{{{P_NS}}}notesMasterId", RID): frozenset({REL_NOTES_MASTER}),
    (f"{{{P_NS}}}handoutMasterId", RID): frozenset({REL_HANDOUT_MASTER}),
    (f"{{{P_NS}}}sldLayoutId", RID): frozenset({REL_SLIDE_LAYOUT}),
    (f"{{{A_NS}}}hlinkClick", RID): frozenset({REL_HYPERLINK, REL_SLIDE}),
    (f"{{{A_NS}}}hlinkHover", RID): frozenset({REL_HYPERLINK, REL_SLIDE}),
    (f"{{{P_NS}}}oleObj", RID): frozenset({REL_OLE_OBJECT, REL_PACKAGE}),
    (f"{{{CHART_NS}}}externalData", RID): frozenset({REL_PACKAGE}),
    (f"{{{CHART_NS}}}chart", RID): frozenset({REL_CHART}),
    (f"{{{P_NS}}}legacyDrawing", RID): frozenset({REL_VML_DRAWING}),
    (f"{{{P_NS}}}legacyDrawingHF", RID): frozenset({REL_VML_DRAWING}),
    (f"{{{P_NS}}}control", RID): frozenset({REL_CONTROL}),
    (f"{{{P_NS}}}contentPart", RID): frozenset({REL_CONTENT_PART}),
    (f"{{{P_NS}}}regular", RID): frozenset({REL_FONT}),
    (f"{{{P_NS}}}bold", RID): frozenset({REL_FONT}),
    (f"{{{P_NS}}}italic", RID): frozenset({REL_FONT}),
    (f"{{{P_NS}}}boldItalic", RID): frozenset({REL_FONT}),
    (f"{{{WEBEXT_NS}}}webextensionref", RID): frozenset({REL_WEB_EXTENSION}),
    (f"{{{A_NS}}}blip", REMBED): frozenset({REL_IMAGE, REL_HD_PHOTO}),
    (f"{{{A_NS}}}blip", RLINK): frozenset({REL_IMAGE, REL_HD_PHOTO}),
    (f"{{{A14_NS}}}imgLayer", REMBED): frozenset({REL_HD_PHOTO, REL_IMAGE}),
    (f"{{{SVG_NS}}}svgBlip", REMBED): frozenset({REL_IMAGE}),
    (f"{{{A_NS}}}audioFile", RLINK): frozenset({REL_AUDIO, REL_MEDIA}),
    (f"{{{A_NS}}}videoFile", RLINK): frozenset({REL_VIDEO, REL_MEDIA}),
    (f"{{{A_NS}}}quickTimeFile", RLINK): frozenset({REL_VIDEO, REL_MEDIA}),
    (f"{{{P14_NS}}}media", REMBED): frozenset({REL_MEDIA, REL_AUDIO, REL_VIDEO}),
    (f"{{{DIAGRAM_NS}}}relIds", f"{{{OFFICE_REL_NS}}}dm"): frozenset({REL_DIAGRAM_DATA}),
    (f"{{{DIAGRAM_NS}}}relIds", f"{{{OFFICE_REL_NS}}}lo"): frozenset({REL_DIAGRAM_LAYOUT}),
    (f"{{{DIAGRAM_NS}}}relIds", f"{{{OFFICE_REL_NS}}}qs"): frozenset({REL_DIAGRAM_QUICK_STYLE}),
    (f"{{{DIAGRAM_NS}}}relIds", f"{{{OFFICE_REL_NS}}}cs"): frozenset({REL_DIAGRAM_COLORS}),
    (f"{{{VML_NS}}}imagedata", f"{{{VML_OFFICE_NS}}}relid"): frozenset({REL_IMAGE}),
    (f"{{{VML_NS}}}fill", f"{{{VML_OFFICE_NS}}}relid"): frozenset({REL_IMAGE}),
    (f"{{{VML_NS}}}stroke", f"{{{VML_OFFICE_NS}}}relid"): frozenset({REL_IMAGE}),
}


def relationship_reference_kind(element: ET.Element, attribute: str) -> str | None:
    return attribute if (str(element.tag), attribute) in RELATIONSHIP_REFERENCE_SCHEMA else None


def is_relationship_namespace_attribute(attribute: str) -> bool:
    return attribute.startswith(f"{{{OFFICE_REL_NS}}}") or attribute == f"{{{VML_OFFICE_NS}}}relid"


def validate_relationships(
    members: set[str],
    roots: dict[str, ET.Element],
    forbid_external_file_links: bool,
    errors: list[dict[str, Any]],
) -> dict[str, dict[str, tuple[str, str]]]:
    rel_maps: dict[str, dict[str, tuple[str, str]]] = {}
    for rel_part, root in roots.items():
        if not rel_part.lower().endswith(".rels"):
            continue
        if root.tag != f"{{{PKG_REL_NS}}}Relationships":
            errors.append({"code": "relationships_root_invalid", "part": rel_part, "tag": str(root.tag)})
        source = relationship_source_part(rel_part)
        if source is None:
            errors.append({"code": "relationship_part_name_invalid", "part": rel_part})
            continue
        if source and source not in members:
            errors.append({"code": "relationship_source_missing", "part": rel_part, "source": source})
        rel_map: dict[str, tuple[str, str]] = {}
        for child in root:
            if child.tag != f"{{{PKG_REL_NS}}}Relationship":
                errors.append({"code": "relationship_child_invalid", "part": rel_part, "tag": str(child.tag)})
                continue
            rel = child
            rel_id = rel.get("Id") or ""
            target = rel.get("Target") or ""
            rel_type = rel.get("Type") or ""
            if not rel_id or rel_id in rel_map:
                errors.append({"code": "relationship_id_duplicate_or_empty", "part": rel_part, "id": rel_id})
                continue
            if not is_xml_ncname(rel_id):
                errors.append({"code": "relationship_id_invalid", "part": rel_part, "id": rel_id})
            if not target:
                errors.append({"code": "relationship_target_empty", "part": rel_part, "id": rel_id})
                continue
            if not rel_type or not urlsplit(rel_type).scheme:
                errors.append({"code": "relationship_type_invalid", "part": rel_part, "id": rel_id})
                continue
            target_mode = (rel.get("TargetMode") or "").lower()
            if target_mode not in {"", "internal", "external"}:
                errors.append(
                    {"code": "relationship_target_mode_invalid", "part": rel_part, "id": rel_id, "mode": target_mode}
                )
            if target_mode == "external":
                if not external_relationship_role_is_valid(source, rel_type):
                    errors.append(
                        {
                            "code": "relationship_type_target_role_mismatch",
                            "part": rel_part,
                            "id": rel_id,
                            "type": rel_type,
                            "target": target,
                        }
                    )
                if forbid_external_file_links and is_external_file_target(target):
                    errors.append(
                        {
                            "code": "external_file_relationship_forbidden",
                            "part": rel_part,
                            "id": rel_id,
                            "target": target,
                        }
                    )
                rel_map[rel_id] = (target, rel_type)
                continue
            target_safe, resolved = safe_internal_relationship_target(source, target)
            if not target_safe or resolved not in members:
                errors.append(
                    {
                        "code": "relationship_target_missing_or_unsafe",
                        "part": rel_part,
                        "id": rel_id,
                        "target": resolved,
                    }
                )
            if target_safe and not relationship_role_is_valid(source, rel_type, resolved):
                errors.append(
                    {
                        "code": "relationship_type_target_role_mismatch",
                        "part": rel_part,
                        "id": rel_id,
                        "type": rel_type,
                        "target": resolved,
                    }
                )
            rel_map[rel_id] = (resolved, rel_type)
        rel_maps[rel_part] = rel_map

    root_relationships = roots.get("_rels/.rels")
    if root_relationships is None:
        errors.append({"code": "package_root_relationships_missing"})
    else:
        office_document = [
            rel
            for rel in root_relationships.findall(f"{{{PKG_REL_NS}}}Relationship")
            if (rel.get("Type") or "") == REL_OFFICE_DOCUMENT
        ]
        if len(office_document) != 1:
            errors.append({"code": "package_office_document_relationship_count", "count": len(office_document)})
        else:
            rel = office_document[0]
            mode = (rel.get("TargetMode") or "").lower()
            resolved = resolve_target("", rel.get("Target") or "")
            if mode == "external" or resolved != "ppt/presentation.xml":
                errors.append(
                    {
                        "code": "package_office_document_relationship_invalid",
                        "target": rel.get("Target") or "",
                        "mode": mode or "internal",
                    }
                )

    for source_part, root in roots.items():
        if source_part.lower().endswith(".rels") or source_part == "[Content_Types].xml":
            continue
        rel_part = companion_relationship_part(source_part)
        defined = rel_maps.get(rel_part, {})
        for element in root.iter():
            for attribute, value in element.attrib.items():
                semantic_kind = relationship_reference_kind(element, attribute)
                if is_relationship_namespace_attribute(attribute) and semantic_kind is None:
                    errors.append(
                        {
                            "code": "relationship_reference_attribute_location_invalid",
                            "part": source_part,
                            "element": str(element.tag),
                            "attribute": attribute,
                        }
                    )
                elif semantic_kind is not None:
                    if not is_xml_ncname(value):
                        errors.append(
                            {
                                "code": "relationship_reference_id_invalid",
                                "part": source_part,
                                "relationship_part": rel_part,
                                "id": value,
                            }
                        )
                    if value not in defined:
                        errors.append(
                            {
                                "code": "dangling_xml_relationship_reference",
                                "part": source_part,
                                "relationship_part": rel_part,
                                "id": value,
                            }
                        )
                    else:
                        actual_type = defined[value][1]
                        expected_types = RELATIONSHIP_REFERENCE_SCHEMA[(str(element.tag), attribute)]
                        if actual_type not in expected_types:
                            errors.append(
                                {
                                    "code": "relationship_reference_type_mismatch",
                                    "part": source_part,
                                    "relationship_part": rel_part,
                                    "id": value,
                                    "type": actual_type,
                                }
                            )
    return rel_maps


PART_ROOT_QNAMES = {
    "presentation": f"{{{P_NS}}}presentation",
    "slide": f"{{{P_NS}}}sld",
    "notesSlide": f"{{{P_NS}}}notes",
    "slideLayout": f"{{{P_NS}}}sldLayout",
    "slideMaster": f"{{{P_NS}}}sldMaster",
    "notesMaster": f"{{{P_NS}}}notesMaster",
    "handoutMaster": f"{{{P_NS}}}handoutMaster",
    "theme": f"{{{A_NS}}}theme",
    "themeOverride": f"{{{A_NS}}}themeOverride",
}


def _typed_relationship_ids(
    rel_maps: dict[str, dict[str, tuple[str, str]]], source: str, rel_type: str
) -> dict[str, str]:
    return {
        rel_id: target
        for rel_id, (target, actual_type) in rel_maps.get(companion_relationship_part(source), {}).items()
        if actual_type == rel_type
    }


def _listed_relationship_ids(root: ET.Element, path: str) -> list[str]:
    return [
        element.get(f"{{{OFFICE_REL_NS}}}id") or ""
        for element in root.findall(path, NS)
    ]


def validate_required_part_topology(
    members: set[str],
    roots: dict[str, ET.Element],
    rel_maps: dict[str, dict[str, tuple[str, str]]],
    errors: list[dict[str, Any]],
) -> None:
    """Validate render-critical part roots and exact relationship topology."""
    for part in sorted(members):
        role = opc_part_role(part)
        expected_root = PART_ROOT_QNAMES.get(role)
        if expected_root is None:
            continue
        root = roots.get(part)
        if root is None:
            errors.append({"code": "required_part_xml_missing", "part": part, "role": role})
        elif root.tag != expected_root:
            errors.append(
                {
                    "code": "required_part_root_invalid",
                    "part": part,
                    "role": role,
                    "expected": expected_root,
                    "actual": str(root.tag),
                }
            )

    presentation = roots.get("ppt/presentation.xml")
    if presentation is not None and presentation.tag == PART_ROOT_QNAMES["presentation"]:
        high_ids = [
            element.get("id") or ""
            for element in presentation.findall("./p:sldMasterIdLst/p:sldMasterId", NS)
        ]
        for part, root in roots.items():
            if opc_part_role(part) == "slideMaster":
                high_ids.extend(
                    element.get("id") or ""
                    for element in root.findall("./p:sldLayoutIdLst/p:sldLayoutId", NS)
                )
        if (
            any(
                not raw_id.isdigit()
                or not (0x80000000 <= int(raw_id) <= 0xFFFFFFFF)
                for raw_id in high_ids
            )
            or len(high_ids) != len(set(high_ids))
        ):
            errors.append({"code": "presentation_master_or_layout_id_invalid_or_duplicate"})
        for path, rel_type, label in (
            ("./p:sldIdLst/p:sldId", REL_SLIDE, "slides"),
            ("./p:sldMasterIdLst/p:sldMasterId", REL_SLIDE_MASTER, "slide_masters"),
            ("./p:notesMasterIdLst/p:notesMasterId", REL_NOTES_MASTER, "notes_masters"),
            ("./p:handoutMasterIdLst/p:handoutMasterId", REL_HANDOUT_MASTER, "handout_masters"),
        ):
            listed = _listed_relationship_ids(presentation, path)
            typed = _typed_relationship_ids(rel_maps, "ppt/presentation.xml", rel_type)
            if (
                any(not rel_id for rel_id in listed)
                or len(listed) != len(set(listed))
                or len(typed.values()) != len(set(typed.values()))
                or set(listed) != set(typed)
            ):
                errors.append(
                    {
                        "code": "presentation_relationship_list_mismatch",
                        "list": label,
                        "listed": listed,
                        "relationships": sorted(typed),
                    }
                )

    for part in sorted(members):
        role = opc_part_role(part)
        required: tuple[tuple[str, int, int | None], ...] = ()
        if role == "slide":
            required = ((REL_SLIDE_LAYOUT, 1, 1),)
        elif role == "slideLayout":
            required = ((REL_SLIDE_MASTER, 1, 1),)
        elif role == "notesSlide":
            required = ((REL_NOTES_MASTER, 1, 1), (REL_SLIDE, 1, 1))
        for rel_type, minimum, maximum in required:
            count = len(_typed_relationship_ids(rel_maps, part, rel_type))
            if count < minimum or (maximum is not None and count > maximum):
                errors.append(
                    {
                        "code": "required_relationship_cardinality_invalid",
                        "part": part,
                        "type": rel_type,
                        "count": count,
                        "minimum": minimum,
                        "maximum": maximum,
                    }
                )
        if role == "slideMaster" and part in roots:
            listed = _listed_relationship_ids(roots[part], "./p:sldLayoutIdLst/p:sldLayoutId")
            typed = _typed_relationship_ids(rel_maps, part, REL_SLIDE_LAYOUT)
            if (
                not listed
                or any(not rel_id for rel_id in listed)
                or len(listed) != len(set(listed))
                or len(typed.values()) != len(set(typed.values()))
                or set(listed) != set(typed)
            ):
                errors.append(
                    {
                        "code": "slide_master_layout_list_mismatch",
                        "part": part,
                        "listed": listed,
                        "relationships": sorted(typed),
                    }
                )

    slide_parts = {part for part in members if opc_part_role(part) == "slide"}
    layout_parts = {part for part in members if opc_part_role(part) == "slideLayout"}
    master_parts = {part for part in members if opc_part_role(part) == "slideMaster"}
    notes_parts = {part for part in members if opc_part_role(part) == "notesSlide"}
    layout_to_master = {
        layout: next(
            iter(_typed_relationship_ids(rel_maps, layout, REL_SLIDE_MASTER).values()),
            "",
        )
        for layout in layout_parts
    }
    master_to_layouts = {
        master: set(_typed_relationship_ids(rel_maps, master, REL_SLIDE_LAYOUT).values())
        for master in master_parts
    }
    for layout in sorted(layout_parts):
        declared_master = layout_to_master.get(layout) or ""
        owners = sorted(
            master for master, layouts in master_to_layouts.items() if layout in layouts
        )
        if len(owners) != 1 or owners[0] != declared_master:
            errors.append(
                {
                    "code": "slide_layout_master_owner_invalid",
                    "layout": layout,
                    "declared_master": declared_master,
                    "owners": owners,
                }
            )

    layout_slide_masters = {master for master in layout_to_master.values() if master}
    presentation_slide_masters = set(
        _typed_relationship_ids(rel_maps, "ppt/presentation.xml", REL_SLIDE_MASTER).values()
    )
    if (slide_parts or layout_parts) and not presentation_slide_masters:
        errors.append({"code": "presentation_slide_master_required"})
    missing_presentation_masters = sorted(layout_slide_masters - presentation_slide_masters)
    if missing_presentation_masters:
        errors.append(
            {
                "code": "used_slide_master_not_in_presentation",
                "parts": missing_presentation_masters,
            }
        )
    used_notes_masters = {
        target
        for notes_part in notes_parts
        for target in _typed_relationship_ids(rel_maps, notes_part, REL_NOTES_MASTER).values()
    }
    presentation_notes_masters = set(
        _typed_relationship_ids(rel_maps, "ppt/presentation.xml", REL_NOTES_MASTER).values()
    )
    if notes_parts and not presentation_notes_masters:
        errors.append({"code": "presentation_notes_master_required"})
    missing_notes_masters = sorted(used_notes_masters - presentation_notes_masters)
    if missing_notes_masters:
        errors.append(
            {
                "code": "used_notes_master_not_in_presentation",
                "parts": missing_notes_masters,
            }
        )

    presentation_handout_masters = set(
        _typed_relationship_ids(rel_maps, "ppt/presentation.xml", REL_HANDOUT_MASTER).values()
    )
    themed_masters = (
        layout_slide_masters
        | presentation_slide_masters
        | used_notes_masters
        | presentation_notes_masters
        | presentation_handout_masters
    )
    for master in sorted(themed_masters):
        themes = _typed_relationship_ids(rel_maps, master, REL_THEME)
        if len(themes) != 1:
            errors.append(
                {
                    "code": "used_master_theme_cardinality_invalid",
                    "part": master,
                    "count": len(themes),
                }
            )


def detect_embedded_and_activex(
    members: set[str],
    roots: dict[str, ET.Element],
) -> tuple[list[str], list[str], list[str]]:
    """Return evidence for embedded objects and ActiveX beyond path heuristics."""
    embedded: set[str] = {
        name for name in members if name.startswith("ppt/embeddings/")
    }
    activex: set[str] = {
        name for name in members if name.startswith("ppt/activeX/")
    }
    macros: set[str] = {
        name for name in members if PurePosixPath(name).name.lower() == "vbaproject.bin"
    }

    for rel_part, root in roots.items():
        if not rel_part.lower().endswith(".rels"):
            continue
        for rel in root.findall(f"{{{PKG_REL_NS}}}Relationship"):
            rel_type = (rel.get("Type") or "").lower()
            rel_id = rel.get("Id") or "?"
            target = rel.get("Target") or "?"
            evidence = f"relationship:{rel_part}#{rel_id}->{target}"
            if rel_type.endswith("/oleobject") or rel_type.endswith("/package"):
                embedded.add(evidence)
            if "activex" in rel_type or rel_type.endswith("/control"):
                activex.add(evidence)
            if rel_type.endswith("/vbaproject") or "vbaproject" in rel_type:
                macros.add(evidence)

    content_types = roots.get("[Content_Types].xml")
    if content_types is not None:
        for element in content_types:
            content_type = (element.get("ContentType") or "").lower()
            part = (element.get("PartName") or element.get("Extension") or "?").lstrip("/")
            evidence = f"content-type:{part}:{content_type}"
            if "oleobject" in content_type or "embeddedpackage" in content_type:
                embedded.add(evidence)
            if "activex" in content_type:
                activex.add(evidence)
            if "vbaproject" in content_type or "macroenabled" in content_type:
                macros.add(evidence)

    for source_part, root in roots.items():
        if source_part.endswith(".rels"):
            continue
        for element in root.iter():
            local = str(element.tag).rsplit("}", 1)[-1].lower()
            if local in {"oleobj", "oleobject"}:
                embedded.add(f"element:{source_part}:{local}")
            if local in {"control", "controlpr", "activexcontrol"}:
                activex.add(f"element:{source_part}:{local}")
    return sorted(embedded), sorted(activex), sorted(macros)


def detect_audio_and_video(
    members: set[str], roots: dict[str, ET.Element]
) -> tuple[list[str], list[str]]:
    audio: set[str] = {
        name for name in members if PurePosixPath(name).suffix.lower() in AUDIO_EXTENSIONS
    }
    video: set[str] = {
        name for name in members if PurePosixPath(name).suffix.lower() in VIDEO_EXTENSIONS
    }
    for rel_part, root in roots.items():
        if not rel_part.lower().endswith(".rels"):
            continue
        for rel in root.findall(f"{{{PKG_REL_NS}}}Relationship"):
            rel_type = (rel.get("Type") or "").lower()
            rel_id = rel.get("Id") or "?"
            target = rel.get("Target") or "?"
            evidence = f"relationship:{rel_part}#{rel_id}->{target}"
            if rel_type.endswith("/audio"):
                audio.add(evidence)
            if rel_type.endswith("/video"):
                video.add(evidence)
            if rel_type.endswith("/media"):
                suffix = PurePosixPath(target).suffix.lower()
                if suffix in AUDIO_EXTENSIONS:
                    audio.add(evidence)
                elif suffix in VIDEO_EXTENSIONS:
                    video.add(evidence)
                else:
                    # Generic media relationships are ambiguous. Fail both
                    # media-forbid gates rather than silently approving one.
                    audio.add(evidence)
                    video.add(evidence)
    content_types = roots.get("[Content_Types].xml")
    if content_types is not None:
        for element in content_types:
            content_type = (element.get("ContentType") or "").lower()
            part = (element.get("PartName") or element.get("Extension") or "?").lstrip("/")
            evidence = f"content-type:{part}:{content_type}"
            if content_type.startswith("audio/"):
                audio.add(evidence)
            if content_type.startswith("video/"):
                video.add(evidence)
    return sorted(audio), sorted(video)


def presentation_slide_entries(
    roots: dict[str, ET.Element], rel_maps: dict[str, dict[str, tuple[str, str]]], errors: list[dict[str, Any]]
) -> list[tuple[str, str]]:
    root = roots.get("ppt/presentation.xml")
    if root is None:
        errors.append({"code": "presentation_xml_missing"})
        return []
    if root.tag != f"{{{P_NS}}}presentation":
        errors.append({"code": "presentation_root_invalid", "tag": str(root.tag)})
    rels = rel_maps.get("ppt/_rels/presentation.xml.rels", {})
    entries: list[tuple[str, str]] = []
    numeric_ids: list[int] = []
    for slide_id in root.findall("./p:sldIdLst/p:sldId", NS):
        raw_id = slide_id.get("id") or ""
        try:
            numeric_id = int(raw_id)
        except ValueError:
            numeric_id = -1
        if not (256 <= numeric_id <= 0x7FFFFFFF):
            errors.append({"code": "presentation_slide_id_invalid", "id": raw_id})
        numeric_ids.append(numeric_id)
        rel_id = slide_id.get(f"{{{OFFICE_REL_NS}}}id") or ""
        target_type = rels.get(rel_id)
        if not target_type or target_type[1] != REL_SLIDE:
            errors.append({"code": "presentation_slide_relationship_invalid", "id": rel_id})
            continue
        entries.append((rel_id, target_type[0]))
    if len(numeric_ids) != len(set(numeric_ids)):
        errors.append({"code": "presentation_slide_id_duplicate"})
    order = [part for _, part in entries]
    if len(order) != len(set(order)):
        errors.append({"code": "presentation_slide_order_duplicate"})
    return entries


def paragraph_text(paragraph: ET.Element) -> str:
    """Serialize DrawingML text, including explicit breaks and tabs, in order."""
    pieces: list[str] = []
    for node in paragraph.iter():
        local = str(node.tag).rsplit("}", 1)[-1]
        if local == "t":
            pieces.append(node.text or "")
        elif local == "br":
            pieces.append("\n")
        elif local == "tab":
            pieces.append("\t")
    return "".join(pieces)


NOTE_EXCLUDED_PLACEHOLDERS = {"sldImg", "sldNum", "hdr", "ftr", "dt"}


def _paragraphs_in_document_order(node: ET.Element) -> list[str]:
    """Return DrawingML paragraphs once, respecting AlternateContent branches."""
    if node.tag == f"{{{MC_NS}}}AlternateContent":
        branch_values: list[tuple[str, list[str]]] = []
        for branch in list(node):
            if branch.tag not in {f"{{{MC_NS}}}Choice", f"{{{MC_NS}}}Fallback"}:
                continue
            values: list[str] = []
            for child in list(branch):
                values.extend(_paragraphs_in_document_order(child))
            normalized = normalize_note_text("\n".join(values))
            branch_values.append((normalized, values))
        if not branch_values:
            return []
        if len({value for value, _ in branch_values}) != 1:
            raise ValueError("ambiguous_alternatecontent_notes")
        if not branch_values[0][0]:
            return []
        return branch_values[0][1]
    if node.tag == f"{{{A_NS}}}p":
        return [paragraph_text(node)]
    values: list[str] = []
    for child in list(node):
        values.extend(_paragraphs_in_document_order(child))
    return values


def _note_blocks_in_document_order(node: ET.Element) -> list[str]:
    """Extract visible note text objects in shape-tree order without duplication."""
    if node.tag == f"{{{MC_NS}}}AlternateContent":
        branch_values: list[tuple[str, list[str]]] = []
        for branch in list(node):
            if branch.tag not in {f"{{{MC_NS}}}Choice", f"{{{MC_NS}}}Fallback"}:
                continue
            values: list[str] = []
            for child in list(branch):
                values.extend(_note_blocks_in_document_order(child))
            normalized = normalize_note_text("\n".join(values))
            branch_values.append((normalized, values))
        if not branch_values:
            return []
        if len({value for value, _ in branch_values}) != 1:
            raise ValueError("ambiguous_alternatecontent_notes")
        if not branch_values[0][0]:
            return []
        return branch_values[0][1]

    if node.tag == f"{{{P_NS}}}sp":
        placeholder = node.find("./p:nvSpPr/p:nvPr/p:ph", NS)
        placeholder_type = placeholder.get("type") if placeholder is not None else ""
        if placeholder_type in NOTE_EXCLUDED_PLACEHOLDERS:
            return []
        text_body = node.find("./p:txBody", NS)
        if text_body is None:
            return []
        value = normalize_note_text("\n".join(_paragraphs_in_document_order(text_body)))
        return [value] if value else []

    if node.tag == f"{{{P_NS}}}graphicFrame":
        value = normalize_note_text("\n".join(_paragraphs_in_document_order(node)))
        return [value] if value else []

    if node.tag in {f"{{{P_NS}}}grpSp", f"{{{P_NS}}}spTree"}:
        values: list[str] = []
        for child in list(node):
            values.extend(_note_blocks_in_document_order(child))
        return values
    return []


def note_body_text(root: ET.Element) -> str:
    shape_tree = root.find("./p:cSld/p:spTree", NS)
    if shape_tree is None:
        raise ValueError("notes_shape_tree_missing")
    return normalize_note_text("\n".join(_note_blocks_in_document_order(shape_tree)))


def normalize_note_text(text: str) -> str:
    """Normalize transport line endings while preserving internal blank paragraphs."""
    normalized = unicodedata.normalize("NFC", text)
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n").replace("\v", "\n")
    return normalized.strip()


def note_violations(text: str) -> list[str]:
    hits: list[str] = []
    for code, pattern in (
        ("time", TIME_RE),
        ("source_line", SOURCE_LINE_RE),
        ("url", URL_RE),
        ("doi", DOI_RE),
        ("production_metadata", PRODUCTION_RE),
    ):
        if pattern.search(text):
            hits.append(code)
    return hits


def validate_slides_and_notes(
    members: set[str],
    roots: dict[str, ET.Element],
    rel_maps: dict[str, dict[str, tuple[str, str]]],
    require_notes: bool,
    forbid_note_metadata: bool,
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    presentation_entries = presentation_slide_entries(roots, rel_maps, errors)
    order = [part for _, part in presentation_entries]
    content_type_root = roots.get("[Content_Types].xml")
    override_types: dict[str, str] = {}
    if content_type_root is not None:
        override_types = {
            (element.get("PartName") or "").lstrip("/"): element.get("ContentType") or ""
            for element in content_type_root
            if element.tag == f"{{{CT_NS}}}Override"
        }
    slide_mime = "application/vnd.openxmlformats-officedocument.presentationml.slide+xml"
    notes_mime = "application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"
    declared_slides = {part for part, mime in override_types.items() if mime == slide_mime}
    slide_parts = sorted(declared_slides | set(order))
    note_relationship_targets = {
        target
        for rel_map in rel_maps.values()
        for target, rel_type in rel_map.values()
        if rel_type == REL_NOTES_SLIDE and target in members
    }
    declared_notes = {part for part, mime in override_types.items() if mime == notes_mime}
    note_parts = sorted(declared_notes | note_relationship_targets)
    for part in order:
        if override_types.get(part) != slide_mime:
            errors.append({"code": "slide_content_type_mismatch", "part": part, "actual": override_types.get(part)})
        slide_root = roots.get(part)
        if slide_root is None or slide_root.tag != f"{{{P_NS}}}sld":
            errors.append({"code": "slide_root_invalid", "part": part})
    for part in note_parts:
        if override_types.get(part) != notes_mime:
            errors.append({"code": "notes_content_type_mismatch", "part": part, "actual": override_types.get(part)})
        note_root = roots.get(part)
        if note_root is None or note_root.tag != f"{{{P_NS}}}notes":
            errors.append({"code": "notes_root_invalid", "part": part})
    if set(order) != set(slide_parts):
        errors.append(
            {
                "code": "presentation_slide_part_mismatch",
                "ordered": len(order),
                "parts": len(slide_parts),
            }
        )

    mapped_notes: list[str] = []
    note_texts: list[str] = []
    slide_mapping: list[dict[str, Any]] = []
    for index, (presentation_rel_id, slide_part) in enumerate(presentation_entries, start=1):
        rel_part = companion_relationship_part(slide_part)
        note_targets = [target for target, rel_type in rel_maps.get(rel_part, {}).values() if rel_type == REL_NOTES_SLIDE]
        if len(note_targets) > 1:
            errors.append(
                {
                    "code": "slide_has_multiple_notes_relationships",
                    "slide": index,
                    "part": slide_part,
                    "count": len(note_targets),
                }
            )
        if require_notes and len(note_targets) != 1:
            errors.append(
                {
                    "code": "slide_notes_relationship_count",
                    "slide": index,
                    "part": slide_part,
                    "count": len(note_targets),
                }
            )
        for note_part in note_targets:
            mapped_notes.append(note_part)
            note_root = roots.get(note_part)
            if note_root is None:
                continue
            try:
                text = note_body_text(note_root)
            except ValueError as exc:
                errors.append(
                    {
                        "code": str(exc),
                        "slide": index,
                        "part": note_part,
                    }
                )
                text = ""
            note_texts.append(text)
            if require_notes and not text:
                errors.append({"code": "empty_speaker_notes", "slide": index, "part": note_part})
            if forbid_note_metadata:
                violations = note_violations(text)
                if violations:
                    errors.append(
                        {
                            "code": "forbidden_note_metadata",
                            "slide": index,
                            "part": note_part,
                            "categories": violations,
                        }
                    )

            note_rel_part = companion_relationship_part(note_part)
            backlinks = [
                target
                for target, rel_type in rel_maps.get(note_rel_part, {}).values()
                if rel_type == REL_SLIDE
            ]
            if len(backlinks) != 1 or backlinks[0] != slide_part:
                errors.append(
                    {
                        "code": "notes_slide_backlink_invalid",
                        "slide": index,
                        "notes": note_part,
                        "backlinks": backlinks,
                    }
                )

        slide_mapping.append(
            {
                "index": index,
                "presentation_rel_id": presentation_rel_id,
                "slide_part": slide_part,
                "notes_part": note_targets[0] if len(note_targets) == 1 else None,
            }
        )

    if len(mapped_notes) != len(set(mapped_notes)):
        errors.append({"code": "notes_part_reused_by_multiple_slides"})
    if set(mapped_notes) != set(note_parts):
        errors.append(
            {
                "code": "orphan_or_unmapped_notes_parts",
                "slides": len(order),
                "mapped_notes": len(mapped_notes),
                "note_parts": len(note_parts),
            }
        )
    if require_notes and len(mapped_notes) != len(order):
        errors.append(
            {
                "code": "required_notes_missing",
                "slides": len(order),
                "mapped_notes": len(mapped_notes),
            }
        )
    return {
        "slides": len(order),
        "slide_parts": len(slide_parts),
        "notes_parts": len(note_parts),
        "nonempty_notes": sum(bool(text) for text in note_texts),
        "_slide_mapping": slide_mapping,
    }


def load_source_ledger(
    path: Path | None, expected_fingerprint: tuple[int, int, str] | None = None
) -> set[str]:
    if path is None:
        return set()
    payload, fingerprint = read_json_snapshot(path)
    if expected_fingerprint is not None and fingerprint != expected_fingerprint:
        raise ValueError("Source ledger bytes differ from frozen dependency fingerprint")
    if not isinstance(payload, dict):
        raise ValueError("Source ledger must be a JSON object")
    raw_keys = payload.get("source_keys")
    if raw_keys is None:
        sources = payload.get("sources")
        if not isinstance(sources, list) or any(
            not isinstance(item, dict)
            or not isinstance(item.get("key"), str)
            or not item["key"].strip()
            for item in sources
        ):
            raise ValueError("Source ledger requires source_keys[] or sources[].key")
        raw_keys = [item["key"] for item in sources]
    if not isinstance(raw_keys, list) or any(not isinstance(key, str) or not key.strip() for key in raw_keys):
        raise ValueError("Source ledger requires source_keys[] or sources[].key")
    if len(raw_keys) != len(set(raw_keys)):
        raise ValueError("Source ledger keys must be unique")
    return set(raw_keys)


def load_canonical_notes(
    path: Path | None,
    decks: Iterable[Path],
    expected_fingerprint: tuple[int, int, str] | None = None,
) -> dict[str, dict[str, str]]:
    if path is None:
        return {}
    payload, fingerprint = read_json_snapshot(path)
    if expected_fingerprint is not None and fingerprint != expected_fingerprint:
        raise ValueError("Canonical notes bytes differ from frozen dependency fingerprint")
    if not isinstance(payload, dict) or type(payload.get("version")) is not int or payload.get("version") != 1:
        raise ValueError("Canonical notes must be a JSON object with version=1")
    entries = payload.get("decks")
    if not isinstance(entries, list):
        raise ValueError("Canonical notes require a decks array")
    discovered = list(decks)
    by_name: dict[str, list[Path]] = {}
    for deck in discovered:
        by_name.setdefault(deck.name.casefold(), []).append(deck)
    result: dict[str, dict[str, str]] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("file"), str):
            raise ValueError("Each canonical-notes deck requires a file basename")
        if Path(entry["file"]).name != entry["file"]:
            raise ValueError("Canonical-notes file must be a basename")
        matches = by_name.get(entry["file"].casefold(), [])
        if len(matches) != 1:
            raise ValueError("Canonical-notes file must match exactly one discovered PPTX")
        notes = entry.get("notes")
        if not isinstance(notes, list):
            raise ValueError("Each canonical-notes deck requires notes[]")
        note_map: dict[str, str] = {}
        for note in notes:
            if (
                not isinstance(note, dict)
                or not isinstance(note.get("slide_uid"), str)
                or not note["slide_uid"].strip()
                or not isinstance(note.get("text"), str)
                or not normalize_note_text(note["text"])
            ):
                raise ValueError("Canonical notes require nonempty slide_uid and text strings")
            uid = note["slide_uid"]
            if uid in note_map:
                raise ValueError("Canonical notes slide_uid values must be unique per deck")
            note_map[uid] = normalize_note_text(note["text"])
        key = os.path.normcase(str(matches[0]))
        if key in result:
            raise ValueError("Duplicate canonical-notes deck entry")
        result[key] = note_map
    missing = [deck.name for deck in discovered if os.path.normcase(str(deck)) not in result]
    if missing:
        raise ValueError("Canonical notes are missing one or more discovered decks")
    return result


def load_manifest(
    path: Path,
    decks: Iterable[Path],
    baseline_root: Path | None,
    expected_fingerprint: tuple[int, int, str] | None = None,
) -> dict[str, dict[str, Any]]:
    resolved = path.expanduser().resolve()
    payload, fingerprint = read_json_snapshot(resolved)
    if expected_fingerprint is not None and fingerprint != expected_fingerprint:
        raise ValueError("Manifest bytes differ from frozen dependency fingerprint")
    if not isinstance(payload, dict) or type(payload.get("version")) is not int or payload.get("version") != 2:
        raise ValueError("Manifest root must be an object with version=2")
    if baseline_root is None:
        raise ValueError("--baseline-root is required with --manifest")
    baseline_root = baseline_root.expanduser().resolve()
    entries = payload.get("decks")
    if not isinstance(entries, list):
        raise ValueError("Manifest must contain a decks array")
    discovered = list(decks)
    by_name: dict[str, list[Path]] = {}
    for deck in discovered:
        by_name.setdefault(deck.name.casefold(), []).append(deck)
    result: dict[str, dict[str, Any]] = {}
    baseline_seen: list[Path] = []
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("file"), str):
            raise ValueError("Each manifest deck requires a file string")
        if Path(entry["file"]).name != entry["file"]:
            raise ValueError("Manifest file must be a basename, not a local path")
        matches = by_name.get(Path(entry["file"]).name.casefold(), [])
        if len(matches) != 1:
            raise ValueError(f"Manifest file must match exactly one discovered PPTX: {entry['file']}")
        baseline_file = entry.get("baseline_file")
        if not isinstance(baseline_file, str) or not baseline_file or Path(baseline_file).is_absolute():
            raise ValueError("Each manifest deck requires a relative baseline_file")
        baseline_path = (baseline_root / baseline_file).resolve()
        if os.path.commonpath([str(baseline_root), str(baseline_path)]) != str(baseline_root):
            raise ValueError("baseline_file must remain inside --baseline-root")
        if not baseline_path.is_file() or baseline_path.suffix.lower() != ".pptx":
            raise ValueError(f"Baseline PPTX not found: {baseline_file}")
        if baseline_path.name.casefold() != entry["file"].casefold():
            raise ValueError("baseline_file basename must match the manifest deck file")
        if any(os.path.samefile(baseline_path, current) for current in discovered):
            raise ValueError("Immutable baseline PPTX must not alias any current deck")
        if any(os.path.samefile(baseline_path, previous) for previous in baseline_seen):
            raise ValueError("Each manifest deck must have a distinct immutable baseline PPTX")
        baseline_seen.append(baseline_path)
        key = os.path.normcase(str(matches[0]))
        if key in result:
            raise ValueError(f"Duplicate manifest deck entry: {entry['file']}")
        entry = dict(entry)
        entry["_baseline_path"] = baseline_path
        result[key] = entry
    missing = [deck.name for deck in discovered if os.path.normcase(str(deck)) not in result]
    if missing:
        raise ValueError(f"Manifest is missing discovered decks: {missing}")
    return result


DRAWING_OWNER_QNAMES = {
    f"{{{P_NS}}}sp",
    f"{{{P_NS}}}pic",
    f"{{{P_NS}}}graphicFrame",
    f"{{{P_NS}}}cxnSp",
    f"{{{P_NS}}}grpSp",
    f"{{{P_NS}}}contentPart",
    f"{{{P_NS}}}spTree",
    f"{{{P14_NS}}}contentPart",
}
AUDIT_NS = "urn:openai:lecture-pptx-audit"


def local_name(element: ET.Element) -> str:
    return str(element.tag).rsplit("}", 1)[-1]


def is_drawing_owner(element: ET.Element) -> bool:
    return str(element.tag) in DRAWING_OWNER_QNAMES


def valid_review_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return False
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value))


def _element_path(element: ET.Element, parents: dict[ET.Element, ET.Element]) -> str:
    pieces: list[str] = []
    cursor = element
    while cursor in parents:
        parent = parents[cursor]
        pieces.append(f"{local_name(parent)}[{list(parent).index(cursor)}]")
        cursor = parent
    return "/".join(reversed(pieces))


def _alternate_context_and_branch(
    element: ET.Element, parents: dict[ET.Element, ET.Element]
) -> tuple[str, str]:
    cursor = element
    while cursor in parents:
        parent = parents[cursor]
        if parent.tag in {f"{{{MC_NS}}}Choice", f"{{{MC_NS}}}Fallback"}:
            grandparent = parents.get(parent)
            if grandparent is not None and grandparent.tag == f"{{{MC_NS}}}AlternateContent":
                return _element_path(grandparent, parents), _element_path(parent, parents)
        cursor = parent
    return "", ""


def _mask_drawing_descendants(container: ET.Element) -> None:
    first_drawing_index: int | None = None
    for child in list(container):
        if is_drawing_owner(child) and child.tag != f"{{{P_NS}}}spTree":
            if first_drawing_index is None:
                first_drawing_index = list(container).index(child)
            container.remove(child)
        else:
            _mask_drawing_descendants(child)
    if first_drawing_index is not None:
        container.insert(first_drawing_index, ET.Element(f"{{{AUDIT_NS}}}drawingContent"))


def _owner_cnvprs(owner: ET.Element) -> list[ET.Element]:
    paths = {
        f"{{{P_NS}}}sp": "./p:nvSpPr/p:cNvPr",
        f"{{{P_NS}}}pic": "./p:nvPicPr/p:cNvPr",
        f"{{{P_NS}}}graphicFrame": "./p:nvGraphicFramePr/p:cNvPr",
        f"{{{P_NS}}}cxnSp": "./p:nvCxnSpPr/p:cNvPr",
        f"{{{P_NS}}}grpSp": "./p:nvGrpSpPr/p:cNvPr",
        f"{{{P_NS}}}spTree": "./p:nvGrpSpPr/p:cNvPr",
        f"{{{P_NS}}}contentPart": "./p:nvContentPartPr/p:cNvPr",
    }
    path = paths.get(str(owner.tag))
    if path is not None:
        return owner.findall(path, NS)
    # Office extension content parts use their own namespace for the
    # non-visual wrapper.  Inspect only that direct wrapper, never nested
    # drawing owners.
    matches: list[ET.Element] = []
    for child in list(owner):
        if local_name(child).startswith("nv"):
            matches.extend(element for element in child.iter() if local_name(element) == "cNvPr")
    return matches


def _owner_metadata(owner: ET.Element) -> ET.Element:
    clone = ET.fromstring(ET.tostring(owner, encoding="utf-8"))
    if clone.tag in {f"{{{P_NS}}}grpSp", f"{{{P_NS}}}spTree"}:
        _mask_drawing_descendants(clone)
    return clone


def _shape_records_from_root(
    root: ET.Element,
) -> dict[str, tuple[ET.Element, ET.Element | None, int, str]]:
    parents = {child: parent for parent in root.iter() for child in parent}
    occurrences: dict[str, list[tuple[ET.Element, str, str]]] = {}
    for owner in root.iter():
        if not is_drawing_owner(owner):
            continue
        cnvprs = _owner_cnvprs(owner)
        if len(cnvprs) != 1:
            raise ValueError("shape_inventory_incomplete_owner")
        raw_id = str(cnvprs[0].get("id") or "")
        # ST_DrawingElementId is an unsigned 32-bit value.  PowerPoint's own
        # compatibility conversion can emit id="0", so zero must remain valid.
        if not raw_id.isdigit() or not (0 <= int(raw_id) <= 0xFFFFFFFF):
            raise ValueError("shape_inventory_invalid_id")
        context_path, branch_path = _alternate_context_and_branch(owner, parents)
        occurrences.setdefault(raw_id, []).append((owner, context_path, branch_path))

    records: dict[str, tuple[ET.Element, ET.Element | None, int, str]] = {}
    for raw_id, values in occurrences.items():
        if len(values) == 1:
            keyed = [(raw_id, values[0][0])]
        else:
            context_paths = [context for _, context, _ in values]
            branch_paths = [branch for _, _, branch in values]
            if (
                not all(context_paths)
                or len(set(context_paths)) != 1
                or not all(branch_paths)
                or len(branch_paths) != len(set(branch_paths))
            ):
                raise ValueError("shape_inventory_duplicate_id")
            keyed = [(f"{raw_id}@{branch}", owner) for owner, _, branch in values]
        for key, owner in keyed:
            parent = parents.get(owner)
            z_index = list(parent).index(owner) if parent is not None else 0
            ancestry: list[str] = []
            cursor = owner
            while cursor in parents:
                ancestor = parents[cursor]
                ancestry.append(f"{local_name(ancestor)}:{list(ancestor).index(cursor)}")
                cursor = ancestor
            records[key] = (owner, parent, z_index, "/".join(reversed(ancestry)))
    return records


def shape_inventory(payload: bytes) -> dict[str, str]:
    """Return each logical drawing owner with local content and ancestry hashes."""
    try:
        root = ET.fromstring(payload)
    except ET.ParseError as exc:
        raise ValueError("shape_inventory_xml_invalid") from exc
    records = _shape_records_from_root(root)
    inventory: dict[str, str] = {}
    for key, (owner, _parent, z_index, ancestry) in records.items():
        canonical = ET.canonicalize(ET.tostring(_owner_metadata(owner), encoding="unicode"))
        material = f"key={key}\0z={z_index}\0path={ancestry}\0{canonical}".encode("utf-8")
        inventory[key] = hashlib.sha256(material).hexdigest()
    return inventory


def slide_shell_hash(payload: bytes) -> str:
    """Hash non-drawing slide XML after masking the drawing canvas.

    Shape content, nesting, and z-order are covered by ``shape_inventory``.
    Masking the drawing children here lets reviewed shape insertions/deletions
    proceed while still protecting slide attributes, background, color-map
    overrides, transitions, timing, extensions, and the root canvas transform.
    """
    try:
        root = ET.fromstring(payload)
    except ET.ParseError as exc:
        raise ValueError("slide_shell_xml_invalid") from exc
    sp_tree = root.find("./p:cSld/p:spTree", NS)
    if sp_tree is None:
        raise ValueError("slide_shell_shape_tree_missing")

    _mask_drawing_descendants(sp_tree)

    canonical = ET.canonicalize(ET.tostring(root, encoding="unicode"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def inspect_baseline(path: Path, args: argparse.Namespace) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    before = path.stat()
    package_limit = args.max_package_mb * 1024 * 1024
    if before.st_size > package_limit:
        return {
            "sha256": None,
            "members": set(),
            "payloads": {},
            "member_hashes": {},
            "mapping": [],
            "slide_count": 0,
            "errors": [
                {
                    "code": "baseline_package_file_size_limit_exceeded",
                    "bytes": before.st_size,
                    "limit": package_limit,
                }
            ],
        }
    snapshot = read_members(path, errors, args)
    members, payloads, member_hashes = snapshot
    deck_sha = snapshot.sha256
    expected_snapshot = getattr(args, "frozen_dependency_fingerprints", {}).get(str(path))
    if expected_snapshot is not None and (
        snapshot.size, snapshot.mtime_ns, snapshot.sha256
    ) != expected_snapshot:
        errors.append({"code": "baseline_snapshot_fingerprint_mismatch"})
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        errors.append({"code": "baseline_drift_during_read", "baseline_path": str(path)})
    roots: dict[str, ET.Element] = {}
    if not snapshot.usable:
        return {
            "sha256": deck_sha,
            "members": set(),
            "payloads": {},
            "member_hashes": {},
            "mapping": [],
            "slide_count": 0,
            "errors": errors,
        }
    for name, payload in payloads.items():
        root = parse_xml(name, payload, errors)
        if root is not None:
            roots[name] = root
    strict = strict_ooxml_parts(roots, payloads)
    if strict:
        errors.append({"code": "strict_ooxml_not_supported", "parts": strict[:20], "scope": "baseline"})
    if members:
        validate_content_types(members, roots, errors)
        relationships = validate_relationships(members, roots, args.forbid_external_file_links, errors)
        validate_required_part_topology(members, roots, relationships, errors)
        counts = validate_slides_and_notes(members, roots, relationships, False, False, errors)
    else:
        counts = {"slides": 0, "_slide_mapping": []}
    return {
        "sha256": deck_sha,
        "members": members,
        "payloads": payloads,
        "member_hashes": member_hashes,
        "mapping": counts.get("_slide_mapping", []),
        "slide_count": counts.get("slides", 0),
        "errors": errors,
    }


def validate_topology_records(
    label: str,
    records: list[dict[str, Any]],
    actual_mapping: list[dict[str, Any]],
    payloads: dict[str, bytes],
    errors: list[dict[str, Any]],
) -> dict[int, dict[str, Any]]:
    by_index: dict[int, dict[str, Any]] = {}
    rel_ids: list[str] = []
    slide_parts: list[str] = []
    notes_parts: list[str] = []
    sha_re = re.compile(r"^[0-9a-fA-F]{64}$")
    for record in records:
        topology = record.get(label)
        if not isinstance(topology, dict):
            errors.append({"code": f"manifest_{label}_record_invalid", "slide_uid": record.get("slide_uid")})
            continue
        index_value = topology.get("index")
        rel_id = topology.get("presentation_rel_id")
        slide_part = topology.get("slide_part")
        notes_part = topology.get("notes_part")
        slide_sha = topology.get("slide_sha256")
        if (
            not isinstance(index_value, int)
            or isinstance(index_value, bool)
            or index_value < 1
            or not isinstance(rel_id, str)
            or not rel_id
            or not isinstance(slide_part, str)
            or not safe_member_name(slide_part)
            or (notes_part is not None and (not isinstance(notes_part, str) or not safe_member_name(notes_part)))
            or not isinstance(slide_sha, str)
            or not sha_re.fullmatch(slide_sha)
        ):
            errors.append({"code": f"manifest_{label}_record_invalid", "slide_uid": record.get("slide_uid")})
            continue
        index = index_value
        if index in by_index:
            errors.append({"code": f"manifest_{label}_index_duplicate", "index": index})
        by_index[index] = record
        rel_ids.append(rel_id)
        slide_parts.append(slide_part)
        if notes_part is not None:
            notes_parts.append(notes_part)
    for field, values in (("rel_id", rel_ids), ("slide_part", slide_parts), ("notes_part", notes_parts)):
        if len(values) != len(set(values)):
            errors.append({"code": f"manifest_{label}_{field}_duplicate"})
    expected_indices = set(range(1, len(actual_mapping) + 1))
    if set(by_index) != expected_indices:
        errors.append(
            {
                "code": f"manifest_{label}_index_set_mismatch",
                "expected": sorted(expected_indices),
                "actual": sorted(by_index),
            }
        )
    for actual in actual_mapping:
        record = by_index.get(actual["index"])
        if record is None:
            continue
        topology = record[label]
        for field in ("presentation_rel_id", "slide_part", "notes_part"):
            if topology.get(field) != actual.get(field):
                errors.append(
                    {
                        "code": f"manifest_{label}_mapping_mismatch",
                        "slide_uid": record.get("slide_uid"),
                        "index": actual["index"],
                        "field": field,
                        "expected": topology.get(field),
                        "actual": actual.get(field),
                    }
                )
        payload = payloads.get(actual["slide_part"])
        actual_sha = hashlib.sha256(payload).hexdigest() if payload is not None else None
        if topology.get("slide_sha256") != actual_sha:
            errors.append(
                {
                    "code": f"manifest_{label}_slide_hash_mismatch",
                    "slide_uid": record.get("slide_uid"),
                    "index": actual["index"],
                }
            )
    return by_index


def relationship_inventory(
    payloads: dict[str, bytes],
) -> dict[tuple[str, str], dict[str, str]]:
    """Return every OPC relationship as a normalized, source-bound record."""
    inventory: dict[tuple[str, str], dict[str, str]] = {}
    for rel_part, payload in payloads.items():
        if not rel_part.lower().endswith(".rels"):
            continue
        source = relationship_source_part(rel_part)
        if source is None:
            continue
        try:
            root = ET.fromstring(payload)
        except ET.ParseError as exc:
            raise ValueError("relationship_inventory_xml_invalid") from exc
        if root.tag != f"{{{PKG_REL_NS}}}Relationships":
            raise ValueError("relationship_inventory_root_invalid")
        for rel in root:
            if rel.tag != f"{{{PKG_REL_NS}}}Relationship":
                raise ValueError("relationship_inventory_child_invalid")
            rel_id = rel.get("Id") or ""
            rel_type = rel.get("Type") or ""
            target = rel.get("Target") or ""
            raw_mode = (rel.get("TargetMode") or "internal").casefold()
            if not rel_id or not rel_type or not target or raw_mode not in {"internal", "external"}:
                raise ValueError("relationship_inventory_record_invalid")
            mode = raw_mode
            if mode == "internal":
                target_safe, normalized_target = safe_internal_relationship_target(source, target)
                if not target_safe:
                    raise ValueError("relationship_inventory_target_invalid")
                if not relationship_role_is_valid(source, rel_type, normalized_target):
                    raise ValueError("relationship_type_target_role_mismatch")
            else:
                if not external_relationship_role_is_valid(source, rel_type):
                    raise ValueError("relationship_type_target_role_mismatch")
                normalized_target = target
            key = (source, rel_id)
            if key in inventory:
                raise ValueError("relationship_inventory_duplicate_id")
            inventory[key] = {
                "type": rel_type,
                "target_mode": mode,
                "target": normalized_target,
            }
    return inventory


def _is_dependency_relationship(source: str, rel_type: str) -> bool:
    """Keep only consumer-to-dependency edges for slide ownership tracing."""
    if rel_type in {REL_SLIDE, REL_HYPERLINK}:
        # Presentation collections and notes backlinks do not make one slide
        # the owner of another slide's assets.
        return False
    if source.startswith("ppt/slideMasters/") and rel_type == REL_SLIDE_LAYOUT:
        # A master lists every child layout.  Traversing this reverse
        # collection edge would make every slide own every sibling layout.
        return False
    return True


def referenced_relationship_ids(payloads: dict[str, bytes]) -> dict[str, dict[str, frozenset[str]]]:
    """Collect semantic relationship references and their allowed types."""
    references: dict[str, dict[str, frozenset[str]]] = {}
    for source, payload in payloads.items():
        if source.lower().endswith(".rels"):
            continue
        try:
            root = ET.fromstring(payload)
        except ET.ParseError:
            continue
        for element in root.iter():
            for name, value in element.attrib.items():
                if relationship_reference_kind(element, name) is not None and value:
                    expected = RELATIONSHIP_REFERENCE_SCHEMA[(str(element.tag), name)]
                    prior = references.setdefault(source, {}).get(value)
                    references[source][value] = expected if prior is None else prior & expected
    return references


def relationship_graph(payloads: dict[str, bytes]) -> dict[str, set[tuple[str, str]]]:
    """Return typed internal consumption edges keyed by their source part."""
    graph: dict[str, set[tuple[str, str]]] = {}
    references = referenced_relationship_ids(payloads)
    implicit_types = {
        REL_SLIDE_LAYOUT,
        REL_NOTES_SLIDE,
        REL_SLIDE_MASTER,
        REL_NOTES_MASTER,
        REL_THEME,
        REL_THEME_OVERRIDE,
    }
    for (source, rel_id), binding in relationship_inventory(payloads).items():
        if binding["target_mode"] != "internal":
            continue
        rel_type = binding["type"]
        if (
            _is_dependency_relationship(source, rel_type)
            and (
                rel_type in implicit_types
                or rel_type in references.get(source, {}).get(rel_id, frozenset())
            )
        ):
            graph.setdefault(source, set()).add((binding["target"], rel_type))
    return graph


def slide_uids_reaching_part(
    records: dict[str, dict[str, Any]],
    topology_label: str,
    payloads: dict[str, bytes],
    target_part: str,
) -> list[str]:
    graph = relationship_graph(payloads)
    owners: list[str] = []
    for uid, record in records.items():
        topology = record.get(topology_label)
        if not isinstance(topology, dict) or not isinstance(topology.get("slide_part"), str):
            continue
        pending = [topology["slide_part"]]
        visited: set[str] = set()
        found = topology["slide_part"] == target_part
        while pending and not found:
            source = pending.pop()
            if source in visited:
                continue
            visited.add(source)
            for destination, _rel_type in graph.get(source, set()):
                if destination == target_part:
                    found = True
                    break
                if destination not in visited:
                    pending.append(destination)
        if found:
            owners.append(uid)
    return sorted(owners)


def validate_manifest_entry(
    deck_sha: str,
    mapping: list[dict[str, Any]],
    xml_payloads: dict[str, bytes],
    member_hashes: dict[str, str],
    baseline: dict[str, Any],
    entry: dict[str, Any],
    canonical_notes: dict[str, str] | None,
    args: argparse.Namespace,
    errors: list[dict[str, Any]],
) -> None:
    sha_re = re.compile(r"^[0-9a-fA-F]{64}$")
    for field, actual in (
        ("current_sha256", deck_sha),
        ("baseline_sha256", baseline["sha256"]),
    ):
        expected = entry.get(field)
        if not isinstance(expected, str) or not sha_re.fullmatch(expected):
            errors.append({"code": f"manifest_{field}_invalid"})
        elif not isinstance(actual, str) or expected.lower() != actual.lower():
            errors.append({"code": f"manifest_{field}_mismatch", "expected": expected, "actual": actual})
    for field, actual in (
        ("current_slide_count", len(mapping)),
        ("baseline_slide_count", baseline["slide_count"]),
    ):
        expected_count = entry.get(field)
        if (
            not isinstance(expected_count, int)
            or isinstance(expected_count, bool)
            or expected_count < 0
        ):
            errors.append({"code": f"manifest_{field}_invalid"})
        elif expected_count != actual:
            errors.append({"code": f"manifest_{field}_mismatch", "expected": entry.get(field), "actual": actual})

    declared_baseline_members = entry.get("baseline_member_sha256")
    if not isinstance(declared_baseline_members, dict) or declared_baseline_members != baseline["member_hashes"]:
        errors.append({"code": "manifest_baseline_member_hashes_mismatch"})
    allowed = entry.get("allowed_changed_parts")
    if not isinstance(allowed, list) or any(not isinstance(part, str) or not safe_member_name(part) for part in allowed):
        errors.append({"code": "manifest_allowed_changed_parts_invalid"})
        allowed_set: set[str] = set()
    else:
        allowed_set = set(allowed)
        if len(allowed_set) != len(allowed):
            errors.append({"code": "manifest_allowed_changed_parts_duplicate"})
    changed_parts = {
        part
        for part in set(member_hashes) | set(baseline["member_hashes"])
        if member_hashes.get(part) != baseline["member_hashes"].get(part)
    }
    outside_allowlist = sorted(changed_parts - allowed_set)
    if outside_allowlist:
        errors.append({"code": "package_changes_outside_manifest_allowlist", "parts": outside_allowlist})
    unused_allowlist = sorted(allowed_set - changed_parts)
    if unused_allowlist:
        errors.append({"code": "manifest_unused_allowed_changed_parts", "parts": unused_allowlist})

    records = entry.get("slides")
    if not isinstance(records, list) or any(not isinstance(record, dict) for record in records):
        errors.append({"code": "manifest_slides_missing_or_invalid"})
        return
    uids = [record.get("slide_uid") for record in records]
    valid_uids = [uid for uid in uids if isinstance(uid, str) and uid.strip()]
    if len(valid_uids) != len(uids) or len(valid_uids) != len(set(valid_uids)):
        errors.append({"code": "manifest_slide_uid_invalid_or_duplicate"})
    invalid_actions = sorted({str(record.get("action")) for record in records if record.get("action") not in {"keep", "insert", "delete"}})
    if invalid_actions:
        errors.append({"code": "manifest_action_invalid", "actions": invalid_actions})
    structural_change = any(record.get("action") != "keep" for record in records)
    for record in records:
        baseline_topology = record.get("baseline")
        current_topology = record.get("current")
        if not isinstance(baseline_topology, dict) or not isinstance(current_topology, dict):
            continue
        if any(
            baseline_topology.get(field) != current_topology.get(field)
            for field in ("index", "presentation_rel_id", "slide_part", "notes_part")
        ):
            structural_change = True
    if entry.get("baseline_slide_count") != entry.get("current_slide_count"):
        structural_change = True
    if structural_change:
        errors.append({"code": "structural_change_requires_new_batch"})
    baseline_records = [record for record in records if record.get("action") in {"keep", "delete"}]
    current_records = [record for record in records if record.get("action") in {"keep", "insert"}]
    for record in records:
        action = record.get("action")
        if action in {"keep", "delete"} and not isinstance(record.get("baseline"), dict):
            errors.append({"code": "manifest_baseline_record_missing", "slide_uid": record.get("slide_uid")})
        if action == "insert" and record.get("baseline") is not None:
            errors.append({"code": "manifest_insert_has_baseline", "slide_uid": record.get("slide_uid")})
        if action == "delete" and record.get("current") is not None:
            errors.append({"code": "manifest_delete_has_current", "slide_uid": record.get("slide_uid")})

        source_keys = record.get("source_keys", [])
        exemption = record.get("source_exemption")
        if not isinstance(source_keys, list) or any(not isinstance(key, str) or not key.strip() for key in source_keys):
            errors.append({"code": "manifest_source_keys_invalid", "slide_uid": record.get("slide_uid")})
            source_keys = []
        elif len(source_keys) != len(set(source_keys)):
            errors.append({"code": "manifest_source_keys_duplicate", "slide_uid": record.get("slide_uid")})
        valid_exemption = (
            isinstance(exemption, dict)
            and exemption.get("type") in SOURCE_EXEMPTION_TYPES
            and isinstance(exemption.get("rationale"), str)
            and len(exemption["rationale"].strip()) >= 10
            and isinstance(exemption.get("reviewed_by"), str)
            and bool(exemption["reviewed_by"].strip())
            and valid_review_date(exemption.get("reviewed_at"))
        )
        if exemption is not None and not valid_exemption:
            errors.append({"code": "manifest_source_exemption_invalid", "slide_uid": record.get("slide_uid")})
        if source_keys and exemption is not None:
            errors.append({"code": "manifest_source_mapping_ambiguous", "slide_uid": record.get("slide_uid")})
        if args.require_source_keys:
            if not source_keys and not valid_exemption:
                errors.append({"code": "manifest_source_mapping_missing", "slide_uid": record.get("slide_uid")})
        if args.source_ledger is not None:
            missing_keys = sorted(set(source_keys) - args.source_ledger_keys)
            if missing_keys:
                errors.append(
                    {"code": "manifest_source_keys_not_in_ledger", "slide_uid": record.get("slide_uid"), "keys": missing_keys}
                )

    validate_topology_records(
        "baseline", baseline_records, baseline["mapping"], baseline["payloads"], errors
    )
    validate_topology_records(
        "current", current_records, mapping, xml_payloads, errors
    )

    uid_records = {
        record["slide_uid"]: record
        for record in records
        if isinstance(record.get("slide_uid"), str) and record["slide_uid"].strip()
    }

    try:
        baseline_relationships = relationship_inventory(baseline["payloads"])
        current_relationships = relationship_inventory(xml_payloads)
    except ValueError as exc:
        errors.append({"code": str(exc)})
        baseline_relationships = {}
        current_relationships = {}

    protected_relationships = entry.get("protected_relationships", [])
    if not isinstance(protected_relationships, list):
        errors.append({"code": "manifest_protected_relationships_invalid"})
        protected_relationships = []
    declared_relationships: dict[tuple[str, str], dict[str, str]] = {}
    for relationship in protected_relationships:
        expected_fields = {"source_part", "relationship_id", "type", "target_mode", "target"}
        source_part = relationship.get("source_part") if isinstance(relationship, dict) else None
        rel_id = relationship.get("relationship_id") if isinstance(relationship, dict) else None
        binding = {
            "type": relationship.get("type"),
            "target_mode": relationship.get("target_mode"),
            "target": relationship.get("target"),
        } if isinstance(relationship, dict) else {}
        valid_source = isinstance(source_part, str) and (
            source_part == "" or safe_member_name(source_part)
        )
        valid_binding = (
            isinstance(binding.get("type"), str)
            and bool(binding["type"])
            and isinstance(binding.get("target"), str)
            and bool(binding["target"])
            and binding.get("target_mode") in {"internal", "external"}
        )
        if (
            not isinstance(relationship, dict)
            or set(relationship) != expected_fields
            or not valid_source
            or not isinstance(rel_id, str)
            or not rel_id
            or not valid_binding
        ):
            errors.append({"code": "manifest_protected_relationship_invalid"})
            continue
        key = (source_part, rel_id)
        if key in declared_relationships:
            errors.append(
                {
                    "code": "manifest_protected_relationship_duplicate",
                    "source_part": source_part,
                    "relationship_id": rel_id,
                }
            )
        declared_relationships[key] = binding
    if declared_relationships != baseline_relationships:
        errors.append(
            {
                "code": "manifest_protected_relationship_inventory_mismatch",
                "missing": sorted(set(baseline_relationships) - set(declared_relationships)),
                "extra": sorted(set(declared_relationships) - set(baseline_relationships)),
            }
        )

    editable_relationships = entry.get("editable_relationships", [])
    if not isinstance(editable_relationships, list):
        errors.append({"code": "manifest_editable_relationships_invalid"})
        editable_relationships = []
    declared_relationship_changes: dict[tuple[str, str], dict[str, Any]] = {}
    for editable in editable_relationships:
        expected_editable_fields = {
            "action",
            "source_part",
            "relationship_id",
            "baseline",
            "current",
            "baseline_owner_slide_uids",
            "current_owner_slide_uids",
            "reason",
            "reviewed_by",
            "reviewed_at",
        }
        action = editable.get("action") if isinstance(editable, dict) else None
        source_part = editable.get("source_part") if isinstance(editable, dict) else None
        rel_id = editable.get("relationship_id") if isinstance(editable, dict) else None
        before_binding = editable.get("baseline") if isinstance(editable, dict) else None
        after_binding = editable.get("current") if isinstance(editable, dict) else None

        def valid_binding(value: Any) -> bool:
            return (
                isinstance(value, dict)
                and set(value) == {"type", "target_mode", "target"}
                and isinstance(value.get("type"), str)
                and bool(value["type"])
                and value.get("target_mode") in {"internal", "external"}
                and isinstance(value.get("target"), str)
                and bool(value["target"])
            )

        valid_endpoints = (
            (action == "modify" and valid_binding(before_binding) and valid_binding(after_binding))
            or (action == "delete" and valid_binding(before_binding) and after_binding is None)
            or (action == "insert" and before_binding is None and valid_binding(after_binding))
        )
        valid_source = isinstance(source_part, str) and (
            source_part == "" or safe_member_name(source_part)
        )
        baseline_owner_uids = editable.get("baseline_owner_slide_uids", []) if isinstance(editable, dict) else []
        current_owner_uids = editable.get("current_owner_slide_uids", []) if isinstance(editable, dict) else []
        if (
            not isinstance(editable, dict)
            or set(editable) != expected_editable_fields
            or action not in {"modify", "insert", "delete"}
            or not valid_source
            or not isinstance(rel_id, str)
            or not rel_id
            or not valid_endpoints
            or not isinstance(baseline_owner_uids, list)
            or not isinstance(current_owner_uids, list)
            or any(not isinstance(uid, str) or uid not in uid_records for uid in [*baseline_owner_uids, *current_owner_uids])
            or len(baseline_owner_uids) != len(set(baseline_owner_uids))
            or len(current_owner_uids) != len(set(current_owner_uids))
            or not isinstance(editable.get("reason"), str)
            or len(editable["reason"].strip()) < 10
            or not isinstance(editable.get("reviewed_by"), str)
            or not editable["reviewed_by"].strip()
            or not valid_review_date(editable.get("reviewed_at"))
        ):
            errors.append({"code": "manifest_editable_relationship_invalid"})
            continue
        key = (source_part, rel_id)
        if key in declared_relationship_changes:
            errors.append(
                {
                    "code": "manifest_editable_relationship_duplicate",
                    "source_part": source_part,
                    "relationship_id": rel_id,
                }
            )
        normalized = dict(editable)
        normalized["baseline_owner_slide_uids"] = sorted(baseline_owner_uids)
        normalized["current_owner_slide_uids"] = sorted(current_owner_uids)
        declared_relationship_changes[key] = normalized

    actual_relationship_changes: dict[tuple[str, str], dict[str, Any]] = {}
    for key in set(baseline_relationships) | set(current_relationships):
        before_binding = baseline_relationships.get(key)
        after_binding = current_relationships.get(key)
        if before_binding == after_binding:
            continue
        action = "modify" if before_binding is not None and after_binding is not None else "delete" if before_binding else "insert"
        actual_relationship_changes[key] = {
            "action": action,
            "baseline": before_binding,
            "current": after_binding,
        }
    if set(declared_relationship_changes) != set(actual_relationship_changes):
        errors.append(
            {
                "code": "manifest_editable_relationship_diff_mismatch",
                "missing": sorted(set(actual_relationship_changes) - set(declared_relationship_changes)),
                "extra": sorted(set(declared_relationship_changes) - set(actual_relationship_changes)),
            }
        )
    for key, actual_change in actual_relationship_changes.items():
        editable = declared_relationship_changes.get(key)
        if editable is None:
            continue
        if any(editable.get(field) != actual_change[field] for field in ("action", "baseline", "current")):
            errors.append(
                {
                    "code": "manifest_editable_relationship_binding_mismatch",
                    "source_part": key[0],
                    "relationship_id": key[1],
                }
            )
        baseline_owners = slide_uids_reaching_part(
            uid_records, "baseline", baseline["payloads"], key[0]
        ) if key[0] else []
        current_owners = slide_uids_reaching_part(
            uid_records, "current", xml_payloads, key[0]
        ) if key[0] else []
        if (
            editable.get("baseline_owner_slide_uids") != baseline_owners
            or editable.get("current_owner_slide_uids") != current_owners
        ):
            errors.append(
                {
                    "code": "manifest_editable_relationship_owner_mismatch",
                    "source_part": key[0],
                    "relationship_id": key[1],
                    "expected_baseline_owners": baseline_owners,
                    "expected_current_owners": current_owners,
                }
            )

    baseline_assets = {
        part: digest for part, digest in baseline["member_hashes"].items() if part.startswith("ppt/media/")
    }
    current_assets = {
        part: digest for part, digest in member_hashes.items() if part.startswith("ppt/media/")
    }
    protected_assets = entry.get("protected_assets", [])
    if not isinstance(protected_assets, list):
        errors.append({"code": "manifest_protected_assets_invalid"})
        protected_assets = []
    declared_assets: dict[str, str] = {}
    for asset in protected_assets:
        if (
            not isinstance(asset, dict)
            or not isinstance(asset.get("part"), str)
            or not safe_member_name(asset["part"])
            or not asset["part"].startswith("ppt/media/")
            or not sha_re.fullmatch(str(asset.get("sha256") or ""))
        ):
            errors.append({"code": "manifest_protected_asset_invalid"})
            continue
        part, expected = asset["part"], str(asset["sha256"]).lower()
        if part in declared_assets:
            errors.append({"code": "manifest_protected_asset_duplicate", "part": part})
        declared_assets[part] = expected
    if declared_assets != baseline_assets:
        errors.append(
            {
                "code": "manifest_protected_asset_inventory_mismatch",
                "missing": sorted(set(baseline_assets) - set(declared_assets)),
                "extra": sorted(set(declared_assets) - set(baseline_assets)),
            }
        )

    editable_assets = entry.get("editable_assets", [])
    if not isinstance(editable_assets, list):
        errors.append({"code": "manifest_editable_assets_invalid"})
        editable_assets = []
    declared_asset_changes: dict[tuple[str, str], dict[str, Any]] = {}
    for editable in editable_assets:
        action = editable.get("action") if isinstance(editable, dict) else None
        part = editable.get("part") if isinstance(editable, dict) else None
        baseline_sha = editable.get("baseline_sha256") if isinstance(editable, dict) else None
        current_sha = editable.get("current_sha256") if isinstance(editable, dict) else None
        valid_hashes = (
            (action == "modify" and sha_re.fullmatch(str(baseline_sha or "")) and sha_re.fullmatch(str(current_sha or "")))
            or (action == "delete" and sha_re.fullmatch(str(baseline_sha or "")) and current_sha is None)
            or (action == "insert" and baseline_sha is None and sha_re.fullmatch(str(current_sha or "")))
        )
        if (
            not isinstance(editable, dict)
            or action not in {"modify", "insert", "delete"}
            or not isinstance(part, str)
            or not safe_member_name(part)
            or not part.startswith("ppt/media/")
            or not valid_hashes
            or not isinstance(editable.get("baseline_owner_slide_uids"), list)
            or not isinstance(editable.get("current_owner_slide_uids"), list)
            or any(
                not isinstance(uid, str) or uid not in uid_records
                for uid in [
                    *editable.get("baseline_owner_slide_uids", []),
                    *editable.get("current_owner_slide_uids", []),
                ]
            )
            or len(editable.get("baseline_owner_slide_uids", []))
            != len(set(editable.get("baseline_owner_slide_uids", [])))
            or len(editable.get("current_owner_slide_uids", []))
            != len(set(editable.get("current_owner_slide_uids", [])))
            or not isinstance(editable.get("reason"), str)
            or len(editable["reason"].strip()) < 10
            or not isinstance(editable.get("reviewed_by"), str)
            or not editable["reviewed_by"].strip()
            or not valid_review_date(editable.get("reviewed_at"))
        ):
            errors.append({"code": "manifest_editable_asset_invalid"})
            continue
        key = (str(action), part)
        if key in declared_asset_changes:
            errors.append({"code": "manifest_editable_asset_duplicate", "action": action, "part": part})
        normalized_editable = dict(editable)
        if isinstance(baseline_sha, str):
            normalized_editable["baseline_sha256"] = baseline_sha.lower()
        if isinstance(current_sha, str):
            normalized_editable["current_sha256"] = current_sha.lower()
        normalized_editable["baseline_owner_slide_uids"] = sorted(editable["baseline_owner_slide_uids"])
        normalized_editable["current_owner_slide_uids"] = sorted(editable["current_owner_slide_uids"])
        declared_asset_changes[key] = normalized_editable

    actual_asset_changes: dict[tuple[str, str], tuple[str | None, str | None]] = {}
    for part in set(baseline_assets) | set(current_assets):
        before_hash, after_hash = baseline_assets.get(part), current_assets.get(part)
        if before_hash == after_hash:
            continue
        action = "modify" if before_hash is not None and after_hash is not None else "delete" if before_hash else "insert"
        actual_asset_changes[(action, part)] = (before_hash, after_hash)
    if set(declared_asset_changes) != set(actual_asset_changes):
        errors.append(
            {
                "code": "manifest_editable_asset_diff_mismatch",
                "missing": sorted(set(actual_asset_changes) - set(declared_asset_changes)),
                "extra": sorted(set(declared_asset_changes) - set(actual_asset_changes)),
            }
        )
    for key, (before_hash, after_hash) in actual_asset_changes.items():
        editable = declared_asset_changes.get(key)
        if editable is None:
            continue
        if editable.get("baseline_sha256") != before_hash or editable.get("current_sha256") != after_hash:
            errors.append({"code": "manifest_editable_asset_hash_mismatch", "action": key[0], "part": key[1]})
        baseline_owners = slide_uids_reaching_part(uid_records, "baseline", baseline["payloads"], key[1])
        current_owners = slide_uids_reaching_part(uid_records, "current", xml_payloads, key[1])
        if (
            editable.get("baseline_owner_slide_uids") != baseline_owners
            or editable.get("current_owner_slide_uids") != current_owners
        ):
            errors.append(
                {
                    "code": "manifest_editable_asset_owner_mismatch",
                    "action": key[0],
                    "part": key[1],
                    "expected_baseline_owners": baseline_owners,
                    "expected_current_owners": current_owners,
                }
            )

    protected_shapes = entry.get("protected_shapes", [])
    if not isinstance(protected_shapes, list):
        errors.append({"code": "manifest_protected_shapes_invalid"})
        protected_shapes = []
    declared_shapes: dict[tuple[str, str], str] = {}
    for protected in protected_shapes:
        if not isinstance(protected, dict):
            errors.append({"code": "manifest_protected_shape_invalid"})
            continue
        protected_uid = protected.get("slide_uid")
        record = uid_records.get(protected_uid) if isinstance(protected_uid, str) else None
        expected = str(protected.get("sha256") or "").lower()
        shape_id = str(protected.get("shape_id") or "")
        if (
            record is None
            or record.get("action") not in {"keep", "delete"}
            or not shape_id
            or not sha_re.fullmatch(expected)
        ):
            errors.append({"code": "manifest_protected_shape_invalid", "slide_uid": protected.get("slide_uid")})
            continue
        key = (str(protected["slide_uid"]), shape_id)
        if key in declared_shapes:
            errors.append({"code": "manifest_protected_shape_duplicate", "slide_uid": key[0], "shape_id": key[1]})
        declared_shapes[key] = expected

    editable_shapes = entry.get("editable_shapes", [])
    if not isinstance(editable_shapes, list):
        errors.append({"code": "manifest_editable_shapes_invalid"})
        editable_shapes = []
    editable_keys: set[tuple[str, str]] = set()
    editable_operations: dict[tuple[str, str], str] = {}
    for editable in editable_shapes:
        if (
            not isinstance(editable, dict)
            or not isinstance(editable.get("slide_uid"), str)
            or editable["slide_uid"] not in uid_records
            or uid_records[editable["slide_uid"]].get("action") != "keep"
            or not isinstance(editable.get("shape_id"), (str, int))
            or not str(editable.get("shape_id")).strip()
            or editable.get("operation") not in {"modify", "insert", "delete"}
            or not isinstance(editable.get("reason"), str)
            or len(editable["reason"].strip()) < 10
            or not isinstance(editable.get("reviewed_by"), str)
            or not editable["reviewed_by"].strip()
            or not valid_review_date(editable.get("reviewed_at"))
        ):
            errors.append({"code": "manifest_editable_shape_invalid"})
            continue
        key = (editable["slide_uid"], str(editable["shape_id"]))
        if key in editable_keys:
            errors.append({"code": "manifest_editable_shape_duplicate", "slide_uid": key[0], "shape_id": key[1]})
        editable_keys.add(key)
        editable_operations[key] = editable["operation"]

    actual_baseline_shapes: dict[tuple[str, str], str] = {}
    actual_current_shapes: dict[tuple[str, str], str] = {}
    for uid, record in uid_records.items():
        action = record.get("action")
        baseline_topology = record.get("baseline") if isinstance(record.get("baseline"), dict) else {}
        current_topology = record.get("current") if isinstance(record.get("current"), dict) else {}
        baseline_payload = baseline["payloads"].get(baseline_topology.get("slide_part"))
        current_payload = xml_payloads.get(current_topology.get("slide_part"))
        if action in {"keep", "delete"} and baseline_payload is not None:
            try:
                for shape_id, digest in shape_inventory(baseline_payload).items():
                    actual_baseline_shapes[(uid, shape_id)] = digest
            except ValueError:
                errors.append({"code": "baseline_shape_inventory_invalid", "slide_uid": uid})
        if action in {"keep", "insert"} and current_payload is not None:
            try:
                for shape_id, digest in shape_inventory(current_payload).items():
                    actual_current_shapes[(uid, shape_id)] = digest
            except ValueError:
                errors.append({"code": "current_shape_inventory_invalid", "slide_uid": uid})

    if declared_shapes != actual_baseline_shapes:
        errors.append(
            {
                "code": "manifest_protected_shape_inventory_mismatch",
                "missing": sorted(set(actual_baseline_shapes) - set(declared_shapes)),
                "extra": sorted(set(declared_shapes) - set(actual_baseline_shapes)),
            }
        )
    actual_shape_operations: dict[tuple[str, str], str] = {}
    for uid, record in uid_records.items():
        if record.get("action") != "keep":
            continue
        baseline_keys = {key for key in actual_baseline_shapes if key[0] == uid}
        current_keys = {key for key in actual_current_shapes if key[0] == uid}
        for key in baseline_keys | current_keys:
            before_hash, after_hash = actual_baseline_shapes.get(key), actual_current_shapes.get(key)
            if before_hash == after_hash:
                continue
            actual_shape_operations[key] = (
                "modify" if before_hash is not None and after_hash is not None else "delete" if before_hash else "insert"
            )
    if editable_operations != actual_shape_operations:
        errors.append(
            {
                "code": "manifest_editable_shape_diff_mismatch",
                "missing": sorted(set(actual_shape_operations) - set(editable_operations)),
                "extra": sorted(set(editable_operations) - set(actual_shape_operations)),
            }
        )
    for key in set(editable_operations) & set(actual_shape_operations):
        if editable_operations[key] != actual_shape_operations[key]:
            errors.append(
                {
                    "code": "manifest_editable_shape_operation_mismatch",
                    "slide_uid": key[0],
                    "shape_id": key[1],
                }
            )

    protected_shells = entry.get("protected_slide_shells", [])
    if not isinstance(protected_shells, list):
        errors.append({"code": "manifest_protected_slide_shells_invalid"})
        protected_shells = []
    declared_shells: dict[str, str] = {}
    for shell in protected_shells:
        if (
            not isinstance(shell, dict)
            or shell.get("slide_uid") not in uid_records
            or uid_records[shell["slide_uid"]].get("action") not in {"keep", "delete"}
            or not sha_re.fullmatch(str(shell.get("sha256") or ""))
        ):
            errors.append({"code": "manifest_protected_slide_shell_invalid"})
            continue
        uid = shell["slide_uid"]
        if uid in declared_shells:
            errors.append({"code": "manifest_protected_slide_shell_duplicate", "slide_uid": uid})
        declared_shells[uid] = str(shell["sha256"]).lower()
    actual_baseline_shells: dict[str, str] = {}
    for uid, record in uid_records.items():
        if record.get("action") not in {"keep", "delete"}:
            continue
        topology = record.get("baseline") if isinstance(record.get("baseline"), dict) else {}
        payload = baseline["payloads"].get(topology.get("slide_part"))
        if payload is None:
            continue
        try:
            actual_baseline_shells[uid] = slide_shell_hash(payload)
        except ValueError:
            errors.append({"code": "baseline_slide_shell_invalid", "slide_uid": uid})
    if declared_shells != actual_baseline_shells:
        errors.append(
            {
                "code": "manifest_protected_slide_shell_inventory_mismatch",
                "missing": sorted(set(actual_baseline_shells) - set(declared_shells)),
                "extra": sorted(set(declared_shells) - set(actual_baseline_shells)),
            }
        )
    for uid, expected in actual_baseline_shells.items():
        record = uid_records[uid]
        if record.get("action") != "keep":
            continue
        topology = record.get("current") if isinstance(record.get("current"), dict) else {}
        payload = xml_payloads.get(topology.get("slide_part"))
        if payload is None:
            continue
        try:
            actual = slide_shell_hash(payload)
        except ValueError:
            errors.append({"code": "current_slide_shell_invalid", "slide_uid": uid})
            continue
        if actual != expected:
            errors.append({"code": "manifest_nonshape_slide_xml_changed", "slide_uid": uid})

    if canonical_notes is not None:
        current_uid_by_index = {
            record["current"]["index"]: record["slide_uid"]
            for record in records
            if record.get("action") in {"keep", "insert"}
            and isinstance(record.get("current"), dict)
            and type(record["current"].get("index")) is int
            and isinstance(record.get("slide_uid"), str)
        }
        expected_uids = set(current_uid_by_index.values())
        if set(canonical_notes) != expected_uids:
            errors.append(
                {
                    "code": "canonical_notes_uid_set_mismatch",
                    "missing": sorted(expected_uids - set(canonical_notes)),
                    "extra": sorted(set(canonical_notes) - expected_uids),
                }
            )
        for slide in mapping:
            uid = current_uid_by_index.get(slide["index"])
            note_part = slide.get("notes_part")
            payload = xml_payloads.get(note_part) if isinstance(note_part, str) else None
            if uid is None or payload is None:
                errors.append({"code": "canonical_notes_mapping_missing", "slide": slide["index"]})
                continue
            try:
                embedded = note_body_text(ET.fromstring(payload))
            except (ET.ParseError, ValueError) as exc:
                errors.append(
                    {
                        "code": str(exc) if isinstance(exc, ValueError) else "canonical_notes_xml_invalid",
                        "slide_uid": uid,
                        "slide": slide["index"],
                    }
                )
                embedded = ""
            if normalize_note_text(embedded) != canonical_notes.get(uid):
                errors.append(
                    {"code": "canonical_notes_text_mismatch", "slide_uid": uid, "slide": slide["index"]}
                )


def audit_deck(path: Path, args: argparse.Namespace) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    initial_stat = path.stat()
    package_limit = args.max_package_mb * 1024 * 1024
    if initial_stat.st_size > package_limit:
        return {
            "path": path.name if args.redact_paths else str(path),
            "sha256": None,
            "size": initial_stat.st_size,
            "mtime_ns": initial_stat.st_mtime_ns,
            "member_count": 0,
            "slides": 0,
            "slide_parts": 0,
            "notes_parts": 0,
            "nonempty_notes": 0,
            "audio_count": 0,
            "video_count": 0,
            "embedding_count": 0,
            "activex_count": 0,
            "macro_count": 0,
            "content_types_scope": "core-presentation-slide-notes",
            "error_count": 1,
            "errors": [
                {
                    "code": "package_file_size_limit_exceeded",
                    "bytes": initial_stat.st_size,
                    "limit": package_limit,
                }
            ],
        }
    snapshot = read_members(path, errors, args)
    members, xml_payloads, member_hashes = snapshot
    deck_sha = snapshot.sha256
    if not snapshot.usable:
        stat = path.stat()
        return {
            "path": path.name if args.redact_paths else str(path),
            "sha256": deck_sha,
            "size": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
            "member_count": 0,
            "content_types_scope": "core-presentation-slide-notes",
            "slides": 0,
            "slide_parts": 0,
            "notes_parts": 0,
            "nonempty_notes": 0,
            "audio_count": 0,
            "video_count": 0,
            "embedding_count": 0,
            "activex_count": 0,
            "macro_count": 0,
            "error_count": len(errors),
            "errors": errors,
        }
    roots: dict[str, ET.Element] = {}
    for name, payload in xml_payloads.items():
        root = parse_xml(name, payload, errors)
        if root is not None:
            roots[name] = root

    strict_parts = strict_ooxml_parts(roots, xml_payloads)
    if strict_parts:
        errors.append(
            {
                "code": "strict_ooxml_not_supported",
                "parts": strict_parts[:20],
                "detail": "This checker intentionally supports Transitional OOXML only.",
            }
        )

    if members:
        validate_content_types(members, roots, errors)
        rel_maps = validate_relationships(
            members, roots, args.forbid_external_file_links, errors
        )
        validate_required_part_topology(members, roots, rel_maps, errors)
        counts = validate_slides_and_notes(
            members,
            roots,
            rel_maps,
            args.require_notes,
            args.forbid_note_metadata,
            errors,
        )
    else:
        counts = {
            "slides": 0,
            "slide_parts": 0,
            "notes_parts": 0,
            "nonempty_notes": 0,
            "_slide_mapping": [],
        }

    slide_mapping = counts.pop("_slide_mapping")
    manifest_entry = args.manifest_map.get(os.path.normcase(str(path)))
    if manifest_entry is not None:
        baseline = inspect_baseline(manifest_entry["_baseline_path"], args)
        for baseline_error in baseline["errors"]:
            scoped_error = dict(baseline_error)
            scoped_error.setdefault("scope", "baseline")
            errors.append(scoped_error)
        validate_manifest_entry(
            deck_sha,
            slide_mapping,
            xml_payloads,
            member_hashes,
            baseline,
            manifest_entry,
            args.canonical_notes_map.get(os.path.normcase(str(path)))
            if args.canonical_notes is not None
            else None,
            args,
            errors,
        )

    expected = args.expected_slide_map.get(os.path.normcase(str(path)))
    if expected is not None and counts["slides"] != expected:
        errors.append(
            {
                "code": "expected_slide_count_mismatch",
                "expected": expected,
                "actual": counts["slides"],
            }
        )

    audio, video = detect_audio_and_video(members, roots)
    embeddings, activex, macros = detect_embedded_and_activex(members, roots)
    if args.forbid_audio and audio:
        errors.append({"code": "audio_present", "members": audio})
    if args.forbid_video and video:
        errors.append({"code": "video_present", "members": video})
    if args.forbid_embeddings and embeddings:
        errors.append({"code": "embedded_objects_present", "members": embeddings})
    if args.forbid_activex and activex:
        errors.append({"code": "activex_present", "members": activex})
    if args.forbid_macros and macros:
        errors.append({"code": "macros_present", "members": macros})

    stat = path.stat()
    if (initial_stat.st_size, initial_stat.st_mtime_ns) != (stat.st_size, stat.st_mtime_ns):
        errors.append({"code": "input_drift_during_audit"})
    return {
        "path": path.name if args.redact_paths else str(path),
        "sha256": deck_sha,
        "size": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
        "member_count": len(members),
        "content_types_scope": "core-presentation-slide-notes",
        **counts,
        "audio_count": len(audio),
        "video_count": len(video),
        "embedding_count": len(embeddings),
        "activex_count": len(activex),
        "macro_count": len(macros),
        "error_count": len(errors),
        "errors": errors,
    }


def fingerprint(
    paths: Iterable[Path], args: argparse.Namespace
) -> tuple[dict[str, tuple[int, int, str]], list[dict[str, Any]]]:
    result: dict[str, tuple[int, int, str]] = {}
    errors: list[dict[str, Any]] = []
    package_limit = args.max_package_mb * 1024 * 1024
    for path in paths:
        try:
            before = path.stat()
            if before.st_size > package_limit:
                errors.append(
                    {
                        "code": "package_file_size_limit_exceeded",
                        "path": str(path),
                        "bytes": before.st_size,
                        "limit": package_limit,
                    }
                )
                continue
            digest = sha256_file(path)
            after = path.stat()
            if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                errors.append({"code": "input_drift_during_hash", "path": str(path)})
                continue
            result[str(path)] = (after.st_size, after.st_mtime_ns, digest)
        except OSError as exc:
            errors.append(
                {
                    "code": "input_changed_or_unreadable",
                    "path": str(path),
                    "detail": str(exc),
                }
            )
    return result, errors


def audit_deck_safe(path: Path, args: argparse.Namespace) -> dict[str, Any]:
    try:
        return audit_deck(path, args)
    except (OSError, RuntimeError, NotImplementedError, zipfile.BadZipFile) as exc:
        return {
            "path": path.name if args.redact_paths else str(path),
            "sha256": None,
            "slides": 0,
            "error_count": 1,
            "errors": [
                {
                    "code": "round_file_changed_or_unreadable",
                    "detail": str(exc),
                }
            ],
        }
    except (TypeError, KeyError, AttributeError, ValueError, ET.ParseError) as exc:
        return {
            "path": path.name if args.redact_paths else str(path),
            "sha256": None,
            "slides": 0,
            "error_count": 1,
            "errors": [
                {
                    "code": "audit_internal_failure",
                    "detail": f"{type(exc).__name__}: {exc}",
                }
            ],
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="PPTX files or directories searched recursively")
    parser.add_argument("--require-notes", action="store_true", help="require one nonempty notes slide per slide")
    parser.add_argument(
        "--forbid-note-metadata",
        action="store_true",
        help="reject time codes, source lines, URLs, DOI strings, and production metadata in notes",
    )
    parser.add_argument("--forbid-audio", action="store_true", help="reject embedded audio media")
    parser.add_argument("--forbid-video", action="store_true", help="reject embedded video media")
    parser.add_argument("--forbid-embeddings", action="store_true", help="reject OLE and other embedded objects")
    parser.add_argument("--forbid-activex", action="store_true", help="reject ActiveX parts")
    parser.add_argument("--forbid-macros", action="store_true", help="reject VBA and macro-enabled package evidence")
    parser.add_argument(
        "--forbid-external-file-links",
        action="store_true",
        help="reject external local or relative-file relationships; allow-listed web and mail links remain allowed",
    )
    parser.add_argument(
        "--expected-slides",
        type=int,
        help="expected slide count; valid only when exactly one PPTX is discovered",
    )
    parser.add_argument(
        "--expected-total-slides",
        type=int,
        help="expected total slide count across all discovered PPTX files",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="optional version-2 slide identity/topology manifest JSON",
    )
    parser.add_argument(
        "--baseline-root",
        type=Path,
        help="immutable baseline directory required with --manifest",
    )
    parser.add_argument(
        "--require-source-keys",
        action="store_true",
        help="require each manifest slide to have source_keys or a specific exemption",
    )
    parser.add_argument(
        "--source-ledger",
        type=Path,
        help="optional JSON source ledger whose keys must cover manifest source_keys",
    )
    parser.add_argument(
        "--canonical-notes",
        type=Path,
        help="optional version-1 JSON mapping manifest slide_uid values to canonical note text",
    )
    parser.add_argument(
        "--frozen-dependency",
        action="append",
        type=Path,
        default=[],
        help="additional source, rights, or approval file whose hash must remain stable; repeat as needed",
    )
    parser.add_argument(
        "--exclude-regex",
        action="append",
        default=[],
        help="case-insensitive regex for paths to exclude during directory discovery; repeat as needed",
    )
    parser.add_argument("--max-members", type=int, default=10000, help="maximum ZIP member count per deck")
    parser.add_argument(
        "--max-package-mb",
        type=int,
        default=1024,
        help="maximum compressed PPTX file size before hashing",
    )
    parser.add_argument(
        "--max-uncompressed-mb",
        type=int,
        default=512,
        help="maximum total uncompressed package size per deck",
    )
    parser.add_argument(
        "--max-xml-mb",
        type=int,
        default=16,
        help="maximum uncompressed size of any XML, relationship, or VML part",
    )
    parser.add_argument(
        "--max-compression-ratio",
        type=float,
        default=250.0,
        help="maximum uncompressed/compressed ratio for any ZIP member",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=1,
        help="repeat the read-only audit and require identical size/mtime/hash; this proves stability, not saturation",
    )
    parser.add_argument("--output", type=Path, help="optional new .json report path; existing files are never replaced")
    parser.add_argument(
        "--redact-paths",
        action="store_true",
        help="redact local paths and deck filenames throughout the JSON report",
    )
    args = parser.parse_args()
    if args.rounds < 1:
        parser.error("--rounds must be at least 1")
    if (
        args.max_members < 1
        or args.max_package_mb < 1
        or args.max_uncompressed_mb < 1
        or args.max_xml_mb < 1
        or not math.isfinite(args.max_compression_ratio)
        or args.max_compression_ratio <= 1
    ):
        parser.error("ZIP safety limits must be positive")
    if args.require_source_keys and (not args.manifest or not args.source_ledger):
        parser.error("--require-source-keys requires --manifest and --source-ledger")
    if args.source_ledger and not args.manifest:
        parser.error("--source-ledger requires --manifest")
    if args.canonical_notes and not args.manifest:
        parser.error("--canonical-notes requires --manifest")
    return args


def validate_output_path(output: Path | None, protected_inputs: Iterable[Path]) -> Path | None:
    if output is None:
        return None
    resolved = output.expanduser().resolve()
    if resolved.suffix.lower() != ".json":
        raise ValueError("--output must use the .json extension")
    protected = [path.expanduser().resolve() for path in protected_inputs]
    output_key = os.path.normcase(str(resolved))
    for path in protected:
        if output_key == os.path.normcase(str(path)):
            raise ValueError("--output must not be the same path as any input or manifest")
        if resolved.exists() and path.exists() and os.path.samefile(resolved, path):
            raise ValueError("--output must not alias any input or manifest")
    if resolved.exists():
        raise FileExistsError(f"Output already exists; choose a new report path: {resolved}")
    return resolved


def write_json_atomic_no_clobber(
    path: Path, rendered: str, pre_link_guard: Callable[[], None] | None = None
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(rendered)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
            temporary_name = handle.name
        if pre_link_guard is not None:
            pre_link_guard()
        # Hard-link creation is atomic and fails if the destination appeared
        # after validation. This deliberately refuses a non-atomic fallback.
        os.link(temporary_name, path)
        Path(temporary_name).unlink()
        temporary_name = None
    finally:
        if temporary_name and Path(temporary_name).exists():
            Path(temporary_name).unlink()


def main() -> int:
    args = parse_args()
    try:
        paths = discover(args.inputs, args.exclude_regex)
    except (FileNotFoundError, OSError, re.error) as exc:
        print(emit_json({"ok": False, "error": str(exc)}, args.redact_paths))
        return 2
    if not paths:
        print(emit_json({"ok": False, "error": "No PPTX files found"}, args.redact_paths))
        return 2

    if args.expected_slides is not None and len(paths) != 1:
        print(
            emit_json(
                {"ok": False, "error": "--expected-slides requires exactly one discovered PPTX"},
                args.redact_paths,
            )
        )
        return 2
    args.expected_slide_map = (
        {os.path.normcase(str(paths[0])): args.expected_slides}
        if args.expected_slides is not None
        else {}
    )
    try:
        explicit_dependencies = [
            *([args.manifest.expanduser().resolve()] if args.manifest else []),
            *([args.source_ledger.expanduser().resolve()] if args.source_ledger else []),
            *([args.canonical_notes.expanduser().resolve()] if args.canonical_notes else []),
            *(path.expanduser().resolve() for path in args.frozen_dependency),
        ]
        explicit_dependencies = list(
            {os.path.normcase(str(path)): path for path in explicit_dependencies}.values()
        )
        protected_inputs = [*paths, *explicit_dependencies]
        output_path = validate_output_path(args.output, protected_inputs)
        dependency_preload, dependency_preload_errors = fingerprint(explicit_dependencies, args)
        if dependency_preload_errors:
            raise ValueError(f"Frozen dependency unreadable: {dependency_preload_errors}")
        def frozen_value(path: Path | None) -> tuple[int, int, str] | None:
            return dependency_preload.get(str(path.expanduser().resolve())) if path else None

        args.source_ledger_keys = load_source_ledger(
            args.source_ledger, frozen_value(args.source_ledger)
        )
        args.manifest_map = (
            load_manifest(
                args.manifest,
                paths,
                args.baseline_root,
                frozen_value(args.manifest),
            )
            if args.manifest
            else {}
        )
        args.canonical_notes_map = load_canonical_notes(
            args.canonical_notes,
            paths,
            frozen_value(args.canonical_notes),
        )
        baseline_dependencies = [
            entry["_baseline_path"] for entry in args.manifest_map.values()
        ]
        args.frozen_dependency_paths = list(
            {
                os.path.normcase(str(path)): path
                for path in [*explicit_dependencies, *baseline_dependencies]
            }.values()
        )
        dependency_baseline, dependency_baseline_errors = fingerprint(
            args.frozen_dependency_paths, args
        )
        if dependency_baseline_errors:
            raise ValueError(f"Frozen dependency unreadable: {dependency_baseline_errors}")
        if any(dependency_baseline.get(key) != value for key, value in dependency_preload.items()):
            raise ValueError("Frozen dependency changed while configuration was loaded")
        args.frozen_dependency_fingerprints = dependency_baseline
    except (ValueError, FileExistsError, OSError, json.JSONDecodeError) as exc:
        print(emit_json({"ok": False, "error": str(exc)}, args.redact_paths))
        return 2

    baseline, baseline_errors = fingerprint(paths, args)
    baseline_path_keys = set(baseline)

    def audit_commit_guard() -> None:
        guard_paths = discover(args.inputs, args.exclude_regex)
        if {str(path) for path in guard_paths} != baseline_path_keys:
            raise ValueError("audit_commit_guard_input_set_changed")
        guard_fingerprint, guard_errors = fingerprint(guard_paths, args)
        if guard_errors or guard_fingerprint != baseline:
            raise ValueError("audit_commit_guard_input_changed")
        guard_dependencies, guard_dependency_errors = fingerprint(
            args.frozen_dependency_paths, args
        )
        if guard_dependency_errors or guard_dependencies != dependency_baseline:
            raise ValueError("audit_commit_guard_dependency_changed")

    if baseline_errors:
        rendered = emit_json(
            {
                "ok": False,
                "stable": False,
                "errors": baseline_errors,
            },
            args.redact_paths,
        )
        if output_path:
            try:
                write_json_atomic_no_clobber(output_path, rendered, audit_commit_guard)
            except (OSError, ValueError, re.error) as exc:
                print(emit_json({"ok": False, "error": f"report_write_failed: {exc}"}, args.redact_paths))
                return 2
        print(rendered)
        return 2
    rounds: list[dict[str, Any]] = []
    stable = True
    for number in range(1, args.rounds + 1):
        global_errors: list[dict[str, Any]] = []
        try:
            round_paths = discover(args.inputs, args.exclude_regex)
        except (FileNotFoundError, OSError, re.error) as exc:
            round_paths = []
            global_errors.append({"code": "round_discovery_failure", "detail": str(exc)})
        round_path_keys = {str(path) for path in round_paths}
        if round_path_keys != baseline_path_keys:
            stable = False
            global_errors.append(
                {
                    "code": "discovered_pptx_set_changed",
                    "added": sorted(round_path_keys - baseline_path_keys),
                    "removed": sorted(baseline_path_keys - round_path_keys),
                }
            )
        decks = [audit_deck_safe(path, args) for path in round_paths]
        for path, deck in zip(round_paths, decks):
            expected_snapshot = baseline.get(str(path))
            actual_snapshot = (deck.get("size"), deck.get("mtime_ns"), deck.get("sha256"))
            if expected_snapshot is None or actual_snapshot != expected_snapshot:
                global_errors.append(
                    {
                        "code": "audited_package_snapshot_mismatch",
                        "path": str(path),
                    }
                )
        actual_total = sum(deck["slides"] for deck in decks)
        if args.expected_total_slides is not None and actual_total != args.expected_total_slides:
            global_errors.append(
                {
                    "code": "expected_total_slide_count_mismatch",
                    "expected": args.expected_total_slides,
                    "actual": actual_total,
                }
            )
        current, fingerprint_errors = fingerprint(round_paths, args)
        global_errors.extend(fingerprint_errors)
        if current != baseline:
            stable = False
        dependency_current, dependency_errors = fingerprint(args.frozen_dependency_paths, args)
        global_errors.extend(
            {**error, "scope": "frozen_dependency"} for error in dependency_errors
        )
        if dependency_current != dependency_baseline:
            stable = False
            global_errors.append({"code": "frozen_dependency_changed"})
        rounds.append(
            {
                "round": number,
                "ok": (
                    all(deck["error_count"] == 0 for deck in decks)
                    and not global_errors
                    and current == baseline
                    and dependency_current == dependency_baseline
                ),
                "errors": global_errors,
                "decks": decks,
            }
        )

    final_errors: list[dict[str, Any]] = []
    try:
        final_paths = discover(args.inputs, args.exclude_regex)
    except (FileNotFoundError, OSError, re.error) as exc:
        final_paths = []
        final_errors.append({"code": "final_discovery_failure", "detail": str(exc)})
    final_path_keys = {str(path) for path in final_paths}
    final_fingerprint, final_fingerprint_errors = fingerprint(final_paths, args)
    final_errors.extend(final_fingerprint_errors)
    if final_path_keys != baseline_path_keys or final_fingerprint != baseline:
        stable = False
        final_errors.append({"code": "final_input_set_or_hash_changed"})
    final_dependency_fingerprint, final_dependency_errors = fingerprint(
        args.frozen_dependency_paths, args
    )
    final_errors.extend(
        {**error, "scope": "frozen_dependency"} for error in final_dependency_errors
    )
    if final_dependency_fingerprint != dependency_baseline:
        stable = False
        final_errors.append({"code": "final_frozen_dependency_changed"})

    def dependency_records(values: dict[str, tuple[int, int, str]]) -> list[dict[str, Any]]:
        return [
            {"path": path, "size": data[0], "mtime_ns": data[1], "sha256": data[2]}
            for path, data in sorted(values.items())
        ]

    result = {
        "ok": stable and all(item["ok"] for item in rounds),
        "audit_scope": {
            "package_integrity": True,
            "manifest_preservation": bool(args.manifest),
            "canonical_notes": bool(args.canonical_notes),
            "source_ledger": bool(args.source_ledger),
        },
        "repeated_rounds_prove_stability_only": True,
        "round_count": args.rounds,
        "deck_count": len(paths),
        "stable": stable,
        "dependency_stable": final_dependency_fingerprint == dependency_baseline,
        "frozen_dependencies_start": dependency_records(dependency_baseline),
        "frozen_dependencies_end": dependency_records(final_dependency_fingerprint),
        "final_stability_errors": final_errors,
        "rounds": rounds,
    }
    if final_errors:
        result["ok"] = False
    rendered = emit_json(result, args.redact_paths)
    if output_path:
        try:
            write_json_atomic_no_clobber(output_path, rendered, audit_commit_guard)
        except (OSError, ValueError, re.error) as exc:
            print(emit_json({"ok": False, "error": f"report_write_failed: {exc}"}, args.redact_paths))
            return 2
    print(rendered)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
