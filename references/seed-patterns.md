# Seed Patterns by Project Type

Use these when initializing a playbook for a specific type of project.

## Python Projects

```python
patterns = [
    ("pitfall", "Don't use mutable default arguments like def foo(items=[])"),
    ("pitfall", "asyncio.run() can't be called from an already-running loop"),
    ("pitfall", "f-strings don't work with walrus operator inside the braces"),
    ("strategy", "Use pathlib.Path instead of os.path for cleaner path handling"),
    ("strategy", "Use contextlib.suppress() instead of try/except/pass"),
    ("strategy", "Run pytest with -x flag to stop on first failure during debugging"),
    ("code", "Type hint pattern: def foo(x: str | None = None) -> dict[str, Any]"),
]
```

## JavaScript/TypeScript Projects

```python
patterns = [
    ("pitfall", "await inside forEach doesn't work - use for...of or Promise.all"),
    ("pitfall", "Object spread creates shallow copies only - nested objects share references"),
    ("pitfall", "typeof null returns 'object' - use explicit null check"),
    ("strategy", "Use optional chaining (?.) for safe nested property access"),
    ("strategy", "Prefer const over let when variable won't be reassigned"),
    ("code", "Async error handling: try { await fn() } catch (e) { if (e instanceof Error) ... }"),
]
```

## React/Frontend Projects

```python
patterns = [
    ("pitfall", "useEffect cleanup function must be returned, not called directly"),
    ("pitfall", "Don't mutate state directly - always use setState or spread operator"),
    ("pitfall", "Keys in lists must be stable - don't use array index if list can reorder"),
    ("strategy", "Use React.memo() for expensive components that receive same props"),
    ("strategy", "Colocate state with the components that use it"),
    ("code", "Custom hook pattern: function useCustomHook() { const [state, setState] = useState(); return { state }; }"),
]
```

## API/Backend Projects

```python
patterns = [
    ("pitfall", "Always validate request body before processing - never trust client input"),
    ("pitfall", "HTTP 401 vs 403: 401 = not authenticated, 403 = authenticated but not authorized"),
    ("pitfall", "Connection pools can be exhausted - always release connections in finally block"),
    ("strategy", "Return consistent error response format across all endpoints"),
    ("strategy", "Log request ID in all log messages for request tracing"),
    ("code", "Pagination pattern: { data: [...], meta: { page, limit, total, hasMore } }"),
]
```

## Infrastructure/DevOps Projects

```python
patterns = [
    ("pitfall", "Terraform destroy doesn't prompt in CI - always use -auto-approve carefully"),
    ("pitfall", "Docker COPY with . ignores .dockerignore only for first COPY"),
    ("strategy", "Use terraform plan -out=plan.tfplan then apply plan.tfplan for safety"),
    ("strategy", "Always pin versions in Dockerfile - never use :latest in production"),
    ("domain", "Container startup can take 30+ seconds - configure health check accordingly"),
]
```

## Database Projects

```python
patterns = [
    ("pitfall", "N+1 query problem - use JOIN or batch loading instead of loop queries"),
    ("pitfall", "Large transactions can lock tables - break into smaller batches"),
    ("strategy", "Add indexes for columns used in WHERE, JOIN, and ORDER BY clauses"),
    ("strategy", "Use connection pooling to avoid connection overhead"),
    ("code", "Safe migration pattern: add column nullable -> backfill -> add constraint"),
]
```

## Custom Seed Script

To seed with custom patterns, create a script:

```python
#!/usr/bin/env python3
import subprocess
import sys

patterns = [
    # Add your patterns here
    ("pitfall", "Your project-specific pitfall"),
    ("strategy", "Your project-specific strategy"),
]

for category, content in patterns:
    subprocess.run([
        sys.executable, "slc_learn.py", "success",
        "--lesson", content,
        "--category", category
    ])
```
