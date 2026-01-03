---
name: self-learning-claude
description: Self-Learning Claude (SLC) framework for building self-improving LLM systems through evolving context playbooks. Use this skill when building agents, workflows, or domain-specific systems that need to accumulate knowledge over time, when optimizing prompts/system instructions through iteration, when implementing memory systems for LLM agents, or when you need structured approaches to prevent context collapse and brevity bias in iterative LLM refinement.
---

# SLC: Self-Learning Claude

SLC enables Claude to learn from experience by maintaining a local playbook of patterns that gets smarter over time.

## How It Works

Each project directory gets a `.playbook/slc-playbook.json` that stores learned patterns:

```
~/project-a/.playbook/slc-playbook.json  # Patterns for project A
~/project-b/.playbook/slc-playbook.json  # Patterns for project B
```

## Automatic Workflow

### 1. At Task Start - Load Patterns
```bash
python3 /path/to/slc_learn.py load --endpoint "METHOD /path"
```

### 2. After Success - Record What Worked
```bash
python3 /path/to/slc_learn.py success \
    --helpful "P-abc123,S-def456" \
    --lesson "What you discovered" \
    --category strategy \
    --endpoint "METHOD /path"
```

### 3. After Failure - Record What Went Wrong
```bash
python3 /path/to/slc_learn.py failure \
    --lesson "What failed and why" \
    --endpoint "METHOD /path"
```

## Categories

| Category | Use For |
|----------|---------|
| `pitfall` | Errors, failures, things to avoid |
| `strategy` | Approaches that worked well |
| `domain` | Project-specific terminology mappings |
| `endpoint` | Specific to one API/function |
| `code` | Code patterns, commands, workarounds |

## CLI Reference

```bash
# Load patterns for current task
slc_learn.py load [-e "endpoint"]

# Record success
slc_learn.py success [--helpful ids] [--lesson text] [--category cat] [-e endpoint]

# Record failure
slc_learn.py failure [--harmful ids] [--lesson text] [-e endpoint]

# Initialize with seed patterns
slc_learn.py seed [--force]

# Show statistics
slc_learn.py stats
```

## Good vs Bad Lessons

**Good** (specific, actionable):
- "API endpoint requires array type for 'items' field, not object"
- "Authentication token expires after 1 hour - implement refresh logic"
- "Database connection must be closed explicitly in finally block"

**Bad** (vague, generic):
- "Be careful with types"
- "Check the schema"
- "This is tricky"

## Integration

Add to your CLAUDE.md:
```markdown
## Self-Learning Mode

Use SLC learning for this project. At task start run `slc_learn.py load`,
after success run `slc_learn.py success --lesson "..."`,
after failure run `slc_learn.py failure --lesson "..."`.
```

The script location should be referenced from your project's CLAUDE.md.
