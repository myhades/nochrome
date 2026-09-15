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
- Ordinary top tabs use Chromium-derived 240/56/32px maximum, active-minimum and inactive-minimum widths; stacked and pinned rows retain native positioning.
- Explicit row height keeps the toolbar from covering the selected tab’s curved feet.
- Reading List, download and extension controls share 20px icon canvases; the new-tab plus uses its own Chrome-sized canvas.
- The native new-tab button is anchored to the last tab using CSS anchor positioning.
- The bookmark row is 34px, shorter than the 44px navigation row, with a one-pixel lower boundary.
- Toolbar and bookmark separators are short round-ended capsules. Tab separators are thinner and taller; those beside an active or hovered tab disappear immediately and fade back with the hover.
- Active-tab corners change immediately, while inactive-tab hover color fades in and out.
- Tab insertion/removal uses Chromium's 18px overlap endpoint and a 150ms linear interpolation; closing mirrors opening, while closing a middle tab freezes the remaining widths until the pointer leaves the strip. New tabs expand toward available space and keep their right edge fixed once the strip reaches its reserved 20px trailing margin.
- Hover cards use Chromium's dynamic 300–1300ms delay, 256px width, 16:9 preview and a separate memory/hibernation footer.
- Vivaldi’s segmented loading spinner is replaced with a continuously rotating, sweep-eased ring based on Chromium’s desktop throbber behavior.
- The omnibox popup follows Chrome’s integrated rounded panel, row height, selection pill, text sizing and title/URL contrast.
- Generic profiles use Chromium’s outlined account-circle icon; real profile avatars are reduced to 80% of their former size.
- Broad rules that hid security text, toolbar children and permission UI removed.
- Local CSS/SVG assets with no network requests at runtime.
- The optional macOS patch adds an independent Chrome-shaped toolbar menu, preserves the native macOS menu bar, and keeps the download control visible for active transfers and for 60 minutes after completion.

## Verification and limits

Manually checked light and dark appearance, theme schedule mappings, navigation to a real HTTPS page, the site-information popup, closing and switching tabs, the adjacent new-tab button, empty-header window dragging, three-dot menu opening and Settings activation, download-button visibility, the loading throbber, drag reordering of three plain tabs, and full restarts with the CSS enabled. Theme archives are validated by `python3 tools/check_themes.py`.

The three-dot menu invokes Vivaldi commands through a Chrome-like layout. Chrome and Vivaldi also have different tab search, start pages and permission dialogs. These retain Vivaldi behavior. Complex tab stacks, overflowing rows, private windows and actual camera/microphone prompts have not been fully regression-tested. Windows/Linux and other display scales are untested. Do not infer pixel-level equivalence from the styling.

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

Native padded glyphs are no longer indiscriminately scaled. Chromium reading-list, download, bookmark-star, folder, account and menu vectors have individual canvas sizes. Native in-progress download artwork is retained during transfers. The measured dark frame, toolbar and address field colors are #1e2020, #3c3c3c and #282828; light uses #e3e3e3, #ffffff and #efeded. Enabled, disabled and expanded states use separate colors.

The empty flex tab strip is explicitly a macOS drag region; tab and button targets remain interactive. The application menu is rendered independently in the toolbar so the macOS menu bar remains available.
