# CLAUDE.md - skill-generator Operating Manual

This file contains rules and context that must be followed in every session.

---

## CRITICAL WORKFLOW RULES

### Rule 1: Never Skip Steps
**DO NOT jump to Step 2 (Plan) before the user confirms Step 1 (Ask) is complete.**

The workflow MUST be followed in exact order:
1. **Step 1: Ask** → Ask all clarifying questions → **WAIT for user confirmation**
2. **Step 2: Plan** → Create files one by one → **WAIT for user approval before each file**
3. **Step 3: Build** → Code step by step → **WAIT for user approval before each step**
4. **Step 4: Pre-launch Check** → Run thorough checks → **WAIT for user confirmation**
5. **Step 5: Debug** → Only activated when errors occur

### Rule 2: Always Ask for Clarification
- Never make assumptions about user requirements
- If input is ambiguous, ask clarifying questions
- If a file already exists, ask whether to overwrite, merge, or skip

### Rule 3: Update Progress After Each Step
- Update `progress.txt` after completing each step
- Update `LESSONS.md` when encountering and resolving errors
- Update `CLAUDE.md` when errors are caused by rules in this file (requires user approval)

---

## Project Context

**Project Name:** skill-generator
**Purpose:** A Claude Code skill that helps non-technical users create process agents (skills) using natural language through iterative conversation.

**Target Users:** Non-technical users with domain expertise (product managers, business analysts)

**Output Location:** Generated skills are created in `~/.claude/skills/[skill-name]/`

---

## Skill Structure (from new-output-folder-structure.png)

Every skill folder contains:
- `SKILL.md` (required) - Instructions in Markdown with YAML frontmatter
- `scripts/` (optional) - Executable code (Python, Bash, etc.)
- `references/` (optional) - Documentation loaded as needed
- `assets/` (optional) - Templates, fonts, icons used in output

---

## Files to Generate (from instruction.xlsx)

| File | Purpose |
|------|---------|
| PRD.md | Complete spec: what, for whom, features, in/out of scope, user stories, success criteria |
| FLOW.md | Every feature and navigation path in plain English, triggers, sequences, decision points |
| TECH_STACK.md | Every package, dependency, API locked to exact versions |
| FRONTEND_GUIDELINES.md | Design system: fonts, colors, spacing, layout rules, component styles |
| BACKEND_STRUCTURE.md | Database schema, tables, columns, types, relationships, API contracts |
| IMPLEMENTATION_PLAN.md | Step-by-step build sequence |
| CLAUDE.md | AI operation manual with rules, constraints, patterns |
| progress.txt | Tracks completed, in-progress, and upcoming work |
| LESSONS.md | Patterns and rules learned from corrections and debugging |

---

## Session Startup Checklist

At the start of each session:
1. Read `CLAUDE.md` for rules and context
2. Read `progress.txt` for current status
3. Read `LESSONS.md` for relevant lessons
4. Determine which step to continue from

---

## Git Workflow

- **Step 2 starts with git initialization:** Always ask user for git identity (name + email) as the first sub-step of Step 2
- Commit after each function module is created
- Use GitHub for version control (not file versioning)
- Ask user before pushing to remote
