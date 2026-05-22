# Response Letter 작성 원칙

리뷰어 응답서(Response to Reviewers) 작성에 관한 상세 원칙. 이 문서는 `SKILL.md`가 리비전 작업 중 Response letter 파트에 들어갔을 때 읽는다.

## 파일 분리 원칙

리뷰어가 **여러 명**이면 **리뷰어별로 파일을 분리**한다. `Response to Reviewer 1.docx`, `Response to Reviewer 2.docx` 식으로. 저널이 단일 파일을 요구하면 합치지만, 기본은 분리이다 — 리뷰어가 서로 모순되는 요구를 할 때 추적이 쉽다.

투고 시스템이 본문 박스에 응답 내용을 입력하라고 하면, 박스에는 "Please find our detailed responses in the uploaded document 'Response to Reviewer N.docx.' Each reviewer comment has been addressed individually with corresponding responses and excerpts from the revised manuscript." 정도의 안내 문장만 넣고, 실제 응답은 파일로 업로드한다.

## 표준 구조

Response letter는 아래 구조를 **엄격히** 따른다. 이 구조가 실제 Gangmin 교수님 작업에서 수렴된 형태이다.

```
[Document title: "Response to Reviewer N"]
[도입부 1~2단락: 감사 인사 + 전반적 수정 방향 + self-initiated improvements 요약]

[Comment 1 박스 (리뷰어 원문 인용)]
  Comment R1Q1: "<리뷰어 코멘트 원문 그대로>"
Response:
  <빨간색, 들여쓰기된 응답 문단 1~여러 개>
  <manuscript excerpt가 필요하면 표 또는 인용 블록으로 삽입>

[Comment 2 박스]
Response:
  ...

[Comment 3 박스]
Response:
  ...
```

### 코멘트 박스

리뷰어 코멘트는 **인용 박스**에 원문 그대로 넣는다. 표(1행1열 테이블)로 구성하고, 배경색은 연한 회색 또는 무색, 테두리가 있는 스타일이 일반적이다. 코멘트 번호(예: "Comment R1Q1:")는 박스 안 첫 줄에 굵게 또는 별도 스타일로 표시한다. **임의로 요약하거나 문장을 다듬지 않는다** — 리뷰어는 자기 원문이 그대로 보이길 기대한다.

### "Response:" 헤딩

코멘트 박스 바로 아래에 "Response:" 를 독립된 한 줄로 놓는다. 이 한 줄은 **들여쓰기 없음, 본문 색상(검정)**. 여기까지는 이전 양식과 동일해야 한다.

### 응답 본문

Response 헤딩 아래의 실제 응답 문단들은:

- **색상: 빨간색 (RGB 255,0,0)** — 이것이 "수정한 내용"임을 시각적으로 알리는 장치.
- **들여쓰기: leftChars=200** (docx 기준, 약 2글자 들여쓰기). 이 수치는 실제 Gangmin 교수님 R1/R2 파일과 일치한다. 들여쓰기 없이 쓰면 텍스트가 코멘트 박스와 시각적으로 구분되지 않아 혼란스러워진다.
- **폰트/크기: 본문과 동일** (Times New Roman 12pt가 일반적).

응답 문단은 보통:
1. 첫 문장: 리뷰어에게 감사 + 수정 방향 한 줄 요약 ("We thank the reviewer for this insightful comment. We have revised the …")
2. 중간 문단들: 구체적으로 어떤 변경을 했는지, **왜** 그렇게 했는지
3. Manuscript excerpt (필요 시): 실제 본문에서 수정된 부분을 인용. 섹션명과 페이지/단락 위치 명시.

### Manuscript excerpt 테이블

응답 본문 안에서 "본문을 이렇게 고쳤습니다"를 보여줄 때는 **인용 블록** 또는 **2열 테이블**을 쓴다. 2열 테이블(Before / After)은 큰 개념 수정에서 유용하고, 단순 문구 수정은 인용 블록 한 개로 충분하다. excerpt는 **manuscript의 실제 문장과 토씨 하나 다르지 않아야 한다** — 이것이 정합성 검증의 핵심 축이다.

excerpt 위치 표시는 "Section 4.3 (p. 18):" 또는 "Introduction, second paragraph:" 식으로 리뷰어가 쉽게 찾을 수 있게. 섹션 번호가 리비전 과정에서 바뀌었으면 **새 번호 기준**으로 쓴다.

## 도입부(서문) 작성

문서 시작 부분의 1~2개 도입 문단은 아래 요소를 담는다:

- 에디터·리뷰어 감사
- 이번 리비전의 전반적 방향 한 줄 요약 ("We have substantially revised the manuscript to address the concerns raised regarding …")
- Self-initiated improvements 언급 (해당되는 경우): "In addition to addressing the reviewers' comments, we have also …"
- 빨간색 표시 규약 명시: "All revisions are highlighted in red in the revised manuscript."

도입부는 **검은색**이며 들여쓰기 없음.

## 피해야 할 것

### "Summary of Revisions" 별도 섹션을 넣지 말 것

이전 작업에서 검증 기준으로 "`Summary of Revisions`, `Overview of Changes` 등 금지 콘텐츠 없음 ✓" 이 확인되었다. 이유는 이 정보가 이미 Cover letter에 들어가고, Response letter 안에 또 넣으면 중복이기 때문이다. Response letter는 comment-by-comment 구조로 충분하다.

### 리뷰어 코멘트를 임의로 번호 매기지 말 것

리뷰어가 번호를 매기지 않은 하나의 긴 단락을 여러 개로 쪼개지 않는다. 반대로, 리뷰어가 1), 2), 3) 식으로 번호를 매겼으면 그 구조를 그대로 따른다. "Comment R1Q1-a, R1Q1-b"처럼 세분할 필요가 있으면 해도 되지만, 리뷰어 원문 구조를 깨지는 않는다.

### 과도한 사과 피하기

"We sincerely apologize for this oversight"를 남발하지 않는다. 프로페셔널한 톤으로 "We thank the reviewer" + "We have revised" 로 충분하다. 리뷰어가 지적한 결점이 명백한 경우에도 "We agree and have now clarified this point" 정도가 적절하다.

## 검증 체크리스트 (Response letter 전용)

Response letter 수정이 끝났을 때 최소 이 항목들을 확인한다:

1. **코멘트 박스가 리뷰어 원문 그대로인가** — 구두점, 인용부호, 줄바꿈까지.
2. **모든 Response 문단이 빨간색 + 들여쓰기인가**
3. **"Response:" 헤딩은 검은색 + 들여쓰기 없음**인가
4. **manuscript excerpt가 실제 본문과 문자 단위 일치**하는가 (grep으로 본문 파일에서 해당 문장을 다시 찾아 매칭 확인)
5. **섹션 번호·페이지 참조가 revised manuscript 기준**인가 (original 기준이 아님)
6. **서문에 "highlighted in red" 안내가 있는가**
7. **"Summary of Revisions" 같은 금지 콘텐츠 없음**
8. **리뷰어 코멘트 수 ↔ 박스 수 일치**
9. **파일명이 이전 라운드 컨벤션과 일치**하는가 — `Response to Reviewer 1.docx` vs `Response_Reviewer1.docx` 처럼 띄어쓰기까지.
10. **폰트/크기/줄간격이 이전 라운드와 동일**한가

## Docx 구현 팁

Python으로 docx를 조작할 때(`python-docx`):

- 빨간색 하이라이팅: `run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)`
- 들여쓰기: paragraph format의 `left_indent` 대신 `paragraph_format.first_line_indent`가 아니라, 한국 문서에서 흔히 쓰는 "leftChars=200"은 pPr의 `ind` 요소의 `w:leftChars` attribute에 대응. 기존 이전 라운드 파일의 XML을 직접 들여다보고 동일한 attribute 세트를 복사하는 것이 가장 안전하다.
- 이전 라운드 파일을 템플릿으로 **복사 후 본문만 교체**하는 전략이 "스타일 호환성" 측면에서 압도적으로 안전하다. 처음부터 만들지 말 것.
- docx 최종 저장 후 `unzip`하고 `document.xml`을 직접 grep해서 색상 태그·들여쓰기 태그가 모든 응답 문단에 들어갔는지 확인할 수 있다. 이게 가장 확실한 검증이다.
