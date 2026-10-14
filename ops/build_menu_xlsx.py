#!/usr/bin/env python3
import os, json
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

# ---------- menu data ----------
# ops/menu.json is the single source of truth, shared with build_menu_page.py.
# Edit the JSON, never these tuples; section names are upper-cased here for the sheet.
MENU_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "menu.json")
with open(MENU_JSON) as _f:
    _menu = json.load(_f)
MENU = [(s["section"].upper(), s["note"],
         [(i["name"], i["desc"], i["price"]) for i in s["items"]]) for s in _menu["food"]]

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

PIZZA = [(g["group"].replace(" Pizza", ""), [(p["name"], p["desc"]) for p in g["pies"]],
          g["price_12"], g["price_16"]) for g in _menu["pizza"]]

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

KIDS = [(s["section"].upper(), s["note"],
         [(i["name"], i["desc"], i["price"]) for i in s["items"]]) for s in _menu["kids"]]

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

# Eric's spreadsheet is a client deliverable; it lives in client/ (gitignored), not in the site.
# Override with MENU_XLSX_OUT=... to write elsewhere.
out = os.environ.get("MENU_XLSX_OUT") or os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "client", "menu", "winchester-menu-for-eric.xlsx")
wb.save(out)
print("saved", out)
