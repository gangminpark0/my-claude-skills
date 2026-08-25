#!/usr/bin/env python3
"""Initialize a version-2 manifest for one frozen PPTX revision batch.

The current deck and immutable baseline must be byte-identical.  The generated
UIDs are scoped to this batch.  After an owner-approved structural change,
freeze the approved candidate as a new baseline and initialize a new batch.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from xml.etree import ElementTree as ET

from audit_pptx_package import (
    emit_json,
    parse_xml,
    read_members,
    relationship_inventory,
    read_json_snapshot,
    sha256_file,
    shape_inventory,
    slide_shell_hash,
    strict_ooxml_parts,
    validate_content_types,
    validate_relationships,
    validate_required_part_topology,
    validate_slides_and_notes,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("decks", nargs="+", type=Path, help="PPTX files to initialize")
    parser.add_argument(
        "--baseline-root",
        type=Path,
        required=True,
        help="directory containing immutable baseline PPTX files with matching basenames",
    )
    parser.add_argument("--output", type=Path, required=True, help="new .json manifest path")
    parser.add_argument("--require-notes", action="store_true", help="require one nonempty note per slide")
    parser.add_argument(
        "--allow-powerpoint-process",
        action="store_true",
        help="allow initialization while PowerPoint is detected after explicit risk approval",
    )
    parser.add_argument(
        "--approval-record",
        type=Path,
        help="version-1 JSON approval required with --allow-powerpoint-process",
    )
    parser.add_argument("--redact-paths", action="store_true", help="redact local paths in console JSON")
    return parser.parse_args()


def validate_paths(args: argparse.Namespace) -> tuple[list[Path], dict[str, Path], Path, Path]:
    decks = [path.expanduser().resolve() for path in args.decks]
    if any(not path.is_file() or path.suffix.lower() != ".pptx" for path in decks):
        raise ValueError("Every deck must be an existing .pptx file")
    normalized = [os.path.normcase(str(path)) for path in decks]
    if len(normalized) != len(set(normalized)):
        raise ValueError("Duplicate PPTX input")
    basenames = [path.name.casefold() for path in decks]
    if len(basenames) != len(set(basenames)):
        raise ValueError("Manifest deck basenames must be unique")

    baseline_root = args.baseline_root.expanduser().resolve()
    if not baseline_root.is_dir():
        raise ValueError("--baseline-root must be an existing directory")
    baseline_by_name: dict[str, list[Path]] = {}
    for candidate in baseline_root.rglob("*"):
        if candidate.is_file() and candidate.suffix.casefold() == ".pptx" and not candidate.name.startswith("~$"):
            baseline_by_name.setdefault(candidate.name.casefold(), []).append(candidate.resolve())
    baseline_map: dict[str, Path] = {}
    for deck in decks:
        matches = baseline_by_name.get(deck.name.casefold(), [])
        if len(matches) != 1:
            raise ValueError(f"Each deck must match exactly one baseline by basename: {deck.name}")
        if os.path.samefile(deck, matches[0]):
            raise ValueError("Baseline PPTX must be a separate immutable copy")
        baseline_map[os.path.normcase(str(deck))] = matches[0]
        if (deck.parent / f"~${deck.name}").exists() or (matches[0].parent / f"~${matches[0].name}").exists():
            raise ValueError("PowerPoint lock file detected; close the deck before manifest initialization")

    baseline_paths = list(baseline_map.values())
    for baseline in baseline_paths:
        if any(os.path.samefile(baseline, current) for current in decks):
            raise ValueError("Immutable baseline PPTX must not alias any current deck")
    for index, baseline in enumerate(baseline_paths):
        if any(os.path.samefile(baseline, other) for other in baseline_paths[index + 1 :]):
            raise ValueError("Each deck must have a distinct immutable baseline PPTX")

    output = args.output.expanduser().resolve()
    if output.suffix.lower() != ".json":
        raise ValueError("--output must use the .json extension")
    if os.path.normcase(str(output)) in set(normalized):
        raise ValueError("--output must not be the same path as an input PPTX")
    if output.exists():
        raise FileExistsError("Output exists; choose a new path instead of resetting the manifest lineage")
    return decks, baseline_map, baseline_root, output


def stable_fingerprint(path: Path, max_package_mb: int = 1024) -> tuple[int, int, str]:
    before = path.stat()
    if before.st_size > max_package_mb * 1024 * 1024:
        raise ValueError("package_file_size_limit_exceeded")
    digest = sha256_file(path)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError("baseline_drift_detected")
    return after.st_size, after.st_mtime_ns, digest


def load_approval_record(path: Path) -> tuple[Path, tuple[int, int, str], dict[str, str]]:
    resolved = path.expanduser().resolve()
    if not resolved.is_file() or resolved.suffix.lower() != ".json":
        raise ValueError("--approval-record must be an existing .json file")
    payload, fingerprint = read_json_snapshot(resolved, max_bytes=1024 * 1024)
    if not isinstance(payload, dict) or type(payload.get("version")) is not int or payload.get("version") != 1:
        raise ValueError("Approval record must be a JSON object with version=1")
    accepted_by = payload.get("accepted_by")
    accepted_at = payload.get("accepted_at")
    rationale = payload.get("rationale")
    scope = payload.get("scope")
    try:
        valid_date = (
            isinstance(accepted_at, str)
            and re.fullmatch(r"\d{4}-\d{2}-\d{2}", accepted_at) is not None
            and dt.date.fromisoformat(accepted_at)
        )
    except ValueError:
        valid_date = False
    if (
        scope != "manifest-initialization-with-powerpoint-open"
        or not isinstance(accepted_by, str)
        or not accepted_by.strip()
        or not valid_date
        or not isinstance(rationale, str)
        or len(rationale.strip()) < 10
    ):
        raise ValueError("Approval record scope, reviewer, date, or rationale is invalid")
    if stable_fingerprint(resolved, max_package_mb=1) != fingerprint:
        raise ValueError("Approval record changed while it was read")
    return resolved, fingerprint, {
        "accepted_by": accepted_by.strip(),
        "accepted_at": str(accepted_at),
    }


def powerpoint_process_state() -> str:
    if os.name != "nt":
        return "not-applicable-non-windows"
    try:
        completed = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq POWERPNT.EXE", "/FO", "CSV", "/NH"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return "check-unavailable"
    if completed.returncode != 0:
        return "check-unavailable"
    output = completed.stdout.strip()
    if not output:
        return "check-unavailable"
    if "POWERPNT.EXE" in output.upper():
        return "detected"
    if output.upper().startswith("INFO:") or output.startswith("정보:"):
        return "not-detected"
    return "check-unavailable"


def lock_files_detected(paths: list[Path]) -> bool:
    return any((path.parent / f"~${path.name}").exists() for path in paths)


def inspect_topology(path: Path, require_notes: bool) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    limits = SimpleNamespace(
        max_members=10000,
        max_uncompressed_mb=512,
        max_xml_mb=16,
        max_compression_ratio=250.0,
    )
    snapshot = read_members(path, errors, limits)
    members, payloads, member_hashes = snapshot
    roots: dict[str, ET.Element] = {}
    for name, payload in payloads.items():
        root = parse_xml(name, payload, errors)
        if root is not None:
            roots[name] = root
    strict = strict_ooxml_parts(roots, payloads)
    if strict:
        errors.append({"code": "strict_ooxml_not_supported", "parts": strict[:20]})
    if snapshot.usable:
        validate_content_types(members, roots, errors)
        # A frozen manifest must never capture a machine-local file binding.
        relationships = validate_relationships(members, roots, True, errors)
        validate_required_part_topology(members, roots, relationships, errors)
        counts = validate_slides_and_notes(
            members,
            roots,
            relationships,
            require_notes,
            False,
            errors,
        )
    else:
        counts = {"slides": 0, "_slide_mapping": []}
    if errors:
        raise ValueError(f"Cannot initialize manifest for {path.name}: {json.dumps(errors, ensure_ascii=False)}")

    return {
        "sha256": snapshot.sha256,
        "fingerprint": (snapshot.size, snapshot.mtime_ns, snapshot.sha256),
        "mapping": counts["_slide_mapping"],
        "payloads": payloads,
        "member_hashes": member_hashes,
    }


def inspect_deck(
    path: Path, baseline_path: Path, baseline_root: Path, require_notes: bool
) -> tuple[dict[str, Any], dict[str, tuple[int, int, str]]]:
    current_before = stable_fingerprint(path)
    baseline_before = stable_fingerprint(baseline_path)
    current_context = inspect_topology(path, require_notes)
    baseline_context = inspect_topology(baseline_path, require_notes)
    current_after = stable_fingerprint(path)
    baseline_after = stable_fingerprint(baseline_path)
    if (
        current_before != current_context["fingerprint"]
        or current_context["fingerprint"] != current_after
        or baseline_before != baseline_context["fingerprint"]
        or baseline_context["fingerprint"] != baseline_after
    ):
        raise ValueError("baseline_drift_detected")
    if current_context["sha256"] != baseline_context["sha256"]:
        raise ValueError("Initial current deck must be byte-identical to its immutable baseline")
    if current_context["mapping"] != baseline_context["mapping"]:
        raise ValueError("Initial current and baseline slide topology differ")

    mapping = current_context["mapping"]
    slides: list[dict[str, Any]] = []
    protected_shapes: list[dict[str, str]] = []
    protected_slide_shells: list[dict[str, str]] = []
    for current in mapping:
        slide_part = current["slide_part"]
        slide_uid = f"slide-{uuid.uuid4()}"
        topology = {
            "index": current["index"],
            "presentation_rel_id": current["presentation_rel_id"],
            "slide_part": slide_part,
            "notes_part": current["notes_part"],
            "slide_sha256": hashlib.sha256(current_context["payloads"][slide_part]).hexdigest(),
        }
        slides.append(
            {
                "slide_uid": slide_uid,
                "action": "keep",
                "source_keys": [],
                "source_exemption": None,
                "baseline": copy.deepcopy(topology),
                "current": topology,
            }
        )
        for shape_id, digest in sorted(
            shape_inventory(current_context["payloads"][slide_part]).items(),
            key=lambda item: (
                int(item[0].split("@", 1)[0]) if item[0].split("@", 1)[0].isdigit() else 2**31,
                item[0],
            ),
        ):
            protected_shapes.append(
                {"slide_uid": slide_uid, "shape_id": shape_id, "sha256": digest}
            )
        protected_slide_shells.append(
            {"slide_uid": slide_uid, "sha256": slide_shell_hash(current_context["payloads"][slide_part])}
        )
    entry = {
        "file": path.name,
        "baseline_file": baseline_path.relative_to(baseline_root).as_posix(),
        "baseline_sha256": baseline_context["sha256"],
        "baseline_slide_count": len(baseline_context["mapping"]),
        "baseline_member_sha256": dict(sorted(baseline_context["member_hashes"].items())),
        "current_sha256": current_context["sha256"],
        "current_slide_count": len(mapping),
        "allowed_changed_parts": [],
        "protected_assets": [
            {"part": part, "sha256": digest}
            for part, digest in sorted(baseline_context["member_hashes"].items())
            if part.startswith("ppt/media/")
        ],
        "editable_assets": [],
        "protected_relationships": [
            {
                "source_part": source_part,
                "relationship_id": relationship_id,
                **binding,
            }
            for (source_part, relationship_id), binding in sorted(
                relationship_inventory(baseline_context["payloads"]).items()
            )
        ],
        "editable_relationships": [],
        "protected_shapes": protected_shapes,
        "editable_shapes": [],
        "protected_slide_shells": protected_slide_shells,
        "slides": slides,
    }
    fingerprints = {str(path): current_after, str(baseline_path): baseline_after}
    return entry, fingerprints


def prepare_atomic_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        handle.write(text)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
        return Path(handle.name)


def link_atomic_no_clobber(temporary: Path, path: Path) -> None:
    os.link(temporary, path)


def assert_commit_guard(
    decks: list[Path],
    baseline_paths: list[Path],
    frozen: dict[str, tuple[int, int, str]],
    initial_process_state: str,
    allow_powerpoint_process: bool,
) -> str:
    if lock_files_detected([*decks, *baseline_paths]):
        raise ValueError("PowerPoint lock file detected before manifest commit")
    process_state = powerpoint_process_state()
    if os.name == "nt" and process_state != initial_process_state:
        raise ValueError("PowerPoint process state changed during manifest initialization")
    if os.name == "nt" and process_state != "not-detected" and not allow_powerpoint_process:
        raise ValueError("PowerPoint process state is not safely closed before manifest commit")
    for frozen_path, expected in frozen.items():
        if stable_fingerprint(Path(frozen_path)) != expected:
            raise ValueError("baseline_drift_detected")
    return process_state


def main() -> int:
    args = parse_args()
    try:
        decks, baseline_map, baseline_root, output = validate_paths(args)
        baseline_paths = [baseline_map[os.path.normcase(str(path))] for path in decks]
        approval_path: Path | None = None
        approval_fingerprint: tuple[int, int, str] | None = None
        approval_summary: dict[str, str] | None = None
        if args.allow_powerpoint_process:
            if args.approval_record is None:
                raise ValueError("--allow-powerpoint-process requires --approval-record")
            approval_path, approval_fingerprint, approval_summary = load_approval_record(args.approval_record)
            if any(os.path.samefile(approval_path, path) for path in [*decks, *baseline_paths]):
                raise ValueError("Approval record must not alias a PPTX input")
            if os.path.normcase(str(approval_path)) == os.path.normcase(str(output)):
                raise ValueError("Approval record must not be the output manifest")
        elif args.approval_record is not None:
            raise ValueError("--approval-record is valid only with --allow-powerpoint-process")
        process_state = powerpoint_process_state()
        if os.name == "nt" and process_state != "not-detected" and not args.allow_powerpoint_process:
            raise ValueError(
                "PowerPoint process state is not safely closed; close PowerPoint or use --allow-powerpoint-process after explicit approval"
            )
        entries: list[dict[str, Any]] = []
        frozen: dict[str, tuple[int, int, str]] = {}
        for path in decks:
            entry, fingerprints = inspect_deck(
                path,
                baseline_map[os.path.normcase(str(path))],
                baseline_root,
                args.require_notes,
            )
            entries.append(entry)
            frozen.update(fingerprints)
        payload = {
            "version": 2,
            "capture": {
                "powerpoint_process": process_state,
                "lock_files_detected": False,
                "approval_record_sha256": approval_fingerprint[2] if approval_fingerprint else None,
                "approval_record_accepted_by": approval_summary["accepted_by"] if approval_summary else None,
                "approval_record_accepted_at": approval_summary["accepted_at"] if approval_summary else None,
            },
            "decks": entries,
        }
        if approval_path is not None and approval_fingerprint is not None:
            frozen[str(approval_path)] = approval_fingerprint
        final_process_state = assert_commit_guard(
            decks, baseline_paths, frozen, process_state, args.allow_powerpoint_process
        )
        payload["capture"]["powerpoint_process"] = final_process_state
        temporary = prepare_atomic_text(output, json.dumps(payload, ensure_ascii=False, indent=2))
        try:
            # Recheck every input after the output bytes have been fsynced and
            # immediately before the no-clobber hard-link.  The link is the
            # commit point.  Never unlink the destination afterward: another
            # writer could replace that pathname between a failed post-check
            # and cleanup.
            assert_commit_guard(decks, baseline_paths, frozen, process_state, args.allow_powerpoint_process)
            link_atomic_no_clobber(temporary, output)
        finally:
            temporary.unlink(missing_ok=True)
    except (OSError, ValueError, FileExistsError) as exc:
        print(emit_json({"ok": False, "error": str(exc)}, args.redact_paths))
        return 2
    print(emit_json({"ok": True, "output": str(output), "deck_count": len(decks)}, args.redact_paths))
    return 0


if __name__ == "__main__":
    sys.exit(main())
