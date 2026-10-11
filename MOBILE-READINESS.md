# Mobile Readiness Report: winchestergrill.com

**Overall: B** — Fast, readable, no layout bugs; tap targets and caching fixed, a few small labels remain.

Audited 2026-10-11 against https://winchestergrill.com (home) and https://winchestergrill.com/menu.html; items 1–5 and 7 below were fixed the same day and re-measured in the browser. Static analysis plus a headless-browser pass at 375×812 (iPhone-size) to measure rendered tap targets, text sizes, and overflow. Not a real-device test.

## Grades

| Category | Grade | Summary |
|---|---|---|
| Viewport & Layout | A | Correct viewport, no horizontal scroll at 375px |
| Tap Targets | B | All measured targets now ≥44px; device check recommended |
| Typography | B | 16px Lora body; a few labels dip under 12px |
| Forms | N/A | No forms by design — every contact path is a phone link |
| Performance | B | First paint ~555KB (one hero photo); photos cached a day |
| Navigation & Interaction | B | Sticky Call bar now on menu page; hamburger needs JS |

## Punch List

Ordered by impact — fix top-down. Items 1–5 and 7 are done (measured at 375px: dots 44×44, footer links 44px tall, chips 44px, menu sticky bar showing with 50px buttons, hero slides 2–3 requested only after the load event, assets cached 24h with ETag revalidation). Items 6 and 8 remain open.

### 1. ✅ FIXED — Navigation — Menu page has no sticky "Call to Order" bar
**Current:** `index.html` has the `.mobile-order` bar (Call + Menu, 50px buttons, safe-area padding) pinned to the bottom on phones. `menu.html` does not. On the page people read longest, the only call buttons are inside the hamburger menu or at the very bottom (`.menu-cta`), roughly 1,400px of scrolling away.
**Fix:** In `ops/build_menu_page.py`, add the same block before `<script>` and the matching CSS (`.mobile-order{…}` plus `@media (max-width:720px){.mobile-order{display:flex} body{padding-bottom:74px}}`), with the second button pointing to `index.html` instead of `menu.html`. Regenerate `menu.html`. Call tracking already tags it as `mobile-bar` — no extra wiring.
**Why it matters:** The site's one job is to make the phone ring; on the menu page the phone number is hidden for the entire read.

### 2. ✅ FIXED — Tap Targets — Review carousel dots are 9×9px
**Current:** `index.html` `.car-dots button{width:9px;height:9px}` — five `role="tab"` buttons at 9px with 10px gaps. Measured 9×9 in the browser. Apple and WCAG both want 44px.
**Fix:** Keep the visual dot but grow the hit area:
```css
.car-dots button{width:44px;height:44px;background:none;position:relative}
.car-dots button::before{content:"";position:absolute;inset:50% auto auto 50%;width:9px;height:9px;transform:translate(-50%,-50%);border-radius:999px;background:rgba(224,169,56,.3);transition:background .2s,transform .2s}
.car-dots button[aria-current="true"]::before{background:var(--gold);transform:translate(-50%,-50%) scale(1.35)}
.car-dots{gap:0}
```
**Why it matters:** A thumb can't land on a 9px dot; people hit the wrong review or nothing.

### 3. ✅ FIXED — Tap Targets — Footer links are 19px tall with 8px gaps
**Current:** `.foot ul{gap:8px}` and `.foot a` are plain inline links; measured 19px tall on both pages (Menu, Pizza, Events & Catering, Facebook, phone number, "← Back to home").
**Fix:** `index.html` and the footer in `ops/build_menu_page.py`:
```css
.foot a{display:inline-block;padding:10px 0;margin:-10px 0}
```
(or `.foot ul{gap:16px}` plus `padding:6px 0` on the links). Target ≥44px row height.
**Why it matters:** The footer phone number is one of the tracked call paths; stacked 19px links mis-tap.

### 4. ✅ FIXED — Tap Targets — Menu section chips are 40px tall
**Current:** `.subnav a{padding:8px 16px;font-size:.82rem}` in `ops/build_menu_page.py` renders 40px-tall pills in the sticky bar (measured).
**Fix:** `padding:10px 16px` → 44px. The bar is already horizontally scrollable, so width is fine.
**Why it matters:** The chips are the primary way to jump around a long menu; 4px short of the guideline is a cheap win.

### 5. ✅ FIXED — Performance — All three hero slides download before first paint
**Current:** `index.html` sets `background-image` on all three `.slide` divs (hero-burger 77KB, hero-pizza 102KB, hero-wings 81KB = 260KB), so the browser fetches all three immediately even though slides 2–3 don't appear for 8 and 16 seconds. With the feature band (86KB) and story photo (136KB) also eager, the home page is ~815KB of first-party bytes — the audit script's 381KB figure counts only `<img>` tags.
**Fix:** Leave slide 1 inline; set slides 2–3 from the script after `load`:
```js
addEventListener('load',()=>{document.querySelectorAll('.slide[data-bg]').forEach(s=>{s.style.backgroundImage='url('+s.dataset.bg+')'})});
```
with `<div class="slide" data-bg="assets/hero-pizza.webp"></div>`. Optionally serve a 750px-wide crop of `story-interior.webp` for phones via a `@media (max-width:720px)` background rule.
**Why it matters:** 81% of visitors are on phones, often on cellular near the lake; ~180KB less before the hero shows.

### 6. Typography — Labels render below 12px
**Current (measured at 375px):** `.tile .tag` and `.feat-label` at `.72rem` = 11.5px; `.ev .when` and the menu `.kicker` at `.74rem` = 11.8px; `.mi-stamp` ("Most Loved") at 9.3px.
**Fix:** `.72rem`/`.74rem` → `.75rem` (12px) in `index.html` and `ops/build_menu_page.py`; `.mi-stamp` font-size up to at least `.7rem` at the mobile breakpoint.
**Why it matters:** These are tracked-uppercase labels, so legibility is already tight; 12px is the floor.

### 7. ✅ FIXED — Performance — Images still on the pre-launch 5-minute cache
**Current:** `server.js` sends `Cache-Control: public, max-age=300` on every asset, with a comment to raise it before launch.
**Fix:** For `/assets/`, `max-age=31536000, immutable` and bump a `?v=` query (the og-image already uses `?v=1`) or the filename when a photo changes.
**Why it matters:** Repeat visitors re-download ~700KB of photos every five minutes instead of using cache.

### 8. Navigation — Content is hidden until JavaScript runs
**Current:** `.fade-up{opacity:0}` is applied unconditionally in `index.html`; every section below the hero only appears once the inline script's IntersectionObserver fires. The hamburger menu is also an `onclick` toggle with no non-JS fallback.
**Fix:** Add `document.documentElement.classList.add('js')` as the first line of the script and scope the rule to `.js .fade-up{opacity:0;…}`. The menu is acceptable as-is because the sticky bar and in-page links cover every destination.
**Why it matters:** One syntax error in the single inline block (or a blocked script) leaves phones showing a hero and a blank dark page.

## What's solid

- No horizontal overflow at 375px on either page; the viewport tag is correct and doesn't block zoom. The audit script's "9 oversize fixed widths" are `max-width` tokens, not real fixed widths.
- The call paths that matter are big: 56px full-width CTAs, 48px hamburger and carousel arrows, 50px sticky bar buttons with safe-area padding on the home page.
- Every `<img>` is WebP with explicit `width`/`height` and `loading="lazy"`; zero render-blocking scripts; fonts use `display=swap`. The menu page comes in around 415KB.
- 16px Lora body with 1.65 line-height, readable on a phone without zooming.

## Verification

After applying fixes, re-run: `python3 mobile-readiness/scripts/audit.py https://winchestergrill.com` or retest at [pagespeed.web.dev](https://pagespeed.web.dev). A real-device check of the carousel dots and menu chips is still recommended before forwarding.
