# 설치 방법

이 스킬은 Claude Code의 user-level skill로 동작함. 한 번 설치하면 해당 계정의 모든 프로젝트에서 자동으로 사용 가능.

## 새 컴퓨터에 설치

1. 이 폴더(`korean-policy-report/`) 전체를 복사
2. 대상 컴퓨터의 다음 경로에 붙여넣기:
   - **Windows**: `C:\Users\<사용자명>\.claude\skills\korean-policy-report\`
   - **macOS / Linux**: `~/.claude/skills/korean-policy-report/`
3. Claude Code를 새 세션으로 실행하면 자동 인식됨
4. 확인: 새 세션에서 "한국어 정책 보고서 쓸 건데" 같은 문구를 던지면 스킬이 트리거됨. 또는 직접 `/korean-policy-report` 호출.

## 폴더 구조

```
korean-policy-report/
├── SKILL.md      # 본체 (frontmatter + 규칙)
└── INSTALL.md    # 이 파일
```

`SKILL.md`만 있어도 동작함. `INSTALL.md`는 참고용.

## 업데이트

규칙을 수정하고 싶으면 `SKILL.md`만 편집하면 됨. frontmatter의 `description` 필드는 Claude가 언제 이 스킬을 발동할지 판단할 때 쓰이므로, 트리거 조건을 바꾸려면 description을 수정.

## 동기화 팁

- Dropbox/iCloud로 `~/.claude/skills/` 전체를 동기화하면 여러 컴퓨터 간 자동 반영
- 또는 git repo로 관리: `~/.claude/skills/` 안에서 `git init` 후 폴더별 커밋
