#!/usr/bin/env python3
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

RED = "9E2B25"; CREAM = "FAF5EC"; TAN = "C9A86A"; INK = "2B2520"; LIGHT = "F1E8D8"
F = "Arial"
thin = Side(style="thin", color="D9CDB8")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = Workbook()

# ---------- READ ME ----------
ws = wb.active; ws.title = "Read Me"
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 4
ws.column_dimensions["B"].width = 95
ws["B2"] = "Winchester Kitchen & Bar — Menu Workbook"
ws["B2"].font = Font(name=F, size=16, bold=True, color=RED)
lines = [
    "",
    "Hi Eric — this is the full menu as it appears on the website today (June 2026).",
    "",
    "HOW TO USE THIS:",
    "1. Check every PRICE — fix anything that's changed.",
    "2. Check every DESCRIPTION — edit wording right in the cell.",
    "3. Use the STATUS column: Keep / Update / Remove / New (pick from the dropdown).",
    "4. Adding an item? Type it in a blank row at the bottom of its section and set Status to New.",
    "5. Don't worry about making it pretty — we'll handle the design. Just make it accurate.",
    "",
    "Tabs: \"Food Menu\" has everything from the kitchen. \"Pizza Menu\" has the pizzas. \"Kids Menu\" has the 12-and-under items.",
    "",
    "Questions? Brian — brian@kd70.com / (web guy)",
]
r = 3
for t in lines:
    ws.cell(row=r, column=2, value=t).font = Font(name=F, size=11, bold=t.endswith(":"), color=INK)
    r += 1

# ---------- FOOD MENU ----------
food = wb.create_sheet("Food Menu")
food.sheet_view.showGridLines = False
widths = {"A": 22, "B": 30, "C": 62, "D": 10, "E": 12, "F": 34}
for c, w in widths.items(): food.column_dimensions[c].width = w

hdr = ["Section", "Item", "Description", "Price", "Status", "Notes / Changes"]
for i, h in enumerate(hdr, 1):
    cell = food.cell(row=1, column=i, value=h)
    cell.font = Font(name=F, size=11, bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", start_color=INK)
    cell.alignment = Alignment(vertical="center")
food.row_dimensions[1].height = 22
food.freeze_panes = "A2"

MENU = [
 ("SIDES & SHAREABLES", "Sauce options for wings: Nashville Hot, Umami, Honey Sriracha, Buffalo, Garlic Parm, BBQ, Korean BBQ, Naked. Extra sauce $1.", [
  ("Famous Bone-In Wings", "Choice of sauce; extra sauce $1", 17.99),
  ("Boneless Wings", "Choice of sauce; extra sauce $1", 14.99),
  ("Super Nachos", "Chicken or beef, onions, tomato, olives, cheese, sour cream, salsa. Jalapenos & guacamole on request", 17.99),
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
 ("FRESH MADE SALADS", "", [
  ("Chef Salad", "Ham, turkey, cheese, egg, tomatoes, olives, on mixed greens", 15.99),
  ("Taco Salad", "Seasoned beef, mixed greens, tomato, cheese, onion, olives, tortilla chips, sour cream, salsa", 14.99),
  ("Cobb Salad", "Chicken, bacon, tomatoes, blue cheese crumbles, egg, on mixed greens", 14.99),
  ("Buffalo Chicken Salad", "Buffalo chicken, tomato, olives, onions, cheese, bacon, on mixed greens", 14.99),
 ]),
 ("CRAFTED BURGERS", "1/3 lb beef. Make it a double for $3. Choice of fries, tater tots, house-made potato chips, or house-made side salad. Upgraded sides: Onion Rings $1.99 · Fried Pickles $1.99 · Pork Rinds $1.99 · Mac & Cheese $2.49 · Cup of Soup $1.99 · Fried Mushrooms $1.99", [
  ("Idaho Classic", "Pickles, lettuce, tomato, onion, cheddar, ketchup, mustard (add bacon $2)", 14.49),
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
 ("SANDWICHES / WRAPS", "Choice of fries, tater tots, house-made potato chips, or house-made side salad. Same upgraded sides as burgers.", [
  ("The PDQ", "Grilled cheese sandwich w/ a cup of the soup of the day", 7.99),
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
 ("ENTREES", "", [
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
 ("DESSERTS", "", [
  ("Brownie Delight", "With ice cream and chocolate drizzle", 5.99),
  ("Raspberry Cheesecake", "", 6.99),
  ("Banana Cream Pie", "", 6.99),
  ("Bowl of Ice Cream", "Vanilla or Huckleberry", 3.99),
 ]),
]

dv = DataValidation(type="list", formula1='"Keep,Update,Remove,New"', allow_blank=True)
food.add_data_validation(dv)

r = 2
for section, note, items in MENU:
    cell = food.cell(row=r, column=1, value=section)
    cell.font = Font(name=F, size=11, bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", start_color=RED)
    for c in range(2, 7):
        food.cell(row=r, column=c).fill = PatternFill("solid", start_color=RED)
    if note:
        nc = food.cell(row=r, column=3, value=note)
        nc.font = Font(name=F, size=8.5, italic=True, color="FFFFFF")
        nc.alignment = Alignment(wrap_text=True, vertical="center")
        food.row_dimensions[r].height = 30 if len(note) > 120 else 18
    r += 1
    band = False
    for name, desc, price in items:
        vals = [section.title(), name, desc, price, "Keep", ""]
        for c, v in enumerate(vals, 1):
            cell = food.cell(row=r, column=c, value=v)
            cell.font = Font(name=F, size=10, color=INK, bold=(c == 2))
            cell.border = border
            if band:
                cell.fill = PatternFill("solid", start_color=LIGHT)
            if c == 3:
                cell.alignment = Alignment(wrap_text=True, vertical="center")
            if c == 4:
                cell.number_format = '$#,##0.00'
        dv.add(food.cell(row=r, column=5))
        band = not band
        r += 1
    # three blank styled rows for additions
    for _ in range(2):
        for c in range(1, 7):
            cell = food.cell(row=r, column=c, value="")
            cell.border = border
            cell.font = Font(name=F, size=10, color=INK)
            if c == 4: cell.number_format = '$#,##0.00'
        dv.add(food.cell(row=r, column=5))
        r += 1
    r += 1  # spacer

# ---------- PIZZA ----------
pz = wb.create_sheet("Pizza Menu")
pz.sheet_view.showGridLines = False
pwidths = {"A": 14, "B": 30, "C": 62, "D": 11, "E": 11, "F": 12, "G": 30}
for c, w in pwidths.items(): pz.column_dimensions[c].width = w
phdr = ["Type", "Pizza", "Description", '12" Price', '16" Price', "Status", "Notes / Changes"]
for i, h in enumerate(phdr, 1):
    cell = pz.cell(row=1, column=i, value=h)
    cell.font = Font(name=F, size=11, bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", start_color=INK)
pz.row_dimensions[1].height = 22
pz.freeze_panes = "A2"

dv2 = DataValidation(type="list", formula1='"Keep,Update,Remove,New"', allow_blank=True)
pz.add_data_validation(dv2)

PIZZA = [
 ("Regular", [
  ("Cheese", ""), ("Pepperoni", ""),
  ("Hawaiian", "Cheese, Canadian bacon, and pineapple"),
  ("Meat Lovers", "Pepperoni, Canadian bacon, sausage, and cheese"),
  ("Vegetarian", "Cheese, mushrooms, olives, green peppers, and onions"),
  ("Parmesan Garlic Chicken w/ Bacon", ""),
  ("BBQ Chicken", "BBQ sauce, cheese, chicken"),
  ("Chicken Bacon Ranch", ""),
  ("Husky", "Mustard sauce, cheese, pepperoni, and pineapple"),
  ("Buffalo Chicken", "Frank's RedHot buffalo sauce, cheese, chicken"),
 ], 13.99, 22.00),
 ("Specialty", [
  ("Supreme", "Cheese, Canadian bacon, sausage, pepperoni, mushrooms, olives, onions, green peppers"),
  ("Korean Chicken", "Gochujang sauce, cheese, bell peppers, green onions, crispy chicken"),
  ("Shotgun", "Mustard sauce, Swiss polish sausage, onions, and sauerkraut"),
  ("Taco Pizza", "Cheese, taco meat, tomatoes, olives, green onion, and lettuce"),
 ], 15.99, 24.99),
]

r = 2
for ptype, pies, p12, p16 in PIZZA:
    cell = pz.cell(row=r, column=1, value=ptype.upper() + " PIZZA")
    cell.font = Font(name=F, size=11, bold=True, color="FFFFFF")
    for c in range(1, 8): pz.cell(row=r, column=c).fill = PatternFill("solid", start_color=RED)
    r += 1
    band = False
    for name, desc in pies:
        vals = [ptype, name, desc, p12, p16, "Keep", ""]
        for c, v in enumerate(vals, 1):
            cell = pz.cell(row=r, column=c, value=v)
            cell.font = Font(name=F, size=10, color=INK, bold=(c == 2))
            cell.border = border
            if band: cell.fill = PatternFill("solid", start_color=LIGHT)
            if c == 3: cell.alignment = Alignment(wrap_text=True, vertical="center")
            if c in (4, 5): cell.number_format = '$#,##0.00'
        dv2.add(pz.cell(row=r, column=6))
        band = not band
        r += 1
    for _ in range(2):
        for c in range(1, 8):
            cell = pz.cell(row=r, column=c, value="")
            cell.border = border
            if c in (4, 5): cell.number_format = '$#,##0.00'
        dv2.add(pz.cell(row=r, column=6))
        r += 1
    r += 1
note = pz.cell(row=r, column=2, value="Toppings: jalapenos, extra cheese, and all other toppings add $2.")
note.font = Font(name=F, size=10, italic=True, color=INK)

# ---------- KIDS MENU (own tab, clearly separate from the regular menu) ----------
kids = wb.create_sheet("Kids Menu")
kids.sheet_view.showGridLines = False
for c, w in widths.items(): kids.column_dimensions[c].width = w

for i, h in enumerate(hdr, 1):
    cell = kids.cell(row=1, column=i, value=h)
    cell.font = Font(name=F, size=11, bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", start_color=INK)
    cell.alignment = Alignment(vertical="center")
kids.row_dimensions[1].height = 22
kids.freeze_panes = "A2"

# banner row spelling out the tab clearly
kids.cell(row=2, column=1, value="KIDS MENU — 12 & UNDER")
for c in range(1, 7):
    bc = kids.cell(row=2, column=c)
    bc.fill = PatternFill("solid", start_color=INK)
    bc.font = Font(name=F, size=11, bold=True, color="C9A86A")
kids.row_dimensions[2].height = 20

dvk = DataValidation(type="list", formula1='"Keep,Update,Remove,New"', allow_blank=True)
kids.add_data_validation(dvk)

KIDS = [
 ("KIDS MEALS", "12 & under — served with fries or tots", [
   ("2 Burger Sliders", "", 6.99),
   ("Chicken Tenders", "", 6.99),
   ("Grilled Cheese Sandwich", "", 4.99),
   ("Peanut Butter & Jelly Sandwich", "", 4.99),
   ("Mac & Cheese", "", 4.99),
 ]),
 ("KIDS DRINKS", "", [
   ("Soda", "", 2.99),
   ("Apple Juice", "", 2.50),
   ("Milk", "", 2.49),
   ("Chocolate Milk", "", 2.99),
 ]),
]

r = 3
for section, knote, items in KIDS:
    cell = kids.cell(row=r, column=1, value=section)
    cell.font = Font(name=F, size=11, bold=True, color="FFFFFF")
    for c in range(1, 7): kids.cell(row=r, column=c).fill = PatternFill("solid", start_color=RED)
    if knote:
        nc = kids.cell(row=r, column=3, value=knote)
        nc.font = Font(name=F, size=8.5, italic=True, color="FFFFFF")
        nc.alignment = Alignment(wrap_text=True, vertical="center")
    r += 1
    band = False
    for name, desc, price in items:
        vals = [section.title(), name, desc, price, "Keep", ""]
        for c, v in enumerate(vals, 1):
            cell = kids.cell(row=r, column=c, value=v)
            cell.font = Font(name=F, size=10, color=INK, bold=(c == 2))
            cell.border = border
            if band: cell.fill = PatternFill("solid", start_color=LIGHT)
            if c == 3: cell.alignment = Alignment(wrap_text=True, vertical="center")
            if c == 4: cell.number_format = '$#,##0.00'
        dvk.add(kids.cell(row=r, column=5))
        band = not band
        r += 1
    for _ in range(2):
        for c in range(1, 7):
            cell = kids.cell(row=r, column=c, value="")
            cell.border = border
            cell.font = Font(name=F, size=10, color=INK)
            if c == 4: cell.number_format = '$#,##0.00'
        dvk.add(kids.cell(row=r, column=5))
        r += 1
    r += 1

# Eric's spreadsheet is a client deliverable; it lives in the Cowork folder, not this repo.
# Override with MENU_XLSX_OUT=... to write elsewhere.
out = os.environ.get("MENU_XLSX_OUT") or os.path.expanduser(
    "~/Documents/Claude/Projects/Winchester Grill/menu/winchester-menu-for-eric.xlsx")
wb.save(out)
print("saved", out)
