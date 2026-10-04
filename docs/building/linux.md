# Building Rinswa on Linux

## Architecture Support
- **Linux x64**
- **Linux ARM64** (Supported where practical, e.g., high-end ARM servers or SBCs)

## Prerequisites & Dependencies
Dependencies vary by distribution. For Debian/Ubuntu-based systems:
1. `sudo apt-get install build-essential python3 python3-dev curl m4`
2. **Mach Bootstrap:** Navigate to the `mozilla-central` folder and run `./mach bootstrap`. This will install Clang, Rust, GTK+3, Wayland development headers, Node.js, and other required packages.

## Build Commands
Open your terminal, navigate to the Rinswa directory, and run:

- `./build.sh release` - Prepares the source, applies `config/mozconfig.linux`, compiles the browser, and packages the tarball.
- `./build.sh debug` - Creates a debug build for development.
- `./build.sh clean` - Wipes the build directory.

## Packaging
The Linux build process produces:
- **Tarball:** A `rinswa-<version>.tar.bz2` archive containing the executable binaries.
- **AppImage:** (Future capability) Scripts wrapping the tarball output to create a distro-agnostic `.AppImage`.
- **Distribution Packages:** Flatpak or Snap configurations can be hooked post-build using standard Linux packaging tools wrapping the tarball.

## Troubleshooting
- **Wayland vs X11:** The default `mozconfig.linux` enables Wayland and X11 support via `cairo-gtk3-wayland`. Ensure your environment has the necessary Wayland protocols installed.
- **Memory Requirements:** Linking `libxul` requires a significant amount of RAM. Ensure your build machine has at least 16GB of RAM or a large swap file, otherwise the linker (`lld` or `gold`) will crash with an OOM error.
