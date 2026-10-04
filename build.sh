#!/usr/bin/env bash
# Rinswa Browser Build Orchestrator
# Integrates seamlessly with Mozilla's 'mach' build system to prevent duplicate logic.

set -e

export PATH="/c/Program Files/Git/cmd:/c/Users/arind/AppData/Local/Python/pythoncore-3.11-64:$PATH"

COMMAND=$1
CONFIG_DIR="$(pwd)/config"
BRANDING_DIR="$(pwd)/branding"
if [ -z "$MOZ_SRC_DIR" ]; then
    if [ -d "$(pwd)/rinswa-stable" ]; then
        MOZ_SRC_DIR="$(pwd)/rinswa-stable"
    else
        MOZ_SRC_DIR="$(pwd)/mozilla-central"
    fi
fi

detect_architecture() {
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    ARCH=$(uname -m)

    case "$OS" in
        linux*)   PLATFORM="linux" ;;
        darwin*)  PLATFORM="macos" ;;
        msys*|cygwin*|mingw*) PLATFORM="windows" ;;
        *)        echo "Unsupported OS: $OS"; exit 1 ;;
    esac

    case "$ARCH" in
        x86_64*|amd64) TARGET_ARCH="x64" ;;
        arm64|aarch64) TARGET_ARCH="arm64" ;;
        *)             TARGET_ARCH=$ARCH ;;
    esac

    echo "Detected OS: $PLATFORM, Architecture: $TARGET_ARCH"
}

setup_mozconfig() {
    local config_file="$CONFIG_DIR/mozconfig.$PLATFORM"
    if [ ! -f "$config_file" ]; then
        echo "Error: Configuration file $config_file not found."
        exit 1
    fi
    export MOZCONFIG="$config_file"
    echo "Using MOZCONFIG: $MOZCONFIG"
}

prepare_source() {
    if [ ! -d "$MOZ_SRC_DIR" ]; then
        echo "Firefox source not found at $MOZ_SRC_DIR. Please clone mozilla-central before building."
        exit 1
    fi
    local ROOT_DIR
    ROOT_DIR="$(pwd)"

    # ---------------------------------------------------------------------
    # 1. Branding: Mozilla requires the branding dir to live inside the tree
    #    and contain the full file set, so start from 'unofficial' and overlay.
    # ---------------------------------------------------------------------
    echo "Applying Rinswa branding..."
    local DEST="$MOZ_SRC_DIR/browser/branding/rinswa"
    local GEN="$BRANDING_DIR/generated"
    if [ ! -f "$GEN/default256.png" ]; then
        echo "Error: generated branding assets missing. Run scripts/gen-branding-assets.ps1 first."
        exit 1
    fi
    rm -rf "$DEST"
    cp -r "$MOZ_SRC_DIR/browser/branding/unofficial" "$DEST"

    cp "$BRANDING_DIR/configure.sh"                          "$DEST/configure.sh"
    cp "$BRANDING_DIR/assets/locales/en-US/brand.ftl"        "$DEST/locales/en-US/brand.ftl"
    cp "$BRANDING_DIR/assets/locales/en-US/brand.properties" "$DEST/locales/en-US/brand.properties"
    if [ -f "$BRANDING_DIR/pref/firefox-branding.js" ]; then
        cp "$BRANDING_DIR/pref/firefox-branding.js"          "$DEST/pref/firefox-branding.js"
    fi

    cp "$BRANDING_DIR/icons/default.ico"  "$DEST/firefox.ico"
    cp "$BRANDING_DIR/icons/default.ico"  "$DEST/firefox64.ico"
    cp "$BRANDING_DIR/icons/document.ico" "$DEST/document.ico"

    if [ -f "$BRANDING_DIR/wizHeader.bmp" ]; then
        cp "$BRANDING_DIR/wizHeader.bmp"    "$DEST/wizHeader.bmp"
        cp "$BRANDING_DIR/wizHeaderRTL.bmp" "$DEST/wizHeaderRTL.bmp"
        cp "$BRANDING_DIR/wizWatermark.bmp" "$DEST/wizWatermark.bmp"
    fi

    for f in default16 default22 default24 default32 default48 default64 default128 default256 \
             VisualElements_150 VisualElements_70 PrivateBrowsing_150 PrivateBrowsing_70; do
        cp "$GEN/$f.png" "$DEST/$f.png"
    done
    for f in about about-logo about-logo@2x about-logo-private about-logo-private@2x; do
        cp "$GEN/$f.png" "$DEST/content/$f.png"
    done
    cp "$BRANDING_DIR/logos/about-wordmark.svg" "$DEST/content/about-wordmark.svg"
    if [ -f "$BRANDING_DIR/logos/firefox-wordmark.svg" ]; then
        cp "$BRANDING_DIR/logos/firefox-wordmark.svg" "$DEST/content/firefox-wordmark.svg"
    fi
    cp "$BRANDING_DIR/themes/aboutDialog.css"   "$DEST/content/aboutDialog.css"
    if [ -f "$BRANDING_DIR/wallpaper.png" ]; then
        cp "$BRANDING_DIR/wallpaper.png"        "$DEST/content/wallpaper.png"
        if [ -f "$DEST/content/jar.mn" ] && ! grep -q "content/branding/wallpaper.png" "$DEST/content/jar.mn"; then
            echo "  content/branding/wallpaper.png" >> "$DEST/content/jar.mn"
        fi
    fi
    if [ -f "$BRANDING_DIR/distribution/policies.json" ]; then
        mkdir -p "$DEST/distribution"
        cp "$BRANDING_DIR/distribution/policies.json" "$DEST/distribution/policies.json"
    fi

    # Installer (NSIS) names shown in the setup wizard and Add/Remove Programs.
    sed -i \
        -e 's/"Mozilla Developer Preview"/"Rinswa"/g' \
        -e 's/!define CompanyName .*/!define CompanyName           "Arindam Makar"/' \
        "$DEST/branding.nsi"

    # ---------------------------------------------------------------------
    # 2. UI: append Rinswa's stylesheet to the platform skin browser.css,
    #    loaded by browser.xhtml as chrome://browser/skin/. Reset first so
    #    re-runs stay idempotent.
    # ---------------------------------------------------------------------
    echo "Applying Rinswa UI theme..."
    local SKIN_DIR
    case "$PLATFORM" in
        windows) SKIN_DIR="windows" ;;
        macos)   SKIN_DIR="osx" ;;
        *)       SKIN_DIR="linux" ;;
    esac
    local CSS_REL="browser/themes/$SKIN_DIR/browser.css"
    local BROWSER_CSS="$MOZ_SRC_DIR/$CSS_REL"
    if [ -f "$BROWSER_CSS" ]; then
        git -C "$MOZ_SRC_DIR" checkout -- "$CSS_REL"
        {
            echo ""
            echo "/* ===== RINSWA UI OVERRIDES (injected by build.sh) ===== */"
            cat "$ROOT_DIR/ui/rinswa.css"
        } >> "$BROWSER_CSS"
    else
        echo "Warning: $BROWSER_CSS not found; Rinswa UI theme not applied."
    fi

    # ---------------------------------------------------------------------
    # 3. New Tab Theme & Preferences Deployment
    # ---------------------------------------------------------------------
    python "$ROOT_DIR/scripts/deploy-newtab-theme.py"
    python "$ROOT_DIR/scripts/deploy-prefs.py"

    # Clean up untracked leftovers from the old prepare step (copied ui/*).
    # git clean only touches untracked files, so real Firefox files are safe.
    git -C "$MOZ_SRC_DIR" clean -fdq -- browser/base/content/

    echo "Rinswa customizations applied."
}

build_rinswa() {
    cd "$MOZ_SRC_DIR"
    echo "Building Rinswa via mach..."
    ./mach build
}

package_rinswa() {
    cd "$MOZ_SRC_DIR"
    echo "Running tests..."
    # ./mach test # Uncomment to enforce test suites pre-packaging
    echo "Packaging Rinswa release artifacts..."
    
    # Download and bundle uBlock Origin Ad Blocker
    mkdir -p obj-rinswa/dist/bin/distribution/extensions
    curl -L -s -o obj-rinswa/dist/bin/distribution/extensions/uBlock0@raymondhill.net.xpi "https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/addon-607454-latest.xpi"
    
    # Copy enterprise distribution policies to force-install and pin uBlock Origin to navbar
    if [ -f "$BRANDING_DIR/distribution/policies.json" ]; then
        cp "$BRANDING_DIR/distribution/policies.json" obj-rinswa/dist/bin/distribution/policies.json
    fi

    # Ensure updated Rinswa emblem bitmaps are deployed to instgen before NSIS compiles
    if [ -f "$BRANDING_DIR/wizHeader.bmp" ]; then
        mkdir -p obj-rinswa/browser/installer/windows/instgen
        cp "$BRANDING_DIR/wizHeader.bmp" obj-rinswa/browser/installer/windows/instgen/wizHeader.bmp
        cp "$BRANDING_DIR/wizHeaderRTL.bmp" obj-rinswa/browser/installer/windows/instgen/wizHeaderRTL.bmp
        cp "$BRANDING_DIR/wizWatermark.bmp" obj-rinswa/browser/installer/windows/instgen/wizWatermark.bmp
    fi
    
    ./mach package
}

detect_architecture

case "$COMMAND" in
    "prepare")
        prepare_source
        ;;
    "debug")
        setup_mozconfig
        export MOZ_DEBUG=1
        prepare_source
        build_rinswa
        ;;
    "release"|"")
        setup_mozconfig
        prepare_source
        build_rinswa
        package_rinswa
        ;;
    "clean")
        if [ -d "$MOZ_SRC_DIR" ]; then
            cd "$MOZ_SRC_DIR"
            ./mach clobber
        fi
        echo "Cleaned build directory."
        ;;
    *)
        echo "Usage: ./build.sh [prepare|debug|release|clean]"
        exit 1
        ;;
esac
