# Rinswa Profile Architecture

## Overview
Rinswa leverages Gecko's robust profile management system (`nsIToolkitProfileService`) to ensure complete cryptographic and functional isolation between user profiles. Each profile acts as a fully independent browser instance.

## Isolation Guarantees
By design, switching profiles completely partitions:
- **State & Storage:** Browsing History, Cache, Cookies, Local Storage (IndexedDB, LocalStorage, ServiceWorkers).
- **Settings:** Preferences (`prefs.js`), Extensions, and Site Permissions.
- **Session:** Active tabs, windows, pinned tabs, and tab groups.

## Data Locations
Profiles are stored locally on the file system and are strictly partitioned. The default profile locations differ by Operating System:

- **Windows:** `%APPDATA%\Rinswa\Profiles\` (Roaming state) and `%LOCALAPPDATA%\Rinswa\Profiles\` (Cache).
- **macOS:** `~/Library/Application Support/Rinswa/Profiles/`
- **Linux:** `~/.rinswa/` (or `~/.config/rinswa/` depending on XDG Base Directory configurations).

The active profile directory and default profiles are managed via the `profiles.ini` and `installs.ini` files residing in the root of the application data folder.

## Profile Selector
Rinswa replaces the legacy Mozilla profile manager (`-P`) with a modern, in-browser Profile Selector dropdown accessible directly from the main toolbar. 
- **Features:** Create, Rename, Delete, Select, Set Avatar.
- **Security:** The selector intentionally masks sensitive information (like sync email addresses or active session counts) from the dropdown preview to protect against shoulder surfing.
