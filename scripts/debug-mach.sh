#!/usr/bin/env bash
cd /c/Users/arind/OneDrive/Documents/Project/browser/mozilla-central || exit 1
export PATH="/c/Users/arind/AppData/Local/Python/pythoncore-3.11-64:$PATH"
export MACH_HIDE_DEV_DRIVE_SUGGESTION=1
export MOZCONFIG=/c/Users/arind/OneDrive/Documents/Project/browser/config/mozconfig.windows

echo "Running mach bootstrap with global --no-interactive..."
python ./mach --no-interactive bootstrap --application-choice=browser
echo "Bootstrap exit code: $?"
