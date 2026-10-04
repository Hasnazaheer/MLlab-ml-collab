# Contributing

## Branch Naming

- feat/<name>
- data/<name>
- exp/<member>-<idea>
- fix/<name>

## Commit Convention

We use Conventional Commits:

- feat: new feature
- data: dataset changes
- exp: experiment changes
- fix: bug fixes
- docs: documentation

## Dependencies

Dependencies are managed with uv in `pyproject.toml` and `uv.lock`.

- Add a package: `uv add <package>` (dev-only tools: `uv add --dev <package>`)
- Remove a package: `uv remove <package>`
- After pulling changes: `uv sync`

Always commit `pyproject.toml` and `uv.lock` together. Don't install packages with
`pip install`, because they won't be recorded in the lock file.

## Merge Strategy

We use squash merging for pull requests.
