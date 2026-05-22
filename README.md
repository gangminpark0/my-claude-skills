# my-claude-skills

Personal Claude Code skills, version-controlled for sync across machines.

## Skills

- **academic-paper-writing** — Author conventions for empirical research papers across fields.
- **korean-policy-report** — Conventions for Korean policy/research reports (정책·연구 보고서) submitted to dispatchers like KERI, KIET, KDI, KIEP, etc.
- **paper-revision** — Reviewer response, revised manuscript, and cover letter conventions for journal R&R submissions.

## Install on a new machine

```bash
# Windows (Git Bash / PowerShell)
git clone https://github.com/gangminpark0/my-claude-skills.git "$HOME/.claude/skills"

# macOS / Linux
git clone https://github.com/gangminpark0/my-claude-skills.git ~/.claude/skills
```

If `~/.claude/skills/` already exists with other content, clone elsewhere and copy folders in selectively instead of clobbering.

Restart Claude Code after cloning; the new session will auto-detect the skills.

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
