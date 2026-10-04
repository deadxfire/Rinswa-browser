# Building Rinswa on macOS

## Architecture Support
- **macOS Intel** (x64)
- **macOS Apple Silicon** (ARM64 / M1, M2, M3, M4)

## Prerequisites & Dependencies
1. **Xcode:** Install via the Mac App Store.
2. **Command Line Tools:** Run `xcode-select --install` in the terminal.
3. **Homebrew:** Highly recommended for bootstrapping the environment.
4. **Mach Bootstrap:** Run `./mach bootstrap` in the `mozilla-central` folder to automatically fetch Clang, Node.js, and Rust.

## Build Commands
Open Terminal, navigate to the Rinswa directory, and run:

- `./build.sh release` - Prepares the source, applies the Rinswa `mozconfig.macos`, compiles the application, and bundles the `.app`.
- `./build.sh debug` - Builds a non-optimized version for development.
- `./build.sh clean` - Clears the build cache and `obj-dir`.

The build script detects your native CPU architecture automatically and passes it to the underlying `mach` system.

## Packaging
Running a release build will output:
- **Rinswa.app:** The macOS application bundle.
- **DMG:** A distributable `.dmg` file for drag-and-drop installation.

## Troubleshooting
- **Universal Builds:** To build a Universal Binary containing both Intel and ARM64 slices, you must explicitly declare cross-compilation targets in `config/mozconfig.macos`.
- **Code Signing:** Local builds are ad-hoc signed. For official distribution, ensure Apple Developer Certificates are available in the environment to avoid Gatekeeper blocks.
