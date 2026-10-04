# Rinswa Import Architecture

## Supported Browsers
Rinswa relies on Gecko's Migration infrastructure (`nsIBrowserProfileMigrator`) to safely import data from other popular desktop browsers:
- **Mozilla Firefox**
- **Google Chrome**
- **Chromium** (including forks like Brave, Vivaldi, Opera)
- **Microsoft Edge**

## Supported Data Types
Depending on the source browser's API restrictions and encryption methods, Rinswa imports:
- Bookmarks
- Browsing History
- Saved Passwords (via OS-level credential decryption where supported)
- Autofill Data (Addresses, Phone numbers)
- Browser Settings (Homepage, default search engine)
- Cookies (if technically supported and unencrypted by the source)

## Security Requirements
The import process is strictly governed by the following rules to ensure user security is never compromised:
1. **Never Log Passwords:** Passwords are decrypted directly into memory and instantly re-encrypted into Rinswa's `logins.json` utilizing the primary password vault. No plaintext credentials touch the disk, terminal output, or diagnostic logs.
2. **Never Expose Credentials:** The import UI will never preview or expose the contents of the imported credentials to the user.
3. **No Unnecessary Copying:** Data is migrated in a single pass to prevent leaving artifacts in temporary directories.
4. **Validation:** All imported data (especially bookmarks and history URLs) is sanitized to prevent malicious JS injection (`javascript:` URIs) or corrupted history databases.

## Migration Behavior per OS
- **Windows:** Rinswa utilizes Windows DPAPI to decrypt Chrome/Edge SQLite databases during import.
- **macOS:** Rinswa accesses the macOS Keychain (prompting the user for OS permission) to read Chrome's Safe Storage Key for decryption.
- **Linux:** Rinswa queries `libsecret` or KWallet for the source browser's encryption keys to successfully migrate passwords.
