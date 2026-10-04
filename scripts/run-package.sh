#!/usr/bin/env bash
export PATH="/c/Program Files/Git/cmd:/c/Users/arind/AppData/Local/Python/pythoncore-3.11-64:$PATH"
export MOZCONFIG="/c/Users/arind/OneDrive/Documents/Project/browser/config/mozconfig.windows"
PROJECT_DIR="/c/Users/arind/OneDrive/Documents/Project/browser"
cd "/c/Users/arind/OneDrive/Documents/Project/browser/rinswa-stable"

mkdir -p obj-rinswa/dist/bin/distribution/extensions
if [ ! -f obj-rinswa/dist/bin/distribution/extensions/uBlock0@raymondhill.net.xpi ]; then
    curl -L -s -o obj-rinswa/dist/bin/distribution/extensions/uBlock0@raymondhill.net.xpi "https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/addon-607454-latest.xpi"
fi

if [ -f "$PROJECT_DIR/branding/distribution/policies.json" ]; then
    cp "$PROJECT_DIR/branding/distribution/policies.json" obj-rinswa/dist/bin/distribution/policies.json
fi

if [ -f "$PROJECT_DIR/branding/wizHeader.bmp" ]; then
    mkdir -p obj-rinswa/browser/installer/windows/instgen
    cp "$PROJECT_DIR/branding/wizHeader.bmp" obj-rinswa/browser/installer/windows/instgen/wizHeader.bmp
    cp "$PROJECT_DIR/branding/wizHeaderRTL.bmp" obj-rinswa/browser/installer/windows/instgen/wizHeaderRTL.bmp
    cp "$PROJECT_DIR/branding/wizWatermark.bmp" obj-rinswa/browser/installer/windows/instgen/wizWatermark.bmp
fi

python ./mach package
