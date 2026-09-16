#!/usr/bin/env python3
"""Install Chromium's fallback icon and retain the search-engine omnibox logo."""
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
EMPTY_CANDIDATE = (
    'if(n){let e="favicon";return"url"===n.faviconType?e="url":'
    '"img"===n.faviconType&&(e="img"),{favIconUrl:n.faviconUrl,favIconType:e}}'
)
ENGINE_FALLBACK = EMPTY_CANDIDATE.replace("if(n){", "if(n?.faviconUrl){", 1)


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
    updated = text
    changes = []
    if replacement not in updated:
        updated, count = PNG_FALLBACK.subn(replacement, updated, count=1)
        if count != 1:
            raise SystemExit("Expected Vivaldi missing-favicon fallback was not found")
        changes.append("Chromium missing-favicon fallback")
    if ENGINE_FALLBACK not in updated:
        count = updated.count(EMPTY_CANDIDATE)
        if count != 1:
            raise SystemExit("Expected omnibox candidate-favicon branch was not found")
        updated = updated.replace(EMPTY_CANDIDATE, ENGINE_FALLBACK, 1)
        changes.append("search-engine fallback for candidates without favicons")
    if not changes:
        print("Favicon patches already installed")
        return
    bundle.write_text(updated)
    print("Installed " + " and ".join(changes))


if __name__ == "__main__":
    main()
