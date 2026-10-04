# Building Rinswa on Windows

## Architecture Support
- **Windows x64** (Intel/AMD)
- **Windows ARM64** (Snapdragon)

## Prerequisites & Dependencies
Rinswa leverages the standard Mozilla build toolchain for Windows:
1. **Visual Studio 2022:** Requires the "Desktop Development with C++" workload and the Windows 11 SDK.
2. **MozillaBuild:** The official MSYS2-based environment required for compiling Gecko on Windows.
3. **Rust:** Latest stable version (usually managed by `mach bootstrap`).

## Build Commands
Open the **MozillaBuild shell** (`start-shell.bat`), navigate to the Rinswa source directory, and run:

- `./build.sh release` - Prepares the source, applies the Rinswa `mozconfig.windows`, compiles the browser, and packages the installer.
- `./build.sh debug` - Builds a non-optimized debug version for development.
- `./build.sh clean` - Cleans the `obj-dir`.

*Note: The orchestrator script (`build.sh`) automatically detects your architecture (x64 or ARM64) and applies `config/mozconfig.windows` accordingly.*

## Packaging
Running `./build.sh release` successfully invokes `./mach package`, which produces:
- **Installer:** A standard NSIS installer (`rinswa-installer.exe`).
- **Portable Build:** A `.zip` archive containing the compiled binaries, executable without installation.

## Troubleshooting
- **Missing SDKs:** Ensure the Windows 11 SDK is installed via the Visual Studio Installer.
- **Path Issues:** Do not place the source tree in a directory with spaces in the name (e.g. avoid `C:\My Documents\`).
