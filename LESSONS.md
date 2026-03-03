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

## Lessons Learned (Future entries will be added here)
