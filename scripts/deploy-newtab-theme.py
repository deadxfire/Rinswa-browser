import os
import shutil

ROOT_DIR = r"c:\Users\arind\OneDrive\Documents\Project\browser"
WALLPAPER_SRC = os.path.join(ROOT_DIR, "Rinswa Alpine Sunset Wallpaper.png")
CSS_SRC = os.path.join(ROOT_DIR, "ui", "newtab-wallpaper.css")
WORDMARK_SRC = os.path.join(ROOT_DIR, "branding", "logos", "about-wordmark.svg")

with open(CSS_SRC, "r", encoding="utf-8") as f:
    custom_css = f.read()

# 1. Deploy wallpaper to all locations
wallpaper_dests = [
    os.path.join(ROOT_DIR, "branding", "wallpaper.png"),
    os.path.join(ROOT_DIR, "mozilla-central", "browser", "branding", "rinswa", "content", "wallpaper.png"),
    os.path.join(ROOT_DIR, "rinswa-stable", "browser", "branding", "rinswa", "content", "wallpaper.png"),
    os.path.join(ROOT_DIR, "mozilla-central", "obj-rinswa", "dist", "bin", "browser", "chrome", "browser", "content", "branding", "wallpaper.png"),
    os.path.join(ROOT_DIR, "mozilla-central", "obj-rinswa", "dist", "bin", "browser", "chrome", "browser", "builtin-addons", "newtab", "data", "wallpaper.png"),
    os.path.join(ROOT_DIR, "mozilla-central", "obj-rinswa", "dist", "bin", "browser", "chrome", "browser", "builtin-addons", "newtab", "data", "css", "wallpaper.png"),
    os.path.join(ROOT_DIR, "mozilla-central", "obj-rinswa", "dist", "bin", "browser", "chrome", "browser", "builtin-addons", "newtab", "data", "css", "nova", "wallpaper.png"),
    os.path.join(ROOT_DIR, "mozilla-central", "obj-rinswa", "dist", "xpi-stage", "newtab", "data", "wallpaper.png"),
    os.path.join(ROOT_DIR, "mozilla-central", "obj-rinswa", "dist", "xpi-stage", "newtab", "data", "css", "wallpaper.png"),
    os.path.join(ROOT_DIR, "rinswa-stable", "obj-rinswa", "dist", "bin", "browser", "chrome", "browser", "content", "branding", "wallpaper.png"),
    os.path.join(ROOT_DIR, "rinswa-stable", "obj-rinswa", "dist", "bin", "browser", "chrome", "browser", "builtin-addons", "newtab", "data", "wallpaper.png"),
    os.path.join(ROOT_DIR, "rinswa-stable", "obj-rinswa", "dist", "bin", "browser", "chrome", "browser", "builtin-addons", "newtab", "data", "css", "wallpaper.png"),
    os.path.join(ROOT_DIR, "rinswa-stable", "obj-rinswa", "dist", "bin", "browser", "chrome", "browser", "builtin-addons", "newtab", "data", "css", "nova", "wallpaper.png"),
    os.path.join(ROOT_DIR, "rinswa-stable", "obj-rinswa", "dist", "xpi-stage", "newtab", "data", "wallpaper.png"),
    os.path.join(ROOT_DIR, "rinswa-stable", "obj-rinswa", "dist", "xpi-stage", "newtab", "data", "css", "wallpaper.png"),
]

for dest in wallpaper_dests:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copyfile(WALLPAPER_SRC, dest)
    print(f"Deployed wallpaper: {dest}")

# 2. Deploy wordmark (replacing Nightly with clean Rinswa)
wordmark_dests = [
    os.path.join(ROOT_DIR, "branding", "logos", "firefox-wordmark.svg"),
    os.path.join(ROOT_DIR, "mozilla-central", "browser", "branding", "rinswa", "content", "firefox-wordmark.svg"),
    os.path.join(ROOT_DIR, "rinswa-stable", "browser", "branding", "rinswa", "content", "firefox-wordmark.svg"),
    os.path.join(ROOT_DIR, "mozilla-central", "obj-rinswa", "dist", "bin", "browser", "chrome", "browser", "content", "branding", "firefox-wordmark.svg"),
    os.path.join(ROOT_DIR, "rinswa-stable", "obj-rinswa", "dist", "bin", "browser", "chrome", "browser", "content", "branding", "firefox-wordmark.svg"),
]

for dest in wordmark_dests:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copyfile(WORDMARK_SRC, dest)
    print(f"Deployed wordmark: {dest}")

# 3. Inject CSS into all activity-stream stylesheets
css_targets = [
    os.path.join(ROOT_DIR, "mozilla-central", "obj-rinswa", "dist", "bin", "browser", "chrome", "browser", "builtin-addons", "newtab", "data", "css", "activity-stream.css"),
    os.path.join(ROOT_DIR, "mozilla-central", "obj-rinswa", "dist", "bin", "browser", "chrome", "browser", "builtin-addons", "newtab", "data", "css", "nova", "activity-stream.css"),
    os.path.join(ROOT_DIR, "mozilla-central", "obj-rinswa", "browser", "extensions", "newtab", "css", "activity-stream.css"),
    os.path.join(ROOT_DIR, "mozilla-central", "obj-rinswa", "browser", "extensions", "newtab", "css", "nova", "activity-stream.css"),
    os.path.join(ROOT_DIR, "mozilla-central", "obj-rinswa", "dist", "xpi-stage", "newtab", "data", "css", "activity-stream.css"),
    os.path.join(ROOT_DIR, "mozilla-central", "obj-rinswa", "dist", "xpi-stage", "newtab", "data", "css", "nova", "activity-stream.css"),
    os.path.join(ROOT_DIR, "rinswa-stable", "obj-rinswa", "dist", "bin", "browser", "chrome", "browser", "builtin-addons", "newtab", "data", "css", "activity-stream.css"),
    os.path.join(ROOT_DIR, "rinswa-stable", "obj-rinswa", "dist", "bin", "browser", "chrome", "browser", "builtin-addons", "newtab", "data", "css", "nova", "activity-stream.css"),
    os.path.join(ROOT_DIR, "rinswa-stable", "obj-rinswa", "browser", "extensions", "newtab", "css", "activity-stream.css"),
    os.path.join(ROOT_DIR, "rinswa-stable", "obj-rinswa", "browser", "extensions", "newtab", "css", "nova", "activity-stream.css"),
    os.path.join(ROOT_DIR, "rinswa-stable", "obj-rinswa", "dist", "xpi-stage", "newtab", "data", "css", "activity-stream.css"),
    os.path.join(ROOT_DIR, "rinswa-stable", "obj-rinswa", "dist", "xpi-stage", "newtab", "data", "css", "nova", "activity-stream.css"),
    os.path.join(ROOT_DIR, "mozilla-central", "browser", "extensions", "newtab", "content-src", "styles", "activity-stream.scss"),
    os.path.join(ROOT_DIR, "mozilla-central", "browser", "extensions", "newtab", "content-src", "styles", "nova", "activity-stream.scss"),
    os.path.join(ROOT_DIR, "rinswa-stable", "browser", "extensions", "newtab", "content-src", "styles", "activity-stream.scss"),
    os.path.join(ROOT_DIR, "rinswa-stable", "browser", "extensions", "newtab", "content-src", "styles", "nova", "activity-stream.scss"),
]

TAG_START = "/* ===== RINSWA NEWTAB ALPINE WALLPAPER & MINIMAL BOTTOM THEME ===== */"
TAG_END = "/* ===== END RINSWA NEWTAB THEME ===== */"

for target in css_targets:
    if os.path.exists(target):
        with open(target, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        # Strip any existing injection to keep file clean
        if TAG_START in content:
            idx_start = content.find(TAG_START)
            idx_end = content.find(TAG_END)
            if idx_end != -1:
                content = content[:idx_start] + content[idx_end + len(TAG_END):]
            else:
                content = content[:idx_start]
        
        # Also strip older "ALPINE SUNSET DEFAULT WALLPAPER" block if present
        if "ALPINE SUNSET DEFAULT WALLPAPER" in content:
            idx = content.find("/* ==========================================================================")
            if idx != -1 and "ALPINE SUNSET" in content[idx:idx+200]:
                content = content[:idx]
        
        # Append updated clean theme
        new_content = content.rstrip() + f"\n\n{TAG_START}\n{custom_css}\n{TAG_END}\n"
        with open(target, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Injected theme into: {target}")

print("\nDeployment of New Tab Theme completed successfully!")
