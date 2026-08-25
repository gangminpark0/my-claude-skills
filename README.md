# my-claude-skills

Personal Claude Code skills, version-controlled for sync across machines.

## Skills

- **academic-paper-writing** — Author conventions for writing, revising, and verifying empirical research papers across fields (economics, management, finance, sociology, public policy, IS, OB, marketing, accounting). Covers workflow philosophy, paper architecture (title → abstract → intro → theory → method → results → robustness → further analyses → discussion), cross-section consistency, prose craft (typography, em-dash rules, sentence length), empirical conventions (lock files, imputation, identification), figures and tables, submission package (cover letter, title page, data availability), workflow tools (memo extraction, formatting preservation), and audit-script catalog.
- **korean-policy-report** — Conventions for Korean policy / research reports (정책·연구 보고서) submitted to dispatchers like KERI, KIET, KDI, KIEP, etc.
- **korean-administrative-documents** — Creates, revises, and verifies Korean official letters, commencement/completion forms, submission lists, attachment forms, query tables, and supporting spreadsheets with public-sector document structure, neutral gray/black styling, fixed table geometry, page numbers, source preservation, and five consecutive frozen-output audits.
- **paper-revision** — R&R (revise & resubmit) response-letter writing for journal submissions. Covers reviewer-comment structuring, response-letter format (citation box + Response heading + red excerpts), manuscript revision with red highlighting, cover-letter conventions for revisions, and multi-pass verification.
- **korean-lecture-pptx** — Plans, revises, and verifies Korean lecture PPTX decks and speaker notes. Covers course-story architecture, natural spoken Korean, first-use explanations for jargon, evidence and rights discipline, preservation of instructor edits, embedded-note synchronization, PowerPoint rendering, learner review, and frozen-output validation.

## Install on a new machine

```bash
# Windows (Git Bash / PowerShell)
git clone https://github.com/gangminpark0/my-claude-skills.git "$HOME/.claude/skills"

# macOS / Linux
git clone https://github.com/gangminpark0/my-claude-skills.git ~/.claude/skills
```

If `~/.claude/skills/` already exists with other content, clone elsewhere and copy folders in selectively instead of clobbering.

Restart Claude Code after cloning; the new session will auto-detect the skills.

For Codex, clone this repository to a separate location, then copy only the skill folder into `~/.codex/skills/`:

```powershell
# Windows PowerShell
git clone https://github.com/gangminpark0/my-claude-skills.git "$env:TEMP\my-claude-skills"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse "$env:TEMP\my-claude-skills\korean-lecture-pptx" "$env:USERPROFILE\.codex\skills\korean-lecture-pptx"
```

```bash
# macOS / Linux
git clone https://github.com/gangminpark0/my-claude-skills.git /tmp/my-claude-skills
mkdir -p ~/.codex/skills
cp -R /tmp/my-claude-skills/korean-lecture-pptx ~/.codex/skills/korean-lecture-pptx
```

Start a new Codex session after copying it.

## Update workflow

```bash
cd ~/.claude/skills
# edit a SKILL.md, then:
git add -A
git commit -m "Update korean-policy-report: <what changed>"
git push
```

On other machines:

```bash
cd ~/.claude/skills && git pull
```
