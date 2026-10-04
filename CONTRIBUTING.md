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

We use merge commits for pull requests ("Create a merge commit" on GitHub), not squash
or rebase merging. This keeps every commit and its author in the history, and keeps
`dev`, `staging` and `main` in line with each other.

- `dev`, `staging` and `main` are protected: changes reach them only through pull requests.
- Work branches merge into `dev`.
- Releases are promoted `dev` -> `staging` -> `main`, then tagged on `main`
  (for example `model-v1.0`).
- If a pull request has conflicts, merge `dev` into the work branch, resolve them there,
  and push. If `dvc.lock` or `metrics.json` conflict, run `uv run dvc repro` after
  resolving instead of picking one side by hand.
