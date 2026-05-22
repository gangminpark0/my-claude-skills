# Cover Letter 작성 원칙

에디터에게 보내는 cover letter(편집자 응답서)에 관한 원칙. 이 문서는 `SKILL.md`가 cover letter 작업에 들어갔을 때 읽는다.

## 기본 방침: **짧게**, **이전 양식 그대로**, **리뷰어 외 개선사항 명시**

Cover letter는 리비전 패키지에서 **가장 짧은** 산출물이다. 에디터는 이걸 먼저 보고 "이 팀이 내 편지에 성실히 반응했는가"를 판단한다. 길이는 보통 A4 한 페이지 이내(4~6 단락).

교수님 실제 피드백: *"cover letter 간단하게 써줄래? 지금 코멘트가 너무 간단해서 쓸 얘기가 많이 없겠는데 그래도 이거 우리가 이 외에도 잘 봤다. 이렇게 해줘."* — 이 한 마디에 커버레터의 본질이 담겨 있다: 짧게, 그리고 self-initiated improvements를 반드시 언급.

## 표준 구조

```
[Sender 주소/소속 — 이전 라운드 그대로]
[Date]
[Editor 이름 + 저널명]

Dear Dr. <Editor name>,

[단락 1: 이번 리비전이 몇 번째인지 + 감사]
We are pleased to submit our <second> revised version of the manuscript entitled "<Title>" (Manuscript ID: <ID>) for your consideration. We are grateful to you and the reviewers for the constructive comments on our previous revision.

[단락 2: 리뷰어 코멘트에 대한 수정 요약 — 2~4문장으로 핵심만]
In this revision, we have addressed the remaining concerns raised by Reviewer <N>. Specifically, we have <핵심 변경 1>, and <핵심 변경 2>. Detailed point-by-point responses are provided in the accompanying "Response to Reviewer <N>" document.

[단락 3: 방법론·분석 보강 사항이 있다면 별도 단락으로]
<예: DDD 준실험 설계의 가설 형식에 대한 정당화, 새 robustness check 추가 등>

[단락 4: Self-initiated improvements — **반드시 포함**]
In addition to addressing the reviewers' comments, we conducted a thorough proofreading of the entire manuscript, corrected minor typographical and grammatical errors, and tidied the reference list. All revisions are marked in red in the revised manuscript.

[마무리]
We hope the revised manuscript now meets the standards of <Journal Name>. Thank you again for your time and consideration.

Sincerely,
<Signature + 소속>
```

## 이전 라운드 파일을 **반드시 템플릿으로**

R1 cover letter가 같은 폴더(또는 상위 폴더)에 있으면 **복사해서 본문만 교체**한다. 주소, Dear, Sincerely, 서명은 그대로. 폰트(Times New Roman 12pt), 줄 간격(1.5), 용지(A4), 여백 — 모두 승계. 이전 파일의 XML을 뜯어 스타일을 그대로 쓰는 것이 "양식 일치"의 가장 확실한 방법이다.

이전 파일이 R1 폴더에만 있고 R2 폴더에 없으면, `cp R1/Cover\ Letter.docx R2/Cover\ Letter.docx` 후 편집한다. 파일명은 **이전 라운드 컨벤션 그대로** — 띄어쓰기까지.

## 톤과 분량 가이드

- **수치나 통계값은 안 쓴다** — 그건 Response letter와 본문의 영역이다. Cover letter는 "방향"만.
- **코멘트 번호(R1Q1 등) 안 쓴다** — Response letter와의 역할 분리.
- **과도한 사과·겸손 피하기** — "We deeply apologize" 류 금지. 프로페셔널하게.
- **한 페이지 넘기지 말기** — 정말 길어야 할 이유가 있어도 A4 한 장 반 이내.

## 투고 시스템 박스에 붙여넣기용

일부 저널 시스템은 cover letter 파일 업로드 외에, 제출 포털의 별도 박스에 "Comments to Editor"를 입력하게 한다. 이런 경우 박스에는 cover letter 전체를 복붙하지 않고, 한두 문장 안내만 넣는다:

> Please find our cover letter and detailed responses attached as separate files ("Cover Letter.docx", "Response to Reviewer 1.docx"). All revisions are marked in red in the revised manuscript.

## 검증 체크리스트 (Cover letter 전용)

1. **한 페이지 이내**인가
2. **이전 라운드 양식** (폰트·줄간격·주소·서명) 동일
3. **몇 번째 리비전인지 명시** ("second revised version" 등)
4. **감사 인사** 포함
5. **Self-initiated improvements 단락** 포함
6. **"highlighted in red" 안내** 포함
7. **Response letter 첨부 안내** 포함
8. **저널명·Editor 이름·Manuscript ID 정확한지** 확인
9. **파일명** `Cover Letter.docx` 등 이전 라운드와 동일
10. **Cover letter의 수정 요약 ↔ Response letter의 실제 응답** 방향 일치 (정합성)

## 예시: R2 Cover letter (실제 작업 참고)

아래는 실제 R2 작성 사례의 골자(내용은 마스킹):

```
[Address]
[Date]
[Editor Name, Journal]

Dear Dr. <Editor>,

We are pleased to submit the second revised version of our manuscript entitled
"<Title>" (Manuscript ID: <ID>) for your consideration.

We thank you and the reviewer for the additional comments. In this revision we
have (i) removed the descriptive clause in the hypothesis statement as suggested,
and (ii) rephrased the hypotheses in the form appropriate to our quasi-experimental
(Difference-in-Differences) design. A detailed point-by-point response is provided
in the attached "Response to Reviewer 2" document.

In addition to the reviewer's comments, we have proofread the entire manuscript,
corrected minor typographical errors, and tidied the reference list. All revisions
in the manuscript are highlighted in red for easy identification.

We hope the revised manuscript now meets the standards of <Journal Name>.
Thank you again for your time and consideration.

Sincerely,
<Signature + Affiliation>
```

이 패턴을 템플릿으로 변형한다. 중요한 건 **리비전 횟수, 주요 수정 방향, self-initiated improvements, red highlighting 안내** 네 요소가 모두 있는 것.
