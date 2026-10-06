#!/usr/bin/env bash
# ==============================================================================
# Rinswa Browser Stable (1.0.1) Build Pipeline
# Developed and made by Arindam Makar
# Target: Windows x64 Standalone Executable & Installer
# ==============================================================================

set -e

PROJECT_DIR="/c/Users/arind/OneDrive/Documents/Project/browser"
MOZ_DIR="$PROJECT_DIR/rinswa-stable"
CONFIG_FILE="$PROJECT_DIR/config/mozconfig.windows"

# Dynamically load version from rinswa-version.txt
VERSION="1.0.5"
if [ -f "$PROJECT_DIR/rinswa-version.txt" ]; then
    VERSION=$(tr -d '\r\n ' < "$PROJECT_DIR/rinswa-version.txt")
fi

# Put Python 3.11 and Git at front of PATH for MSYS2
export PATH="/c/Program Files/Git/cmd:/c/Users/arind/AppData/Local/Python/pythoncore-3.11-64:$PATH"
export MOZCONFIG="$CONFIG_FILE"
export MOZ_SRC_DIR="$MOZ_DIR"
export MACH_HIDE_DEV_DRIVE_SUGGESTION=1
export DISABLE_TELEMETRY=1
export MOZ_NOSPAM=1

echo "======================================================="
echo "     RINSWA BROWSER STABLE (v$VERSION) BUILD SYSTEM"
echo "        Developed and made by Arindam Makar"
echo "======================================================="
echo "Active Python: $(command -v python) ($(python --version 2>&1 || true))"
echo "Version:       $VERSION Stable"
echo "Project Path:  $PROJECT_DIR"
echo "Source Tree:   $MOZ_DIR"
echo "Mozconfig:     $MOZCONFIG"
echo "======================================================="
echo ""

STEP=${1:-"all"}

run_bootstrap() {
    echo ""
    echo "[Step 1/4] Checking compiler toolchains and SDKs for Rinswa Stable..."
    cd "$MOZ_DIR"
    if [ -f "$MOZ_DIR/obj-rinswa/buildid.h" ] || [ -f "$HOME/.mozbuild/toolchains/clang-dist-toolchain.tar.xz" ]; then
        echo "Toolchains already configured and verified. Skipping bootstrap."
    else
        python ./mach --no-interactive bootstrap --application-choice=browser
    fi
    echo ">> Step 1 (Bootstrap) complete."
}

run_prepare() {
    echo ""
    echo "[Step 2/4] Applying Rinswa branding, Cyber-Glass UI, and v$VERSION settings..."
    cd "$PROJECT_DIR"
    export MOZ_SRC_DIR="$MOZ_DIR"
    ./build.sh prepare
    echo ">> Step 2 (Customization injection) complete."
}

run_compile() {
    echo ""
    echo "[Step 3/4] Compiling Gecko Engine into Rinswa Stable v$VERSION..."
    cd "$MOZ_DIR"
    python ./mach build -j16
    echo ">> Step 3 (Compilation) complete."
}

run_package() {
    echo ""
    echo "[Step 4/4] Packaging standalone Rinswa Stable installer (.exe)..."
    cd "$MOZ_DIR"
    
    # Download and bundle uBlock Origin Ad Blocker
    mkdir -p obj-rinswa/dist/bin/distribution/extensions
    curl -L -s -o obj-rinswa/dist/bin/distribution/extensions/uBlock0@raymondhill.net.xpi "https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/addon-607454-latest.xpi"
    
    # Bundle native Rinswa Smart Tab Manager & Clean Tabs
    if [ -f "$PROJECT_DIR/branding/distribution/extensions/smart-tabs@rinswa.com.xpi" ]; then
        cp "$PROJECT_DIR/branding/distribution/extensions/smart-tabs@rinswa.com.xpi" obj-rinswa/dist/bin/distribution/extensions/smart-tabs@rinswa.com.xpi
    fi

    # Copy enterprise distribution policies to force-install and pin extensions to navbar
    if [ -f "$PROJECT_DIR/branding/distribution/policies.json" ]; then
        cp "$PROJECT_DIR/branding/distribution/policies.json" obj-rinswa/dist/bin/distribution/policies.json
    fi

    # Ensure updated Rinswa emblem bitmaps are deployed to instgen before NSIS compiles
    if [ -f "$PROJECT_DIR/branding/wizHeader.bmp" ]; then
        mkdir -p obj-rinswa/browser/installer/windows/instgen
        cp "$PROJECT_DIR/branding/wizHeader.bmp" obj-rinswa/browser/installer/windows/instgen/wizHeader.bmp
        cp "$PROJECT_DIR/branding/wizHeaderRTL.bmp" obj-rinswa/browser/installer/windows/instgen/wizHeaderRTL.bmp
        cp "$PROJECT_DIR/branding/wizWatermark.bmp" obj-rinswa/browser/installer/windows/instgen/wizWatermark.bmp
    fi
    
    python ./mach package
    if [ -f "$PROJECT_DIR/scripts/update-release-metadata.py" ]; then
        python "$PROJECT_DIR/scripts/update-release-metadata.py" || true
    fi
    echo ">> Step 4 (Packaging) complete."
}

case "$STEP" in
    bootstrap)
        run_bootstrap
        ;;
    prepare)
        run_prepare
        ;;
    compile)
        run_compile
        ;;
    package)
        run_package
        ;;
    all)
        run_bootstrap
        run_prepare
        run_compile
        run_package
        ;;
    *)
        echo "Unknown step: $STEP"
        echo "Valid steps: bootstrap | prepare | compile | package | all"
        exit 1
        ;;
esac
