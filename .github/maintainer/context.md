# Maintainer Context

Repository: `adrighem/ha-kpn-experia-v10`

Project: Home Assistant custom integration for the KPN Experia Box v10 / ZTE H369A router.

Current priorities:

- Keep HACS and hassfest validation green.
- Preserve local-polling Home Assistant compatibility and stable config-flow behavior.
- Treat router API behavior from real devices as the highest-value bug signal.
- Prefer small, tested fixes over broad rewrites.

Tone and public posture:

- Direct, practical, and appreciative.
- Ask users for logs or firmware/router details only when needed to reproduce.
- Do not post, label, close, or merge without explicit human approval.

Known maintenance constraints:

- The installed open-source-maintainer skill is missing its optional `references/` and `scripts/` files in this environment, so the first run used manual GitHub CLI capture.
- Local working trees may contain router probing scratch files; avoid committing them unless intentionally promoted into tests or documentation.
