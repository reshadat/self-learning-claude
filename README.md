# SLC: Self-Learning Claude

A framework for building self-improving LLM systems through evolving context playbooks.

## Overview

SLC enables Claude to learn from experience by maintaining a local playbook of patterns that gets smarter over time. Each project directory gets its own `.playbook/slc-playbook.json` that stores learned patterns.

## Installation

### As a Claude Code Skill

Copy the folder to your Claude skills directory:

```bash
cp -r self-learning-claude ~/.claude/skills/
```

### Standalone Usage

Copy `scripts/slc_learn.py` to your project and reference it in your project's `CLAUDE.md`.

## Quick Start

1. **Initialize** a playbook with seed patterns:
   ```bash
   python3 scripts/slc_learn.py seed
   ```

2. **Load** patterns at task start:
   ```bash
   python3 scripts/slc_learn.py load --endpoint "POST /api/users"
   ```

3. **Record success** when something works:
   ```bash
   python3 scripts/slc_learn.py success \
       --helpful "P-abc123,S-def456" \
       --lesson "API requires Content-Type header" \
       --category strategy
   ```

4. **Record failure** when something goes wrong:
   ```bash
   python3 scripts/slc_learn.py failure \
       --lesson "Timeout occurs when payload > 1MB" \
       --endpoint "POST /api/upload"
   ```

5. **View stats**:
   ```bash
   python3 scripts/slc_learn.py stats
   ```

## Pattern Categories

| Category   | Use For                                    |
|------------|-------------------------------------------|
| `pitfall`  | Errors, failures, things to avoid         |
| `strategy` | Approaches that worked well               |
| `domain`   | Project-specific terminology mappings     |
| `endpoint` | Specific to one API/function              |
| `code`     | Code patterns, commands, workarounds      |

## File Structure

```
self-learning-claude/
├── README.md              # This file
├── LICENSE.md             # MIT License
├── SKILL.md               # Claude Code skill definition
├── references/
│   └── seed-patterns.md   # Example patterns by project type
└── scripts/
    └── slc_learn.py       # Main learning script
```

## Integration with CLAUDE.md

Add to your project's `CLAUDE.md`:

```markdown
## Self-Learning Mode

Use SLC learning for this project:
- At task start: `python3 /path/to/slc_learn.py load`
- After success: `python3 /path/to/slc_learn.py success --lesson "..."`
- After failure: `python3 /path/to/slc_learn.py failure --lesson "..."`
```

## Writing Good Lessons

**Good** (specific, actionable):
- "API endpoint requires array type for 'items' field, not object"
- "Authentication token expires after 1 hour - implement refresh logic"
- "Database connection must be closed explicitly in finally block"

**Bad** (vague, generic):
- "Be careful with types"
- "Check the schema"
- "This is tricky"

## Playbook Storage

Playbooks are stored locally per project:
```
~/project-a/.playbook/slc-playbook.json  # Patterns for project A
~/project-b/.playbook/slc-playbook.json  # Patterns for project B
```

## License

MIT - See [LICENSE.md](LICENSE.md)
