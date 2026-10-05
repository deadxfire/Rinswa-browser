#!/usr/bin/env python3
"""
Rinswa Browser - Release Metadata & Update Feed Generator
Calculates exact SHA-256 hash and byte size of the packaged installer (.exe/.mar),
updates update.xml with complete cryptographic integrity metadata,
and outputs checksums for GitHub Releases.
"""

import os
import sys
import re
import hashlib
import glob

def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dist_dir = os.path.join(root, "rinswa-stable", "obj-rinswa", "dist")
    
    ver_path = os.path.join(root, "rinswa-stable", "browser", "config", "version.txt")
    version = "1.0.4"
    if os.path.exists(ver_path):
        with open(ver_path, "r", encoding="utf-8") as f:
            v = f.read().strip()
            if v:
                version = v

    print(f"\n[Release Metadata Generator] Checking artifacts for Rinswa v{version}...")
    
    # Locate installer executable
    installer_path = os.path.join(dist_dir, f"rinswa-{version}.en-US.win64.installer.exe")
    if not os.path.exists(installer_path):
        # Fallback search for any installer in dist
        found = glob.glob(os.path.join(dist_dir, f"*{version}*.installer.exe"))
        if found:
            installer_path = found[0]

    if not os.path.exists(installer_path):
        print(f"[!] Installer not found at {installer_path}. Skipping update.xml patch calculation.")
        return

    # Calculate SHA256 and byte size
    with open(installer_path, "rb") as f:
        sha256_hash = hashlib.sha256(f.read()).hexdigest()
    file_size = os.path.getsize(installer_path)

    print(f"[OK] Found Installer: {os.path.basename(installer_path)}")
    print(f"     Size:   {file_size:,} bytes")
    print(f"     SHA256: {sha256_hash}")

    # Write / Update update.xml
    update_xml_path = os.path.join(root, "update.xml")
    if os.path.exists(update_xml_path):
        with open(update_xml_path, "r", encoding="utf-8") as f:
            content = f.read()

        content = re.sub(r'displayVersion="[^"]*"', f'displayVersion="{version}"', content)
        content = re.sub(r'appVersion="[^"]*"', f'appVersion="{version}"', content)
        content = re.sub(
            r'URL="https://github.com/deadxfire/Rinswa-browser/releases/download/v[^/]*/rinswa-[^.]*.en-US.win64.installer.exe"',
            f'URL="https://github.com/deadxfire/Rinswa-browser/releases/download/v{version}/rinswa-{version}.en-US.win64.installer.exe"',
            content
        )
        content = re.sub(r'hashValue="[^"]*"', f'hashValue="{sha256_hash}"', content)
        content = re.sub(r'size="[^"]*"', f'size="{file_size}"', content)

        with open(update_xml_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"[OK] Successfully updated update.xml with exact hash and size for v{version}!")

    # Write SHA256SUMS.txt
    sums_path = os.path.join(dist_dir, "SHA256SUMS.txt")
    with open(sums_path, "w", encoding="utf-8") as f:
        f.write(f"{sha256_hash}  {os.path.basename(installer_path)}\n")
    print(f"[OK] Generated {sums_path}\n")

if __name__ == "__main__":
    main()
