# Rinswa Browser: Guide to Updating & Building the Installer

This guide provides step-by-step instructions for updating Rinswa Browser, merging upstream Mozilla Firefox releases, and compiling the standalone Windows release installer (`.exe`).

---

## Architecture Overview

Rinswa uses an **overlay architecture**:
- **Source Engine:** Located in `rinswa-stable/` (Firefox stable engine).
- **Rinswa Customizations:** Stored cleanly in the root directory:
  - `branding/` — Logos, icons, branding properties, enterprise policies, and bundled extensions.
  - `ui/rinswa.css` — The complete Cyber-Glass browser UI stylesheet.
  - `ui/newtab-wallpaper.css` — Alpine Sunset wallpaper and minimal new tab styling.
  - `config/` — Build flags and mozconfig definitions.
  - `scripts/` — Automation scripts for deploying themes, preferences, and packaging.
- **The Orchestrator:** Running `./build.sh prepare` automatically merges and injects all Rinswa customizations into the Gecko engine.

---

## Prerequisites

Before building or packaging, ensure you have:
1. **Windows 10 / 11 (64-bit)**
2. **Visual Studio 2022 Community / Professional:**
   - Workload: *Desktop development with C++*
   - Component: *Windows 10 or 11 SDK* (latest)
3. **Python 3.11+** installed and available in PATH.
4. **Git for Windows** (with Git Bash).
5. **MozillaBuild:** (Standard MSYS2 environment for Firefox builds, default path `C:\mozilla-build`).

---

## Workflow 1: Building & Packaging Rinswa (Current Version)

Follow these steps if you made UI changes, modified preferences, or want to create a new `.installer.exe`.

### Step 1: Apply Rinswa Customizations
Open Git Bash (or PowerShell) in the project root:

```bash
cd /c/Users/arind/OneDrive/Documents/Project/browser
./build.sh prepare
```

This automatically:
- Injects `ui/rinswa.css` into `browser/themes/windows/browser.css`.
- Injects `ui/newtab-wallpaper.css` and copies wallpapers into all new tab stylesheets.
- Deploys `branding/distribution/policies.json` and `branding/distribution/extensions/uBlock0@raymondhill.net.xpi`.
- Deploys `firefox-branding.js` default preferences.

### Step 2: Compile the Engine
Navigate into the engine directory and compile:

```bash
cd /c/Users/arind/OneDrive/Documents/Project/browser/rinswa-stable

# Full multi-core compile (recommended):
python ./mach build -j16
```

*(Optional quick rebuild: If you only modified CSS, JS, or XUL files, you can run `python ./mach build faster` for near-instant updates).*

### Step 3: Package the Windows Installer
Run the packaging command:

```bash
cd /c/Users/arind/OneDrive/Documents/Project/browser/rinswa-stable

# Run packaging script or mach directly:
python ./mach package
```

*(Alternatively, run `./scripts/run-package.sh` from the root directory).*

### Step 4: Locate the Output Installer
Upon completion, the release installer will be generated at:
```
rinswa-stable/obj-rinswa/dist/install/sea/rinswa-<version>.en-US.win64.installer.exe
```
A portable zip archive is also created at:
```
rinswa-stable/obj-rinswa/dist/rinswa-<version>.en-US.win64.zip
```

---

## Workflow 2: Upstream Firefox Engine Update

When Mozilla releases a new version of Firefox (for example, Firefox 158 or a minor security update like 157.0.2 → 157.0.3), follow these steps to incorporate the update into Rinswa.

### Step 1: Save Current In-Tree Rinswa Modifications
Before pulling code from Mozilla, save your local modifications inside `rinswa-stable`:

```bash
cd /c/Users/arind/OneDrive/Documents/Project/browser/rinswa-stable
git add -A
git commit -m "chore: save local Rinswa changes before upstream merge"
```

### Step 2: Fetch and Merge Upstream Mozilla
Fetch the latest tags and branches from the official Firefox repository:

```bash
cd /c/Users/arind/OneDrive/Documents/Project/browser/rinswa-stable

# Fetch upstream commits
git fetch origin

# Merge the latest release branch (or specific release tag like FIREFOX_158_0_RELEASE)
git merge origin/release
```

#### Resolving Merge Conflicts:
If Git flags conflicts, keep the Rinswa enhancements:
- `browser/installer/package-manifest.in`: Ensure `@RESPATH@/distribution/*` remains included without `#if defined(BUILT_BY_MOZILLA)`.
- `browser/components/preferences/preferences.js`: Ensure `"adblocker"` remains in `CONFIG_PANES.privacy.groupIds`.
- `browser/components/preferences/config/privacy.mjs`: Keep the `adblocker` setting group and `Preferences.addSetting({ id: "adblockerEnabled", ... })`.
- `browser/components/aiwindow/ui/modules/AIWindow.sys.mjs`: Keep `_updateGroupTabsButtonVisibility` with `lazy.autoTabGroupingEnabled && (this.isAIWindowActive(node.documentGlobal) || this.isAIWindowEnabled())`.

After resolving any conflicts:
```bash
git add -A
git commit -m "merge: upstream Firefox release update"
```

### Step 3: Bump the Rinswa Version Numbers
Update the version string across the project:
1. `rinswa-stable/browser/config/version.txt` → Update to new version (e.g. `1.0.3`)
2. `rinswa-stable/browser/config/version_display.txt` → Update to new version (e.g. `1.0.3`)
3. `README.md` → Update version badge (e.g. `1.0.3_Stable`)

### Step 4: Re-apply Rinswa Customizations
Run the preparation script from the repository root:

```bash
cd /c/Users/arind/OneDrive/Documents/Project/browser
./build.sh prepare
```

### Step 5: Re-compile & Package
```bash
cd /c/Users/arind/OneDrive/Documents/Project/browser/rinswa-stable

# Compile the new engine
python ./mach build -j16

# Package the installer
python ./mach package
```

---

## Workflow 3: Publishing the Update to Users

Once the installer `.exe` is generated, follow these steps to release it to existing and new users.

### Step 1: Calculate File Hash & Size
Open PowerShell and run:

```powershell
# Get SHA-256 hash of the installer:
Get-FileHash rinswa-stable\obj-rinswa\dist\install\sea\*.installer.exe

# Get exact size in bytes:
(Get-Item rinswa-stable\obj-rinswa\dist\install\sea\*.installer.exe).Length
```

### Step 2: Update `update.xml`
Edit `update.xml` in the root of the repository with the new release information:

```xml
<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="1.0.3" appVersion="1.0.3" platformVersion="158.0.0" buildID="20261004190000">
        <patch type="complete" 
               URL="https://github.com/deadxfire/Rinswa-browser/releases/download/v1.0.3/rinswa-1.0.3.en-US.win64.installer.exe" 
               hashFunction="SHA256" 
               hashValue="<INSERT_SHA256_HASH_HERE>" 
               size="<INSERT_SIZE_IN_BYTES_HERE>"/>
    </update>
</updates>
```

### Step 3: Commit, Tag, and Push to GitHub
In the root repository:

```bash
cd /c/Users/arind/OneDrive/Documents/Project/browser

# Stage and commit
git add -A
git commit -m "release: v1.0.3 release update"

# Create git tag
git tag -a v1.0.3 -m "Rinswa Browser Stable v1.0.3"

# Push main branch and tags
git push origin main --tags

# Update stable branch
git checkout stable
git merge main --ff-only
git push origin stable
git checkout main
```

### Step 4: Publish GitHub Release
1. Open your browser and go to: `https://github.com/deadxfire/Rinswa-browser/releases`
2. Click **Draft a new release**.
3. Choose the tag you just created (e.g. `v1.0.3`).
4. Set the title to `Rinswa Browser Stable v1.0.3`.
5. Upload the compiled installer file from:
   `rinswa-stable/obj-rinswa/dist/install/sea/rinswa-<version>.en-US.win64.installer.exe`
6. Click **Publish release**.

Existing Rinswa users will automatically detect the new update through `update.xml` and can update directly with one click!

---

## Troubleshooting & Important Notes

- **Antivirus Locking Binaries:** If `mach build` or `mach package` fails with `Access is denied` or `Permission denied` on `obj-rinswa/dist/bin/rinswa.exe`, ensure Rinswa is closed and add `obj-rinswa` to Windows Defender exclusions.
- **Distribution Directory Packaging:** Never wrap `@RESPATH@/distribution/*` with `#if defined(BUILT_BY_MOZILLA)` in `package-manifest.in`. In non-Mozilla community builds, that macro is false, which will cause the installer to drop `policies.json` and `distribution/extensions/uBlock0@raymondhill.net.xpi`.
- **Testing Clean Profile:** To test how clean installations behave on a fresh machine:
  ```bash
  rinswa-stable/obj-rinswa/dist/bin/rinswa.exe -ProfileManager -no-remote
  ```
  Create a temporary new profile to verify default ad blocking, Smart Window widgets, and light mode readability.
