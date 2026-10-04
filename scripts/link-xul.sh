#!/usr/bin/env bash
cd /c/Users/arind/OneDrive/Documents/Project/browser/mozilla-central || exit 1
export PATH="/c/Users/arind/AppData/Local/Python/pythoncore-3.11-64:$PATH"
export MACH_HIDE_DEV_DRIVE_SUGGESTION=1
export MOZCONFIG="/c/Users/arind/OneDrive/Documents/Project/browser/config/mozconfig.windows"

echo "=== Resuming Build for toolkit/library ==="
python ./mach build toolkit/library/build
echo "mach build toolkit/library/build exit code: $?"
