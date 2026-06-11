# Maintainer Patterns

## Router API support

- Real router responses can vary by firmware state. Preserve tests around API error handling and add fixtures for every newly observed router response shape.

## Release hygiene

- After release-please merges a release PR, feature branches created before the release can carry stale `manifest.json` versions. Check branch manifests before merging follow-up fixes.

## Validation

- Minimum local verification for code changes: run the CI-style pytest command from `.github/workflows/tests.yml`.
- HACS and hassfest results should be checked through GitHub Actions before release.
