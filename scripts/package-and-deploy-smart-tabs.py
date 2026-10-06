"""Package and Deploy Rinswa Smart Tab Manager extension across distributions and profiles"""
import os
import zipfile
import json
import shutil
import glob

ROOT_DIR = r"c:\Users\arind\OneDrive\Documents\Project\browser"
EXT_SRC = os.path.join(ROOT_DIR, "extensions", "smart-tabs")
XPI_NAME = "smart-tabs@rinswa.com.xpi"
DIST_EXT_DIR = os.path.join(ROOT_DIR, "branding", "distribution", "extensions")
os.makedirs(DIST_EXT_DIR, exist_ok=True)
OUT_XPI = os.path.join(DIST_EXT_DIR, XPI_NAME)

print(f"Packaging {EXT_SRC} into {OUT_XPI}...")
with zipfile.ZipFile(OUT_XPI, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(EXT_SRC):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, EXT_SRC)
            zf.write(full_path, rel_path)
            print(f"  + {rel_path}")

print(f"Created {OUT_XPI} (size: {os.path.getsize(OUT_XPI)} bytes)")

# Destination paths
destinations = [
    os.path.join(ROOT_DIR, "rinswa-stable", "obj-rinswa", "dist", "bin", "distribution", "extensions", XPI_NAME),
    os.path.join(ROOT_DIR, "mozilla-central", "obj-rinswa", "dist", "bin", "distribution", "extensions", XPI_NAME),
    os.path.join(r"C:\Program Files\Rinswa", "distribution", "extensions", XPI_NAME),
]

for d in destinations:
    try:
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copyfile(OUT_XPI, d)
        print(f"Copied to {d}")
    except Exception as e:
        print(f"Note: Could not copy to {d}: {e}")

# Deploy to all Rinswa Profiles
profile_dirs = glob.glob(os.path.expandvars(r"%APPDATA%\Mozilla\Rinswa\Profiles\*"))
for p in profile_dirs:
    if os.path.isdir(p):
        prof_ext_dir = os.path.join(p, "extensions")
        os.makedirs(prof_ext_dir, exist_ok=True)
        prof_xpi = os.path.join(prof_ext_dir, XPI_NAME)
        shutil.copyfile(OUT_XPI, prof_xpi)
        print(f"Deployed XPI to profile: {prof_xpi}")

# Update policies.json
policies_file = os.path.join(ROOT_DIR, "branding", "distribution", "policies.json")
if os.path.exists(policies_file):
    with open(policies_file, "r", encoding="utf-8") as f:
        policies = json.load(f)
    
    ext_settings = policies.get("policies", {}).get("ExtensionSettings", {})
    if "smart-tabs@rinswa.com" not in ext_settings:
        ext_settings["smart-tabs@rinswa.com"] = {
            "installation_mode": "normal_installed",
            "default_area": "navbar"
        }
        policies["policies"]["ExtensionSettings"] = ext_settings
        with open(policies_file, "w", encoding="utf-8") as f:
            json.dump(policies, f, indent=2)
        print(f"Updated {policies_file} with smart-tabs@rinswa.com policy")

print("Smart Tab Manager package and deployment complete!")
