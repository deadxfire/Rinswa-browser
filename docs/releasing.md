# Rinswa Release Infrastructure

## Versioning Strategy
Rinswa clearly delineates its UI/feature version from the underlying Gecko engine. This ensures users are never misled about their exact security patch level and know exactly what standard they are browsing with.
* **Format:** `Rinswa {RinswaVersion} (Firefox Base: {FirefoxVersion})`
* **Example:** `Rinswa 1.0.0 (Firefox Base: 128.0esr)`
* Displayed natively in `about:rinswa` (which overrides `about:dialog`).

## Update System
Rinswa maintains Firefox's secure updating mechanisms (the `updater` binary and MAR - Mozilla ARchive files). We explicitly reject insecure or unverified updates.
1. **Verification:** All updates are cryptographically signed. The updater strictly verifies the MAR file using our custom public certificate (`app-update.certs` located in the application directory) before applying any patches.
2. **Checks & Notifications:** The browser checks for updates silently in the background and surfaces an unobtrusive notification on the main menu when a restart is required. Manual checks can be run via `about:rinswa`.
3. **Security Priority:** Urgent security patches will enforce an aggressive update cadence, bypassing user delays.
4. **Rollback Strategy:** While `libpref` database migrations are generally one-way, retaining the previous release's uninstaller (Windows) and keeping prior DMG images on the release server allows manual user downgrades in emergency breakage scenarios.

## CI/CD Pipeline
We use GitHub Actions to automate our pipeline, ensuring rigorous consistency across platforms. The pipeline is triggered upon pushing a semver tag (e.g., `v1.0.0`).
1. **Linting & Tests:** Static analysis of Rinswa-specific UI overrides (`.css`, `.js`).
2. **Build Matrix:** Compiles Windows (x64, ARM64), macOS (Intel, Apple Silicon), and Linux (x64, ARM64) simultaneously.
3. **Packaging:** Generates standard native outputs via `./mach package`.
4. **Security Checks:** Executes basic checks and outputs `SHA256` sums for all artifacts.

## Release Artifacts
Every release output includes:
- **Windows:** NSIS Installer (`.exe`) and Portable (`.zip`).
- **macOS:** Disk Image (`.dmg`) containing the `.app` bundle.
- **Linux:** Standalone `.tar.bz2` and a distro-agnostic `.AppImage`.
- **Metadata:** Cryptographic Checksums (`SHA256SUMS.txt`) and Third-Party Licenses (`about:license`).

## Cryptographic Signing
All binaries must be signed to prevent OS-level warnings (Gatekeeper / SmartScreen) and to guarantee integrity to the user.
- **Secrets:** Keys and certificates are **never** committed to the repository. They are stored strictly as encrypted GitHub Actions Secrets.
- **Windows:** Executables are signed via `signtool.exe` using an EV Code Signing Certificate.
- **macOS:** Bundles are signed using `codesign` with Apple Developer ID Application certificates, followed by mandatory `xcrun altool` submission for Apple Notarization.
- **Linux:** Distro packages are signed with a dedicated Rinswa GPG key.

## Maintenance
To maintain this process during upstream Firefox upgrades:
- Rinswa's `app-update.certs` and update URLs must not be overwritten during upstream merges.
- Developers must monitor `mach` build requirement changes (e.g., newer Rust, Clang, or Python versions) in upstream `mozilla-central` release notes prior to tagging a Rinswa release.
