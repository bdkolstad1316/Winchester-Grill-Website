# Mobile Readiness Report: winchestergrill.com

**Overall: B** — Fast, readable, thumb-friendly; only page weight on the home page keeps it from an A.

Audited 2026-11-21 against https://winchestergrill.com (home) and https://winchestergrill.com/menu.html. Static analysis plus a browser pass at 375×812 and 320×640 to measure rendered tap targets, text sizes and overflow. Not a real-device test. Grades reflect the fixes made during this audit, which go live with the next deploy.

## Grades

| Category | Grade | Summary |
|---|---|---|
| Viewport & Layout | A | Correct viewport; no horizontal scroll at 375px or 320px |
| Tap Targets | A | Every button and call link measures 43×44px or larger |
| Typography | A | 16px Lora body; all labels now 12px or larger |
| Forms | N/A | No forms by design — every contact path is a phone link |
| Performance | B | Home ~420KB before load, ~640KB all-in; menu ~460KB |
| Navigation & Interaction | A | Sticky Call bar on both pages; readable without JavaScript |

## Punch List

Ordered by impact — fix top-down.

### 1. Performance — Two below-the-fold photos load immediately on the home page
**Current:** `index.html` sets `background-image` inline on `.feature` (`cooked-pepperoni.webp`, 86KB) and `.story-img` (`story-interior.webp`, 136KB). Both sit well below the first screen but download before the page finishes loading — 222KB of the 420KB a phone fetches up front.
**Fix:** Give them the same treatment as hero slides 2–3: move the URL to `data-bg` and let the existing `load` handler in the inline script attach it (`document.querySelectorAll('[data-bg]')` instead of `.slide[data-bg]`). Optionally serve a 750px-wide `story-interior` for phones.
**Why it matters:** Cuts what a phone downloads before the page is usable roughly in half, which is felt on campground cellular.

### 2. Typography — The "Most Loved" stamp renders at 9.3px
**Current:** `.mi-stamp` in `ops/build_menu_page.py` (the inked stamp beside Banana Cream Pie on the menu).
**Fix:** Raise its `font-size` to `.75rem` inside the `@media (max-width:820px)` block.
**Why it matters:** It is decoration rather than information, so this is cosmetic — but it is the one piece of text on the site under 12px.

## Fixed during this audit

- Review-carousel arrows were being squeezed to 34px wide on phones; now a fixed 48×48 (dots stay 43×44 at 375px, 32×44 on a 320px screen).
- The phone number in the Visit section and the logo link in the nav were 18–20px tall; both are now 44px or taller.
- Small uppercase labels (`.tile .tag`, `.ev .when`, the menu `.kicker` and `.feat-label`) raised from 11.5–11.8px to 12px.

## What's solid

- Call paths are impossible to miss: 56px full-width buttons in the hero, a sticky Call bar on both pages, and a tappable number in the nav, billboard, Visit section and footer.
- No horizontal scrolling at any phone width tested; zoom is not blocked.
- Every photo is WebP with explicit dimensions and lazy loading; no render-blocking scripts; only one hero photo loads before the page is ready.
- If JavaScript fails, the whole page is still readable and every call link still works.

## Verification

After applying fixes, re-run: `python3 mobile-readiness/scripts/audit.py https://winchestergrill.com` or retest at [pagespeed.web.dev](https://pagespeed.web.dev). A thumb test on a real phone is still worth thirty seconds.
