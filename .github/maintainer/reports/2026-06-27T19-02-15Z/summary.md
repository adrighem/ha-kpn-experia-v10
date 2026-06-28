# Maintainer Run - 2026-06-27T19:02:15Z

Mode: Maintain -> Ship

Capture method: manual GitHub CLI. The installed open-source-maintainer skill still lacks the optional `references/` and `scripts/` bundle in this environment.

## Snapshot

- Repository: `adrighem/ha-kpn-experia-v10`
- Default branch: `master`
- Open issues: 1
- Open pull requests: 0
- Latest release: `v3.2.1`, published 2026-06-11T17:05:31Z
- Current manifest version: `3.2.1`
- CI signal: recent scheduled hassfest and CodeQL runs on `master` are green

## Top Recommendations

1. Ship the local fix for `ISSUE:8`.
2. After human approval, comment on `ISSUE:8` that permission-denied optional endpoints are now handled without warning spam.
3. Cut a patch release after CI passes on the fix branch, because the issue affects every 30-second polling interval on firmware `V10.C.25.08.15`.

## Issue Analysis

`ISSUE:8` reports repeated coordinator warnings on Home Assistant 2026.6.4, integration `3.2.1`, KPN Experia Box V10 firmware `V10.C.25.08.15`.

Observed failures:

- Endpoint index 3: `NeMo.Intf.eth0` returns router error `13`, `Permission denied`.
- Endpoint index 5: `NMC.Wifi` returns router error `13`, `Permission denied`.

Intent: the reporter says the integration otherwise works and asks to stop the non-fatal repeated log failures.

Decision: treat router error `13` as a distinct permission-denied API error and downgrade optional endpoint permission-denied failures to debug logging in the coordinator. This preserves warning logs for unexpected partial failures and preserves first-run failures for critical data.

## Local Work Done

- Added `ExperiaBoxV10PermissionDeniedError` for router application error `13`.
- Avoid clearing the login context when an endpoint-specific permission denial occurs.
- Added named partial-update logging in the coordinator.
- Logged optional permission-denied failures from traffic, guest Wi-Fi, and Wi-Fi status endpoints at debug level instead of warning level.
- Added focused tests for API classification and coordinator logging behavior.

## Verification

- Targeted tests:
  `PYTHONPATH=. uv run --with aiohttp --with voluptuous --with pytest --with pytest-asyncio pytest test/test_api.py::test_request_raises_permission_denied_without_clearing_context test/test_coordinator_entities.py::test_coordinator_logs_optional_permission_denied_at_debug`
- Full test suite:
  `PYTHONPATH=. uv run --with aiohttp --with voluptuous --with pytest --with pytest-asyncio pytest`
- Result: 33 passed.
- Live router probe using `KPN_ROUTER_*` environment variables:
  local router firmware `V10.C.26.02.06` returned successfully for traffic counters and Wi-Fi status, so it did not reproduce `ISSUE:8`.
- Live-style coordinator probe:
  live core router data loaded successfully while injected optional permission-denied failures for traffic counters and Wi-Fi status produced 0 warnings and 2 debug records.

## Risks And Unknowns

- The exact router behavior on firmware `V10.C.25.08.15` is still inferred from the issue payload; the local live router runs firmware `V10.C.26.02.06`.
- Downgrading optional permission-denied logs means users will no longer see warnings when traffic counters or Wi-Fi status are unavailable. This is intentional for known optional endpoint denials, but real-device confirmation is still useful.

## Public Actions

No public GitHub actions were taken. Commenting, labeling, closing, release work, and PR actions still require explicit human approval.
