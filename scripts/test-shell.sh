#!/usr/bin/env bash
echo "=== HELLO FROM MOZILLABUILD BASH ==="
which python3
python3 --version
cd /c/Users/arind/OneDrive/Documents/Project/browser/mozilla-central || exit 1
git log -1 --format="%H %cd %s"
./mach --version
