#!/usr/bin/env python3
"""Check distributable theme content and referenced icons without dependencies."""
import json
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
ids = set()
for variant in ('light', 'dark'):
    source = json.loads((root / 'themes' / f'{variant}.json').read_text())
    with ZipFile(root / 'nochrome' / f'theme-nochrome-{variant}.zip') as archive:
        assert archive.testzip() is None
        assert json.loads(archive.read('settings.json')) == source
        for filename in set(source['buttons'].values()):
            data = archive.read(filename)
            assert data == (root / 'themes' / filename).read_bytes()
            assert ET.fromstring(data).tag.endswith('svg')
    assert source['id'] not in ids
    ids.add(source['id'])
    assert source['accentFromPage'] is False
    print(f'{variant}: archive, settings and SVG references OK')
