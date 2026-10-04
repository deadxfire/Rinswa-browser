"""Fix menu and submenu side option fitting, shortcuts, and arrows in ui/rinswa.css and deploy"""
import os
import re

root = r"c:\Users\arind\OneDrive\Documents\Project\browser"
rinswa_css_file = os.path.join(root, "ui", "rinswa.css")

with open(rinswa_css_file, "r", encoding="utf-8") as f:
    css = f.read()

# 1. Update container sizing for #appMenu-popup, #appMenu-multiView, .panel-viewcontainer, .panel-viewstack, #appMenu-mainView, .PanelUI-subView
old_sizing_pattern = r"#appMenu-mainView,\s*#appMenu-popup\s+panelview\s*\{[^}]*\}\s*#appMenu-popup\s+panelview:not\(#appMenu-mainView\)\s*\{[^}]*\}"

new_sizing = """#appMenu-popup,
#appMenu-multiView,
#appMenu-multiView > .panel-viewcontainer,
#appMenu-multiView > .panel-viewcontainer > .panel-viewstack,
#appMenu-popup panelview,
#appMenu-mainView,
.PanelUI-subView {
  width: 380px !important;
  min-width: 380px !important;
  max-width: 440px !important;
  box-sizing: border-box !important;
}

#appMenu-popup panelview:not(#appMenu-mainView) {
  width: 380px !important;
  min-width: 380px !important;
  max-width: 440px !important;
  box-sizing: border-box !important;
}"""

if re.search(old_sizing_pattern, css):
    css = re.sub(old_sizing_pattern, new_sizing, css, count=1)
    print("Replaced menu container sizing")
else:
    print("Could not match old sizing pattern directly, checking lines...")

# 2. Update .panel-subview-body padding
css = re.sub(
    r"#appMenu-popup\s+\.panel-subview-body\s*\{[^}]*\}",
    """#appMenu-popup .panel-subview-body,
.PanelUI-subView .panel-subview-body {
  background: transparent !important;
  color: #f1f5f9 !important;
  box-sizing: border-box !important;
  padding: 6px 10px !important;
  width: 100% !important;
}""",
    css
)

# 3. Update menu item buttons and label text for both main menu and submenus
old_button_pattern = r"#appMenu-popup panelview toolbarbutton\.subviewbutton:not\(\.toolbaritem-combined-buttons > toolbarbutton\):not\(\.panel-banner-item\):not\(#appMenu-update-banner\):not\(#appMenu-create-profile-button\):not\(#appMenu-profiles-button\):not\(#appMenu-referrals-button\):not\(\[hidden\]\):not\(\[hidden=\"true\"\]\):not\(\[hidden=\"\"\]\):not\(\[collapsed\]\):not\(\[collapsed=\"true\"\]\)\s*\{[^}]*\}"

new_button = """#appMenu-popup panelview toolbarbutton.subviewbutton:not(.toolbaritem-combined-buttons > toolbarbutton):not(.panel-banner-item):not(#appMenu-update-banner):not(#appMenu-create-profile-button):not(#appMenu-profiles-button):not(#appMenu-referrals-button):not([hidden]):not([hidden="true"]):not([hidden=""]):not([collapsed]):not([collapsed="true"]),
.PanelUI-subView toolbarbutton.subviewbutton:not(.toolbaritem-combined-buttons > toolbarbutton):not(.panel-banner-item):not([hidden]):not([hidden="true"]):not([hidden=""]):not([collapsed]):not([collapsed="true"]) {
  display: flex !important;
  align-items: center !important;
  min-height: 30px !important;
  height: auto !important;
  padding: 4px 10px !important;
  margin: 1px 0 !important;
  border-radius: 8px !important;
  color: #cbd5e1 !important;
  font-size: 12.5px !important;
  font-weight: 500 !important;
  line-height: 1.2 !important;
  box-sizing: border-box !important;
  width: 100% !important;
  max-width: 100% !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1) !important;
}"""

if re.search(old_button_pattern, css):
    css = re.sub(old_button_pattern, new_button, css, count=1)
    print("Replaced subviewbutton rule")

# 4. Update .toolbarbutton-text
old_text_pattern = r"#appMenu-popup panelview toolbarbutton\.subviewbutton:not\(\.toolbaritem-combined-buttons > toolbarbutton\)\s*>\s*\.toolbarbutton-text\s*\{[^}]*\}"

new_text = """#appMenu-popup panelview toolbarbutton.subviewbutton:not(.toolbaritem-combined-buttons > toolbarbutton) > .toolbarbutton-text,
.PanelUI-subView toolbarbutton.subviewbutton:not(.toolbaritem-combined-buttons > toolbarbutton) > .toolbarbutton-text {
  flex: 1 1 auto !important;
  min-width: 0 !important;
  text-align: start !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
  padding-inline-end: 8px !important;
}"""

if re.search(old_text_pattern, css):
    css = re.sub(old_text_pattern, new_text, css, count=1)
    print("Replaced toolbarbutton-text rule")

# 5. Fix Shortcut Accelerator text - replace nonexistent .toolbarbutton-accel with the REAL &[shortcut]::after pseudo-element!
old_accel_pattern = r"/\* Keyboard Shortcut Accelerator Text \*/\s*#appMenu-popup panelview toolbarbutton\.subviewbutton:not\(\.toolbaritem-combined-buttons > toolbarbutton\)\s*>\s*\.toolbarbutton-accel\s*\{[^}]*\}"

new_accel = """/* Real Keyboard Shortcut Accelerator Pseudo-Element */
#appMenu-popup panelview toolbarbutton.subviewbutton[shortcut]::after,
.PanelUI-subView toolbarbutton.subviewbutton[shortcut]::after,
.subviewbutton[shortcut]::after {
  content: attr(shortcut) !important;
  display: flex !important;
  align-items: center !important;
  margin-inline-start: auto !important;
  margin-inline-end: 8px !important;
  padding-inline-start: 12px !important;
  flex: 0 0 auto !important;
  flex-shrink: 0 !important;
  white-space: nowrap !important;
  color: #818cf8 !important;
  font-size: 11px !important;
  font-weight: 500 !important;
  opacity: 0.9 !important;
}"""

if re.search(old_accel_pattern, css):
    css = re.sub(old_accel_pattern, new_accel, css, count=1)
    print("Replaced shortcut accelerator rule with real [shortcut]::after")
else:
    # If not matched, replace by finding .toolbarbutton-accel
    css = re.sub(
        r"#appMenu-popup panelview toolbarbutton\.subviewbutton:not\(\.toolbaritem-combined-buttons > toolbarbutton\)\s*>\s*\.toolbarbutton-accel\s*\{[^}]*\}",
        new_accel,
        css,
        count=1
    )
    print("Replaced .toolbarbutton-accel directly")

# 6. Fix Submenu Navigation Arrow - use content: url(...) so -moz-context-properties works!
old_arrow_pattern = r"/\* Universal Submenu Arrow for Panel Subviews across the entire browser \*/\s*\.subviewbutton-nav:not\(\.subviewbutton-nav-down\)::after,\s*\.moz-button-subviewbutton-nav::after\s*\{[^}]*\}\s*\.subviewbutton-nav:hover::after,\s*\.subviewbutton-nav\[_moz-menuactive=\"true\"\]::after,\s*\.moz-button-subviewbutton-nav:hover::after\s*\{[^}]*\}"

new_arrow = """/* Universal Submenu Arrow for Panel Subviews across the entire browser */
#appMenu-popup panelview .subviewbutton-nav:not(.subviewbutton-nav-down)::after,
.PanelUI-subView .subviewbutton-nav:not(.subviewbutton-nav-down)::after,
.subviewbutton-nav:not(.subviewbutton-nav-down)::after,
.moz-button-subviewbutton-nav::after {
  -moz-context-properties: fill, fill-opacity !important;
  content: url("chrome://global/skin/icons/arrow-right.svg") !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 16px !important;
  height: 16px !important;
  min-width: 16px !important;
  min-height: 16px !important;
  fill: #94a3b8 !important;
  fill-opacity: 0.85 !important;
  margin-inline-start: auto !important;
  margin-inline-end: 8px !important;
  flex: 0 0 auto !important;
  flex-shrink: 0 !important;
  transition: transform 0.15s ease, fill 0.15s ease, fill-opacity 0.15s ease !important;
}

#appMenu-popup panelview .subviewbutton-nav:not(.subviewbutton-nav-down):hover::after,
.PanelUI-subView .subviewbutton-nav:not(.subviewbutton-nav-down):hover::after,
.subviewbutton-nav:not(.subviewbutton-nav-down):hover::after,
.subviewbutton-nav[_moz-menuactive="true"]::after,
.moz-button-subviewbutton-nav:hover::after {
  fill: #ffffff !important;
  fill-opacity: 1 !important;
  transform: translateX(2px) !important;
}"""

if re.search(old_arrow_pattern, css):
    css = re.sub(old_arrow_pattern, new_arrow, css, count=1)
    print("Replaced submenu arrow rule")
else:
    # Try replacing .subviewbutton-nav:not(.subviewbutton-nav-down)::after block directly
    css = re.sub(
        r"\.subviewbutton-nav:not\(\.subviewbutton-nav-down\)::after[^{]*\{[^}]*\}",
        new_arrow,
        css,
        count=1
    )
    print("Replaced .subviewbutton-nav::after block directly")

# Save updated ui/rinswa.css
with open(rinswa_css_file, "w", encoding="utf-8") as f:
    f.write(css)
print(f"Saved {rinswa_css_file}")

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

print("Menu and submenu side option fitting fix applied and deployed!")
