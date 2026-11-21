#!/bin/sh
# Prints menu.html to a PDF with headless Chrome and reports the page count.
# The printed menu is meant to fit on one sheet, both sides: expect "pages: 2".
# Run from the repo root after any menu or print.css change:   sh ops/print_check.sh
# Needs Google Chrome and pypdf (pip3 install --user pypdf).
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="${1:-${TMPDIR:-/tmp}/winchester-menu-print.pdf}"
[ -x "$CHROME" ] || { echo "Google Chrome not found at $CHROME"; exit 1; }
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=6000 \
  --print-to-pdf="$OUT" "file://$(pwd)/menu.html" >/dev/null 2>&1
python3 - "$OUT" <<'PY'
import sys
try:
    from pypdf import PdfReader
except ImportError:
    sys.exit("pypdf is not installed: pip3 install --user pypdf")
n = len(PdfReader(sys.argv[1]).pages)
print(f"pages: {n}   ({sys.argv[1]})")
sys.exit(0 if n <= 2 else 1)
PY
