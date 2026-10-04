#!/usr/bin/env bash
set -e
cd /c/Users/arind/OneDrive/Documents/Project/browser/mozilla-central
export PATH="/c/Users/arind/AppData/Local/Python/pythoncore-3.11-64:$PATH"
export MOZCONFIG="/c/Users/arind/OneDrive/Documents/Project/browser/config/mozconfig.windows"
export MACH_HIDE_DEV_DRIVE_SUGGESTION=1

echo ">>> Launching mach build with verbose logging..."
python ./mach build --verbose
