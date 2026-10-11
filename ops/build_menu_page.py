#!/usr/bin/env python3
"""Generate SEO-friendly menu.html for winchestergrill-site from verified menu data."""
import json, html, os

# Repo root (this file lives in <repo>/ops/). Override with SITE_DIR=... if needed.
SITE_DIR   = os.environ.get("SITE_DIR") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(SITE_DIR, "assets")

# Featured real-photo per menu section: anchor -> (image_file, eyebrow, dish, tagline).
# Rendered as a hero banner at the top of that section — but ONLY if the image file
# actually exists in assets/, so a missing photo never ships a broken image.
FEATURES = {
    "sandwiches": ("featured-cuban.webp", "House Favorite", "The Cuban",
                   "Grilled ham, Swiss, pickles & mustard — with tots"),
    "desserts": ("featured-brownie.webp", "Best Seller", "Brownie Delight",
                 "Warm brownie, ice cream & chocolate drizzle"),
    "burgers": ("featured-local-mac.webp", "House-Made", "The Local Mac",
                "House-made mac & cheese and smoked bacon"),
    "entrees": ("featured-bite-size-steak.webp", "Cut to Order", "Bite Size Steak",
                "Fresh mashed, garlic toast, soup or salad", "16 / 9"),
}

# (Section, anchor, note, [(name, desc, price)])
FOOD = [
 ("Sides & Shareables", "sides",
  "Wing sauces: Nashville Hot, Umami, Honey Sriracha, Buffalo, Garlic Parm, BBQ, Korean BBQ, or Naked. Extra sauce $1.", [
  ("Famous Bone-In Wings", "Choice of sauce", 17.99),
  ("Boneless Wings", "Choice of sauce", 14.99),
  ("Super Nachos", "Chicken or beef, onions, tomato, olives, cheese, sour cream, salsa. Jalapenos & guacamole on request.", 17.99),
  ("Chili Cheese Fries", "", 9.99),
  ("Cup of Soup", "", 4.99),
  ("Bowl of Soup w/ Toast", "", 7.99),
  ("Deep Fried Pickles", "With ranch", 9.99),
  ("Stuffed Tater Kegs", "", 11.99),
  ("Mozzarella Moons", "With marinara", 9.99),
  ("Giant Soft Pretzel", "With brew pub mustard", 9.99),
  ("Chicken Quesadilla", "With sour cream and salsa", 9.99),
  ("Fried Mushrooms", "", 9.99),
  ("Onion Rings", "", 13.99),
  ("Basket of Bacon", "", 13.99),
  ("Fries / Tater Tots", "", 7.99),
  ("House-Made Potato Chips", "With ranch", 5.99),
  ("Pork Rinds", "", 7.99),
  ("Bowl of Mac & Cheese", "", 5.99),
 ]),
 ("Fresh Made Salads", "salads", "", [
  ("Chef Salad", "Ham, turkey, cheese, egg, tomatoes, olives, on mixed greens", 15.99),
  ("Taco Salad", "Seasoned beef, mixed greens, tomato, cheese, onion, olives, tortilla chips, sour cream, salsa", 14.99),
  ("Cobb Salad", "Chicken, bacon, tomatoes, blue cheese crumbles, egg, on mixed greens", 14.99),
  ("Buffalo Chicken Salad", "Buffalo chicken, tomato, olives, onions, cheese, bacon, on mixed greens", 14.99),
 ]),
 ("Crafted Burgers", "burgers",
  "1/3 lb beef. Make it a double for $3. Choice of fries, tater tots, house-made potato chips, or house-made side salad. "
  "Upgrade your side: Onion Rings, Fried Pickles, Pork Rinds, or Fried Mushrooms +$1.99 · Mac & Cheese +$2.49 · Cup of Soup +$1.99.", [
  ("Idaho Classic", "Pickles, lettuce, tomato, onion, cheddar, ketchup, mustard. Add bacon $2", 14.49),
  ("The Winchester", "Cheddar, bacon, onion rings, BBQ sauce", 16.99),
  ("The Local Mac", "House-made mac & cheese and smoked bacon", 16.99),
  ("Chili Cheese Burger", "Steak chili, cheese, diced onions", 16.99),
  ("Mushroom & Swiss", "Bacon, sauteed mushrooms, Swiss cheese, mayo", 16.99),
  ("Black and Blue Burger", "Blue cheese crumble, lettuce, tomato", 14.99),
  ("Jalapeno Burger", "Bacon, pepper jack cheese, and mayo", 15.99),
  ("Peanut Butter Burger", "Peanut butter, bacon and pickles", 15.99),
  ("The Motherlode", "Double prime rib beef patty, bacon, fried egg, grilled onions, lettuce, tomato, mayo", 18.99),
  ("Chicken Cordon Burger", "Fried chicken breast, ham, Swiss cheese, mayo, lettuce and tomato", 14.99),
  ("Spicy Chicken Burger", "Chicken breast, bacon, jalapeno, pepper jack, lettuce and tomato", 15.99),
  ("Reuben Burger", "Corned beef, sauerkraut, Swiss cheese and 1000 island dressing", 16.99),
 ]),
 ("Sandwiches & Wraps", "sandwiches",
  "Choice of fries, tater tots, house-made potato chips, or house-made side salad. Same side upgrades as burgers.", [
  ("The PDQ", "Grilled cheese sandwich with a cup of the soup of the day", 7.99),
  ("Winchester BLT", "", 11.99),
  ("French Dip Sandwich", "Swiss, grilled onions, mushrooms", 15.99),
  ("Philly Cheese Steak Sandwich", "Peppers, onions, Swiss cheese", 15.99),
  ("Patty Melt", "Patty, grilled onions, Swiss cheese, on marbled rye", 13.99),
  ("Cuban Sandwich", "Grilled ham, Swiss, pickles and mustard sauce", 14.99),
  ("Classic Club", "Hope you're hungry — it's big!", 15.99),
  ("Grilled Ham & Cheese", "", 11.99),
  ("Grilled Turkey & Swiss", "", 11.99),
  ("Reuben Sandwich", "Corned beef, sauerkraut, Swiss cheese, 1000 island, on marbled rye", 13.99),
  ("Chicken Wrap", "Chicken, bacon, cheese, lettuce, tomato, ranch", 12.99),
  ("Buffalo Chicken Wrap", "Buffalo chicken, bacon, lettuce, tomato, cheese, ranch", 12.99),
  ("Chicken Caesar Wrap", "Chicken, lettuce, parmesan, Caesar dressing", 11.99),
  ("Pulled Pork Sandwich", "Smoked pulled pork, BBQ sauce, pickles", 12.99),
  ("Fish Sandwich", "Cheddar cheese, lettuce and tartar sauce", 15.99),
 ]),
 ("Entrees", "entrees", "", [
  ("Pulled Pork Mac and Cheese", "", 13.99),
  ("Chicken Bacon Ranch Mac & Cheese", "", 12.99),
  ("Chicken & Cilantro Lime Rice Bowl", "", 14.99),
  ("Orange Chicken Rice Bowl", "", 14.99),
  ("Chicken Strip Basket", "With choice of side", 13.99),
  ("Shrimp Basket", "Grilled or breaded shrimp", 14.99),
  ("Fish and Chips", "", 15.99),
  ("Finger Steak Basket", "", 13.99),
  ("12 oz Bite Size Steak", "Fresh made mashed, garlic toast, choice of soup or salad. Add 5 grilled shrimp $9", "Market Price"),
  ("6 oz Bite Size Steak", "Fresh made mashed, garlic toast, choice of soup or salad. Add 5 grilled shrimp $9", "Market Price"),
  ("Chicken Fried Steak", "Fresh made mashed, white gravy, garlic toast, choice of soup or salad", 19.99),
  ("Grilled New York Steak", "16 oz New York, fresh made mashed, garlic toast, choice of soup or salad. Add 5 grilled shrimp $9", "Market Price"),
 ]),
 ("Desserts", "desserts", "", [
  ("Brownie Delight", "With ice cream and chocolate drizzle", 5.99),
  ("Raspberry Cheesecake", "", 6.99),
  ("Banana Cream Pie", "", 6.99),
  ("Bowl of Ice Cream", "Vanilla or Huckleberry", 3.99),
 ]),
]

PIZZA = [
 ("Regular Pizza", 13.99, 22.00, [
  ("Cheese", ""), ("Pepperoni", ""),
  ("Hawaiian", "Cheese, Canadian bacon, and pineapple"),
  ("Meat Lovers", "Pepperoni, Canadian bacon, sausage, and cheese"),
  ("Vegetarian", "Cheese, mushrooms, olives, green peppers, and onions"),
  ("Parmesan Garlic Chicken w/ Bacon", ""),
  ("BBQ Chicken", "BBQ sauce, cheese, chicken"),
  ("Chicken Bacon Ranch", ""),
  ("Husky", "Mustard sauce, cheese, pepperoni, and pineapple"),
  ("Buffalo Chicken", "Frank's RedHot buffalo sauce, cheese, chicken"),
 ]),
 ("Specialty Pizza", 15.99, 24.99, [
  ("Supreme", "Cheese, Canadian bacon, sausage, pepperoni, mushrooms, olives, onions, green peppers"),
  ("Korean Chicken", "Gochujang sauce, cheese, bell peppers, green onions, crispy chicken"),
  ("Shotgun", "Mustard sauce, Swiss polish sausage, onions, and sauerkraut"),
  ("Taco Pizza", "Cheese, taco meat, tomatoes, olives, green onion, and lettuce"),
 ]),
]

KIDS = [
 ("Kids Meals", "12 & under — served with fries or tots", [
  ("2 Burger Sliders", "", 6.99),
  ("Chicken Tenders", "", 6.99),
  ("Grilled Cheese Sandwich", "", 4.99),
  ("Peanut Butter & Jelly Sandwich", "", 4.99),
  ("Mac & Cheese", "", 4.99),
 ]),
 ("Kids Drinks", "", [
  ("Soda", "", 2.99),
  ("Apple Juice", "", 2.50),
  ("Milk", "", 2.49),
  ("Chocolate Milk", "", 2.99),
 ]),
]

e = lambda s: html.escape(s, quote=True)

# ---------- JSON-LD ----------
sections_ld = []
for name, anchor, note, items in FOOD:
    mi = []
    for nm, desc, price in items:
        item = {"@type": "MenuItem", "name": nm}
        if isinstance(price, (int, float)):
            item["offers"] = {"@type": "Offer", "price": f"{price:.2f}", "priceCurrency": "USD"}
        if desc: item["description"] = desc
        mi.append(item)
    sec = {"@type": "MenuSection", "name": name, "hasMenuItem": mi}
    if note: sec["description"] = note
    sections_ld.append(sec)
for name, p12, p16, pies in PIZZA:
    mi = []
    for nm, desc in pies:
        item = {"@type": "MenuItem", "name": nm, "offers": [
            {"@type": "Offer", "price": f"{p12:.2f}", "priceCurrency": "USD", "name": "12 inch"},
            {"@type": "Offer", "price": f"{p16:.2f}", "priceCurrency": "USD", "name": "16 inch"}]}
        if desc: item["description"] = desc
        mi.append(item)
    sections_ld.append({"@type": "MenuSection", "name": name, "hasMenuItem": mi})
for name, note, items in KIDS:
    mi = []
    for nm, desc, price in items:
        item = {"@type": "MenuItem", "name": nm}
        if isinstance(price, (int, float)):
            item["offers"] = {"@type": "Offer", "price": f"{price:.2f}", "priceCurrency": "USD"}
        if desc: item["description"] = desc
        mi.append(item)
    sec = {"@type": "MenuSection", "name": name, "hasMenuItem": mi}
    if note: sec["description"] = note
    sections_ld.append(sec)

menu_ld = {"@context": "https://schema.org", "@type": "Menu",
           "name": "Winchester Grill Menu",
           "inLanguage": "en-US", "hasMenuSection": sections_ld}
ld_json = json.dumps(menu_ld, indent=2)

# ---------- section chips ----------
chips = "".join(f'<a href="#{a}">{e(n)}</a>' for n, a, _, _ in FOOD)
chips += '<a href="#pizza">Pizza</a>'
chips += '<a href="#kids">Kids</a>'

# ---------- food sections ----------
# Items that get an inked "stamp" beside the name. Add any dish here to flag it.
# The stamp animates once when scrolled into view (see .mi-stamp CSS + observer).
STAMPS = {
    "Banana Cream Pie": "Most Loved",
}

def item_row(nm, desc, price):
    d = f'<p class="mi-desc">{e(desc)}</p>' if desc else ''
    price_html = f'${price:.2f}' if isinstance(price, (int, float)) else e(price)
    stamp = (f'<span class="mi-stamp">{e(STAMPS[nm])}</span>'
             if nm in STAMPS else '')
    return (f'<div class="mi">'
            f'<div class="mi-top"><span class="mi-name">{e(nm)}</span>{stamp}'
            f'<span class="mi-dots"></span><span class="mi-price">{price_html}</span></div>{d}</div>')

def feature_html(anchor):
    f = FEATURES.get(anchor)
    if not f:
        return ''
    fn, label, dish, tag = f[0], f[1], f[2], f[3]
    aspect = f[4] if len(f) > 4 else None  # optional per-feature aspect (default 7:3 in CSS)
    if not os.path.exists(os.path.join(ASSETS_DIR, fn)):
        return ''  # graceful skip until the real photo is dropped in
    style = f' style="aspect-ratio:{aspect}"' if aspect else ''
    # Intrinsic width/height stop the page shifting while the banner loads.
    dims = ''
    try:
        from PIL import Image
        with Image.open(os.path.join(ASSETS_DIR, fn)) as _im:
            dims = f' width="{_im.size[0]}" height="{_im.size[1]}"'
    except Exception:
        pass
    return (f'<figure class="menu-feature">'
            f'<img src="assets/{fn}" alt="{e(dish)} — {e(tag)}" loading="lazy" decoding="async"{dims}{style}>'
            f'<figcaption><span class="feat-label">{e(label)}</span>'
            f'<span class="feat-name">{e(dish)}</span>'
            f'<span class="feat-tag">{e(tag)}</span></figcaption></figure>')

food_html = ""
for name, anchor, note, items in FOOD:
    note_html = f'<p class="sec-note">{e(note)}</p>' if note else ''
    rows = "\n".join(item_row(*it) for it in items)
    food_html += f'''
<section class="menu-sec" id="{anchor}">
  <div class="sec-bar"><h2 class="display">{e(name)}</h2></div>
  {note_html}
  {feature_html(anchor)}
  <div class="mi-grid">
{rows}
  </div>
</section>'''

# ---------- pizza ----------
pizza_groups = ""
for name, p12, p16, pies in PIZZA:
    rows = "\n".join(item_row(nm, desc, p12) if False else
        f'<div class="mi"><div class="mi-top"><span class="mi-name">{e(nm)}</span>'
        f'<span class="mi-dots"></span></div>'
        + (f'<p class="mi-desc">{e(desc)}</p>' if desc else '') + '</div>'
        for nm, desc in pies)
    pizza_groups += f'''
  <div class="pizza-group">
    <div class="pizza-head"><h3 class="display">{e(name)}</h3>
      <span class="pizza-price">12″ ${p12:.2f} &nbsp;·&nbsp; 16″ ${p16:.2f}</span></div>
    <div class="mi-grid">
{rows}
    </div>
  </div>'''

# ---------- kids ----------
kids_groups = ""
for name, note, items in KIDS:
    note_html = f'<p class="pizza-intro">{e(note)}</p>' if note else ''
    rows = "\n".join(item_row(*it) for it in items)
    kids_groups += f'''
  <div class="pizza-group">
    <div class="pizza-head"><h3 class="display">{e(name)}</h3></div>
    {note_html}
    <div class="mi-grid">
{rows}
    </div>
  </div>'''

HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Menu | Winchester Grill — Burgers, Steak, Wings &amp; Pizza in Winchester, Idaho</title>
<meta name="description" content="The full Winchester Grill menu: scratch burgers, hand-cut steak, wings, salads, sandwiches, rice bowls, desserts, and take-and-bake pizza. Winchester, Idaho. (208) 924-6420.">
<link rel="canonical" href="https://winchestergrill.com/menu.html">
<meta property="og:type" content="restaurant.menu">
<meta property="og:title" content="Menu | Winchester Grill">
<meta property="og:description" content="Scratch burgers, hand-cut steak, wings, and take-and-bake pizza in Winchester, Idaho.">
<meta property="og:url" content="https://winchestergrill.com/menu.html">
<meta property="og:image" content="https://winchestergrill.com/assets/og-image.jpg?v=1">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://winchestergrill.com/assets/og-image.jpg?v=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bevan&family=Fraunces:ital,opsz,wght@1,9..144,500;1,9..144,600&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&display=swap" rel="stylesheet">
<!-- Privacy-friendly analytics by Plausible -->
<script async src="https://plausible.io/js/pa-_UZvFYMx1dSc_E12NUXJv.js"></script>
<script>
  window.plausible=window.plausible||function(){{(plausible.q=plausible.q||[]).push(arguments)}},plausible.init=plausible.init||function(i){{plausible.o=i||{{}}}};
  plausible.init()
</script>
<script type="application/ld+json">
{ld_json}
</script>
<style>
:root{{--char:#15110D;--char2:#1F1812;--char3:#2A2118;--gold:#E0A938;--gold-d:#B9852A;--ember:#C24A2C;--cream:#F8F1E4;--mut:#C8BBA4;--line:rgba(224,169,56,.26);--max:1180px;--navh:78px;--subh:59px}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{font-family:'Lora',serif;font-size:16px;text-size-adjust:100%;-webkit-text-size-adjust:100%;background:var(--char);color:var(--mut);line-height:1.65;-webkit-tap-highlight-color:rgba(224,169,56,.2);overflow-x:hidden}}
a{{color:inherit}}
.display{{font-family:'Bevan',serif;font-weight:400;text-transform:uppercase;letter-spacing:.01em;line-height:.95}}
.accent{{font-family:'Fraunces',serif;font-style:italic;font-weight:600}}
.kicker{{font-size:.74rem;font-weight:700;letter-spacing:.32em;text-transform:uppercase;color:var(--gold)}}
.wrap{{max-width:var(--max);margin:0 auto;padding:0 26px}}
section{{scroll-margin-top:calc(var(--navh) + var(--subh) + 26px)}}

/* NAV */
nav{{position:fixed;top:0;left:0;right:0;z-index:60;height:var(--navh);display:flex;align-items:center;background:rgba(21,17,13,.96);backdrop-filter:blur(12px);box-shadow:0 1px 0 var(--line)}}
.nav-in{{max-width:var(--max);margin:0 auto;width:100%;display:flex;align-items:center;justify-content:space-between;padding:0 26px}}
.nav-brand{{display:flex;align-items:center;gap:12px;text-decoration:none}}
.nav-brand img{{height:50px;width:auto}}
.nav-brand b{{font-family:'Bevan',serif;color:var(--cream);font-size:1.32rem;letter-spacing:.02em;text-transform:uppercase}}
.nav-brand b span{{color:var(--gold)}}
.links{{display:flex;gap:30px;align-items:center}}
.links a{{color:var(--cream);text-decoration:none;font-weight:600;font-size:.86rem;letter-spacing:.08em;text-transform:uppercase;padding:8px 2px}}
.links a:hover,.links a[aria-current]{{color:var(--gold)}}
.links .order{{display:inline-flex;align-items:center;gap:8px;background:var(--gold);color:var(--char);padding:11px 20px;border-radius:999px;font-weight:700;white-space:nowrap}}
.links .order svg{{width:16px;height:16px;flex:0 0 auto}}
.links .order:hover{{background:var(--cream)}}
.burger{{display:none;background:none;border:none;cursor:pointer;width:48px;height:48px;align-items:center;justify-content:center}}
.burger svg{{stroke:var(--cream)}}

/* HEADER */
.mhead{{padding:calc(var(--navh) + 54px) 26px 40px;text-align:center;background:radial-gradient(ellipse 80% 70% at 50% 0%,rgba(224,169,56,.1),transparent 60%),var(--char)}}
.mhead h1{{color:var(--cream);font-size:clamp(2.6rem,6vw,4.4rem);margin:12px 0 10px}}
.mhead h1 .accent{{color:var(--gold);text-transform:none}}
.mhead p{{max-width:560px;margin:0 auto;font-size:1.05rem}}
.mhead .price-note{{margin-top:10px;font-size:.92rem;color:var(--mut);opacity:.85}}

/* SUBNAV chips */
.subnav{{position:sticky;top:var(--navh);z-index:50;background:rgba(21,17,13,.97);backdrop-filter:blur(10px);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}}
.subnav-in{{max-width:var(--max);margin:0 auto;display:flex;gap:8px;overflow-x:auto;padding:12px 26px;scrollbar-width:none}}
.subnav-in::-webkit-scrollbar{{display:none}}
.subnav a{{flex:0 0 auto;text-decoration:none;color:var(--mut);font-weight:600;font-size:.82rem;letter-spacing:.04em;padding:10px 16px;border:1px solid var(--line);border-radius:999px;white-space:nowrap;transition:background .2s,color .2s}}
.subnav a:hover{{background:var(--gold);color:var(--char);border-color:var(--gold)}}

/* MENU SECTIONS */
.menu-body{{padding:54px 0 90px}}
.menu-sec{{margin-bottom:58px}}
.sec-bar{{border-bottom:2px solid var(--line);padding-bottom:10px;margin-bottom:8px}}
.sec-bar h2{{color:var(--gold);font-size:clamp(1.6rem,3.4vw,2.3rem)}}
.sec-note{{font-family:'Fraunces',serif;font-style:italic;color:var(--mut);font-size:.96rem;margin:10px 0 22px;max-width:760px}}
.menu-feature{{position:relative;border-radius:16px;overflow:hidden;margin:4px 0 32px;border:1px solid var(--line);background:#0C0907}}
.menu-feature img{{width:100%;aspect-ratio:7/3;object-fit:cover;display:block}}
.menu-feature figcaption{{position:absolute;left:0;right:0;bottom:0;padding:22px 26px;background:linear-gradient(transparent,rgba(10,7,5,.92))}}
.menu-feature .feat-label{{display:block;font-size:.72rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:5px}}
.menu-feature .feat-name{{font-family:'Bevan',serif;text-transform:uppercase;color:var(--cream);font-size:clamp(1.5rem,4vw,2.3rem);line-height:1}}
.menu-feature .feat-tag{{display:block;margin-top:6px;font-size:.98rem;color:var(--mut)}}

/* Inked "Most Loved" stamp — thumps down once when the row scrolls into view. */
.mi-stamp{{
  font-family:'Bevan',serif;font-size:.58rem;letter-spacing:.12em;text-transform:uppercase;
  color:var(--gold);border:2px solid var(--gold);border-radius:3px;
  padding:3px 7px 2px;margin-left:2px;flex:0 0 auto;white-space:nowrap;
  transform:rotate(-7deg);opacity:.92;
}}
.mi-stamp.ink{{animation:stamp-thump .5s cubic-bezier(.2,1.5,.4,1) both}}
@keyframes stamp-thump{{
  0%{{transform:rotate(-24deg) scale(2.4);opacity:0}}
  55%{{transform:rotate(-5deg) scale(.94);opacity:1}}
  75%{{transform:rotate(-8deg) scale(1.04)}}
  100%{{transform:rotate(-7deg) scale(1);opacity:.92}}
}}
@media (prefers-reduced-motion:reduce){{
  .mi-stamp.ink{{animation:none}}
}}
.mi-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px 48px;margin-top:18px}}
.mi{{padding:12px 0;border-bottom:1px solid rgba(224,169,56,.1)}}
.mi-top{{display:flex;align-items:baseline;gap:8px}}
.mi-name{{font-weight:700;color:var(--cream);font-size:1.06rem}}
.mi-dots{{flex:1;border-bottom:2px dotted rgba(224,169,56,.3);transform:translateY(-4px)}}
.mi-price{{font-weight:800;color:var(--gold);font-size:1.02rem;white-space:nowrap}}
.mi-desc{{font-size:.9rem;color:var(--mut);margin-top:3px;max-width:54ch}}

/* PIZZA */
.pizza-intro{{font-family:'Fraunces',serif;font-style:italic;color:var(--mut);font-size:.96rem;margin:8px 0 26px;max-width:760px}}
.pizza-group{{margin-bottom:40px}}
.pizza-head{{display:flex;align-items:baseline;justify-content:space-between;gap:16px;flex-wrap:wrap;border-bottom:2px solid var(--line);padding-bottom:10px}}
.pizza-head h3{{color:var(--gold);font-size:clamp(1.4rem,3vw,2rem)}}
.pizza-price{{font-weight:800;color:var(--cream);font-size:1rem;letter-spacing:.02em}}
.topping-note{{font-family:'Fraunces',serif;font-style:italic;color:var(--mut);margin-top:6px}}
.menu-disclaimer{{max-width:760px;margin:54px auto 0;padding-top:22px;border-top:1px solid var(--line);text-align:center;font-size:.82rem;line-height:1.6;color:#9A8C70}}

/* CTA strip */
.menu-cta{{background:var(--gold);color:var(--char);text-align:center;padding:46px 26px}}
.menu-cta h2{{font-size:clamp(1.6rem,3.6vw,2.4rem);margin-bottom:8px}}
.menu-cta p{{color:#5a4420;font-weight:600;margin-bottom:22px}}
.btn{{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:54px;padding:15px 32px;border-radius:999px;font-weight:700;font-size:1rem;letter-spacing:.04em;text-transform:uppercase;text-decoration:none;transition:transform .15s,background .2s}}
.btn:active{{transform:scale(.97)}}
.btn-dark{{background:var(--char);color:var(--cream)}}
.btn-dark:hover{{background:#000}}

/* FOOTER */
footer{{background:#0C0907;border-top:1px solid var(--line);padding:54px 26px 28px}}
.foot{{max-width:var(--max);margin:0 auto;display:flex;justify-content:space-between;gap:30px;flex-wrap:wrap;align-items:center}}
.foot-logotype{{font-family:'Bevan',serif;text-transform:uppercase;color:var(--cream);font-size:1.5rem;letter-spacing:.02em;line-height:1}}
.foot-logotype span{{color:var(--gold)}}
.foot p,.foot a{{font-size:.9rem;color:var(--mut);text-decoration:none}}
.foot p a{{display:inline-block;padding:10px 0;margin:-10px 0}} /* 44px tap height without changing the layout */
.foot a:hover{{color:var(--gold)}}
.legal{{max-width:var(--max);margin:36px auto 0;padding-top:20px;border-top:1px solid rgba(224,169,56,.14);display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:.8rem;color:#7E725D}}
.mocknote{{max-width:var(--max);margin:16px auto 0;font-size:.74rem;color:#5C5343}}

@media (max-width:820px){{
  .mi-grid{{grid-template-columns:1fr;gap:0}}
  .nav-brand b{{font-size:1.15rem}}
}}
@media (max-width:920px){{
  .links{{position:fixed;inset:var(--navh) 0 auto 0;flex-direction:column;gap:0;background:rgba(21,17,13,.98);padding:8px 0 22px;display:none;border-bottom:1px solid var(--line)}}
  .links.open{{display:flex}}
  .links a{{font-size:1.05rem;padding:15px;width:100%;text-align:center}}
  .links .order{{border-radius:0;margin-top:6px;justify-content:center}}
  .burger{{display:flex}}
}}
/* STICKY MOBILE ORDER BAR (same as index.html) */
.mobile-order{{position:fixed;left:0;right:0;bottom:0;z-index:55;display:none;gap:10px;padding:12px 16px calc(12px + env(safe-area-inset-bottom));background:rgba(21,17,13,.96);backdrop-filter:blur(12px);border-top:1px solid var(--line)}}
.mobile-order .btn{{flex:1;min-height:50px;padding:12px 16px;font-size:.9rem}}
.btn-gold{{background:var(--gold);color:var(--char)}}
.btn-gold:hover{{background:var(--cream)}}
.btn-glass{{border:1.5px solid rgba(248,241,228,.55);color:var(--cream);background:rgba(21,17,13,.25)}}
.btn-glass:hover{{border-color:var(--gold);color:var(--gold)}}

@media (max-width:720px){{
  .btn{{width:100%;max-width:340px}}
  .mobile-order{{display:flex}}
  .mobile-order .btn{{max-width:none}}
  body{{padding-bottom:74px}}
}}
</style>
</head>
<body>

<nav id="nav">
  <div class="nav-in">
    <a class="nav-brand" href="index.html">
      <b>Winchester <span>Grill</span></b>
    </a>
    <button class="burger" aria-label="Open menu" onclick="document.querySelector('.links').classList.toggle('open')">
      <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
    <div class="links">
      <a href="menu.html" aria-current="page">Menu</a>
      <a href="index.html#takeandbake">Pizza</a>
      <a href="index.html#story">Our Story</a>
      <a href="index.html#events">Events</a>
      <a href="index.html#visit">Visit</a>
      <a class="order" href="tel:+12089246420"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>(208) 924-6420</a>
    </div>
  </div>
</nav>

<header class="mhead">
  <span class="kicker">Winchester, Idaho · Family Bar &amp; Grill</span>
  <h1 class="display">The <span class="accent">Menu</span></h1>
  <p>Scratch burgers, hand-cut steak, wings, and take-and-bake pizza for the campsite. Everything below is made to order.</p>
  <p class="price-note"><em>Prices are subject to change.</em></p>
</header>

<div class="subnav">
  <div class="subnav-in">{chips}</div>
</div>

<div class="menu-body">
  <div class="wrap">
{food_html}

    <section class="menu-sec" id="pizza">
      <div class="sec-bar"><h2 class="display">Pizza</h2></div>
      <p class="pizza-intro">Regular and specialty pies, available 12″ or 16″ — dine in, or grab a take-and-bake to finish at the lake.</p>
{pizza_groups}
      <p class="topping-note">Add jalapenos, extra cheese, or any other topping for $2 each.</p>
    </section>

    <section class="menu-sec" id="kids">
      <div class="sec-bar"><h2 class="display">Kids Menu</h2></div>
      <p class="pizza-intro">For the 12-and-under crowd. Bring the whole family.</p>
{kids_groups}
    </section>

    <p class="menu-disclaimer">Prices and menu items are subject to change without notice. Items are cooked to order — consuming raw or undercooked meats, poultry, seafood, or eggs may increase your risk of foodborne illness.</p>
  </div>
</div>

<div class="menu-cta">
  <h2 class="display">Ready to order?</h2>
  <p>Call ahead for carry-out or a take-and-bake pizza.</p>
  <a class="btn btn-dark" href="tel:+12089246420">Call (208) 924-6420</a>
</div>

<footer>
  <div class="foot">
    <div class="foot-logotype">Winchester <span>Grill</span></div>
    <p>317 Nezperce Ave, Winchester, ID 83555<br><a href="tel:+12089246420">(208) 924-6420</a></p>
    <p><a href="index.html">← Back to home</a></p>
  </div>
  <div class="legal">
    <span>© 2026 Winchester Grill. All rights reserved.</span>
    <span>winchestergrill.com</span>
  </div>
</footer>

<!-- STICKY MOBILE ORDER BAR -->
<div class="mobile-order">
  <a class="btn btn-gold" href="tel:+12089246420">Call to Order</a>
  <a class="btn btn-glass" href="index.html">Home</a>
</div>

<script>
document.querySelectorAll('.links a').forEach(a=>a.addEventListener('click',()=>document.querySelector('.links').classList.remove('open')));

/* Jump to menu sections with an offset that measures the real sticky-header height,
   so headings never hide under the nav + pill bar regardless of screen or font. */
(function(){{
  var nav=document.getElementById('nav');
  var sub=document.querySelector('.subnav');
  function offset(){{return (nav?nav.offsetHeight:0)+(sub?sub.offsetHeight:0)+16;}}
  document.querySelectorAll('.subnav a[href^="#"]').forEach(function(a){{
    a.addEventListener('click',function(e){{
      var el=document.getElementById(a.getAttribute('href').slice(1));
      if(!el)return;
      e.preventDefault();
      var y=el.getBoundingClientRect().top+window.pageYOffset-offset();
      window.scrollTo({{top:y,behavior:'smooth'}});
      history.replaceState(null,'',a.getAttribute('href'));
    }});
  }});
}})();

/* Stamp the flagged dishes once, as they scroll into view. */
(function(){{
  var stamps=document.querySelectorAll('.mi-stamp');
  if(!stamps.length)return;
  if(!('IntersectionObserver' in window)){{
    stamps.forEach(function(s){{s.classList.add('ink');}});return;
  }}
  var io=new IntersectionObserver(function(entries){{
    entries.forEach(function(en){{
      if(en.isIntersecting){{en.target.classList.add('ink');io.unobserve(en.target);}}
    }});
  }},{{threshold:.9}});
  stamps.forEach(function(s){{io.observe(s);}});
}})();

/* Report taps on any phone link to Plausible as a "Call" goal, tagged with
   which button was used, so we can see what's actually driving orders. */
document.addEventListener('click',function(ev){{
  var a=ev.target.closest?ev.target.closest('a[href^="tel:"]'):null;
  if(!a||typeof window.plausible!=='function')return;
  var sec=a.closest('section');
  var where=a.closest('nav')?'nav':a.closest('.mobile-order')?'mobile-bar'
           :a.closest('footer')?'footer':(sec&&sec.id)||'page';
  window.plausible('Call',{{props:{{location:where}}}});
}});
</script>
</body>
</html>'''

out = os.path.join(SITE_DIR, "menu.html")
with open(out, "w") as f:
    f.write(HTML)

# sanity: counts + JSON validity
n_food = sum(len(s[3]) for s in FOOD)
n_pizza = sum(len(s[3]) for s in PIZZA)
json.loads(ld_json)
print(f"menu.html written. food items={n_food}, pizzas={n_pizza}, sections={len(sections_ld)}")
