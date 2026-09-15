# noChrome — Vivaldi 8.2 port

Chrome-inspired browser chrome, based on [nokocu/nochrome](https://github.com/nokocu/nochrome). This fork replaces the old pre-2024 UI selectors and adds independent light and dark themes.

**Tested locally:** Vivaldi 8.2.4133.52 / Chromium 152.0.7977.124 on macOS. Other versions and platforms need testing. This is a close visual approximation, not a pixel-identical replacement for Chrome.

## Install

1. Clone this repository. Keep it in a permanent location.
2. Open `vivaldi://flags/#vivaldi-css-mods`, enable **Allow CSS modifications**, and relaunch.
3. In Settings → Appearance, find **Custom UI Modifications**. Use **Select Folder** to choose the repository's `nochrome` subfolder, then restart Vivaldi.
4. In Settings → Themes, import `nochrome/theme-nochrome-light.zip` and `nochrome/theme-nochrome-dark.zip`.
5. Under Theme Schedule choose **Operating System**; map **Light → noChrome Light**, **Dark → noChrome Dark**. Importing a theme may replace the current schedule entry, so configure the schedule after both imports.
6. Enable **Use Icon Set from → Currently Active Theme**.

On the tested Mac, typing the CSS path directly produced a startup splash hang; selecting the same directory through the native folder picker worked, including a subsequent full restart. Use the picker rather than pasting into the settings field.

Recommended native layout: top tabs and address bar, Regular density, 100% UI zoom, panel hidden, status information overlay, workspaces button removed from the toolbar, and tab close buttons on the right. Toolbar contents remain customizable. The start page and search provider remain Vivaldi settings.

## What changed

- Connected selected tabs with curved corners, inactive separators and rounded hover states.
- Light/dark Chrome-like palettes, a capsule address field and round toolbar buttons.
- Upstream navigation and extension SVG icons packaged into both themes.
- Current `.tab-wrapper` structure and macOS window controls supported.
- Native tab widths and transforms retained so layout and click targets stay aligned.
- Broad rules that hid security text, toolbar children and permission UI removed.
- No injected JavaScript, remote dependencies or application bundle patching.

## Verification and limits

Manually checked light and dark appearance, theme schedule mappings, navigation to a real HTTPS page, the site-information popup, closing tabs, and a full restart with the CSS enabled. Theme archives are validated by `python3 tools/check_themes.py`.

Chrome and Vivaldi have different native menus, tab search, start pages and permission dialogs. These retain Vivaldi behavior. Complex tab stacks, overflow/drag interactions, private windows and actual camera/microphone prompts have not been fully regression-tested. Windows/Linux and other display scales are untested. Do not infer pixel-level equivalence from the styling.

## Build and restore

Run `python3 tools/build_themes.py` to rebuild the theme ZIP files from `themes/*.json` and the SVG assets; then run `python3 tools/check_themes.py`. Restart Vivaldi after CSS edits. Reimport rebuilt themes to update installed theme assets.

To uninstall, clear **Custom UI Modifications**, choose a built-in theme and restart. To temporarily disable styling, rename `nochrome/nochrome.css` to a name without the `.css` suffix and restart. If a saved directory path itself prevents launch, with Vivaldi fully stopped and the profile backed up, clear only `vivaldi.appearance.css_ui_mods_directory` in the profile's `Preferences` JSON. Do not replace the entire profile.

The original stylesheet is preserved in `legacy/nochrome-v2.css`; keep it outside the active CSS directory. The original `theme-nochrome.zip` and screenshots are historical upstream assets, not screenshots of this port.
