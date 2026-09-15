# Chromium vector sources

These vector paths are from the Chromium Authors, under the included BSD license.
Retrieved 2026-09-16 from the Chromium 152.0.7977.83 tag:
https://chromium.googlesource.com/chromium/src/+/refs/tags/152.0.7977.83/.

- `chrome/app/vector_icons/`: add, close, close_weight500, more_vert, reading_list_old, download_toolbar_button_chrome_refresh_old, download, navigate_stop_chrome_refresh_old and close_tab_chrome_refresh_old.
- `components/vector_icons/`: arrow_back, arrow_forward, refresh, warning, dangerous_filled, the retained `*_old` alternatives, extension_chrome_refresh_old, expand_more_old, tune, folder_chrome_refresh_old and account_circle_chrome_refresh_old (stored here as `account_circle_outline.icon`).
- `components/omnibox/browser/vector_icons/`: page_info_custom.

Chrome 152 enables Rounded Icons, so the visible navigation controls use
`arrow_back`, `arrow_forward`, `refresh` and `close`; tabs use
`close_weight500`, and a normal secure origin uses
`page_info_custom`. HTTP warnings use `warning`, while invalid HTTPS uses
`dangerous_filled`. The `*_old` files remain only where Chrome 152 still selects
that artwork or as provenance for unused alternatives. `tools/build_icons.py`
converts the checked-in path operations to local SVG masks and performs no
network requests.
