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

## Lesson 5: Documentation Updates When Problems Are Solved
**Date:** 2026-03-03
**Trigger:** User instruction to formalize documentation update requirements.

**Problem:** The initial rule incorrectly required documentation updates before EVERY git commit, even when no problems were solved.

**Solution:**
- Updated Rule 5 in CLAUDE.md to clarify when documentation updates are required
- Established two flows:
  1. Problem solved → Update LESSONS.md → progress.txt → CLAUDE.md (if needed) → Git Commit
  2. No problem solved → Git Commit directly
- LESSONS.md must be updated only when a problem is solved
- progress.txt should be updated after each step/sub-task
- CLAUDE.md must be updated when new rules are needed based on experience

**Rule Added to CLAUDE.md:**
> **Rule 5: Documentation Updates (When Problems Are Solved)** - When you solve a problem, update LESSONS.md, progress.txt, and CLAUDE.md (if needed) BEFORE git commit. If no problem was solved, git commit directly.

---

## Lesson 6: Remove Unnecessary Web Extraction Template Code
**Date:** 2026-03-03
**Trigger:** User questioned the necessity of SKILL.md Integration and Example Skill Script sections in TECH_STACK.md.

**Problem:** TECH_STACK.md contained template code (YAML frontmatter and Python subprocess wrapper) for web extraction, when skills should simply load and use the firecrawl skill directly via Claude Code's Skill tool.

**Solution:**
- Removed "SKILL.md Integration" YAML template section
- Removed "Example Skill Script" Python subprocess wrapper code
- Added "Usage in Skills" note: "When a skill needs to scrape web content, it should load and use the firecrawl skill directly via Claude Code's Skill tool. No wrapper scripts or subprocess calls are needed."

**Rule Clarification:**
> Skills should load and use the firecrawl skill directly - no wrapper scripts or subprocess calls needed.

---

## Lesson 7: Add Web Scraping Flow Diagram to TECH_STACK.md
**Date:** 2026-03-03
**Trigger:** User asked to summarize the flow of what a skill should do when it needs to scrape a web page.

**Problem:** TECH_STACK.md had the rule "use firecrawl skill" but lacked a clear visual flow showing the step-by-step process and explicit DO/DON'T guidance.

**Solution:**
- Added "Web Scraping Flow" diagram showing 5 steps from URL to result
- Added "What TO Do" list (load firecrawl skill, pass URL, use returned content)
- Added "What NOT to Do" list (no firecrawl-py, no requests/BeautifulSoup, no custom scrapers, no subprocess wrappers)

**Rule Added to TECH_STACK.md:**
> **Web Scraping Flow:** 1) Skill needs to scrape URL → 2) Load firecrawl skill → 3) Pass URL → 4) Firecrawl returns content → 5) Skill processes and returns results.

---

## Lesson 8: Never Delete Existing Lessons Without Permission
**Date:** 2026-03-03
**Trigger:** User noticed that Lessons 1-6 were accidentally deleted when adding Lesson 7.

**Problem:** When adding a new lesson to LESSONS.md, the assistant accidentally replaced all existing lessons (1-6) instead of appending the new lesson.

**Solution:**
- Restored all 6 deleted lessons
- Added Rule 6 to CLAUDE.md: "Never Delete Existing Content Without Permission"
- Updated Rule 5 to explicitly state: "NEVER delete or overwrite existing lessons - always append new lessons after existing ones"

**Rule Added to CLAUDE.md:**
> **Rule 6: Never Delete Existing Content Without Permission** - When updating LESSONS.md, never delete or replace existing lessons. Always append new lessons after existing ones. If content is accidentally deleted, acknowledge immediately, restore it, and document the incident.

---

## Lesson 9: Update TECH_STACK.md Chart Types and References Folder
**Date:** 2026-03-03
**Trigger:** User reviewed TECH_STACK.md and identified two limitations that needed correction.

**Problem:**
1. The "Supported Chart Types" list was presented as a limited/exhaustive list when it should be open-ended
2. The `references/` folder description only mentioned `.md` files when it should support all file types (pdf, pptx, docx, xlsx, etc.)

**Solution:**
1. **Chart Types:**
   - Changed the list header to "(non-exhaustive list)"
   - Added more chart types to the list
   - Added note clarifying that skills can create any chart type supported by matplotlib/plotly

2. **References Folder:**
   - Updated folder description from "Documentation loaded as needed" to "Reference files of any type"
   - Added examples of supported file types: .md, .pdf, .docx, .pptx, .xlsx, .csv
   - Added note clarifying that references/ can contain any file type the skill needs

**Rule Added to TECH_STACK.md:**
> **Note:** The `references/` folder can contain any file type that the skill needs to load and use, including but not limited to: PDF, DOCX, PPTX, XLSX, CSV, TXT, JSON, XML, images, and more.

---

## Lesson 10: VIOLATION - Deleted Lessons 1-8 Despite Explicit Rule
**Date:** 2026-03-03
**Trigger:** User discovered that Lessons 1-8 were deleted from LESSONS.md when Lesson 9 was added.

**Problem:** The assistant violated Rule 5 in CLAUDE.md which explicitly states "**NEVER delete or overwrite existing lessons** - always append new lessons after existing ones". When adding Lesson 9, the assistant used Write() which replaced the entire file content instead of using Edit() to append.

**Solution:**
- Immediately restored all 8 deleted lessons
- This incident is documented here as a reminder
- Future lesson additions MUST use Edit() to append after the "Lessons Learned" section, NOT Write() to replace the file

**Rule Reinforcement:**
> **CRITICAL:** When adding new lessons to LESSONS.md:
> 1. ALWAYS use Edit() tool to append after existing content
> 2. NEVER use Write() tool which replaces the entire file
> 3. Verify all previous lessons are intact before committing

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