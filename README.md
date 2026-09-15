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
7. On the tested macOS version, run `python3 tools/patch_macos_menu.py` and restart to add the functioning three-dot menu after the profile. This modifies the installed `bundle.js`; the unmodified resource is backed up under `~/Library/Application Support/noChrome/backups/8.2.4133.52/`.

On the tested Mac, typing the CSS path directly produced a startup splash hang; selecting the same directory through the native folder picker worked, including a subsequent full restart. Use the picker rather than pasting into the settings field.

Recommended native layout: top tabs and address bar, Regular density, 100% UI zoom, panel hidden, status information overlay, workspaces button removed from the toolbar, and tab close buttons on the right. Place TabButton in the toolbar before tabs, and NewTab in the toolbar after tabs. Toolbar contents remain customizable. The start page and search provider remain Vivaldi settings.

## What changed

- Connected selected tabs with curved corners, inactive separators and rounded hover states.
- Light/dark Chrome-like palettes, a capsule address field and round toolbar buttons.
- Upstream navigation and extension SVG icons packaged into both themes.
- Current `.tab-wrapper` structure and macOS window controls supported.
- Ordinary top tabs use a 240px flex layout; stacked, pinned and scrolling rows retain native positioning.
- Explicit row height keeps the toolbar from covering the selected tab’s curved feet.
- SVG canvases are limited to 20px rather than Vivaldi toolbar-large’s 28px.
- The native new-tab button is anchored to the last tab using CSS anchor positioning.
- Broad rules that hid security text, toolbar children and permission UI removed.
- Local CSS/SVG assets with no network requests at runtime.
- The optional macOS menu patch restores Vivaldi’s menu component and uses its Mac context-menu interface with the existing command handlers.

## Verification and limits

Manually checked light and dark appearance, theme schedule mappings, navigation to a real HTTPS page, the site-information popup, closing tabs, pointer selection, the adjacent new-tab button, empty-header window dragging, three-dot menu opening and Settings activation, drag reordering of three plain tabs, and a full restart with the CSS enabled. Theme archives are validated by `python3 tools/check_themes.py`.

The three-dot menu invokes Vivaldi commands; its contents retain Vivaldi’s menu structure. Chrome and Vivaldi also have different tab search, start pages and permission dialogs. These retain Vivaldi behavior. Complex tab stacks, overflowing rows, private windows and actual camera/microphone prompts have not been fully regression-tested. Windows/Linux and other display scales are untested. Do not infer pixel-level equivalence from the styling.

## Build and restore

Run `python3 tools/build_icons.py` to regenerate `nochrome/icons.css` from the checked-in, BSD-licensed Chromium vectors. Both CSS files in `nochrome/` must be loaded.

Run `python3 tools/build_themes.py` to rebuild the theme ZIP files from `themes/*.json` and the SVG assets; then run `python3 tools/check_themes.py`. Restart Vivaldi after CSS edits. Reimport rebuilt themes to update installed theme assets.

To remove the native menu patch, run `python3 tools/patch_macos_menu.py --restore` and restart. Vivaldi updates replace the patched resource: the patch deliberately refuses other versions and requires review for each update.

To uninstall the styling, clear **Custom UI Modifications**, choose a built-in theme and restart. To temporarily disable styling, rename `nochrome/nochrome.css` to a name without the `.css` suffix and restart. If a saved directory path itself prevents launch, with Vivaldi fully stopped and the profile backed up, clear only `vivaldi.appearance.css_ui_mods_directory` in the profile's `Preferences` JSON. Do not replace the entire profile.

The original stylesheet is preserved in `legacy/nochrome-v2.css`; keep it outside the active CSS directory. The original `theme-nochrome.zip` and screenshots are historical upstream assets, not screenshots of this port.

## 8.2 geometry correction

The second pass fixes the first port's covered tab feet: the parent row now has a 34px content height plus 6px top padding, followed by a 44px toolbar and a 34px omnibox. Plain tabs use a 240px maximum width and 20px navigation SVG canvases. The tab search button sits before the tabs. The new-tab button follows the last tab through CSS anchor positioning; its containing toolbar must not establish a separate positioning context.

The flex width override is gated on an existing `.tab-position`. This is required for the native initial measurement to run during session restoration; applying it to an empty row prevents tabs from appearing until an interaction.

## Icon, color and drag correction

Native padded 28px glyphs are no longer indiscriminately reduced to 20px. The Chromium reading-list/download/folder/menu vectors have their own canvas sizes; the new-tab glyph is separately enlarged. Native in-progress download artwork is retained during transfers. The dark toolbar is neutral #3c3c3c, the tab strip #202020, and the address field #282828. Enabled/disabled/expanded states use separate colors.

The empty flex tab strip is explicitly a macOS drag region; tab/button targets remain non-draggable as window chrome. The menu's first activation requests its content before opening, and uses the macOS-compatible context-menu path rather than the Windows/Linux Views menu path.
