# 🤖 GitHub Copilot Agents - Intelligent Heating Pilot

## 📋 Overview

This directory contains specialized GitHub Copilot agents that orchestrate development workflow following **Test-Driven Development (TDD)** and **Domain-Driven Design (DDD)** principles.

## ⚡ Quick Start: Just Use Project Manager!

**You only need one command**:

```markdown
@project-manager

Fix Issue #45: [describe problem]
```

The Project Manager automatically coordinates all other agents! See [project_manager.agent.md](project_manager.agent.md) for details.

---

## 🎭 Available Agents

### 0. Project Manager (`project_manager.agent.md`) ⭐ **RECOMMENDED**
**Role**: Orchestrate the entire workflow - single entry point for all work

**Specialization**:
- Requirement analysis
- Automatic agent coordination (Testing → Tech Lead → Documentation)
- Progress tracking and quality gates
- Error handling and user communication

**Invoke with**: `@project-manager`

**Example**:
```markdown
@project-manager

Implement Issue #50: Add multi-zone coordination feature.

Users want IHP to manage multiple heating zones with priority-based
scheduling and conflict resolution.
```

The Project Manager will handle everything automatically!

---

### 1. Testing Specialist (`testing_specialist.agent.md`)
**Role**: Write comprehensive tests BEFORE implementation (TDD Red phase)

**Specialization**:
- Test design and planning
- Unit, integration, and architectural compliance tests
- Centralized fixtures and DRY principles
- Parameterized tests for edge cases
- Mock external dependencies

**Invoke with**: `@testing-specialist`

**Example**:
```markdown
@testing-specialist

Please write tests for Issue #30: Add humidity compensation to LHS.

Requirements:
- LHS increases for high humidity (>60%)
- Compensation capped at reasonable bounds
- Graceful degradation if sensor unavailable
```

---

### 2. Tech Lead (`tech_lead.agent.md`)
**Role**: Implement clean, DDD-compliant code that makes tests pass (TDD Green + Refactor)

**Specialization**:
- Domain-Driven Design architecture
- Clean code and SOLID principles
- Type hints and comprehensive documentation
- Code refactoring while keeping tests green
- Latest library versions and best practices

**Invoke with**: `@tech-lead`

**Example**:
```markdown
@tech-lead

Tests ready for Issue #30 (humidity compensation).
Location: tests/unit/domain/test_lhs_humidity.py
Status: 4 tests failing (RED phase)

Please implement:
1. Domain: Humidity compensation in LHSCalculationService
2. Infrastructure: Update HAEnvironmentReader
3. Application: Wire humidity logic
```

---

### 3. Documentation Specialist (`documentation_specialist.agent.md`)
**Role**: Maintain and update all project documentation

**Specialization**:
- CHANGELOG.md maintenance (Keep a Changelog format)
- README.md user documentation
- ARCHITECTURE.md technical docs
- GitHub templates and release notes
- Automated release preparation

**Invoke with**: `@documentation-specialist`

**Example**:
```markdown
@documentation-specialist

Issue #30 implementation approved.

Changes:
- Added: Humidity compensation in LHS
- Modified: Environment reader includes humidity

Please update docs and prepare for merge.
```

---

## 🔄 Development Workflow

The agents work in a **structured sequence** to ensure quality:

```
1. Testing Specialist  →  2. Tech Lead  →  3. Documentation Specialist
      (Write Tests)      (Implement Code)     (Update Docs)
         ↓                      ↓                    ↓
    RED Phase              GREEN + Refactor      Ready to Merge
```

**Full workflow details**: See [AGENT_WORKFLOW.md](../AGENT_WORKFLOW.md)

### Quick Start

1. **User requests feature/bug fix**
   ```markdown
   Issue #XX opened: New feature needed
   ```

2. **Invoke Testing Specialist**
   ```markdown
   @testing-specialist
   Write tests for Issue #XX covering [scenarios]...
   ```

3. **Invoke Tech Lead** (after tests ready)
   ```markdown
   @tech-lead
   Implement Issue #XX, tests in tests/unit/domain/test_XX.py
   ```

4. **Code Review** (user validates)
   - Review implementation
   - Approve or request changes

5. **Invoke Documentation Specialist** (after approval)
   ```markdown
   @documentation-specialist
   Update docs for Issue #XX, changes: [list]...
   ```

6. **Merge PR**

---

## 📚 Documentation

### Agent Instructions
- [testing_specialist.agent.md](testing_specialist.agent.md) - Testing Specialist guidelines
- [tech_lead.agent.md](tech_lead.agent.md) - Tech Lead guidelines  
- [documentation_specialist.agent.md](documentation_specialist.agent.md) - Documentation Specialist guidelines

### Workflow & Process
- [AGENT_WORKFLOW.md](../AGENT_WORKFLOW.md) - Complete orchestrated workflow
- [../CONTRIBUTING.md](../../CONTRIBUTING.md) - General contribution guide
- [../ARCHITECTURE.md](../../ARCHITECTURE.md) - DDD architecture documentation

### Templates & Tools
- [../PULL_REQUEST_TEMPLATE.md](../PULL_REQUEST_TEMPLATE.md) - PR template with agent checklist
- [../RELEASE_TEMPLATE.md](../RELEASE_TEMPLATE.md) - Release process guide
- [../workflows/create-release.yml](../workflows/create-release.yml) - Automated release workflow

---

## 🎯 Agent Philosophy

### Test-Driven Development (TDD)

All development follows the **Red-Green-Refactor** cycle:

1. **🔴 RED**: Write failing tests (Testing Specialist)
2. **🟢 GREEN**: Make tests pass (Tech Lead)
3. **🔵 REFACTOR**: Improve code quality (Tech Lead)

**Benefits**:
- Tests define requirements
- Code is inherently testable
- Refactoring is safe (tests catch regressions)
- Documentation through tests

### Domain-Driven Design (DDD)

All code follows **DDD architecture**:

```
domain/              # Pure business logic (NO Home Assistant)
├── value_objects/   # Immutable data carriers
├── entities/        # Domain entities
├── interfaces/      # Abstract contracts
└── services/        # Domain services

infrastructure/      # Home Assistant integration
├── adapters/        # HA API implementations
└── repositories/    # Data persistence

application/         # Use case orchestration
```

**Benefits**:
- Business logic isolated and testable
- Clear boundaries and responsibilities
- Easy to understand and maintain
- Resilient to HA changes

### Clean Code Principles

All agents follow **clean code standards**:

✅ Complete type hints
✅ Google-style docstrings
✅ Small, focused functions (<20 lines)
✅ Descriptive naming
✅ No magic numbers/strings
✅ Proper error handling
✅ DRY (Don't Repeat Yourself)

---

## 🔧 Configuration

### Agent Metadata

Each agent file (`*.agent.md`) contains:

```yaml
--- 
name: Agent-Name
description: Agent role and specialization
tools: ['edit/createFile', 'search', 'runTests', ...]
---
```

**Available tools**:
- `edit/createFile` - Create new files
- `edit/editFiles` - Modify existing files
- `search` - Search codebase
- `usages` - Find code usages
- `runTests` - Execute test suite
- `errors` - Get compilation/lint errors
- `github.*/issue_fetch` - Read GitHub issues
- `todos` - Manage todo lists

### GitHub Copilot Setup

Agents are automatically available in GitHub Copilot when:

1. Agent files exist in `.github/agents/`
2. Files follow `*.agent.md` naming convention
3. Valid frontmatter metadata present

**No additional setup required!**

---

## 📊 Workflow Metrics

Track these metrics for quality:

### Testing Phase
- Test coverage: >80% for domain layer
- Tests written before code: 100%
- Architectural compliance: 100%
- Test execution time: <30s for unit tests

### Implementation Phase
- All tests passing: 100%
- Linting errors: 0
- Type hint coverage: 100%
- Average function size: <20 lines

### Documentation Phase
- CHANGELOG updated: 100%
- Documentation completeness: 100%
- Broken links: 0
- Documentation lag: <24h after merge

---

## 🚀 Advanced Usage

### Parallel Work with Agents

For complex features, invoke agents in sequence with context:

```markdown
@testing-specialist

Write tests for Issue #40 - Multi-zone coordination.

This is a multi-part feature:
- Part 1: Zone priority system (write tests for this first)
- Part 2: Cross-zone optimization (defer)
- Part 3: Conflict resolution (defer)

Focus on Part 1 only for now.
```

### Agent Context Switching

If code review requests changes:

```markdown
@testing-specialist

Code review feedback for Issue #40:
- Add test for equal priority zones (tie-breaking)
- Test should verify deterministic ordering

Update tests, then hand to @tech-lead for re-implementation.
```

### Custom Agent Workflows

For special cases (e.g., refactoring without new features):

```markdown
@tech-lead

Refactor LHSCalculationService to extract trimmed mean logic.

Context:
- No new tests needed (behavior unchanged)
- Existing tests must stay green
- Goal: Reuse trimmed mean in other services

Focus on:
1. Extract to utility function
2. Update all usages
3. Keep tests passing
```

---

## 🐛 Troubleshooting

### Agent Not Responding as Expected

**Problem**: Agent ignores instructions or gives generic response

**Solution**: Be more specific
```markdown
# Too vague
@testing-specialist write some tests

# Better
@testing-specialist write tests for Issue #30 covering:
1. Happy path: feature works normally
2. Edge case: boundary condition X
3. Error case: invalid input Y
```

### Tests Fail After Implementation

**Problem**: Tech Lead's code doesn't pass tests

**Solution**: Review with Testing Specialist
```markdown
@testing-specialist

Tech Lead's implementation fails test_scenario_x.
Error: AssertionError: Expected Y, got Z

Please review if test expectations are correct or if
implementation is wrong. Update tests if needed.
```

### Documentation Out of Sync

**Problem**: Docs don't reflect recent changes

**Solution**: Always invoke Documentation Specialist
```markdown
@documentation-specialist

Features merged without doc updates:
- Issue #30 (humidity compensation)
- Issue #31 (storage optimization)

Please:
1. Update CHANGELOG.md for both
2. Update README.md if user-facing
3. Update ARCHITECTURE.md if needed
```

---

## 🎓 Learning Resources

### For New Contributors

1. **Start here**: [AGENT_WORKFLOW.md](../AGENT_WORKFLOW.md)
2. **Learn TDD**: Read Testing Specialist agent docs
3. **Learn DDD**: Read [ARCHITECTURE.md](../../ARCHITECTURE.md)
4. **Practice**: Try fixing a "good first issue"

### For Agent Improvement

1. **Analyze metrics**: Review workflow efficiency
2. **Refine instructions**: Update agent docs based on experience
3. **Add examples**: Document edge cases and solutions
4. **Share learnings**: Update AGENT_WORKFLOW.md with patterns

---

## 🏆 Success Criteria

Development is successful when:

✅ **All tests pass** (TDD discipline)
✅ **Architecture respected** (DDD compliance)
✅ **Code is clean** (readable, maintainable)
✅ **Documentation current** (CHANGELOG, README up-to-date)
✅ **Process followed** (agents used in sequence)
✅ **Quality metrics met** (coverage, linting, etc.)

---

## 📝 Quick Reference

### Agent Invocation Syntax

```markdown
@agent-name

Brief description of task.

Context:
- Relevant information
- Related issues
- Constraints

Expected deliverables:
1. Item 1
2. Item 2
```

### Workflow Phases

| Phase | Agent | Input | Output |
|-------|-------|-------|--------|
| 1. Test Design | Testing Specialist | Issue requirements | Failing tests (RED) |
| 2. Implementation | Tech Lead | Failing tests | Passing tests (GREEN) |
| 3. Code Review | User | Implementation | Approval or feedback |
| 4. Documentation | Documentation Specialist | Approved code | Updated docs |
| 5. Merge | User | Complete PR | Merged feature |

---

**Last Updated**: November 2025  
**Agent System Version**: 1.0  
**For Questions**: See [AGENT_WORKFLOW.md](../AGENT_WORKFLOW.md) or open a discussion
