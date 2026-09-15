# Chromium vector sources

These vector paths are from the Chromium Authors, under the included BSD license.
Retrieved 2026-09-15 from https://chromium.googlesource.com/chromium/src/+/refs/heads/main/.

- `chrome/app/vector_icons/`: add, more_vert, reading_list_old, download_toolbar_button_chrome_refresh_old, download, navigate_stop_chrome_refresh_old and close_tab_chrome_refresh_old.
- `components/vector_icons/`: back_arrow_chrome_refresh_old, forward_arrow_chrome_refresh_old, reload_chrome_refresh_old, extension_chrome_refresh_old, expand_more_old, tune, folder_chrome_refresh_old and account_circle_chrome_refresh_old (stored here as `account_circle_outline.icon`).

The *_old names are Chromium's names for its retained Chrome Refresh artwork. The visible navigation, tab-strip, reading-list, download, extension and folder shapes match the Chrome 152 toolbar inspected on the test Mac. `tools/build_icons.py` converts their path operations to local SVG masks; it performs no network requests. Unused source alternatives are retained for provenance.
