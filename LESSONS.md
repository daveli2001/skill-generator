# LESSONS.md - Learned Patterns and Rules

This file captures patterns and rules learned from corrections, debugging sessions, and user feedback.

---

## Lesson 1: Never Skip Steps
**Date:** 2026-03-02
**Trigger:** Assistant jumped to Step 2 (Plan) without waiting for user confirmation that Step 1 (Ask) was complete.

**Problem:** The assistant started drafting PRD.md content before the user confirmed all discovery questions were answered.

**Solution:**
- Always wait for explicit user confirmation before moving to the next step
- Step 1 (Ask) must be explicitly confirmed as complete by the user before proceeding to Step 2 (Plan)
- This rule is now encoded in CLAUDE.md under "CRITICAL WORKFLOW RULES"

**Rule Added to CLAUDE.md:**
> **DO NOT jump to Step 2 (Plan) before the user confirms Step 1 (Ask) is complete.**

---

## Lesson 2: Correct Working Directory
**Date:** 2026-03-02
**Trigger:** Assistant created files in `/home/dave/mopa/` instead of `/home/dave/skill-generator/`

**Problem:** Files were created in the wrong directory, requiring cleanup and recreation.

**Solution:**
- Always verify the current working directory before creating files
- skill-generator root is `/home/dave/skill-generator/`
- Generated skills are created in `~/.claude/skills/[skill-name]/`

**Rule Added to CLAUDE.md:**
> Verify working directory is `/home/dave/skill-generator/` before any file operations

---

## Lesson 3: Git Repository Linking Standard Operation
**Date:** 2026-03-02
**Trigger:** User requested to link local folder to GitHub repository using SSH.

**Problem:** The assistant needed a repeatable process for linking local skill-generator folders to GitHub repositories.

**Solution:**
- Created a standard operation procedure in CLAUDE.md for git repository linking
- Steps include: initialize git, configure identity, add remote, generate SSH key, test connection, push
- Always check if repository is already linked before attempting to link again (use `git remote -v`)

**Rule Added to CLAUDE.md:**
> **Git Repository Check (Always First):** Before any git operations, always check if the repository is already linked using `git remote -v`. If origin is already set, skip linking.

**Standard SSH Key Setup:**
```bash
ssh-keygen -t ed25519 -C "[email]" -f ~/.ssh/id_ed25519 -N ""
cat ~/.ssh/id_ed25519.pub  # User adds this to GitHub
ssh -T git@github.com -o StrictHostKeyChecking=no
```

---

## Lesson 4: Use Firecrawl Skill/CLI for Web Extraction (Not Python SDK)
**Date:** 2026-03-03
**Trigger:** User asked to test Firecrawl scraping on an Amazon URL. Assistant tried to install `firecrawl-py` Python SDK instead of using the firecrawl skill.

**Problem:** The assistant attempted to use `pip install firecrawl-py` and the Python SDK when the correct approach was to use the firecrawl skill (Claude Code skill) or firecrawl CLI.

**Solution:**
- Changed TECH_STACK.md to specify firecrawl CLI/skill as the MANDATORY method for web extraction
- Removed `firecrawl-py` from all requirements.txt templates
- Added CLI usage: `firecrawl scrape -f markdown <url>`
- Added `firecrawl-py Python SDK` to Prohibited Technologies
- Verified: Firecrawl CLI successfully scrapes URLs when FIRECRAWL_API_KEY is set

**Rule Added to TECH_STACK.md:**
> All skills created by skill-generator MUST use the firecrawl skill for web extraction. Other methods (requests, BeautifulSoup, firecrawl-py Python SDK, etc.) are NOT permitted for web scraping.

---

## Lessons Learned (Future entries will be added here)

### Template for New Lessons:
```
## Lesson X: [Title]
**Date:** YYYY-MM-DD
**Trigger:** [What caused the issue]

**Problem:** [Description of the problem]

**Solution:** [How it was resolved]

**Rule Added/Updated in CLAUDE.md:** [Reference to any rule changes]
```
