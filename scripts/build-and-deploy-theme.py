"""Build and deploy Rinswa signature Glossy Ribbon theme and menu layout fixes across profiles and source trees"""
import os
import base64
import re

root = r"c:\Users\arind\OneDrive\Documents\Project\browser"
ui_dir = os.path.join(root, "ui")

rinswa_css_file = os.path.join(ui_dir, "rinswa.css")
with open(rinswa_css_file, "r", encoding="utf-8") as f:
    css = f.read()

# Deploy to source directories
source_destinations = [
    os.path.join(root, "rinswa-stable", "browser", "themes", "windows", "browser.css"),
    os.path.join(root, "mozilla-central", "browser", "themes", "windows", "browser.css"),
    os.path.join(root, "rinswa-stable", "obj-rinswa", "dist", "bin", "browser", "chrome", "browser", "skin", "classic", "browser", "browser.css"),
]

for s_dest in source_destinations:
    if os.path.exists(os.path.dirname(s_dest)):
        with open(s_dest, "w", encoding="utf-8") as f:
            f.write(css)
        print("Updated source CSS:", s_dest)

# Deploy to all active user profiles
profiles_dir = os.path.expandvars(r"%APPDATA%\Mozilla\Rinswa\Profiles")
if os.path.exists(profiles_dir):
    for prof in os.listdir(profiles_dir):
        prof_path = os.path.join(profiles_dir, prof)
        if not os.path.isdir(prof_path):
            continue
        chrome_dir = os.path.join(prof_path, "chrome")
        os.makedirs(chrome_dir, exist_ok=True)
        user_chrome = os.path.join(chrome_dir, "userChrome.css")
        with open(user_chrome, "w", encoding="utf-8") as f:
            f.write(css)
        print(f"Deployed userChrome.css to {prof}")

        user_js = os.path.join(prof_path, "user.js")
        pref_lines = [
            'user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);\n',
            'user_pref("svg.context-properties.content.enabled", true);\n'
        ]
        existing = ""
        if os.path.exists(user_js):
            with open(user_js, "r", encoding="utf-8", errors="ignore") as f:
                existing = f.read()
        with open(user_js, "a", encoding="utf-8") as f:
            for l in pref_lines:
                pref_name = l.split('"')[1]
                if pref_name not in existing:
                    f.write(l)
        print(f"Ensured preferences in {prof}/user.js")

print("Theme build and deployment complete!")
