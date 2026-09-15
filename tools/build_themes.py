#!/usr/bin/env python3
"""Rebuild the two importable theme archives with Python's standard library."""
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
root = Path(__file__).resolve().parents[1]
for variant in ('light', 'dark'):
    settings = json.loads((root / 'themes' / f'{variant}.json').read_text())
    target = root / 'nochrome' / f'theme-nochrome-{variant}.zip'
    with ZipFile(target, 'w', ZIP_DEFLATED) as archive:
        archive.writestr('settings.json', json.dumps(settings, indent=2) + '\n')
        for filename in sorted(set(settings['buttons'].values())):
            archive.write(root / 'themes' / filename, filename)
    print(target.name)
