#!/usr/bin/env bash
# ==============================================================================
# Rinswa Browser Automated Build Pipeline
# Author: Arindam Makar
# Target: Windows x64 Standalone Executable & Installer
# ==============================================================================

set -e

PROJECT_DIR="/c/Users/arind/OneDrive/Documents/Project/browser"
MOZ_DIR="$PROJECT_DIR/mozilla-central"
CONFIG_FILE="$PROJECT_DIR/config/mozconfig.windows"

# Put Python 3.11 at front of PATH for MSYS2
export PATH="/c/Users/arind/AppData/Local/Python/pythoncore-3.11-64:$PATH"
export MOZCONFIG="$CONFIG_FILE"
export MACH_HIDE_DEV_DRIVE_SUGGESTION=1
export DISABLE_TELEMETRY=1
export MOZ_TELEMETRY_REPORTING=0
export MOZ_NOSPAM=1

echo "======================================================="
echo "        RINSWA BROWSER BUILD ORCHESTRATION"
echo "        Developed and made by Arindam Makar"
echo "======================================================="
echo "Active Python: $(command -v python) ($(python --version))"
echo "Project Path:  $PROJECT_DIR"
echo "Source Tree:   $MOZ_DIR"
echo "Mozconfig:     $MOZCONFIG"
echo "======================================================="
echo ""

STEP=${1:-"all"}

run_bootstrap() {
    echo ""
    echo "[Step 1/4] Checking compiler toolchains and SDKs..."
    cd "$MOZ_DIR"
    if [ -f "$MOZ_DIR/obj-rinswa/buildid.h" ] || [ -f "$HOME/.mozbuild/toolchains/clang-dist-toolchain.tar.xz" ]; then
        echo "Toolchains already configured and verified. Skipping redundant bootstrap prompt."
    else
        python ./mach --no-interactive bootstrap --application-choice=browser
    fi
    echo ">> Step 1 (Bootstrap) complete."
}

run_prepare() {
    echo ""
    echo "[Step 2/4] Applying custom Rinswa branding, icons, and UI overrides..."
    cd "$PROJECT_DIR"
    ./build.sh prepare
    echo ">> Step 2 (Customization injection) complete."
}

run_compile() {
    echo ""
    echo "[Step 3/4] Compiling Gecko Engine into Rinswa Browser..."
    echo ">> Running mozmake directly for live compiler & linker output..."
    cd "$MOZ_DIR"
    export MACH=1
    export OBJDIR="$MOZ_DIR/obj-rinswa"
    /c/Users/arind/.mozbuild/mozmake/mozmake.exe -f client.mk -j$(nproc)
    echo ">> Step 3 (Compilation) complete."
}

run_package() {
    echo ""
    echo "[Step 4/4] Packaging standalone Rinswa installer .exe..."
    cd "$MOZ_DIR"
    python ./mach package
    python ./mach build installer
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

echo ""
echo "======================================================="
echo "           RINSWA BUILD PIPELINE SUCCESS"
echo "======================================================="
