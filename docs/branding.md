# Rinswa Branding Guidelines

## Rinswa Naming
* **Product Name:** Rinswa
* **Application Name:** Rinswa Browser
* **Executable Name:** `rinswa` (Linux/macOS) / `rinswa.exe` (Windows)
* **Profile Folder:** `.rinswa` (Linux), `Rinswa` (macOS, Windows AppData)

## Brand Assets
The visual identity communicates a modern, fast, clean, private, reliable, minimal, and professional experience.
* **Colors:** Minimalist palette. No excessive gradients.
* **Imagery:** Professional and technology-focused. Avoid generic "shield" imagery or animal mascots.
* **Typography:** Clean, sans-serif, modern.

## Application Identifiers
* **Windows AppUserModelID:** `Rinswa.Browser.Release`
* **macOS Bundle Identifier:** `org.rinswa.browser`
* **Linux Desktop Entry:** `rinswa.desktop`
* **User Agent String:** `Mozilla/5.0 (...) Gecko/20100101 Rinswa/1.0` (Pending privacy considerations; may prefer mimicking Firefox strictly for anti-fingerprinting).

## Platform Icon Requirements
To ensure a native feel, icons must be generated for all platforms:
* **Windows:** `.ico` format containing sizes from 16x16 up to 256x256.
* **macOS:** `.icns` format providing high-resolution assets (up to 1024x1024) following Apple's Big Sur/Monterey icon guidelines.
* **Linux:** High-resolution `.png` and `.svg` files for Freedesktop.org standard system trays and application launchers.

## Trademark Considerations
* **Mozilla Trademarks:** The terms "Mozilla", "Firefox", and all associated logos are registered trademarks of the Mozilla Foundation. Rinswa must completely replace these trademarks in user-facing UI, installers, and metadata.
* **Copyright Notices:** Legally required copyright notices and open-source licenses (MPL, GPL, etc.) from Mozilla and third-party dependencies must be retained in `about:license`.
* **Rinswa Trademarks:** "Rinswa" and its logo are unique to this project and serve to differentiate it entirely from upstream.

## Files Modified for Branding
During the build process, Rinswa points the Mozilla build system (`mozconfig`) to our custom `branding/` directory via the `ac_add_options --with-branding=../branding` flag. 
The following internal files are typically provided by our branding directory to replace Firefox's:
1. **Localization Strings:** 
   - `brand.ftl` (Fluent UI translations)
   - `brand.properties` / `brand.dtd` (Legacy string references)
2. **Metadata & Manifests:** 
   - `browser/branding/official/moz.build` (Build directives)
   - `browserconfig.xml` (Windows start menu tiles)
   - `document.icns` / `app.icns` (macOS icons)
3. **Graphics:** 
   - `about-logo.svg`, `about-logo.png` (Used in `about:about` and `about:support`)
   - `default16.png` - `default128.png` (Extensions, default window icons)
   - `installer-header.bmp` (Windows NSIS installer)

## How Branding is Applied During Builds
To keep changes isolated from the `mozilla-central` core tree, Rinswa places all branding assets in the external `branding/` folder structure.
When building, the `.mozconfig` includes:
```bash
ac_add_options --with-branding=path/to/rinswa/branding
```
This instructs the Mozilla build system to completely swap out the official Firefox branding with the Rinswa assets, ensuring our branding survives upstream `mozilla-central` merges without manual conflict resolution.
