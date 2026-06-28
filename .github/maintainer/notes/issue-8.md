# ISSUE:8 - Partial update failure for endpoint index 3 and index 5

URL: https://github.com/adrighem/ha-kpn-experia-v10/issues/8

Reporter: `rason92`

Created: 2026-06-26T21:57:10Z

## Intent

The reporter wants repeated "Partial update failure" warnings removed for non-fatal router permission denials. The integration continues to function for most sensors.

## Environment

- Home Assistant: 2026.6.4
- Integration: 3.2.1
- Router: KPN Experia Box V10
- Firmware: V10.C.25.08.15

## Observed Signal

- `NeMo.Intf.eth0` returns router application error `13`, `Permission denied`.
- `NMC.Wifi` returns router application error `13`, `Permission denied`.
- These map to coordinator optional endpoint indexes 3 and 5.

## Decision

Priority: high for patch release. The issue creates warning spam every polling interval but does not block core integration use.

Action: implemented a local fix that classifies router error `13` as permission denied and logs optional endpoint permission denials at debug level.

## Verification

- Added API test for permission-denied classification without context clearing.
- Added coordinator test proving optional permission-denied failures do not emit "Partial update failure" warnings.
- Full local pytest suite passes.
- Local live router probe did not reproduce the permission-denied responses because the available router runs firmware `V10.C.26.02.06` and returned traffic/Wi-Fi status successfully.
- Live-style coordinator probe with live core router data plus injected optional permission-denied failures completed with zero warning logs and debug records for traffic counters and Wi-Fi status.

## Public Action Status

Owner comment posted on 2026-06-28T18:04:23Z. `v3.2.2` closed the issue on 2026-06-28T18:11:50Z.

## 2026-06-28 Follow-up

After updating to `3.2.2`, the reporter confirmed the original endpoint warnings were reduced but posted a new repeated warning:

- `Devices.Device.guest` returns router application error `13`, `Permission denied`.

Decision: keep device discovery permission denials fatal on first load, because config setup currently validates through device discovery. During later coordinator refreshes, reuse the previous device list and log device permission denials at debug level to avoid warning spam.

Verification:

- Added coordinator regression test for `Devices.Device.guest` permission-denied logging after existing data is available.
- Full local pytest suite passes.

Public action needed: after this follow-up fix is released, consider a short response on `ISSUE:8` acknowledging the extra endpoint and asking the reporter to update again.
