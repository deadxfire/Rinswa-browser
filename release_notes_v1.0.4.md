## Rinswa Browser v1.0.4 (Official Stable Release)

Welcome to the **Rinswa Browser 1.0.4 Stable** release! This update addresses critical layout enhancements for browser extensions, updates verification and feed delivery, and cleans up enterprise notification banners in Settings.

---

### 🚀 Key Improvements & Highlights in v1.0.4

* **🧩 Extension Popup Layout & Truncation Fix:**
  - Resolved an issue where extension popups (such as **Proton Pass**, **Bitwarden**, and other password/security extensions) were cut off on the right side due to rigid panel clipping.
  - Extension popups now dynamically adapt with a responsive width (`min-width: 380px`, `max-width: 800px`) and `overflow: visible`, ensuring buttons, text fields, and branding elements render with complete visibility.

* **⚙️ Clean Settings Screen (Managed Organization Notice Suppressed):**
  - Suppressed the *"Your browser is being managed by your organization"* banner in `about:preferences`.
  - While enterprise policies continue to cleanly deliver built-in ad blocking (`uBlock Origin`) and optimized default settings, the distracting administrative notice is now hidden from the user interface.

* **🔄 Update Feed Integrity & Automatic Update System Fix:**
  - Fixed an issue where `update.xml` previously lacked SHA-256 hash values and byte sizes, causing the browser to reject update downloads.
  - Fixed false *"Update available"* loop triggers by properly synchronizing build IDs and update metadata.
  - Automated hash and byte size calculation in the build pipeline (`scripts/update-release-metadata.py`) to guarantee flawless verification.

---

### 📦 Release Assets & Checksums

| File | Description | Target Platform | Size |
| :--- | :--- | :--- | :--- |
| **`rinswa-1.0.4.en-US.win64.installer.exe`** | Standalone Release Installer | Windows x64 (64-bit) | ~96.7 MB |
| **`rinswa-1.0.4.en-US.win64.zip`** | Standalone Portable Archive | Windows x64 (64-bit) | ~149.5 MB |

---

### 🔐 SHA-256 Checksums

```text
9bfe48da4b70fd76822d82c3ebedab8ec9f2fe71a98c6596adbcbb5b54172652  rinswa-1.0.4.en-US.win64.installer.exe
7a99a553202c20aff76da910a5426c4d5aac87b8551364f8d2f3079a9f808d04  rinswa-1.0.4.en-US.win64.zip
```
