# Installing this skill on another computer

This skill is **user-level**, not project-local. It lives at `~/.claude/skills/academic-paper-writing/` and is automatically discovered by Claude Code on any machine where it's placed there.

## Quick install — copy method

1. Copy the entire `academic-paper-writing/` directory (containing `SKILL.md` and this `INSTALL.md`) to the new computer.
2. Place it at:
   - **Windows**: `C:\Users\<username>\.claude\skills\academic-paper-writing\`
   - **macOS / Linux**: `~/.claude/skills/academic-paper-writing/`
3. Done. The skill is auto-discovered on the next Claude Code session.

## Cloud-synced install

To keep the skill in sync across computers automatically:

### Option A: Git repository
1. Put the skill directory in a private Git repo (e.g., GitHub, GitLab).
2. On each computer, clone the repo to a known location (e.g., `~/dotfiles/claude-skills/`).
3. Symlink:
   - **macOS / Linux**: `ln -s ~/dotfiles/claude-skills/academic-paper-writing ~/.claude/skills/academic-paper-writing`
   - **Windows (PowerShell admin)**: `New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\academic-paper-writing" -Target "$env:USERPROFILE\dotfiles\claude-skills\academic-paper-writing"`
4. Pull the repo to update on any machine.

### Option B: Cloud-synced folder (Dropbox / OneDrive / iCloud)
1. Place the skill directory in a cloud-synced folder.
2. Symlink to `~/.claude/skills/` as above.
3. Edits on one computer sync to all others.

## Verification

After install, check that the skill is recognized:

```bash
ls ~/.claude/skills/academic-paper-writing/SKILL.md
```

(Windows PowerShell: `Get-Item $env:USERPROFILE\.claude\skills\academic-paper-writing\SKILL.md`)

If the file exists at this path, Claude Code will discover the skill automatically on the next session.

## When the skill activates

This skill auto-activates when the user asks for help with:
- Drafting or revising an empirical research paper.
- Resolving Word comments / memos on a manuscript.
- Running paper-revision audits.
- Editor-perspective review or cover-letter writing.

It does NOT activate for non-paper code tasks. The skill description in `SKILL.md` controls activation.

## What's in this skill

`SKILL.md` covers 12 parts:

1. Workflow philosophy (plan → execute → verify; multi-round verification; audit-driven revision; integrity over speed; question vs revision; autonomous execution; pause patterns; compact-summarize).
2. Paper architecture (title, abstract, intro, hypothesis development + statement, methods, results deductive, robustness prediction-test, further analyses, discussion).
3. Cross-section consistency (Method↔Results, cover letter↔paper, numerical 4-way, contradiction detection, leftover detection, "important repeats", concept-discovery audit).
4. Prose craft (concise sentences, paragraph bumpers, AI-fingerprint cleanup, no math notation, forward-reference discipline, variable italicization, no author-name branding).
5. Empirical conventions (lock-file methodology, sample-shrinkage → imputation, sample-restriction matches outcome, time-window consistency, domain consistency, significance honesty, coefficient-sign sanity check, Within R², "best split", reuse existing analyses, control-variable citations).
6. Robustness and honest framing (cherry-pick management, marginal significance, tone-down, negative result honesty).
7. Figures and tables (necessity check, design rules, format conventions, bundle skepticism, reference-paper matching).
8. Submission package (cover letter, title page, data availability, self-citation, acceptance probability, journal-fit trade-offs).
9. Workflow tools (Word-comments extraction, script-regen workflow, md vs docx ground truth, save key state, version naming).
10. Audit script catalog.
11. Pre-submission checklist.
12. User feedback pattern reference table.

## Updating the skill

When new patterns emerge in your workflow that should be captured in this skill, edit `SKILL.md` directly. The Claude Code session will pick up changes on next activation. If sharing across machines, commit the change to your Git repo or let the cloud sync handle it.
