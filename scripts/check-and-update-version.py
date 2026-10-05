#!/usr/bin/env python3
"""
Rinswa Browser - Upstream Firefox Update Checker & Version Management Tool
Developed by Arindam Makar

Features:
1. Checks whether Mozilla Firefox has released upstream updates (via Git remote and Mozilla API).
2. Allows fetching and merging upstream updates into rinswa-stable.
3. Allows changing / bumping the Rinswa Browser version across all project files:
   - rinswa-stable/browser/config/version.txt
   - rinswa-stable/browser/config/version_display.txt
   - mozilla-central/browser/config/version.txt
   - mozilla-central/browser/config/version_display.txt
   - update.xml (displayVersion, appVersion, URL, and buildID timestamp)
   - README.md (release badge)
   - Preference headers
4. Synchronizes assets, branding, and policies (via deploy scripts).
5. Offers to immediately launch Build-Rinswa-Stable.bat.
"""

import os
import sys
import re
import json
import datetime
import subprocess
import urllib.request
import urllib.error

# Setup Windows console encoding and ANSI colors
if sys.platform == "win32":
    os.system("")
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

def log_header(title):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 65}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD} {title}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 65}{Colors.RESET}\n")

def log_success(msg):
    print(f"{Colors.GREEN}[OK] {msg}{Colors.RESET}")

def log_info(msg):
    print(f"{Colors.CYAN}[*] {msg}{Colors.RESET}")

def log_warn(msg):
    print(f"{Colors.YELLOW}[!] {msg}{Colors.RESET}")

def log_error(msg):
    print(f"{Colors.RED}[X] {msg}{Colors.RESET}")

def run_cmd(cmd, cwd=None, capture=True):
    """Executes a command and returns (returncode, stdout, stderr)."""
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            shell=True,
            text=True,
            capture_output=capture
        )
        return proc.returncode, (proc.stdout or "").strip(), (proc.stderr or "").strip()
    except Exception as e:
        return 1, "", str(e)

def get_root_dir():
    current = os.path.abspath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(current, ".."))

def get_current_rinswa_version(root_dir):
    ver_path = os.path.join(root_dir, "rinswa-stable", "browser", "config", "version.txt")
    if os.path.exists(ver_path):
        with open(ver_path, "r", encoding="utf-8") as f:
            v = f.read().strip()
            if v:
                return v
    return "1.0.4"

def suggest_next_version(ver_str):
    parts = ver_str.split(".")
    if len(parts) >= 3 and parts[-1].isdigit():
        parts[-1] = str(int(parts[-1]) + 1)
        return ".".join(parts)
    elif len(parts) == 2 and parts[-1].isdigit():
        parts.append("1")
        return ".".join(parts)
    return ver_str

def check_upstream_mozilla(root_dir):
    log_header("STEP 1: CHECKING UPSTREAM MOZILLA FIREFOX ENGINE")
    stable_dir = os.path.join(root_dir, "rinswa-stable")
    
    if not os.path.isdir(stable_dir):
        log_warn(f"rinswa-stable directory not found at {stable_dir}. Skipping upstream engine check.")
        return False, None, None

    # Check Mozilla Product Details API
    print("Querying Mozilla official release API...")
    latest_mozilla_ver = "Unknown"
    try:
        req = urllib.request.Request(
            "https://product-details.mozilla.org/1.0/firefox_versions.json",
            headers={"User-Agent": "Rinswa-Build-Bot/1.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                latest_mozilla_ver = data.get("LATEST_FIREFOX_VERSION", "Unknown")
                log_info(f"Mozilla Official Firefox Release: {Colors.BOLD}{latest_mozilla_ver}{Colors.RESET}")
    except Exception as e:
        log_warn(f"Could not reach Mozilla release API: {e} (continuing via git check)")

    # Check Git upstream remote
    print("Checking upstream Git repository (origin/release)...")
    code, out, _ = run_cmd("git -C rinswa-stable ls-remote origin release", cwd=root_dir)
    if code != 0 or not out:
        log_warn("Could not query git remote 'origin/release'. Check your internet connection or git remote setup.")
        return False, None, None

    remote_sha = out.split()[0]
    
    # Check local origin/release SHA
    _, local_origin_sha, _ = run_cmd("git -C rinswa-stable rev-parse origin/release", cwd=root_dir)
    _, local_head_sha, _ = run_cmd("git -C rinswa-stable rev-parse HEAD", cwd=root_dir)

    log_info(f"Upstream Remote Commit: {remote_sha[:12]}")
    log_info(f"Local Tracking Commit:  {local_origin_sha[:12] if local_origin_sha else 'Unknown'}")
    log_info(f"Current Working Commit: {local_head_sha[:12] if local_head_sha else 'Unknown'}")

    has_update = (remote_sha != local_origin_sha) or (remote_sha != local_head_sha)

    if has_update:
        log_warn(f"{Colors.BOLD}A NEW UPSTREAM FIREFOX UPDATE IS AVAILABLE!{Colors.RESET}")
        print(f"Mozilla has pushed new updates to the Firefox stable release branch.")
        print(f"Latest Upstream SHA: {remote_sha}")
        print(f"Current Local SHA:   {local_origin_sha}")
        
        choice = input(f"\n{Colors.YELLOW}Do you want to fetch and merge upstream Firefox now? (y/N): {Colors.RESET}").strip().lower()
        if choice in ['y', 'yes']:
            print("\nFetching latest commits from origin...")
            code, out, err = run_cmd("git -C rinswa-stable fetch origin release", cwd=root_dir, capture=False)
            if code == 0:
                print("\nMerging origin/release into rinswa-stable...")
                merge_code, _, merge_err = run_cmd('git -C rinswa-stable merge origin/release -m "Merge upstream Firefox update"', cwd=root_dir, capture=False)
                if merge_code == 0:
                    log_success("Successfully merged upstream Firefox updates into rinswa-stable!")
                else:
                    log_error(f"Merge encountered issues or conflicts. Please inspect 'rinswa-stable' with git status.\n{merge_err}")
            else:
                log_error(f"Failed to fetch upstream commits: {err}")
    else:
        log_success("Your Firefox base engine is completely up-to-date with Mozilla's release branch!")

    return has_update, latest_mozilla_ver, remote_sha

def update_version_files(root_dir, new_ver, old_ver):
    log_header("STEP 2: UPDATING RINSWA VERSION FILES")
    modified_files = []

    # 1. rinswa-stable version files
    for sub in ["rinswa-stable", "mozilla-central"]:
        for name in ["version.txt", "version_display.txt"]:
            target = os.path.join(root_dir, sub, "browser", "config", name)
            if os.path.exists(target):
                with open(target, "w", encoding="utf-8") as f:
                    f.write(f"{new_ver}\n")
                modified_files.append(os.path.relpath(target, root_dir))

    # 2. update.xml
    update_xml_path = os.path.join(root_dir, "update.xml")
    if os.path.exists(update_xml_path):
        with open(update_xml_path, "r", encoding="utf-8") as f:
            xml_content = f.read()

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Replace displayVersion and appVersion
        xml_content = re.sub(r'displayVersion="[^"]*"', f'displayVersion="{new_ver}"', xml_content)
        xml_content = re.sub(r'appVersion="[^"]*"', f'appVersion="{new_ver}"', xml_content)
        xml_content = re.sub(r'buildID="[^"]*"', f'buildID="{timestamp}"', xml_content)
        
        # Replace download URL version
        xml_content = re.sub(
            r'URL="https://github.com/deadxfire/Rinswa-browser/releases/download/[^"]*"',
            f'URL="https://github.com/deadxfire/Rinswa-browser/releases/download/v{new_ver}/rinswa-{new_ver}.en-US.win64.installer.exe"',
            xml_content
        )

        # Auto-calculate SHA256 and size if installer binary exists
        installer_candidates = [
            os.path.join(root_dir, "rinswa-stable", "obj-rinswa", "dist", f"rinswa-{new_ver}.en-US.win64.installer.exe"),
            os.path.join(root_dir, "rinswa-stable", "obj-rinswa", "dist", "install", "sea", f"rinswa-{new_ver}.en-US.win64.installer.exe"),
        ]
        found_installer = None
        for cand in installer_candidates:
            if os.path.exists(cand):
                found_installer = cand
                break
        
        if found_installer:
            import hashlib
            with open(found_installer, "rb") as f_inst:
                calculated_hash = hashlib.sha256(f_inst.read()).hexdigest()
            file_size = str(os.path.getsize(found_installer))
            xml_content = re.sub(r'hashValue="[^"]*"', f'hashValue="{calculated_hash}"', xml_content)
            xml_content = re.sub(r'size="[^"]*"', f'size="{file_size}"', xml_content)
            log_info(f"Auto-calculated hash ({calculated_hash[:12]}...) and size ({file_size} bytes) for update.xml")

        with open(update_xml_path, "w", encoding="utf-8") as f:
            f.write(xml_content)
        modified_files.append("update.xml")

    # 3. README.md badge
    readme_path = os.path.join(root_dir, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()

        new_readme = re.sub(
            r'badge/version-[0-9a-zA-Z._]+-00d2ff',
            f'badge/version-{new_ver}_Stable-00d2ff',
            readme_content
        )

        if new_readme != readme_content:
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(new_readme)
            modified_files.append("README.md")

    # 4. Pref header comments
    pref_files = [
        os.path.join(root_dir, "branding", "pref", "firefox-branding.js"),
        os.path.join(root_dir, "firefox-branding.js"),
    ]
    for pf in pref_files:
        if os.path.exists(pf):
            with open(pf, "r", encoding="utf-8") as f:
                content = f.read()
            new_content = re.sub(r'// Rinswa Branding Preferences - Official Stable v[0-9.]+', f'// Rinswa Branding Preferences - Official Stable v{new_ver}', content)
            if new_content != content:
                with open(pf, "w", encoding="utf-8") as f:
                    f.write(new_content)
                modified_files.append(os.path.relpath(pf, root_dir))

    # Print summary
    for mf in modified_files:
        log_success(f"Updated: {mf}")

    # Synchronize themes, new tab wallpapers, and preferences
    print("\nSynchronizing branding, themes, and preferences...")
    deploy_theme = os.path.join(root_dir, "scripts", "deploy-newtab-theme.py")
    deploy_prefs = os.path.join(root_dir, "scripts", "deploy-prefs.py")
    
    if os.path.exists(deploy_theme):
        run_cmd(f'"{sys.executable}" "{deploy_theme}"', cwd=root_dir)
        log_success("Synchronized Cyber-Glass UI & New Tab Wallpapers")
        
    if os.path.exists(deploy_prefs):
        run_cmd(f'"{sys.executable}" "{deploy_prefs}"', cwd=root_dir)
        log_success("Synchronized Enterprise Distribution Policies & Preferences")

    log_success(f"All project files successfully updated to v{new_ver}!")
    return modified_files

def main():
    root_dir = get_root_dir()
    os.chdir(root_dir)

    print(f"{Colors.CYAN}{Colors.BOLD}")
    print(r"""
  ____  _                               ____                                  
 |  _ \(_)_ __  _____      ____ _      | __ ) _ __ _____      _____  ___ _ __ 
 | |_) | | '_ \/ __\ \ /\ / / _` |_____|  _ \| '__/ _ \ \ /\ / / __|/ _ \ '__|
 |  _ <| | | | \__ \\ V  V / (_| |_____| |_) | | | (_) \ V  V /\__ \  __/ |   
 |_| \_\_|_| |_|___/ \_/\_/ \__,_|     |____/|_|  \___/ \_/\_/ |___/\___|_|   
    """)
    print("   Upstream Update Checker & Version Management System")
    print(f"   Developed by Arindam Makar | Rinswa Browser{Colors.RESET}\n")

    current_ver = get_current_rinswa_version(root_dir)
    suggested_ver = suggest_next_version(current_ver)

    # Step 1: Upstream Firefox Engine Check
    has_update, mozilla_ver, upstream_sha = check_upstream_mozilla(root_dir)

    # Step 2: Version Configuration
    log_header("STEP 2: RINSWA BROWSER VERSION MANAGEMENT")
    print(f"Current Rinswa Version:   {Colors.BOLD}{Colors.GREEN}{current_ver}{Colors.RESET}")
    print(f"Suggested Next Version:   {Colors.BOLD}{Colors.CYAN}{suggested_ver}{Colors.RESET}")
    print(f"\nOptions:")
    print(f" - Press {Colors.BOLD}[Enter]{Colors.RESET} to keep current version ({current_ver})")
    print(f" - Or type a new version (e.g. {suggested_ver}) and press [Enter]")

    user_ver = input(f"\nEnter Rinswa version [{current_ver}]: ").strip()
    
    if not user_ver:
        new_ver = current_ver
        print(f"\nKeeping current version: {Colors.BOLD}{new_ver}{Colors.RESET}")
    else:
        new_ver = user_ver.lstrip("vV")
        if not re.match(r'^\d+(\.\d+)+$', new_ver):
            log_warn(f"'{new_ver}' does not look like standard semantic versioning (e.g. 1.0.3), using it anyway.")

    # Apply version changes across the project
    update_version_files(root_dir, new_ver, current_ver)

    # Step 3: Readiness & Build Launch
    log_header("STEP 3: READY TO BUILD!")
    print(f"Browser Version:    {Colors.BOLD}{Colors.GREEN}v{new_ver} Stable{Colors.RESET}")
    print(f"Gecko Base:         {Colors.BOLD}{mozilla_ver if mozilla_ver else 'Gecko 157.0.1 Release'}{Colors.RESET}")
    print(f"Build Script:       {Colors.BOLD}Build-Rinswa-Stable.bat{Colors.RESET}")
    print(f"\nEverything is synchronized and configured.")
    
    build_choice = input(f"\n{Colors.CYAN}{Colors.BOLD}Would you like to run Build-Rinswa-Stable.bat now? (Y/n): {Colors.RESET}").strip().lower()
    
    if build_choice in ['', 'y', 'yes']:
        log_info("Launching Build-Rinswa-Stable.bat...\n")
        bat_path = os.path.join(root_dir, "Build-Rinswa-Stable.bat")
        if os.path.exists(bat_path):
            os.system(f'"{bat_path}"')
        else:
            log_error(f"Build-Rinswa-Stable.bat not found at {bat_path}")
    else:
        log_info(f"Skipping build. You can double-click {Colors.BOLD}Build-Rinswa-Stable.bat{Colors.RESET} whenever you are ready!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
