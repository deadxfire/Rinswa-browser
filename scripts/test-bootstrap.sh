#!/usr/bin/env bash
set -e
export MACH_HIDE_DEV_DRIVE_SUGGESTION=1
export MOZCONFIG=/c/Users/arind/OneDrive/Documents/Project/browser/config/mozconfig.windows

cd /c/Users/arind/OneDrive/Documents/Project/browser/mozilla-central
echo "Testing mach bootstrap dry run / artifact check on latest commit..."
python3 ./mach --no-interactive bootstrap --application-choice=browser
