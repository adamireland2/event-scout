# Event Scout — AI-powered event finder

Two installable web apps (PWAs) that use Claude AI with live web search to
find in-person events where tax incentive clients will be:

| Edition | Path | Focus |
|---|---|---|
| 🏙️ **Event Scout CRE** | [`cre/`](cre/) | Commercial real estate, construction, 179D |
| 🏡 **Event Scout Residential** | [`residential/`](residential/) | Homebuilders, multifamily, investors, 45L |

The root [`index.html`](index.html) is a chooser page linking to both.
Each edition installs as its own app with its own icon, theme, saved
search history, and AI instructions.

Live (once GitHub Pages is enabled on this repo):
`https://adamireland2.github.io/event-scout/`

## Keeping costs low

- **Budget mode** (default, in Settings): uses Claude Haiku and fewer web
  searches — roughly $0.03–0.10 per search instead of $0.10–0.40.
- **Search history** (🕘 button): the last 10 searches are saved on-device
  and free to reopen; the most recent results auto-restore on launch.
- **Demo mode**: add `?demo=1` to either app's address to browse sample
  data with no API key and no cost.

## Editing the apps

- `cre/index.html` is the **source of truth** for the app code.
- `residential/index.html` is **generated** — don't edit it by hand. After
  changing the CRE app, regenerate with:

  ```
  python3 tools/generate_residential.py
  ```

  The residential branding, colors, AI instructions, categories, and demo
  data live inside `tools/generate_residential.py`.
- Residential icons are generated from `icons/` with
  `python3 tools/generate_residential_icons.py` (requires `pip install pillow`).

## Google Play Store

Everything prepared for the store — screenshots, feature graphics, listing
text, and a beginner-friendly step-by-step guide — is in
[`play-store/`](play-store/). Start with
[`play-store/PLAY_STORE_GUIDE.md`](play-store/PLAY_STORE_GUIDE.md).
