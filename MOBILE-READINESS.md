# Mobile Readiness Report: winchestergrill.com

**Overall: A** — Fast, readable and thumb-friendly on a phone; nothing left on the punch list.

Audited 2026-11-21 against https://winchestergrill.com (home) and https://winchestergrill.com/menu.html. Static analysis plus a browser pass at 375×812 and 320×640 to measure rendered tap targets, text sizes, overflow and what loads when. Not a real-device test.

## Grades

| Category | Grade | Summary |
|---|---|---|
| Viewport & Layout | A | Correct viewport; no horizontal scroll at 375px or 320px |
| Tap Targets | A | Every button and call link measures 43×44px or larger |
| Typography | A | 16px Lora body; no text under 12px |
| Forms | N/A | No forms by design — every contact path is a phone link |
| Performance | A | Home ~116KB to first screen, ~307KB before scrolling |
| Navigation & Interaction | A | Sticky Call bar on both pages; readable without JavaScript |

## Punch List

Nothing open. Everything this audit found was fixed the same day:

- **Performance — below-the-fold photos.** The take-and-bake band and the story photo (222KB together) used to download with the page. They now load only as a visitor scrolls toward them, and the first hero photo is preloaded so the opening screen paints sooner. A phone that never scrolls fetches about 307KB; scrolling the whole home page brings it to about 765KB. The menu page is about 460KB.
- **Tap targets.** Review-carousel arrows were squeezed to 34px wide on phones; now a fixed 48×48. The phone number in the Visit section and the logo link in the nav were 18–20px tall; both are now 44px or taller.
- **Typography.** Small uppercase labels raised from 11.5–11.8px to 12px. The "Most Loved" stamp on the menu went from 9px to 12px and sits on its own line under the dish name on phones, so the name and price stay on one row.

## What's solid

- Call paths are impossible to miss: 56px full-width buttons in the hero, a sticky Call bar on both pages, and a tappable number in the nav, billboard, Visit section and footer.
- No horizontal scrolling at any phone width tested; zoom is not blocked.
- Every photo is WebP with explicit dimensions; nothing below the first screen loads until it is needed; no render-blocking scripts.
- If JavaScript fails, the whole page is still readable, the photos still show, and every call link still works.

## Verification

Re-run: `python3 mobile-readiness/scripts/audit.py https://winchestergrill.com` or retest at [pagespeed.web.dev](https://pagespeed.web.dev). A thumb test on a real phone is still worth thirty seconds.
