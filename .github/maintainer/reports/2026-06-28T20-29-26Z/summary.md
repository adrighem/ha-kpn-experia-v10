# Maintainer Run - 2026-06-28T20:29:26Z

Mode: Maintain -> Ship

Capture method: manual GitHub CLI. The installed open-source-maintainer skill still lacks the optional `references/` and `scripts/` bundle in this environment.

## Snapshot

- Repository: `adrighem/ha-kpn-experia-v10`
- Default branch: `master`
- Open issues: 0
- Open pull requests: 0
- Latest release: `v3.2.2`, published 2026-06-28T18:12:00Z
- Current branch: `master` at `2140207`, tag `v3.2.2`
- CI signal: latest `master` Tests, HACS Validation, hassfest, release-please, and CodeQL runs are green

## Top Recommendations

1. Ship the local follow-up fix for `ISSUE:8:C:3`.
2. Cut a patch release after CI passes, because the reporter still sees warning spam every polling interval on firmware `V10.C.25.08.15`.
3. After human approval and release, post a short follow-up on `ISSUE:8` asking the reporter to update and confirm the new `Devices.Device.guest` warning is gone.

## Issue Analysis

`ISSUE:8` is closed by `v3.2.2`, but the reporter added a post-release comment after updating:

- Endpoint: `Devices.Device.guest`
- Router error: `13`, `Permission denied`
- Log path: `custom_components.experiaboxv10.coordinator`
- Behavior: repeated "Partial update failure for devices" warnings

Intent: the same as the original issue: stop non-fatal permission-denied router behavior from creating repeated warning logs.

Decision: keep device discovery strict on initial setup/first refresh, but when previous coordinator data exists, preserve the last device list and log device permission-denied failures at debug level.

## Local Work Done

- Added `devices` to the coordinator permission-denied debug policy.
- Removed the older index-based optional endpoint rule in favor of explicit endpoint names.
- Added a regression test for `Devices.Device.guest` permission-denied behavior after prior data exists.

## Verification

- Targeted tests:
  `PYTHONPATH=. uv run --with aiohttp --with voluptuous --with pytest --with pytest-asyncio pytest test/test_coordinator_entities.py::test_coordinator_logs_device_permission_denied_at_debug test/test_coordinator_entities.py::test_coordinator_logs_optional_permission_denied_at_debug`
- Full test suite:
  `PYTHONPATH=. uv run --with aiohttp --with voluptuous --with pytest --with pytest-asyncio pytest`
- CI matrix local checks:
  `PYTHONPATH=. uv run --python 3.13 --with aiohttp --with voluptuous --with pytest --with pytest-asyncio pytest`
  `PYTHONPATH=. uv run --python 3.12 --with aiohttp --with voluptuous --with pytest --with pytest-asyncio pytest`
- Result: 34 passed on Python 3.14.2, 3.13.12, and 3.12.13.

## Risks And Unknowns

- The exact router still cannot be reproduced locally because the available live router firmware differs from the reporter's `V10.C.25.08.15`.
- If all device discovery endpoints are denied on first setup, setup still fails. That is intentional for now because the config flow uses `get_devices()` as connection validation.

## Public Actions

No public GitHub actions were taken in this run. Commenting, labeling, closing, release work, and PR actions still require explicit human approval.
