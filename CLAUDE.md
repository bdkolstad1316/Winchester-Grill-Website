# winchester-grill

## What this is
The website for Winchester Grill, a family bar & grill in Winchester, Idaho — one mile from
Winchester Lake State Park. Static HTML/CSS/JS served by a zero-dependency Node server.
The audience is overwhelmingly mobile (81% of visitors) and the site's single job is to make
the phone ring: there are no forms, and every contact path is a `tel:` link.

## Client
- Name: Eric Frei — Winchester Grill, 317 Nezperce Ave, Winchester, ID 83555, (208) 924-6420
- Contact: ericfrei7475@gmail.com (he texts menu changes; he does not use email at the domain)
- Client material — reports, brand files, photos, menu spreadsheet, correspondence — lives
  in `client/` inside this folder. It is gitignored, so it never reaches GitHub or Railway.
  Keep it that way: nothing from `client/` gets committed or copied into the site.
  Monthly Plausible report pipeline: `client/reports/`.

## Run locally
```
npm start                 # http://localhost:8080   (no dependencies to install)
```
There are no npm dependencies. `server.js` uses only Node builtins, so there's no lockfile
and nothing to `npm ci`.

## Deploy
- GitHub: `bdkolstad1316/Winchester-Grill-Website`, private
- Railway deploys automatically on push to `main` (project "Winchester Grill", ID
  `053ed80b-22f4-4ea7-a1ba-bd933e091654`; the CLI is installed — `railway login` then
  `railway link -p <that id>` to manage it from the terminal)
- Live: https://winchestergrill.com
- DNS, SSL and the registrar are all Cloudflare, on Brian's account
- `www.winchestergrill.com` 301-redirects to the bare domain, keeping path and query, via a
  Cloudflare Redirect Rule on the zone (added 2026-11-21). The bare domain is canonical.
- `winchesterkitchenandbar.com` (the old domain, also on Brian's Cloudflare) 301-redirects
  here. Don't let it lapse — it still sends real traffic and carries the old SEO equity.

## IMPORTANT: menu.html is generated — never hand-edit it
`menu.html` is written by `ops/build_menu_page.py`. Editing `menu.html` directly means
your changes vanish on the next build.

**The menu lives in `ops/menu.json`.** To change it: edit the JSON, regenerate, commit
`menu.json` + `menu.html`:
```
python3 ops/build_menu_page.py      # writes ./menu.html (system python3; needs Pillow, fails loudly without it)
```
Section names, anchors and prices in `menu.json` are the client's; don't rename or round.

`ops/build_menu_xlsx.py` builds an editable spreadsheet from the same JSON. Eric texts
his menu changes rather than using it, so it's a nice-to-have — run it only when asked:
```
python3 ops/build_menu_xlsx.py      # needs openpyxl (pip3 install --user openpyxl)
```
It writes to `client/menu/` (gitignored). Set `MENU_XLSX_OUT` to write elsewhere.

`server.js` refuses to serve anything under `ops/`, so the generators never reach the
public site.

## Things that are easy to break
- **CSP lives in `server.js`.** It allowlists `plausible.io` (analytics) and
  `static.cloudflareinsights.com` / `cloudflareinsights.com` (Core Web Vitals). Adding any
  third-party script means adding its host there, or it silently fails to load.
- **Inline JS is one block per page** (plus the one-line `<html class="js">` tagger in the
  head of `index.html`, which must stay separate so content isn't hidden if the main block
  fails). A syntax error in the main block kills the carousel, sticky nav, fade-ins, and
  call tracking together, silently — the page still shows, un-animated. Run
  `node --check` on extracted inline scripts before committing. Don't verify with grep;
  grep will happily confirm broken code is "present."
- **An `<img>` with `width`/`height` attributes needs `height:auto` (or an explicit CSS height).**
  Without it the `height` attribute is a fixed pixel height and `aspect-ratio` is ignored.
  That bug made the menu banners 686–900px tall on phones until Nov 2026.
- **Images must stay WebP with explicit `width`/`height`.** Both pages hold an A mobile
  grade (372KB home / 450KB menu). Dropping in a full-size JPEG without dimensions costs
  the grade and reintroduces layout shift.
- **Colours are tokens.** Every colour lives in the `:root` block at the top of each page
  (`index.html` and the generator for `menu.html` — two copies, kept in step by hand). Gold text on cream uses `--gold-ink`, not `--gold`/`--gold-d` (too faint
  there); quiet text on dark uses `--mut-2`. Check contrast (4.5:1) before adding a colour.
- **Accessibility wiring:** each page has a skip link and a `<main id="main">`; the hamburger
  carries `aria-expanded`/`aria-controls="nav-links"`. Keep those ids if the nav is reworked.
- **Design-hook exceptions live in `.impeccable/config.json`.** Brian has confirmed three things
  the impeccable detector dislikes as intentional: the Fraunces italic accent, the scrolling
  gold ticker, and the dashed stitch line on the home-page tiles. Don't "fix" them, and don't
  reintroduce small tracked-caps labels above headings; those were folded into the copy.
- **Favicon set:** `favicon.ico` (root; 16/32/48), `assets/favicon-32.png`, `assets/apple-touch-icon.png`,
  `assets/icon-192.png` / `icon-512.png`, `site.webmanifest`. All generated from a Bevan "W" in
  gold on charcoal; regenerate the whole set together if the mark ever changes.
- **`server.js` answers GET and HEAD only** (anything else is a 405), compares blocked names
  case-insensitively, refuses `ops/` and `client/`, and wraps every request so a hostile URL
  (bad `%`-escape, `%00`) is a 404 instead of a crash. If a feature ever needs POST, that
  method check is the first thing to change.
- **Only extensions listed in `TYPES` (server.js) are served; everything else is a 404.**
  Adding a new asset type (fonts, video…) means adding its MIME type there, or it 404s.
- **Photos under `assets/` are cached for a day** (`Cache-Control: max-age=86400` plus an
  ETag so browsers/Cloudflare revalidate). Swapping a photo under the same filename shows
  up within 24h on its own; to force it sooner, change the filename or bump a `?v=`.
  HTML is `no-cache`, so menu and price edits are live on the next load.
- **`Content-Length` must be sent on every response.** Apple's iMessage link-preview
  crawler requires it; without it the share card degrades to a grey box.
- Phone-call tracking fires `plausible('Call', {props:{location:…}})` from a delegated
  listener on every `tel:` link. Adding a call button anywhere needs no extra wiring.

## Rules for Claude
- Pull before editing. Brian may have committed through GitHub Desktop.
- Don't push to `main` without asking. A push is a deploy to a live client site. Once Brian
  says push, do it from the shell (`git push origin main` — the `gh` CLI is logged in, so
  he doesn't need GitHub Desktop), then verify the live deploy.
- Keep dependencies at zero unless there's a real reason; that's why this thing is fast.
- Redesign work goes on a branch, not a `v2/` folder.
- Brand: Bevan (display), Lora (body), Fraunces italic (accent); gold `#E0A938`,
  charcoal `#15110D`, cream `#F8F1E4`. Menu prices are the client's — never invent or
  "correct" one. "Motherlode" and "Nezperce" are both intentional; leave them alone.
