# PRD.md - Product Requirements Document

## Product Overview

**Product Name:** skill-generator

**Purpose:** A Claude Code skill that helps non-technical users create skills using natural language through iterative conversation.

**Tagline:** Turn your domain expertise into actionable AI skills - no coding required.

---

## Target Users

### Primary Users
- **Product Managers** who want to codify their product processes into reusable AI skills
- **Business Analysts** who need to document and automate business workflows
- **Domain Experts** with professional knowledge but no programming experience

### User Characteristics
- Comfortable with natural language communication
- May have limited or no coding experience
- Have clear domain knowledge they want to operationalize
- Value iterative refinement over perfect-first-time output

---

## Core Features

### Feature 1: Guided Discovery (Step 1: Ask)
**Description:** skill-generator asks structured questions to understand the user's intended skill before any code is written.

**User Story:** As a product manager, I want to be asked the right questions about my process so that the generated skill accurately reflects my requirements.

**Acceptance Criteria:**
- [ ] skill-generator creates core context files first (CLAUDE.md, progress.txt, LESSONS.md)
- [ ] skill-generator asks all 7 core questions:
  1. Who is this for?
  2. What is the user's core action?
  3. What happens after the action?
  4. What data needs to be saved?
  5. What data needs to be displayed?
  6. What happens on error?
  7. What happens on success?
- [ ] skill-generator asks technical clarification questions:
  - Agent framework preferences (default: as defined in CLAUDE.md Skill Structure section)
  - Structure preferences (default: as defined in CLAUDE.md Skill Structure section)
- [ ] skill-generator waits for explicit user confirmation before proceeding to Step 2

**Out of Scope:** Auto-generating questions based on vague input - skill-generator must ask specific, structured questions.

---

### Feature 2: Iterative File Creation (Step 2: Plan)
**Description:** skill-generator creates specification files one by one, requiring user approval before each file.

**User Story:** As a business analyst, I want to review each specification file before the next is created so I can catch errors early.

**Acceptance Criteria:**
- [ ] Files are created in order: PRD.md → FLOW.md → TECH_STACK.md → FRONTEND_GUIDELINES.md → BACKEND_STRUCTURE.md → IMPLEMENTATION_PLAN.md
- [ ] Each file requires explicit user approval before the next is created
- [ ] User can request modifications to any file before approval
- [ ] Git commit is made after each file is approved

**Out of Scope:** Bulk file generation without review.

---

### Feature 3: Step-by-Step Build (Step 3: Build)
**Description:** skill-generator implements the skill following IMPLEMENTATION_PLAN.md, one step at a time with user approval.

**User Story:** As a domain expert, I want to see each implementation step before the next so I can verify the skill is being built correctly.

**Acceptance Criteria:**
- [ ] Each implementation step requires user approval before proceeding
- [ ] progress.txt is updated after each step
- [ ] Errors are documented in LESSONS.md with resolution patterns
- [ ] CLAUDE.md is updated when errors are caused by existing rules

**Out of Scope:** Skipping steps or batch implementation.

---

### Feature 4: Pre-launch Check (Step 4: Pre-launch Check)
**Description:** Before launching the skill, skill-generator runs a thorough check across multiple dimensions.

**User Story:** As a user, I want confidence that my skill works correctly before I deploy it.

**Acceptance Criteria:**
- [ ] **Redundancy check:** No duplicate or conflicting logic in generated files
- [ ] **Security check:** No vulnerabilities (command injection, path traversal, etc.)
- [ ] **Output Quality check:** User provides a real use case for the skill being created
  - skill-generator loads the created skill to execute the use case
  - **Direct task execution or using other skills is prohibited** - the skill being created must be loaded and run
  - User reviews the output/result
  - If user approves the result → Quality check passed, proceed to launch
  - If user reports issues → Activate Step 5: Debug to help fix the skill
- [ ] User must manually approve Redundancy and Security checkpoints before launch

**Out of Scope:** Manual file-by-file verification by users (quality is validated through actual use case execution).

---

### Feature 5: Debug Mode (Step 5: Debug)
**Description:** When the launched skill encounters errors, users can activate debug mode to diagnose and fix issues.

**User Story:** As a user, I want an easy way to fix errors in my skill without starting over.

**Acceptance Criteria:**
- [ ] skill-generator reads CLAUDE.md, progress.txt, LESSONS.md for context
- [ ] skill-generator helps identify root cause of errors
- [ ] Fixes are documented in LESSONS.md
- [ ] CLAUDE.md is updated if the error reveals a rule gap

**Out of Scope:** Debugging third-party tools or external services.

---

### Feature 6: Progress Dashboard
**Description:** skill-generator displays current progress, completed files, and next steps.

**User Story:** As a user, I want to see where I am in the skill creation process at a glance.

**Acceptance Criteria:**
- [ ] progress.txt shows current step status
- [ ] Completed items are clearly marked
- [ ] Next steps are clearly indicated
- [ ] Session notes provide context for resumption

**Out of Scope:** Visual/GUI dashboard (text-based tracking only).

---

### Feature 7: Conversation History
**Description:** skill-generator saves conversation history with users for context continuity.

**User Story:** As a user, I want the skill to remember our conversation so I don't have to repeat myself.

**Acceptance Criteria:**
- [ ] Conversation context is preserved in CLAUDE.md
- [ ] progress.txt tracks session notes
- [ ] LESSONS.md captures learnings from corrections

**Out of Scope:** Long-term conversation storage beyond the current skill project.

---

## Success Criteria

### Functional Success
- [ ] skill-generator can create a complete, working skill from natural language input
- [ ] All 9 specification files are generated correctly (PRD.md, FLOW.md, TECH_STACK.md, FRONTEND_GUIDELINES.md, BACKEND_STRUCTURE.md, IMPLEMENTATION_PLAN.md, CLAUDE.md, progress.txt, LESSONS.md)
- [ ] Generated skills follow the required structure (SKILL.md + scripts/ + references/ + assets/)
- [ ] Git repository is properly initialized and maintained

### User Experience Success
- [ ] Non-technical users can complete skill creation without external help
- [ ] Users feel in control with approval gates at each step
- [ ] Errors are resolved through clear, guided debugging

---

## Non-Goals (Out of Scope)

- **Visual/GUI Interface:** skill-generator is a text-based Claude Code skill
- **Multi-language Support:** English only for initial version
- **Automated Testing:** Manual verification is required at each step
- **Batch Processing:** All operations require user approval before proceeding
- **External Integrations:** No integration with external project management tools
- **Version Comparison:** Only comparison conclusions shown, not full diffs

---

## Technical Constraints

- **Platform:** Claude Code skills (Markdown-based with YAML frontmatter)
- **Output Location:** Generated skills are created in `~/.claude/skills/[skill-name]/`
- **Framework:** Anthropic's agent framework
- **Version Control:** Git with GitHub

---

## Dependencies

| Dependency | Purpose | Version |
|------------|---------|---------|
| Claude Code | Host platform | Latest |
| Git | Version control | System default |
| Bash | Script execution | System default |
| Python (optional) | Helper scripts | 3.x |

---

## Future Considerations (Not in MVP)

- Visual progress dashboard
- Template library for common skill patterns
- Multi-language support
- Integration with external documentation tools
- Automated testing framework
