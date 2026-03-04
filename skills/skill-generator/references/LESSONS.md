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

## Lesson 13: Create Demo Chart Generation Script
**Date:** 2026-03-03
**Trigger:** User requested a demo Word document showcasing all 17 chart types defined in FRONTEND_GUIDELINES.md.

**Problem:** Needed to demonstrate the custom design system (Times New Roman, Black/Orange colors, sharp corners) applied to all chart types.

**Solution:**
Created `scripts/create_demo_charts.py` that generates:
- 17 chart types as PNG images using matplotlib
- A Word document (demo_charts_collection.docx) embedding all charts
- All charts use the design system colors and typography

**Charts Generated:**
1. Combination Bar and Line Chart
2. 100% Stacked Bar Chart
3. Line Chart
4. Pie Chart
5. Radar Chart
6. Mekko Chart
7. Area Chart
8. Scatter Plot
9. Heatmap
10. Histogram
11. Box Plot
12. Violin Plot
13. Funnel Chart
14. Gauge Chart
15. Treemap
16. Sunburst Chart
17. Waterfall Chart

**Required Dependencies:**
```bash
pip install python-docx matplotlib numpy squarify
```

**Usage:**
```bash
python3 scripts/create_demo_charts.py
```

---

## Lesson 14: Never Skip Sub-Step Approval in Step 4 (Pre-launch Check)
**Date:** 2026-03-04
**Trigger:** Assistant completed Step 4.1, 4.2, and 4.3 in a single message without asking for user approval after each sub-step.

**Problem:** The assistant displayed all three Step 4 sub-steps (Documentation Review, Code Review, Final Testing) together and only asked for approval at the end. This violates Rule 11 in CLAUDE.md which explicitly requires checklist + permission request after EVERY sub-step (4.1 → 4.2 → 4.3).

**Solution:**
- Stopped and acknowledged the violation immediately
- Updated CLAUDE.md Rule 11 to explicitly state: "**NEVER batch multiple sub-steps together - each sub-step (e.g., 4.1, 4.2, 4.3) requires its own checklist + approval before proceeding to the next**"
- Added "VIOLATION CONSEQUENCE" section specifying what to do if approval is skipped
- Updated both CLAUDE.md (root) and references/CLAUDE.md (in skill folder)

**Rule Added to CLAUDE.md:**
> **VIOLATION CONSEQUENCE:** If you skip approval for any sub-step, you MUST:
> 1. Acknowledge the violation immediately
> 2. Stop and display the missed checklist
> 3. Wait for explicit user approval before continuing
> 4. Document the incident in LESSONS.md

---

## Lesson 15: Must "Dogfood" skill-generator Before Launch (CRITICAL)
**Date:** 2026-03-04
**Trigger:** User discovered that skill-generator was NOT actually tested by using it to create a skill. The assistant only tested helper scripts (main.py init command), not the full skill workflow.

**Problem:**
- Step 4.3 (Final Testing) only tested `scripts/main.py` commands
- The skill-generator skill itself was NEVER used to create a skill
- All files were created directly via Bash/Write tools, not through the skill's conversational flow
- This violates the intent of Step 4.3: "skill-generator MUST load the created skill and run a real use case"

**Solution:**
- Added Rule 9 to SKILL.md: "Before launch, skill-generator MUST be tested by creating at least one complete skill using its own conversational flow"
- Step 4.3 checklist now requires: "Skill tested by creating a real skill using its own triggers and workflow"
- Test output must be preserved for user verification (not in /tmp/ which gets cleaned)

**Rule Added to SKILL.md:**
> **Rule 9: Dogfooding Requirement (Pre-launch)** - Before Step 5 (Launch), skill-generator MUST be tested by creating at least one complete skill using its own conversational flow. The test skill output must be preserved for user verification.

---

## Lesson 16: Never Install firecrawl-py - Use Firecrawl Skill/CLI Only
**Date:** 2026-03-04
**Trigger:** User instruction to ensure skill-generator and all generated skills use firecrawl skill/CLI, not Python SDK.

**Problem:**
- There's a risk that generated skills might try to install `firecrawl-py` Python SDK
- Using Python SDK defeats the purpose - firecrawl is meant to be used as a Claude Code skill or CLI tool
- Python web scraping libraries (`requests`, `BeautifulSoup`, etc.) are unreliable and break easily

**Solution:**
- Updated TECH_STACK.md: `firecrawl-py` is PROHIBITED, only firecrawl skill/CLI allowed
- Updated SKILL.md Rule 4: Explicitly prohibits firecrawl-py, selenium, playwright, scrapy
- Updated CLAUDE.md Rule 4: Added prohibited technologies table
- When a skill needs web extraction, it must load the firecrawl skill via `/skill firecrawl`

**Rule Added to TECH_STACK.md:**
> **Web Extraction (CRITICAL - MUST USE FIRECRAWL SKILL/CLI):** NEVER install `firecrawl-py` Python SDK. Use firecrawl skill or CLI: `firecrawl scrape -f markdown <url>`

---

## Lesson 17: Core Context Files Must Be Created at Start of Step 0
**Date:** 2026-03-04
**Trigger:** User instruction to ensure CLAUDE.md, LESSONS.md, and progress.txt are created at the very beginning of Step 0.

**Problem:**
- Without CLAUDE.md, there are no rules to guide the process
- Without LESSONS.md, past mistakes won't be captured
- Without progress.txt, there's no way to track current status
- These files must exist BEFORE any verification or skill creation begins

**Solution:**
- Added Step 0.0: Create Core Context Files (MUST BE FIRST)
- Step 0.0 must be completed before Step 0.1 (Verify Core Platform)
- All three files (CLAUDE.md, LESSONS.md, progress.txt) must be verified before proceeding
- Updated IMPLEMENTATION_PLAN.md, SKILL.md, and CLAUDE.md

**Rule Added to IMPLEMENTATION_PLAN.md:**
> **Step 0.0: Create Core Context Files (MUST BE FIRST)** - Create CLAUDE.md with base rules, progress.txt initialized to Step 0, and LESSONS.md with template. Verify all three files exist before proceeding to Step 0.1.

---

## Lesson 18: Remove skill-generator Root .env for Security
**Date:** 2026-03-04
**Trigger:** User security concern about storing API keys at skill-generator level.

**Problem:**
- skill-generator creates skills but doesn't use APIs itself
- Storing FIRECRAWL_API_KEY in skill-generator's `.env` is unnecessary
- Security risk: one compromised location affects all generated skills
- Each skill should have its OWN isolated `.env` file

**Solution:**
- Deleted `/home/dave/skill-generator/.env`
- Updated Step 0.3: "Verify Skill-Generator Configuration" (no API key checks)
- Each generated skill creates its own `.env` with its own API keys
- Updated CLAUDE.md: "FIRECRAWL_API_KEY should be in each generated skill's `.env` file, NOT in skill-generator"

**Security Principle:**
> skill-generator is a meta-tool - it creates skills but doesn't execute them. API keys belong in each generated skill's isolated `.env` file, not at the framework level.

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
