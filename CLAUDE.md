# winchester-grill

## What this is
The website for Winchester Grill, a family bar & grill in Winchester, Idaho — one mile from
Winchester Lake State Park. Static HTML/CSS/JS served by a zero-dependency Node server.
The audience is overwhelmingly mobile (81% of visitors) and the site's single job is to make
the phone ring: there are no forms, and every contact path is a `tel:` link.

## Client
- Name: Eric Frei — Winchester Grill, 317 Nezperce Ave, Winchester, ID 83555, (208) 924-6420
- Contact: ericfrei7475@gmail.com (he texts menu changes; he does not use email at the domain)
- Deliverables — reports, brand files, photos, menu spreadsheet, correspondence — live in
  `~/Documents/Claude/Projects/Winchester Grill/` (Cowork). **Not in this repo.**

## Run locally
```
npm start                 # http://localhost:8080   (no dependencies to install)
COMING_SOON=false npm start   # force the real site instead of the holding page
```
There are no npm dependencies. `server.js` uses only Node builtins, so there's no lockfile
and nothing to `npm ci`.

## Deploy
- GitHub: `bdkolstad1316/Winchester-Grill-Website`, private
- Railway deploys automatically on push to `main`
- Live: https://winchestergrill.com
- DNS, SSL and the registrar are all Cloudflare, on Brian's account
- `winchesterkitchenandbar.com` (the old domain, also on Brian's Cloudflare) 301-redirects
  here. Don't let it lapse — it still sends real traffic and carries the old SEO equity.

## IMPORTANT: menu.html is generated — never hand-edit it
`menu.html` is written by `build_menu_page.py` (currently in the Cowork folder at
`Winchester Grill/ops/build_menu_page.py`; moving into this repo). Editing `menu.html`
directly means your changes vanish on the next build.

To change the menu: edit the `FOOD` / `PIZZA` / `KIDS` data in the generator, run it, then
commit the regenerated `menu.html`.

The same menu data is **duplicated** in `build_menu_xlsx.py`, which builds Eric's editable
spreadsheet. Both must be updated together or the website and his spreadsheet drift apart.
Extracting this to a single `menu.json` both scripts read is the next planned cleanup.

## Things that are easy to break
- **CSP lives in `server.js`.** It allowlists `plausible.io` (analytics) and
  `static.cloudflareinsights.com` / `cloudflareinsights.com` (Core Web Vitals). Adding any
  third-party script means adding its host there, or it silently fails to load.
- **Inline JS is one block per page.** A syntax error kills the whole block — carousel,
  sticky nav, fade-ins, and call tracking all die together, silently. Run
  `node --check` on extracted inline scripts before committing. Don't verify with grep;
  grep will happily confirm broken code is "present."
- **Images must stay WebP with explicit `width`/`height`.** Both pages hold an A mobile
  grade (372KB home / 450KB menu). Dropping in a full-size JPEG without dimensions costs
  the grade and reintroduces layout shift.
- **`Content-Length` must be sent on every response.** Apple's iMessage link-preview
  crawler requires it; without it the share card degrades to a grey box.
- Phone-call tracking fires `plausible('Call', {props:{location:…}})` from a delegated
  listener on every `tel:` link. Adding a call button anywhere needs no extra wiring.

## Rules for Claude
- Pull before editing. Brian commits through GitHub Desktop and may have changed things.
- Don't push to `main` without asking. A push is a deploy to a live client site.
- Keep dependencies at zero unless there's a real reason; that's why this thing is fast.
- Redesign work goes on a branch, not a `v2/` folder.
- Brand: Bevan (display), Lora (body), Fraunces italic (accent); gold `#E0A938`,
  charcoal `#15110D`, cream `#F8F1E4`. Menu prices are the client's — never invent or
  "correct" one. "Motherlode" and "Nezperce" are both intentional; leave them alone.
