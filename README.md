# Poimandres Theme

Faithful [Zed](https://zed.dev) port of [drcmda/poimandres-theme](https://github.com/drcmda/poimandres-theme) (both **Poimandres** and **Poimandres Storm**, in **Unbordered** and **Bordered** variants) packaged in a single `themes/poimandres.json` file, with harmonized Poimandres git colors + 65%-blended gutter bars, clean borderless file selection, and a pure white `#ffffff` cursor.

## Variants

- **Poimandres** — Unbordered (`#1b1e28` seamless)
- **Poimandres Bordered** — Bordered (`#161922` shell → `#1b1e28` editor)
- **Poimandres Storm** — Unbordered (`#252b37` seamless)
- **Poimandres Storm Bordered** — Bordered (`#1f2530` shell → `#252b37` editor)

## Install locally

1. In Zed, open the command palette and run `zed: install dev extension`.
2. Select this folder.
3. Run `theme selector: toggle` and pick any `Poimandres` variant.

Or copy `themes/poimandres.json` into `~/.config/zed/themes/`.

## Regenerating

```bash
python3 scripts/build.py
```
