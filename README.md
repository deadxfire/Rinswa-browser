<div align="center">

<img src="Glossy%20Multicolour%20Ribbon%20R%20Emblem.png" alt="Rinswa Browser Emblem" width="140" height="140" style="margin-bottom: 12px;"/>

# Rinswa Browser

**A fast, private, and stunning modern web browser built on the Gecko engine.**

Developed and maintained by **[Arindam Makar](https://github.com/deadxfire)**

[![Version](https://img.shields.io/badge/version-1.0.4_Stable-00d2ff?style=for-the-badge&logo=firefox)](https://github.com/deadxfire/Rinswa-browser/releases)
[![Engine](https://img.shields.io/badge/engine-Gecko_157.0.1-orange?style=for-the-badge&logo=mozilla)](https://github.com/deadxfire/Rinswa-browser)
[![Platform](https://img.shields.io/badge/platform-Windows_x64-blue?style=for-the-badge&logo=windows)](https://github.com/deadxfire/Rinswa-browser)
[![License](https://img.shields.io/badge/license-MPL_2.0-blueviolet?style=for-the-badge)](LICENSE)
[![Adblocker](https://img.shields.io/badge/adblocker-uBlock_Origin_Bundled-red?style=for-the-badge&logo=ublockorigin)](https://github.com/gorhill/uBlock)

[Features](#key-features) • [Architecture](#repository-structure) • [Building from Source](#building-from-source) • [Update & Build Guide](docs/UPDATING_AND_BUILDING.md) • [Privacy Policy](#privacy--security-first) • [License](#license)

---

</div>

## Overview

**Rinswa Browser** is a next-generation web browser engineered for users who value aesthetic refinement, absolute privacy, and uncompromised performance. Powered by the modern, battle-tested Mozilla Gecko engine, Rinswa completely removes sponsored telemetry, invasive data collection, and distracting commercial bloat, replacing them with a sleek **Cyber-Glass** visual theme, native ad blocking, and customizable privacy controls.

---

## Key Features

### 🎨 Cyber-Glass & Multicolour Ribbon UI
- **Signature Visual Identity:** Designed with a vibrant, translucent glass aesthetic, custom window controls, and the signature Rinswa glossy multicolour ribbon emblem.
- **Modern Tabstrip & Navigation:** Streamlined tabs, refined omnibar, and responsive UI micro-animations tailored for Windows 11 and modern desktop environments.
- **Alpine Sunset Theme & Wallpapers:** High-resolution dynamic backgrounds crafted for new tab and start experiences.

### 🛡️ Privacy & Security First
- **Zero Hidden Telemetry:** All internal telemetry is disabled at compile time (`--disable-telemetry`), and crash reports to external servers are completely neutralized.
- **No Sponsored Content:** Absolutely no sponsored tiles, sponsored shortcuts, activity stream ads, or affiliate link injection.
- **Strict Anti-Tracking:** Upstream Enhanced Tracking Protection (ETP) enabled out-of-the-box with strict third-party cookie isolation and fingerprinting protection.
- **HTTPS-First Enforcement:** Encrypted connections prioritized across all web navigation.

### ⚡ Out-of-the-Box Native Ad Blocking
- **Pre-Integrated uBlock Origin:** Comes bundled directly with Raymond Hill's industry-leading `uBlock Origin` extension in the distribution folder, giving you instant, lightweight, and effective ad and tracker blocking on your first launch.

### 🚀 Cutting-Edge Engine Performance
- **Gecko 157.0.1 Stable Engine:** Full support for the latest web standards, WebAssembly, WebGPU, and modern CSS features.
- **Hardware-Accelerated WebRender:** Butter-smooth rendering and low GPU memory utilization.
- **Process Sandboxing (Fission):** Full site isolation architecture ensuring untrusted sites cannot access data across tabs.

---

## Repository Structure

```
Rinswa-browser/
├── branding/               # Rinswa brand identity, icons, logos, and fluent UI strings
│   ├── assets/             # Raw vector logos and high-res icon assets
│   ├── distribution/       # Pre-packaged browser extensions (uBlock Origin)
│   ├── icons/              # Multi-resolution Windows .ico and PNG icons
│   └── pref/               # Custom default preferences (branding, welcome page)
├── config/                 # Build configurations and mozconfig directives
│   └── mozconfig.windows   # Windows x64 release build configuration (-j16, release flags)
├── docs/                   # Full technical and architectural documentation
│   ├── branding.md         # Brand identity guidelines and asset specs
│   ├── privacy.md          # Data collection policy and tracking mitigations
│   ├── support.html        # Interactive offline and online support center
│   └── ui.md               # Cyber-Glass interface design documentation
├── scripts/                # Automated build orchestration scripts
│   ├── build-stable.sh     # End-to-end compilation and packaging pipeline
│   └── gen-branding-assets.ps1 # Automated icon and asset generator
├── rinswa-stable/          # Gecko engine source tree (v157.0.1)
├── Build-Rinswa-Stable.bat # One-click Windows build launcher
├── LICENSE                 # Mozilla Public License Version 2.0
└── README.md               # Project documentation
```

---

## Building from Source

> For a complete, step-by-step walkthrough on building the installer, merging upstream Firefox engine updates, and publishing releases, see the **[Updating & Building Guide](docs/UPDATING_AND_BUILDING.md)**.

### Prerequisites

To compile Rinswa Browser on Windows, ensure the following are installed:
1. **Windows 10 / 11 (64-bit)**
2. **[MozillaBuild 4.0+](https://ftp.mozilla.org/pub/mozilla.org/mozilla/libraries/win32/MozillaBuildSetup-Latest.exe)** (installed at default path `C:\mozilla-build\`)
3. **Visual Studio 2022 Build Tools** (C++ Desktop Development workload and Windows 10/11 SDK)
4. **Git for Windows** and **Python 3.11**

### Quick Build (One-Click)

The simplest way to build Rinswa is using the preconfigured Windows batch script:

1. Double-click **`Build-Rinswa-Stable.bat`** (or launch via PowerShell / Command Prompt):
   ```cmd
   .\Build-Rinswa-Stable.bat
   ```
2. The automated pipeline will:
   - Generate all multi-resolution branding assets and `.ico` files.
   - Configure the environment via MozillaBuild.
   - Compile the full Gecko engine using 16 parallel compilation threads (`-j16`).
   - Bundle uBlock Origin into the application distribution.
   - Package the standalone release installer (`.exe`) into `rinswa-stable\obj-rinswa\dist\install\sea\`.

### Advanced Build via Command Line

You can also run specific pipeline phases using `scripts/build-stable.sh` inside the MozillaBuild MSYS2 shell:

```bash
# Enter MozillaBuild environment
C:\mozilla-build\start-shell.bat

# Navigate to project directory
cd /c/Users/arind/OneDrive/Documents/Project/browser

# Available phases: bootstrap | prepare | compile | package | all
./scripts/build-stable.sh compile
```

---

## Release Outputs

Once compiled, build artifacts are located in:
- **Standalone Installer:** `rinswa-stable\obj-rinswa\dist\install\sea\Rinswa.Setup.exe`
- **Portable Distribution:** `rinswa-stable\obj-rinswa\dist\bin\` (Run via `rinswa.exe`)

---

## Privacy & Security

Rinswa's default network policy ensures complete user sovereignty:
- **No telemetry transmission:** Telemetry servers and pings are stripped.
- **Zero user profiling:** No browsing patterns or history are monitored or externalized.
- **Cryptographic verification:** Reuses standard Mozilla certificate revocation (OCSP) and SafeBrowsing threat blocklist updates to ensure real-time protection against malicious websites.

For details, refer to the [Rinswa Privacy & Security Documentation](docs/privacy.md).

---

## Support & Contributing

- **Issue Tracker:** [GitHub Issues](https://github.com/deadxfire/Rinswa-browser/issues)
- **Support Portal:** [Rinswa Browser Support Page](https://github.com/deadxfire/Rinswa-Browser-Support)
- **Interactive Offline Help:** Open `docs/support.html` in any browser for interactive troubleshooting, diagnostics, and FAQ.

---

## License

This project is licensed under the **[Mozilla Public License Version 2.0 (MPL-2.0)](LICENSE)**.

- **Gecko Engine & Portions:** Copyright © Mozilla Contributors and others under MPL 2.0.
- **Rinswa Browser, Brand Identity & UI Enhancements:** Copyright © 2026 **Arindam Makar**. All rights reserved.
- *Trademarks:* "Mozilla" and "Firefox" are trademarks of the Mozilla Foundation. "Rinswa" and the Rinswa logo are trademarks of the Rinswa project.
