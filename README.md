# SLC: Self-Learning Claude

A framework for building self-improving LLM systems through evolving context playbooks.

## Installation

Copy the folder to your Claude Code skills directory:

```bash
cp -r self-learning-claude ~/.claude/skills/
```

## Usage

Invoke the skill in Claude Code:

```
/self-learning-claude
```

Claude will automatically use the SLC workflow:
- **Load** patterns at task start
- **Record success** when approaches work
- **Record failure** when things go wrong

## How It Works

Each project directory gets its own `.playbook/slc-playbook.json` that stores learned patterns. Patterns are categorized as:

| Category   | Use For                                    |
|------------|-------------------------------------------|
| `pitfall`  | Errors, failures, things to avoid         |
| `strategy` | Approaches that worked well               |
| `domain`   | Project-specific terminology mappings     |
| `endpoint` | Specific to one API/function              |
| `code`     | Code patterns, commands, workarounds      |

## License

MIT - See [LICENSE.md](LICENSE.md)
