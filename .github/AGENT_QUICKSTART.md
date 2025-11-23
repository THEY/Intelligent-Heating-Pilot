# 🚀 Quick Start: Agent-Driven Development

## Welcome to Intelligent Heating Pilot Development!

This project uses **specialized GitHub Copilot agents** to ensure high-quality, test-driven development following Domain-Driven Design principles.

---

## ⚡ Super Simple: Just Talk to the Project Manager!

**You don't need to manage multiple agents!** 

Just invoke the **Project Manager** agent, and it will automatically coordinate all the other agents for you:

```markdown
@project-manager

Fix Issue #45: Pre-heating starts too early in humid weather.
```

The Project Manager will:
1. ✅ Automatically invoke Testing Specialist to write tests
2. ✅ Automatically invoke Tech Lead to implement code
3. ✅ Ask you to review
4. ✅ Automatically invoke Documentation Specialist after approval
5. ✅ Report completion

**That's it!** One command, complete workflow.

---

## 🎯 The 4-Agent System (Orchestrated)

```
┌─────────────────────────────────────────────────────────────┐
│                  Feature/Bug Fix Request                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │  1️⃣  Testing Specialist Agent    │
        │      Write Tests FIRST (TDD)      │
        │                                    │
        │  📝 Input:  Issue requirements     │
        │  📤 Output: Failing tests (RED)    │
        └────────────┬───────────────────────┘
                     │ Tests ready
                     ▼
        ┌────────────────────────────────────┐
        │  2️⃣  Tech Lead Agent              │
        │      Implement Clean Code          │
        │                                    │
        │  📝 Input:  Failing tests          │
        │  📤 Output: Passing tests (GREEN)  │
        └────────────┬───────────────────────┘
                     │ Code ready
                     ▼
        ┌────────────────────────────────────┐
        │  👤  User Code Review              │
        │                                    │
        │  ✅ Approved  →  Continue          │
        │  ❌ Changes   →  Back to Agent 1   │
        └────────────┬───────────────────────┘
                     │ Approved
                     ▼
        ┌────────────────────────────────────┐
        │  3️⃣  Documentation Specialist    │
        │      Update All Docs               │
        │                                    │
        │  📝 Input:  Approved code          │
        │  📤 Output: Updated documentation  │
        └────────────┬───────────────────────┘
                     │ Docs ready
                     ▼
        ┌────────────────────────────────────┐
        │        🎉 Merge PR                │
        └────────────────────────────────────┘
```

---

## ⚡ 5-Minute Quick Start

### 1. You Have an Issue to Fix

Example: **Issue #45** - "Pre-heating starts too early in humid weather"

### 2. Invoke Testing Specialist

```markdown
@testing-specialist

Please write tests for Issue #45: Pre-heating too early in humid weather.

The problem: LHS calculation doesn't account for humidity, causing 
pre-heating to start 30-45 minutes too early when humidity > 70%.

Write tests to verify:
1. LHS adjusts upward when humidity is high (>60%)
2. Adjustment is proportional (linear 0-60%)
3. Missing humidity sensor doesn't break predictions
4. Extreme humidity values (99%) are capped reasonably
```

**Agent Response**:
```
✅ Tests ready for Issue #45
- 4 tests written (domain layer)
- All tests failing (RED phase)
- Files: tests/unit/domain/test_lhs_humidity_fix.py
- Ready for @tech-lead
```

### 3. Invoke Tech Lead

```markdown
@tech-lead

Tests ready for Issue #45. Please implement humidity compensation.

Test location: tests/unit/domain/test_lhs_humidity_fix.py
Status: 4 tests failing (RED phase)

Requirements:
- Add humidity parameter to LHSCalculationService.calculate()
- Apply compensation: adjusted_lhs = base_lhs * (1 + humidity_factor)
- Update HAEnvironmentReader to read humidity sensor
- Wire humidity data through application layer
- Keep domain layer pure (no HA imports)
```

**Agent Response**:
```
✅ Implementation complete for Issue #45
- All 4 tests passing (GREEN phase)
- Domain: LHSCalculationService applies humidity compensation
- Infrastructure: HAEnvironmentReader reads humidity sensor
- Coverage: 87% domain, 72% overall
- No linting errors
- Ready for code review!
```

### 4. Review Code

Check:
- [ ] Tests make sense
- [ ] Code is clean and readable
- [ ] Architecture respected (DDD)
- [ ] No regression

**Approve** or **Request Changes**

### 5. Invoke Documentation Specialist

```markdown
@documentation-specialist

Issue #45 approved and ready for documentation.

Changes:
- Fixed: Pre-heating timing in humid weather
- Added: Humidity compensation in LHS calculation
- Modified: Environment reader includes humidity sensor

Please update all relevant documentation.
```

**Agent Response**:
```
✅ Documentation updated for Issue #45
- CHANGELOG.md: Added fix under [Unreleased]
- README.md: Updated optional sensors section
- ARCHITECTURE.md: Documented humidity compensation
- PR ready for merge!
```

### 6. Merge

```bash
git checkout integration
git merge feature/issue-45 --no-ff
git push origin integration
```

**Done!** 🎉

---

## 📚 Detailed Documentation

### Must-Read Documents

1. **[AGENT_WORKFLOW.md](.github/AGENT_WORKFLOW.md)** ⭐ **START HERE**
   - Complete workflow explanation
   - Detailed examples
   - Troubleshooting guide

2. **[agents/README.md](.github/agents/README.md)**
   - Agent system overview
   - Quick reference
   - Configuration details

3. **[CONTRIBUTING.md](CONTRIBUTING.md)**
   - Development environment setup
   - Coding standards
   - Testing requirements

4. **[ARCHITECTURE.md](ARCHITECTURE.md)**
   - Domain-Driven Design principles
   - Layer structure
   - Best practices and anti-patterns

### Agent Instructions

- **[testing_specialist.agent.md](.github/agents/testing_specialist.agent.md)** - How Testing Specialist works
- **[tech_lead.agent.md](.github/agents/tech_lead.agent.md)** - How Tech Lead works
- **[documentation_specialist.agent.md](.github/agents/documentation_specialist.agent.md)** - How Documentation Specialist works

---

## 🎓 Key Principles

### Test-Driven Development (TDD)

```
🔴 RED   →  Write failing tests
🟢 GREEN →  Make tests pass
🔵 BLUE  →  Refactor code
```

**Why?**
- Tests define requirements
- Code is inherently testable
- Safe refactoring
- Living documentation

### Domain-Driven Design (DDD)

```
domain/          ← Pure business logic (NO Home Assistant)
infrastructure/  ← HA integration (thin adapters)
application/     ← Orchestration
```

**Why?**
- Business logic isolated and testable
- Clear boundaries
- Easy to understand and maintain
- Resilient to framework changes

### Clean Code

✅ Type hints everywhere
✅ Google-style docstrings
✅ Small functions (<20 lines)
✅ Descriptive naming
✅ No magic values
✅ Proper error handling

---

## 🚨 Common Mistakes (Avoid!)

### ❌ Skipping Tests

**Wrong**:
```markdown
@tech-lead
Implement Issue #45 - humidity compensation
```

**Right**:
```markdown
@testing-specialist
Write tests for Issue #45 first

Then @tech-lead can implement
```

### ❌ Breaking DDD Architecture

**Wrong** (in `domain/` layer):
```python
from homeassistant.core import HomeAssistant  # ❌ NO!
```

**Right**:
```python
from domain.interfaces.reader import IReader  # ✅ Use interfaces
```

### ❌ Skipping Documentation

**Wrong**: Merge without updating docs

**Right**: Always invoke `@documentation-specialist` before merge

---

## 💡 Pro Tips

### Tip 1: Be Specific with Agents

```markdown
# Too vague
@testing-specialist write some tests

# Better
@testing-specialist write tests for Issue #45 covering:
1. Happy path: humidity compensation works
2. Edge case: missing humidity sensor
3. Error case: invalid humidity value (>100%)
```

### Tip 2: Run Tests Frequently

```bash
# After each small change
pytest tests/unit/domain/test_feature.py -v

# Check coverage
pytest --cov=custom_components.intelligent_heating_pilot
```

### Tip 3: Keep Tests Green During Refactoring

```bash
# Before refactoring
pytest tests/ -v  # All green

# Refactor code
# ...

# After refactoring
pytest tests/ -v  # Still all green!
```

---

## 🎯 Success Checklist

Before merging any PR:

- [ ] Tests written first (TDD Red phase)
- [ ] All tests passing (TDD Green phase)
- [ ] Code refactored and clean (TDD Refactor phase)
- [ ] Domain layer has NO HA imports (DDD compliance)
- [ ] Type hints and docstrings complete
- [ ] No linting errors
- [ ] CHANGELOG.md updated
- [ ] Documentation updated
- [ ] Code reviewed and approved

---

## 🆘 Need Help?

### Quick Links

- **[AGENT_WORKFLOW.md](.github/AGENT_WORKFLOW.md)** - Complete workflow guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development setup
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - DDD architecture
- **[GitHub Discussions](https://github.com/RastaChaum/Intelligent-Heating-Pilot/discussions)** - Ask questions

### Troubleshooting

**Agent not responding?** → Be more specific in your request

**Tests failing?** → Review test expectations with Testing Specialist

**Architecture violation?** → Check domain layer has no HA imports

**Docs out of sync?** → Always invoke Documentation Specialist

---

## 🎉 You're Ready!

Follow the 3-agent workflow for all features and bug fixes to maintain high quality and consistency.

**First contribution?** Try a "good first issue" to practice the workflow!

---

**Last Updated**: November 2025  
**Workflow Version**: 1.0  
**Questions?** Open a [Discussion](https://github.com/RastaChaum/Intelligent-Heating-Pilot/discussions)
