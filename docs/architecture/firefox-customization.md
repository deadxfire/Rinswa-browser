# Firefox Components Customized for Rinswa

The following Firefox/Gecko components require modification, replacement, or configuration for Rinswa. 

## 1. Branding (`browser/branding/`)
**Modifications:** Replace Firefox logos, icons, wordmarks, and legal text.
- `browser/branding/official/` - Replaced with Rinswa branding assets.
- Changes require no core engine patches and are safe for upstream merges.

## 2. Default Preferences (`browser/app/profile/firefox.js`, `modules/libpref/init/all.js`)
**Modifications:** Disable telemetry, sponsored tiles, Pocket, and adjust privacy defaults.
- Set `toolkit.telemetry.enabled` to `false`.
- Set `browser.newtabpage.activity-stream.showSponsored` to `false`.
- Disable default Google Safebrowsing telemetry if required.
- Safe for upstream merges.

## 3. Main Browser UI (`browser/base/content/`)
**Modifications:** Redesign `browser.html`, `browser.css`, and custom WebComponents.
- Simplify toolbars, tabs, and menus for a minimalist aesthetic.
- *Conflict Risk:* High. Mozilla frequently refactors UI code. Rebase strategies will need careful conflict resolution here.

## 4. Settings Page (`browser/components/preferences/`)
**Modifications:** Remove settings related to disabled features (e.g., Firefox Sync, Telemetry, Pocket).
- Add specific Rinswa privacy toggles.
- *Conflict Risk:* Medium.

## 5. New Tab Page (`browser/components/newtab/`)
**Modifications:** Strip out "Activity Stream", Pocket integrations, and sponsored top sites.
- Replace with a fast, private, customizable new tab page.
- *Conflict Risk:* Medium.

## 6. Telemetry and Data Collection (`toolkit/components/telemetry/`, `browser/components/pingcentre/`)
**Modifications:** Hard-disable or rip out telemetry components at compile time (`mozconfig` flags) and runtime.
- Use `--disable-telemetry` and `--disable-crashreporter` in `mozconfig`.
- *Conflict Risk:* Low if managed via build flags; High if C++ code is manually stripped.

## 7. Updater (`toolkit/mozapps/update/`)
**Modifications:** Point update URLs to Rinswa servers. Modify update certificates.
- Update `app-update.certs`, `updater.ini`, and relevant `libpref` strings.
- *Conflict Risk:* Low.

## 8. Build System (`mozconfig`, `old-configure.in`, `python/mozbuild/`)
**Modifications:** Introduce Rinswa-specific compilation flags.
- Create default `.mozconfig` files for Rinswa platforms (Windows x64/ARM64, macOS Intel/Apple Silicon, Linux x64/ARM64).
- *Conflict Risk:* Low.

## 9. Add-on Signing (`toolkit/components/extensions/`)
**Modifications:** Remove forced signing requirements or support a Rinswa-specific extension store.
- Alter `xpinstall.signatures.required`.
- Update standard AMO (addons.mozilla.org) URLs in preferences if opting for a self-hosted extension repository.
- *Conflict Risk:* Low.

## 10. Search Defaults (`browser/components/search/`)
**Modifications:** Change default search engines to privacy-respecting alternatives (e.g., DuckDuckGo, Brave Search).
- Update search engine configurations and default choices.
- *Conflict Risk:* Low.

---

## Modifications Without Modifying Gecko
Almost all Rinswa features can be implemented without touching the core Gecko engine (`dom/`, `layout/`, `js/`, `gfx/`). 
- UI changes (HTML/CSS/JS).
- Preference overrides.
- Branding asset replacements.
- Build configurations (`mozconfig`).
- Search engine defaults.

## Modifications Requiring Firefox Patches
- Any deep removal of telemetry APIs that cannot be disabled via `mozconfig`.
- Removing hardcoded URLs in C++ components (e.g., captive portal detection, some geolocation endpoints) if they cannot be changed via `libpref`.
- Modifying OS-level integration inside `widget/` (unlikely for Phase 1).

## Upstream Merge Conflict Areas
The highest risk of merge conflicts lies in `browser/base/content/` (the main UI) and `browser/components/` (New Tab, Preferences). Mozilla rapidly iterates on these frontend components. Keeping our changes well-documented and localized to specific files (or utilizing userchrome.css/usercontent.css style injection via build processes) will minimize these issues.
