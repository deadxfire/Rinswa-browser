# Rinswa Settings Architecture

## Overview
Rinswa completely replaces Firefox's fragmented `about:preferences` with a centralized, modern settings experience. Instead of hard-coding preferences directly into individual UI components (XUL or HTML), Rinswa introduces a `SettingsManager` abstraction that cleanly maps user-facing toggles to Gecko's internal `libpref` system. This allows us to rapidly evolve the UX without touching backend C++ code.

## Settings Navigation
The UI is organized into clear, intuitive categories:
- **General:** Startup behavior, homepage, new tab, restore session, default browser, language.
- **Appearance:** Theme (Light/Dark/System), compact mode, toolbar customization, font configuration.
- **Tabs:** New tab behavior, tab closing behavior, pinned tabs, tab restoration, previews.
- **Search:** Default search engine, suggestions, shortcuts, custom engines.
- **Privacy & Security:** Tracking protection, cookies, HTTPS-only, fingerprinting, history, cache, site storage, passwords.
- **Permissions:** Camera, microphone, location, notifications, popups, automatic downloads, clipboard.
- **Downloads:** Directory management, ask where to save.
- **Extensions:** Add-on management hooks.
- **Sync:** Synchronization management.
- **Profiles:** Local profile handling and fast switching.
- **Advanced:** Hardware acceleration, developer tools, experimental features, diagnostics.
- **About Rinswa:** Version, legal, and update status.

## Architecture
Every setting is defined in a centralized JSON schema (`settings-schema.json`), enforcing strict separation of concerns between the UI and Gecko internals.

### Reusable Abstraction (`SettingsManager.js`)
The `SettingsManager` class provides the following guarantees:
- **Stable Identifier:** A Rinswa-specific ID (e.g., `appearance.theme`) mapped to the underlying Gecko pref (e.g., `extensions.activeThemeID`).
- **Validation:** Type checking (boolean, int, string) and predefined array validation before writing to `Services.prefs`.
- **Persistence:** Real-time sync with `Services.prefs`, allowing cross-window synchronization.
- **Reset Capability:** Fetching the `default` branch of `libpref` to allow users to restore factory defaults instantly per-setting or per-category.
- **Migration Capability:** Versioned schema support so preferences can be seamlessly migrated during browser upgrades without relying on legacy Mozilla migration scripts.

## Preference Mapping Examples
- `privacy.https_only` -> `dom.security.https_only_mode`
- `appearance.theme` -> `extensions.activeThemeID`
- `advanced.hardware_acceleration` -> `layers.acceleration.disabled` (Using a `valueMap` to invert logic, since Firefox stores "disabled", but the UI shows "Use acceleration").
- `permissions.location` -> `permissions.default.geo`

## UX Considerations
- **Search:** A unified search bar instantly filters the schema and UI components.
- **Descriptions:** Every toggle includes clear, plain-language explanations.
- **Immediate Feedback:** State changes are saved instantly; no manual "Save" buttons are used.
- **Safety:** Dangerous or deprecated internal `about:config` preferences are intentionally excluded from this UI. Users who need them must explicitly navigate to `about:config`.
