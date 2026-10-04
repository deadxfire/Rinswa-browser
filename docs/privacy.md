# Rinswa Privacy & Security

## Overview
Rinswa's primary objective is to offer a fast, modern browsing experience that respects user privacy by default. We do not invent unsupported privacy claims. Instead, we rely on Mozilla Firefox's mature, battle-tested security architecture (Gecko) while stripping away unnecessary data collection and telemetry to give users honest, understandable controls over their privacy.

## Privacy Defaults & Data Collection Policy
Rinswa operates on the following strict default principles:
- **No Advertisements:** No sponsored tiles, activity stream ads, or injected content anywhere in the browser.
- **No Profiling or Selling Data:** Rinswa does not build user profiles, track history externally, or monetize browsing habits.
- **No Hidden Telemetry:** All internal telemetry is hard-disabled at compile time (`--disable-telemetry`). We do not collect usage metrics.
- **Third-Party Pings Disabled:** Integrations such as Pocket, telemetry components of Google SafeBrowsing, and captive portal analytics are disabled by default.

### Documented Required Communications
To ensure the browser functions securely, the following automated network requests remain enabled by default (reusing upstream Firefox infrastructure):
- **SafeBrowsing Blocklist Updates:** Downloads hashes of malicious domains to protect users from phishing and malware.
- **Extension Blocklist:** Checks for known malicious add-ons.
- **Certificate Revocation (OCSP):** Validates the security of HTTPS connections.
- **Browser Updates:** Checks the Rinswa update server for new releases.

## Firefox Functionality Reused
Rinswa does not compromise browser security to achieve a minimal UI. The following core Gecko security mechanisms remain completely unmodified:
- **Process Sandboxing** (e10s / Fission)
- **Strict Site Isolation**
- **Content Security Policy (CSP)** enforcement
- **Certificate validation** and trusted root stores
- **Enhanced Tracking Protection (ETP)** engine

## Rinswa-Specific Functionality
- **Privacy Dashboard:** A dedicated, easy-to-read UI popup accessed via the address bar. It aggregates site-specific privacy metrics (Trackers blocked, Cross-Site Cookies blocked) directly from Gecko's tracking protection events, ensuring the data is accurate and not misleading.
- **Simplified Permission Manager:** A clean interface to audit global and site-specific permissions.
- **URL Bar Security Indicators:** The address bar features prominent but clean indicators for HTTPS locks, ETP shield status, and active permissions (e.g., a pulsating microphone icon when audio is captured). We explicitly preserve Firefox's strict visual security indicators to prevent spoofing.

## User Controls
Users have granular, understandable control over their privacy via the Settings menu:
- **Tracking Protection:** Exposed as Standard (balanced), Strict (maximum privacy but may break some sites), and Custom.
- **Cookies:** Global controls for third-party cookies, localized site exceptions, and clearing browsing data.
- **HTTPS-Only:** A toggle to force HTTPS connections globally, utilizing Gecko's native `dom.security.https_only_mode`.
- **Permissions:** Global blocking or prompt-based approval for sensitive APIs like Camera, Microphone, Autoplay, Location, Popups, and Notifications.
