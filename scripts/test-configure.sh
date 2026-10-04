#!/usr/bin/env bash
cd /c/rinswa/mozilla-central || exit 1
export PATH="/c/Users/arind/AppData/Local/Python/pythoncore-3.11-64:$PATH"
export MACH_HIDE_DEV_DRIVE_SUGGESTION=1
export MOZCONFIG=/c/rinswa/config/mozconfig.windows

echo "Running mach configure test via junction /c/rinswa..."
python ./mach configure
echo "Configure exit code: $?"
