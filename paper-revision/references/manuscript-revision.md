# Manuscript Revision (본문 리비전 반영) 원칙

본문 수정에 관한 상세 원칙. 이 문서는 `SKILL.md`가 본문(`.docx`) 수정 작업에 들어갔을 때 읽는다.

## 기본 원칙: 변경사항은 **빨간색**으로

리뷰어·에디터가 diff를 눈으로 따라가야 한다. 따라서 **새로 쓴 텍스트, 바뀐 단어, 추가된 문단은 전부 빨간색(RGB 255,0,0)**. 삭제는 보통 strikethrough 없이 깔끔히 제거(새 텍스트만 빨간색으로 보이게). 일부 저널은 "Tracked Changes"를 요구하는데, 그런 경우 Word의 리뷰 모드를 쓰고 빨간색 수동 표시를 중복 사용하지 않는다 — 혼선의 원인이 된다. 어떤 방식을 쓸지는 **이전 라운드와 동일하게** 한다.

Cover letter와 Response letter 모두에 "All changes are highlighted in red" 안내를 넣어 이 규약을 명시한다.

## 수정 전 반드시 확인할 사항

### 파일 상태 점검

교수님이 이미 손을 댄 수정본인지, 원본 그대로인지 먼저 확인한다. 파일 생성/수정 날짜를 `stat` 또는 Bash로 확인하고, 같은 폴더에 `Manuscript.docx`와 `Manuscript_revised.docx`가 공존하면 둘의 차이를 파악한다. **교수님이 직접 수정한 부분을 덮어쓰지 않도록** 주의.

### Appendix/별도 asset 누락 점검

실제 사례: Appendix 5 초안이 `.md` 파일로 작업 폴더에 존재했지만 manuscript에 삽입되지 않은 상태에서 "왜 Appendix 5가 없지?" 문의가 들어왔다. 리비전 시작 전에 폴더를 `ls`로 훑어 `appendix`, `table`, `figure` 관련 asset이 manuscript에 전부 반영되어 있는지 확인한다. 여러 버전이 있으면 **Response letter에 언급된 내용**과 매칭해서 올바른 버전을 고른다.

### 이전 라운드의 빨간색이 검정으로 바뀌었는지 확인

R2 시작 시점에서 R1의 빨간색은 검정으로 돌려놓는 것이 일반적이다 (R1 수정사항은 이미 accept된 상태이므로). 이 작업이 안 돼 있으면 R2 수정사항과 시각적으로 구분이 안 된다. 폴더에 `Revised Manuscript.docx` (빨간색 표시 있음)과 `Revised Manuscript_clean.docx` (검정 버전)가 별도로 있어야 하는 저널도 있다.

## 수정 작업 순서

1. **리뷰어 코멘트별로 요구 변경사항을 목록화** — "R1Q1 → §3.2 두 번째 문단 수정, R1Q2 → §4.5 전체 재작성"
2. **큰 구조 변경 먼저, 세부 문구 수정 나중** — 섹션 이동·재작성을 먼저 하고, 오타·citation 수정은 마지막에. 순서를 반대로 하면 세부 수정이 재작성으로 무효화된다.
3. **각 수정 직후 빨간색 표시** — 나중에 일괄 표시하려고 하면 누락이 발생한다.
4. **검증 라운드** — 아래 검증 축 참고.

## 반복적으로 나타나는 오류 패턴 (체크리스트)

실제 검증에서 걸린 것들:

### 오타·문법
- `treatement` → `treatment`
- `enterprises.The` → `enterprises. The` (마침표 뒤 공백)
- `over time.While` → `over time. While`
- `risks creates` → `risks creating` (주어-동사 수 일치)
- `exclude sure market participants` → `exclude certain market participants` (단어 치환 오류)

### Citation 포맷
- `Shipilov, & Gawer, 2020` → `Shipilov & Gawer, 2020` (comma 중복)
- `(Burt, 1992; 2005; Uzzi, 1997)` → `(Burt 1992, 2005; Uzzi 1997)` (저널 스타일에 따라)
- 본문 citation과 reference list 스타일 불일치 (APA 7th가 가장 흔함)
- `&` vs `and` 혼재 — 본문에서 "X and Y (2020)"인지 "X & Y (2020)"인지 저널마다 다름. 통일 확인.

### 참고문헌 무결성 (가장 중요)
- **Orphan references**: reference list에는 있지만 본문에서 인용하지 않는 항목 — 삭제.
- **Missing references**: 본문에서 인용하지만 list에 없는 항목 — 교수님 확인 후 APA 형식으로 추가 제안. 임의 추가 금지.
- **연도 불일치**: 본문은 `(2020)`인데 list는 `(n.d.)`인 경우, 둘 다 가능한 진실이므로 **교수님 결정 필요**.
- **인명 오기**: 본문은 `Walters (2006)`인데 list는 `Walter et al. (2006)` — 어느 쪽이 맞는지 확인.

확인 방법: Python으로 docx의 모든 `(저자, 연도)` 패턴을 정규식으로 추출 → reference list에서 매칭. Bash one-liner로 간단히 짤 수 있다.

### 섹션 번호
- `§4.3` 다음 `§4.5`로 건너뜀 (`§4.4` 없음). 본문 확인 후 누락된 번호를 채우거나, 번호를 당긴다. 어느 쪽인지 **교수님 확인**.
- Appendix 번호 점프도 동일하게 체크.

### Figure / Table 캡션
- 동일 캡션이 두 번 나타남 (Figure 5 중복 사례 있음). 원인은 두 이미지 파일에 같은 캡션 복사된 경우가 많음.
- 캡션 번호와 본문 참조 번호 일치 확인.
- Table note 스타일 통일 (이탤릭 vs 일반, "Note:" vs "Notes:").

### Abbreviation / Funding
- 첫 사용 시 풀네임 → 이후 약어. Funding 문장에서 `(MSIT)`를 `(Ministry of Science and ICT)`로 쓰는 것이 표준. 공식 영문명을 확인한다 (e.g., MSIT는 Ministry of Science and ICT, SPRi는 Software Policy & Research Institute).
- 연구비 지원 문구에 grant number·지원 기관 공식명·연도 포함.

## Abstract 수정 시 고려

Abstract는 별도 신경을 쓴다:

- **첫 문장**: 추상적 문장보다 구체적 본론 문장이 독자를 잡는다. "This study investigates the unintended gap…" 보다 "This study investigates how entry restrictions on large firms, while successfully redistributing market access, simultaneously disrupted…" 식이 강하다.
- **시제 통일**: 보통 과거형 권장. "We isolated" "The findings reveal" 같이 혼재되면 어색하다. 과거형으로 통일하되 "The findings reveal" 같은 관용 표현은 현재형 허용.
- **단복수 통일**: `coordination vacuums` vs `coordination vacuum` 같은 불일치 검사.
- **Key term의 대문자 고유명사 처리**: `"Brokers"`, `"Integrators"` 같이 연구 내 정의된 역할명은 인용부호 또는 이탤릭으로 일관되게.
- 분량: 저널 abstract 단어 수 제한(보통 200~300 단어) 확인.

## 다중 검증 라운드 — 실제 구현

교수님이 "10회 검증"을 요청하면, 이를 10번 같은 것을 반복이 아닌 **10개 서로 다른 관점의 스캔**으로 해석한다. 예시:

1. 빨간색 적용 범위 스캔 (수정 문단 전부 빨간색인가)
2. 들여쓰기·폰트·줄간격 스캔
3. Orphan reference 스캔 (Python으로 본문 ↔ list 매칭)
4. Missing reference 스캔
5. Citation 포맷 일관성 스캔 (`&` vs `and`, 괄호 위치, 연도 쉼표)
6. 섹션 번호 연속성 스캔
7. Figure/Table 번호 연속성 + 캡션 중복 스캔
8. 오타·공백 누락 grep
9. Response letter excerpt ↔ manuscript 원문 일치 스캔
10. Cover letter 요약 ↔ 실제 수정사항 일치 스캔

각 스캔은 가능한 한 **스크립트**로 자동화한다 — 사람 눈으로 훑는 것보다 빠르고 놓치는 게 적다. 결과는 `{ "수정 완료": [...], "교수님 확인 필요": [...] }` 구조로 분리 보고한다.

## 교수님 결정이 필요한 사항은 **수정하지 않고 보고**

다음은 함부로 수정하지 않는다:

- 참고문헌 누락 5건 같은 reference 추가 (APA 형식 제안만)
- 본문 인용 연도 vs list 연도 불일치 (둘 다 가능)
- 섹션 번호 4.4 누락 (채우기 vs 당기기 중 선택)
- "as of 2020" vs "after 2008" 같은 시점 불일치
- Walters vs Walter et al. 같은 인명 오기
- Abstract 구조 대폭 개편

보고 형식:
```
**수정 완료 사항** (n건)
1. ...

**교수님 확인/결정 필요 사항** (m건)
1. 누락 참고문헌 n개 — APA 형식 제안 첨부
2. 섹션 4.4 누락 — 새 섹션 추가 vs 번호 당기기 중 택일 필요
...
```

## 파일 출력과 저장

- 항상 **이전 라운드 파일을 복사해서 편집**. Zero부터 만들면 스타일 호환성 문제.
- 최종 파일명은 이전 라운드 컨벤션 따라. 띄어쓰기까지 동일하게 (`Revised Manuscript.docx` vs `Manuscript_revised.docx`).
- 동일 폴더에 `Revised Manuscript.docx` (track changes 포함)와 `Revised Manuscript_clean.docx` (accept all changes 버전)를 함께 제공하는 경우가 많다. 저널 요구사항 확인.
- 완료 시 `computer://` 링크로 **사용자 폴더 경로** 제공. 내부 `/sessions/...` 경로 노출 금지.

## Docx 조작 스크립트 팁

- `python-docx`로 run 단위 색상 변경: `run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)`
- 한 paragraph 안 일부만 빨간색으로 하려면 run을 쪼개야 함.
- docx는 내부적으로 zip — `unzip` 후 `document.xml`을 직접 grep/sed 하는 것이 runs가 많은 복잡 문서에서는 더 안정적.
- 수정 후 `zip -r output.docx .` 로 repack. zip 옵션 `-X`를 쓰면 Finder 메타데이터 제외. `[Content_Types].xml`이 반드시 포함되어야 Word가 연다.
- 검증: 최종 docx를 unzip하고 `document.xml`에서 색상 태그(`<w:color w:val="FF0000"/>`) 개수, 들여쓰기 태그 개수를 세어 예상치와 비교.
