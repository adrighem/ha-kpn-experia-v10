# Maintainer Decisions

## 2026-06-27 - Handle optional endpoint permission denials

- `ISSUE:8` reports repeated warning logs on firmware `V10.C.25.08.15` when optional endpoints `NeMo.Intf.eth0` and `NMC.Wifi` return router error `13`, `Permission denied`.
- Decided to classify router error `13` as a distinct permission-denied API error.
- Decided optional permission-denied failures should be debug-level coordinator logs, not warnings, because core data can still update and warning spam repeats every polling interval.
- Kept unexpected partial failures at warning level and critical first-run failures as hard update failures.

## 2026-06-11 - Establish maintainer baseline

- Captured GitHub backlog manually because the skill's triage script is unavailable locally.
- Confirmed there are no open issues and no open pull requests.
- Recorded `ISSUE:4` as recently resolved by `PR:5`.
- Updated the current branch manifest version from `3.1.1` to `3.2.0` to avoid regressing the already-published release version if this branch is merged later.
