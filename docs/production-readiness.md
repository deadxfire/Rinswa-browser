# Rinswa Production Readiness Audit

## Overview
This document represents a comprehensive production-readiness audit of the Rinswa browser architecture prior to a 1.0 release. 

**Status: NOT PRODUCTION READY.** 

While the foundational architecture successfully decouples Rinswa's branding, UI, and settings from the underlying Gecko engine, several critical security, stability, and upstream maintainability limitations remain. These must be resolved before general availability.

---

## 1. Browser Stability
**Issue: Blindness to process crashes**
* **Severity:** High
* **Files Affected:** `config/mozconfig.*`
* **Description:** Hard-disabling the crash reporter (`--disable-crashreporter`) ensures absolute privacy but leaves developers completely blind to in-the-wild renderer or GPU process crashes.
* **Recommended Fix:** Implement an opt-in, self-hosted crash ingestion server (e.g., Mozilla Socorro or Sentry) so users can voluntarily report tab/GPU crashes.
* **Upstream Impact:** Zero impact; requires pointing the crash reporter endpoint URLs to Rinswa servers in `branding/`.

**Issue: Profile Corruption during Rollback**
* **Severity:** High
* **Description:** `libpref` database schema changes between Gecko versions are not backwards compatible. A user downgrading from Rinswa 1.1 (Gecko 130) to Rinswa 1.0 (Gecko 128) will experience severe profile corruption.
* **Recommended Fix:** Implement a version-check in the Rinswa startup launcher that forces a new profile creation or warns the user if a downgrade is detected.

---

## 2. Security
**Issue: Extension Signing Infrastructure**
* **Severity:** Critical
* **Files Affected:** `ui/settings/SettingsManager.js`
* **Description:** We currently rely on Mozilla's AMO (addons.mozilla.org). If Mozilla restricts our API access as a third-party browser, or if we disable `xpinstall.signatures.required` to bypass them, users become highly vulnerable to malicious side-loaded extensions.
* **Recommended Fix:** We must either establish a formal API agreement with Mozilla or stand up a verified Rinswa extension signing proxy.
* **Upstream Impact:** High. Altering extension signature enforcement deeply touches `toolkit/components/extensions/`.

---

## 3. Privacy
**Issue: Upstream network pings leaking IPs**
* **Severity:** Medium
* **Files Affected:** `branding/assets/locales/en-US/brand.ftl` (Needs a companion `prefs.js`)
* **Description:** While internal telemetry is disabled, captive portal detection (`detectportal.firefox.com`) and push notification WebSockets still ping Mozilla servers, leaking user IP addresses.
* **Recommended Fix:** Proxy these requests or host our own endpoint to ensure zero Mozilla IP leakage. Set `network.captive-portal-service.enabled` to `false` if hosting an endpoint is too expensive.
* **Upstream Impact:** Low. Can be disabled via `libpref` overrides during the build.

---

## 4. Cross-Platform Consistency
**Issue: macOS Universal Binaries**
* **Severity:** Medium
* **Files Affected:** `.github/workflows/release.yml`
* **Description:** The current GitHub Actions pipeline treats Apple Silicon and Intel as separate `.dmg` targets. This creates user confusion during installation.
* **Recommended Fix:** Utilize `lipo` or `mach package` universal flags to merge the x64 and ARM64 slices into a single `Rinswa-Universal.dmg`.

**Issue: Linux Wayland Fallback**
* **Severity:** Low
* **Files Affected:** `config/mozconfig.linux`
* **Description:** The `cairo-gtk3-wayland` flag may crash on older X11 distributions if Wayland is missing.
* **Recommended Fix:** Ensure the `MOZ_ENABLE_WAYLAND=1` environment variable falls back gracefully to X11 in the Linux `.desktop` file launcher.

---

## 5. Firefox Upstream Maintainability
**Issue: UI CSS Fragility**
* **Severity:** Critical
* **Files Affected:** `ui/rinswa.css`, `browser/base/content/browser.html`
* **Description:** Our custom UI targets specific XUL/HTML IDs (e.g., `#urlbar`, `#TabsToolbar`). Mozilla frequently refactors these elements in upstream `mozilla-central`. Upstream merges will silently break the Rinswa UI, leading to missing tabs or broken navigation.
* **Recommended Fix:** We must write a DOM-integration test suite (running inside `mach test`) that verifies these IDs and classes still exist before every release. 
* **Upstream Impact:** By relying on CSS overrides rather than C++ patches, we minimize git source conflicts, but maximize functional fragility. The test suite is mandatory to prevent UI collapse.

---

## Conclusion
Rinswa's architecture successfully achieves the "One Codebase" and "Privacy Default" mandates. However, the browser **cannot be declared production-ready** until the extension signing vulnerability is addressed and a robust DOM-integration test suite is established to guarantee UI stability against Mozilla's rapid release cycle.
