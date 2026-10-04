"""Build and deploy Rinswa signature Glossy Ribbon theme and menu layout fixes across profiles and source trees"""
import os
import base64
import re

root = r"c:\Users\arind\OneDrive\Documents\Project\browser"
ui_dir = os.path.join(root, "ui")

with open(os.path.join(ui_dir, "rinswa-ribbon-left.svg"), "rb") as f:
    b64_left = base64.b64encode(f.read()).decode("utf-8")

with open(os.path.join(ui_dir, "rinswa-ribbon-right.svg"), "rb") as f:
    b64_right = base64.b64encode(f.read()).decode("utf-8")

rinswa_css_file = os.path.join(ui_dir, "rinswa.css")
with open(rinswa_css_file, "r", encoding="utf-8") as f:
    css = f.read()

# 1. Update :root tokens to signature Glossy Multicolour Ribbon
new_root = f""":root {{
  /* Core Theme Deep Obsidian & Glass Surfaces */
  --rinswa-bg-base: #090616;
  --rinswa-bg-surface: #120b24;
  --rinswa-bg-card: rgba(22, 14, 46, 0.82);
  --rinswa-bg-glass: rgba(255, 255, 255, 0.05);
  --rinswa-border-subtle: rgba(255, 255, 255, 0.08);
  --rinswa-border-glow: rgba(0, 242, 254, 0.35);

  /* Master Logo Glossy Multicolour Ribbon Accents */
  --rinswa-cyan: #00f2fe;
  --rinswa-sky: #00b4d8;
  --rinswa-blue: #0072ff;
  --rinswa-indigo: #6366f1;
  --rinswa-purple: #a855f7;
  --rinswa-magenta: #ec4899;
  --rinswa-coral: #ff758c;

  --rinswa-ribbon-gradient: linear-gradient(90deg, #00f2fe 0%, #0072ff 25%, #6366f1 50%, #a855f7 75%, #ec4899 100%);
  --rinswa-ribbon-bar: linear-gradient(90deg, #00f2fe, #00b4d8, #0072ff, #6366f1, #a855f7, #ec4899, #ff758c);
  --rinswa-ribbon-glow: 0 0 16px rgba(0, 242, 254, 0.4), 0 0 24px rgba(236, 72, 153, 0.25);

  --rinswa-fg-primary: #f8fafc;
  --rinswa-fg-secondary: #94a3b8;
  --rinswa-fg-muted: #64748b;

  --rinswa-radius-card: 14px;
  --rinswa-radius-pill: 9999px;
  --rinswa-radius-tab: 10px;
  --rinswa-radius-input: 12px;
}}"""

# Replace :root { ... }
css = re.sub(r":root\s*\{[^}]*--rinswa-radius-input:[^}]*\}", new_root, css, count=1)

# 2. Update :root:not([lwtheme]) tokens
new_non_lwt = """:root:not([lwtheme]) {
  --toolbar-bgcolor: var(--rinswa-bg-base) !important;
  --toolbar-color: var(--rinswa-fg-primary) !important;
  --toolbox-non-lwt-bgcolor: var(--rinswa-bg-base) !important;
  --tab-selected-bgcolor: rgba(45, 23, 84, 0.85) !important;
  --tab-selected-textcolor: #ffffff !important;
  --toolbarbutton-border-radius: 8px !important;
  --lwt-toolbar-field-background-color: rgba(24, 15, 48, 0.85) !important;
  --lwt-toolbar-field-color: #f8fafc !important;
}"""
css = re.sub(r":root:not\(\[lwtheme\]\)\s*\{[^}]*--lwt-toolbar-field-color:[^}]*\}", new_non_lwt, css, count=1)

# 3. Update #navigator-toolbox background to incorporate the signature flowing ribbon waves
toolbox_replacement = f"""#navigator-toolbox {{
  background-color: #0b0718 !important;
  background-image:
    url("data:image/svg+xml;base64,{b64_left}"),
    url("data:image/svg+xml;base64,{b64_right}"),
    linear-gradient(180deg, #090616 0%, #120b24 50%, #1a1033 100%) !important;
  background-position: left top, right top, center !important;
  background-repeat: no-repeat, no-repeat, no-repeat !important;
  background-size: auto 144px, auto 144px, 100% 100% !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
  padding-bottom: 2px !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI Variable Text", "Segoe UI", Roboto, sans-serif !important;
}}"""

css = re.sub(r":root:not\(\[lwtheme\]\)\s+#navigator-toolbox\s*\{[^}]*\}", toolbox_replacement, css, count=1)

# 4. Active tab styling: deep violet glass, frosted border, and glowing ribbon accent line
tab_replacement = """.tabbrowser-tab[selected="true"] .tab-background {
  background: rgba(45, 23, 84, 0.85) !important;
  border: 1px solid rgba(168, 85, 247, 0.45) !important;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.25) !important;
  position: relative !important;
}

/* Active Tab Neon Bottom Indicator Line */
.tabbrowser-tab[selected="true"] .tab-background::after {
  content: "" !important;
  position: absolute !important;
  bottom: 0 !important;
  left: 8% !important;
  right: 8% !important;
  height: 2px !important;
  background: var(--rinswa-ribbon-gradient) !important;
  border-radius: 2px 2px 0 0 !important;
  box-shadow: 0 0 10px rgba(0, 242, 254, 0.7), 0 0 4px rgba(236, 72, 153, 0.7) !important;
}"""

css = re.sub(
    r"\.tabbrowser-tab\[selected=\"true\"\]\s+\.tab-background\s*\{[^}]*\}[^}]*\.tabbrowser-tab\[selected=\"true\"\]\s+\.tab-background::after\s*\{[^}]*\}",
    tab_replacement,
    css,
    count=1
)

# 5. Fix Menu and Submenu sizing: expand width from 320px to 380px, allow up to 440px
css = re.sub(
    r"#appMenu-mainView\s*\{\s*width:\s*320px\s*!important;\s*min-width:\s*320px\s*!important;\s*\}",
    """#appMenu-mainView,
#appMenu-popup panelview {
  width: 380px !important;
  min-width: 380px !important;
  max-width: 440px !important;
  box-sizing: border-box !important;
}""",
    css
)

css = re.sub(
    r"#appMenu-popup\s+panelview:not\(#appMenu-mainView\)\s*\{\s*min-width:\s*320px\s*!important;\s*\}",
    """#appMenu-popup panelview:not(#appMenu-mainView) {
  width: 380px !important;
  min-width: 380px !important;
  max-width: 440px !important;
  box-sizing: border-box !important;
}""",
    css
)

# 6. Fix Menu row buttons: ensure width 100%, padding 4px 10px, margin 1px 0
css = re.sub(
    r"(#appMenu-popup\s+panelview\s+toolbarbutton\.subviewbutton[^{]*\{[^}]*?)padding:\s*3px\s*8px\s*!important;([^}]*?)margin:\s*1px\s*3px\s*!important;([^}]*?)width:\s*calc\(100%\s*-\s*6px\)\s*!important;([^}]*?)max-width:\s*calc\(100%\s*-\s*6px\)\s*!important;",
    r"\1padding: 4px 10px !important;\2margin: 1px 0 !important;\3width: 100% !important;\4max-width: 100% !important;",
    css
)

# 7. Fix Keyboard Shortcut Accelerator (.toolbarbutton-accel): add margin-inline-end: 8px !important;
if "margin-inline-end: 8px !important;" not in css:
    css = re.sub(
        r"(#appMenu-popup panelview toolbarbutton\.subviewbutton:not\(\.toolbaritem-combined-buttons > toolbarbutton\) > \.toolbarbutton-accel\s*\{[^}]*?)margin-inline-start:\s*auto\s*!important;",
        r"\1margin-inline-start: auto !important;\n  margin-inline-end: 8px !important;",
        css
    )

# 8. Fix Submenu Navigation Arrow (.subviewbutton-nav::after): add margin-inline-end: 6px !important;
if "margin-inline-end: 6px !important;" not in css:
    css = re.sub(
        r"(\.subviewbutton-nav:not\(\.subviewbutton-nav-down\)::after[^{]*\{[^}]*?)margin-inline-start:\s*auto\s*!important;",
        r"\1margin-inline-start: auto !important;\n  margin-inline-end: 6px !important;",
        css
    )

# 9. Header inside #appMenu-mainView
header_replacement = """#appMenu-mainView .panel-subview-body::before {
  content: "Rinswa Browser" !important;
  display: flex !important;
  align-items: center !important;
  min-height: 38px !important;
  height: 38px !important;
  font-size: 14px !important;
  font-weight: 700 !important;
  color: #f8fafc !important;
  letter-spacing: -0.2px !important;
  padding-inline-start: 40px !important;
  background-image: url("chrome://branding/content/about-logo.png") !important;
  background-repeat: no-repeat !important;
  background-size: 24px 24px !important;
  background-position: 8px center !important;
  margin: 2px 0 6px 0 !important;
  border-bottom: 2px solid transparent !important;
  border-image: var(--rinswa-ribbon-bar) 1 !important;
}"""

css = re.sub(
    r"#appMenu-mainView\s+\.panel-subview-body::before\s*\{[^}]*\}",
    header_replacement,
    css,
    count=1
)

# Save updated ui/rinswa.css
with open(rinswa_css_file, "w", encoding="utf-8") as f:
    f.write(css)
print(f"Updated {rinswa_css_file} (length: {len(css)})")

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
