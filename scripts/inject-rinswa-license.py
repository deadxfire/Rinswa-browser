#!/usr/bin/env python3
"""
Rinswa Browser - License Injection Script
Injects the official Rinswa Browser License into about:license across:
1. rinswa-stable/obj-rinswa/dist/rinswa/browser/omni.ja (chrome/browser/content/browser/license.html)
2. rinswa-stable/obj-rinswa/dist/rinswa/omni.ja (chrome/toolkit/content/global/license.html & aboutLicense.css)
3. Active user profile userContent.css files
4. Repacks rinswa-1.0.4.en-US.win64.zip
"""

import os
import re
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

RINSW_LICENSE_ROW = """        <tr>
          <td>
            <h1 id="rinswa">Rinswa Browser License</h1>
          </td>
          <td>
            <p>Rinswa Browser Source Code, Branding, UI Design, Glossy Ribbon Theme, Smart Window, AI Integration, and Customizations</p>
          </td>
          <td>
            <h2>Rinswa Browser Software License &amp; Terms</h2>
            <p><b>Rinswa Browser</b> &mdash; Developed and created by <b>Arindam Makar</b>.</p>
            <p>Copyright &copy; 2026 Arindam Makar. All rights reserved.</p>
            <p>Portions copyright &copy; Mozilla Contributors and other contributors under the Mozilla Public License 2.0 (MPL 2.0).</p>

            <hr>

            <h3>1. Grant of License</h3>
            <p>
              Rinswa Browser is free and open-source software. Permission is hereby granted to any person obtaining a copy
              of this software and associated documentation files to use, study, copy, modify, merge, publish, distribute,
              and run the software, subject to the conditions and notices set forth herein and under the terms of the
              <a href="about:license#mpl">Mozilla Public License, Version 2.0 (MPL 2.0)</a>.
            </p>

            <h3>2. Source Code Availability</h3>
            <p>
              All source code for Rinswa Browser, including custom enhancements, user interface layouts, themes, and
              integrated extensions, is publicly available at:
              <br>
              <a href="https://github.com/deadxfire/Rinswa-browser">https://github.com/deadxfire/Rinswa-browser</a>
            </p>

            <h3>3. Trademarks and Branding</h3>
            <p>
              The names <b>"Rinswa"</b>, <b>"Rinswa Browser"</b>, the signature Rinswa ribbons and logos, and associated artwork are
              trademarks and copyrighted assets of <b>Arindam Makar</b>.
            </p>
            <p>
              This license does not grant permission to use the trade names, trademarks, service marks, or product names of Rinswa
              for commercial purposes or in modified binary distributions without prior express written consent, except as required
              for reasonable and customary use in describing the origin of the software and reproduction of copyright notices.
            </p>

            <h3>4. Disclaimer of Warranty</h3>
            <p>
              COVERED SOFTWARE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED,
              IMPLIED, OR STATUTORY, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED SOFTWARE IS FREE OF DEFECTS,
              MERCHANTABLE, FIT FOR A PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF
              THE COVERED SOFTWARE IS WITH YOU. SHOULD ANY COVERED SOFTWARE PROVE DEFECTIVE IN ANY RESPECT, YOU ASSUME THE COST
              OF ANY NECESSARY SERVICING, REPAIR, OR CORRECTION.
            </p>

            <h3>5. Limitation of Liability</h3>
            <p>
              UNDER NO CIRCUMSTANCES AND UNDER NO LEGAL THEORY, WHETHER TORT (INCLUDING NEGLIGENCE), CONTRACT, OR OTHERWISE, SHALL
              THE AUTHOR, COPYRIGHT HOLDERS, OR CONTRIBUTORS BE LIABLE TO ANY PERSON FOR ANY DIRECT, INDIRECT, SPECIAL, INCIDENTAL,
              OR CONSEQUENTIAL DAMAGES OF ANY CHARACTER ARISING AS A RESULT OF THIS LICENSE OR THE USE OR INABILITY TO USE THE
              COVERED SOFTWARE.
            </p>
          </td>
        </tr>
"""

CSS_ADDITION = """
/* Rinswa Browser License Highlighting & Styling */
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
"""

def patch_html(html):
    # 1. Header notice
    old_header_pattern = r'<p>\s*<b>Binaries</b> of this product have been made available to you by the\s*<a href="http://www.mozilla.org/">Mozilla Project</a>.*?<a href="about:rights">Know your rights</a>\.\s*</p>'
    new_header = '''<p>
  <b>Rinswa Browser</b> binaries and components have been made available to you by
  <a href="https://github.com/deadxfire/Rinswa-browser">Arindam Makar</a> under the
  <a href="about:license#rinswa">Rinswa Browser License</a> and the
  <a href="about:license#mpl">Mozilla Public License 2.0</a> (MPL).
  <a href="about:rights">Know your rights</a>.
</p>'''
    if "Mozilla Project" in html and "Rinswa Browser License" not in html[:html.find("<h1>") + 300]:
        html = re.sub(old_header_pattern, new_header, html, flags=re.DOTALL)
    
    # 2. List index
    if 'about:license#rinswa' not in html:
        mpl_needle = '<li><a href="about:license#mpl">Mozilla Public License 2.0</a>'
        if mpl_needle in html:
            html = html.replace(
                mpl_needle,
                '<li><a href="about:license#rinswa">Rinswa Browser License</a>\n      <br><br>\n      </li>\n      ' + mpl_needle
            )
            
    # 3. Table body
    if 'id="rinswa"' not in html:
        idx = html.find('<h1 id="mpl">')
        if idx != -1:
            tr_idx = html.rfind('<tr>', 0, idx)
            if tr_idx != -1:
                html = html[:tr_idx] + RINSW_LICENSE_ROW + html[tr_idx:]
    return html

def main():
    print("[Rinswa License Injector] Starting injection...")

    # 0. Patch dist/bin unpacked files
    dist_bin = os.path.join(ROOT, "rinswa-stable", "obj-rinswa", "dist", "bin")
    bin_browser_license = os.path.join(dist_bin, "browser", "chrome", "browser", "content", "browser", "license.html")
    if os.path.exists(bin_browser_license):
        with open(bin_browser_license, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        patched = patch_html(content)
        with open(bin_browser_license, "w", encoding="utf-8") as f:
            f.write(patched)
        print("  [OK] Patched dist/bin browser license.html")

    bin_global_license = os.path.join(dist_bin, "chrome", "toolkit", "content", "global", "license.html")
    if os.path.exists(bin_global_license):
        with open(bin_global_license, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        patched = patch_html(content)
        with open(bin_global_license, "w", encoding="utf-8") as f:
            f.write(patched)
        print("  [OK] Patched dist/bin global license.html")

    bin_about_css = os.path.join(dist_bin, "chrome", "toolkit", "skin", "classic", "global", "aboutLicense.css")
    if os.path.exists(bin_about_css):
        with open(bin_about_css, "r", encoding="utf-8", errors="ignore") as f:
            css_str = f.read()
        if "#rinswa" not in css_str:
            css_str += CSS_ADDITION
            with open(bin_about_css, "w", encoding="utf-8") as f:
                f.write(css_str)
            print("  [OK] Patched dist/bin aboutLicense.css")

    # 1. Patch browser/omni.ja
    browser_omni = os.path.join(ROOT, "rinswa-stable", "obj-rinswa", "dist", "rinswa", "browser", "omni.ja")
    if os.path.exists(browser_omni):
        with zipfile.ZipFile(browser_omni, "r") as zin:
            entries = []
            for item in zin.infolist():
                content = zin.read(item.filename)
                if item.filename == "chrome/browser/content/browser/license.html":
                    content = patch_html(content.decode("utf-8", errors="ignore")).encode("utf-8")
                    print("  [OK] Patched chrome/browser/content/browser/license.html in browser/omni.ja")
                entries.append((item, content))
        tmp = browser_omni + ".tmp"
        with zipfile.ZipFile(tmp, "w") as zout:
            for item, content in entries:
                zinfo = zipfile.ZipInfo(item.filename)
                zinfo.compress_type = item.compress_type
                zinfo.date_time = item.date_time
                zout.writestr(zinfo, content)
        os.replace(tmp, browser_omni)

    # 2. Patch root omni.ja
    root_omni = os.path.join(ROOT, "rinswa-stable", "obj-rinswa", "dist", "rinswa", "omni.ja")
    if os.path.exists(root_omni):
        with zipfile.ZipFile(root_omni, "r") as zin:
            entries = []
            for item in zin.infolist():
                content = zin.read(item.filename)
                if item.filename == "chrome/toolkit/content/global/license.html":
                    content = patch_html(content.decode("utf-8", errors="ignore")).encode("utf-8")
                    print("  [OK] Patched chrome/toolkit/content/global/license.html in root omni.ja")
                elif item.filename == "chrome/toolkit/skin/classic/global/aboutLicense.css":
                    css_str = content.decode("utf-8", errors="ignore")
                    if "#rinswa" not in css_str:
                        css_str += CSS_ADDITION
                    content = css_str.encode("utf-8")
                    print("  [OK] Patched aboutLicense.css in root omni.ja")
                entries.append((item, content))
        tmp = root_omni + ".tmp"
        with zipfile.ZipFile(tmp, "w") as zout:
            for item, content in entries:
                zinfo = zipfile.ZipInfo(item.filename)
                zinfo.compress_type = item.compress_type
                zinfo.date_time = item.date_time
                zout.writestr(zinfo, content)
        os.replace(tmp, root_omni)

    # 3. Patch userContent.css in user profiles
    profiles_dir = os.path.expandvars(r"%APPDATA%\Mozilla\Rinswa\Profiles")
    if os.path.exists(profiles_dir):
        for prof in os.listdir(profiles_dir):
            prof_path = os.path.join(profiles_dir, prof)
            if not os.path.isdir(prof_path):
                continue
            chrome_dir = os.path.join(prof_path, "chrome")
            os.makedirs(chrome_dir, exist_ok=True)
            user_content = os.path.join(chrome_dir, "userContent.css")
            existing = ""
            if os.path.exists(user_content):
                with open(user_content, "r", encoding="utf-8", errors="ignore") as f:
                    existing = f.read()
            if "#rinswa" not in existing:
                with open(user_content, "a", encoding="utf-8") as f:
                    f.write(f"\n@-moz-document url('about:license'), url-prefix('about:license') {{{CSS_ADDITION}}}\n")
                print(f"  [OK] Injected about:license styles into {prof}/userContent.css")

    # 4. Repack release zip
    zip_path = os.path.join(ROOT, "rinswa-stable", "obj-rinswa", "dist", "rinswa-1.0.4.en-US.win64.zip")
    if os.path.exists(zip_path) and os.path.exists(browser_omni) and os.path.exists(root_omni):
        root_omni_bytes = open(root_omni, "rb").read()
        browser_omni_bytes = open(browser_omni, "rb").read()
        with zipfile.ZipFile(zip_path, "r") as zin:
            entries = []
            for item in zin.infolist():
                content = zin.read(item.filename)
                if item.filename == "rinswa/omni.ja":
                    content = root_omni_bytes
                elif item.filename == "rinswa/browser/omni.ja":
                    content = browser_omni_bytes
                entries.append((item, content))
        tmp = zip_path + ".tmp"
        with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item, content in entries:
                zinfo = zipfile.ZipInfo(item.filename)
                zinfo.compress_type = item.compress_type
                zinfo.date_time = item.date_time
                zout.writestr(zinfo, content)
        os.replace(tmp, zip_path)
        print(f"  [OK] Repacked {os.path.basename(zip_path)}")

    print("[Rinswa License Injector] Complete!")

if __name__ == "__main__":
    main()
