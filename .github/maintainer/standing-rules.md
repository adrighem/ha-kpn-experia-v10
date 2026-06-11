# Maintainer Standing Rules

- Never merge external pull requests directly; use them as implementation input.
- Get explicit human approval before any public action: comments, labels, closures, PRs, releases.
- Keep changes scoped and covered by tests when component behavior changes.
- Avoid committing generated dependency trees, scratch probe output, local credentials, or live-router artifacts.
- Before merging a branch, compare `custom_components/experiaboxv10/manifest.json` against the current release and `origin/master`.
