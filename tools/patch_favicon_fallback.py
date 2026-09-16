#!/usr/bin/env python3
"""Replace Vivaldi's generic missing-favicon document image with Chromium search."""
from pathlib import Path
from urllib.parse import quote
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLE = Path(
    "/Applications/Vivaldi.app/Contents/Frameworks/Vivaldi Framework.framework/"
    "Versions/8.2.4133.52/Resources/vivaldi/bundle.js"
)
PNG_FALLBACK = re.compile(
    r'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0[0-9A-Za-z+/=]+'
)


def chromium_search_data_url() -> str:
    source = (ROOT / "themes/chromium/search_chrome_refresh_old.icon").read_text()
    commands = {
        "MOVE_TO": "M", "R_MOVE_TO": "m", "LINE_TO": "L", "R_LINE_TO": "l",
        "H_LINE_TO": "H", "R_H_LINE_TO": "h", "V_LINE_TO": "V", "R_V_LINE_TO": "v",
        "CUBIC_TO": "C", "R_CUBIC_TO": "c", "CUBIC_TO_SHORTHAND": "S",
        "R_CUBIC_TO_SHORTHAND": "s", "QUADRATIC_TO": "Q", "R_QUADRATIC_TO": "q",
        "ARC_TO": "A", "R_ARC_TO": "a", "CLOSE": "Z",
    }
    selected = False
    path = []
    for raw in source.splitlines():
        line = raw.split("//")[0].strip().rstrip(",")
        if not line:
            continue
        values = [value.strip().removesuffix("f") for value in line.split(",")]
        command, args = values[0], values[1:]
        if command == "CANVAS_DIMENSIONS":
            selected = int(args[0]) == 20
        elif selected and command not in ("FILL_RULE_NONZERO", "FLIPS_IN_RTL", "NEW_PATH"):
            path.append(commands[command] + " ".join(args))
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">'
        f'<path fill="#5f6368" d="{" ".join(path)}"/></svg>'
    )
    return "data:image/svg+xml," + quote(svg, safe="")


def main() -> None:
    bundle = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_BUNDLE
    text = bundle.read_text()
    replacement = chromium_search_data_url()
    if replacement in text:
        print("Chromium favicon fallback already installed")
        return
    updated, count = PNG_FALLBACK.subn(replacement, text, count=1)
    if count != 1:
        raise SystemExit("Expected Vivaldi missing-favicon fallback was not found")
    bundle.write_text(updated)
    print("Installed Chromium missing-favicon fallback")


if __name__ == "__main__":
    main()
