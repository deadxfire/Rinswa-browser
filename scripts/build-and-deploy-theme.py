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
    os.path.join(root, "mozilla-central", "obj-rinswa", "dist", "bin", "browser", "chrome", "browser", "skin", "classic", "browser", "browser.css"),
]

prefix_imports = """/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

@import url("chrome://browser/skin/browser-shared.css");
@import url("chrome://browser/skin/contextmenu.css");

"""

for s_dest in source_destinations:
    if os.path.exists(os.path.dirname(s_dest)):
        with open(s_dest, "w", encoding="utf-8") as f:
            if s_dest.endswith("browser.css"):
                f.write(prefix_imports + css)
            else:
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

        user_content = os.path.join(chrome_dir, "userContent.css")
        license_css = """
@-moz-document url('about:license'), url-prefix('about:license') {
  #rinswa {
    background: linear-gradient(135deg, #00d2ff 0%, #a855f7 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-weight: 700 !important;
  }
  tr:has(#rinswa) {
    background: rgba(0, 210, 255, 0.06) !important;
    border-left: 4px solid #00d2ff !important;
  }
  tr:has(#rinswa) h2 {
    color: #00d2ff !important;
    font-size: 1.25em !important;
    margin-top: 0.5em !important;
  }
  tr:has(#rinswa) h3 {
    color: #93c5fd !important;
    font-size: 1.05em !important;
    margin-top: 1.2em !important;
  }
}
"""
        existing_content = ""
        if os.path.exists(user_content):
            with open(user_content, "r", encoding="utf-8", errors="ignore") as f:
                existing_content = f.read()
        if "#rinswa" not in existing_content:
            with open(user_content, "a", encoding="utf-8") as f:
                f.write(license_css)
            print(f"Injected about:license styles into {prof}/userContent.css")

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
