"""Generate an ultra-high quality HTML showcase of Rinswa's Glossy Ribbon theme and render it to a PNG screenshot"""
import os
import subprocess
import base64

root = r"c:\Users\arind\OneDrive\Documents\Project\browser"
artifacts_dir = r"C:\Users\arind\.gemini\antigravity-ide\brain\ab0978df-dd10-4afe-977a-73563dadba56"

with open(os.path.join(root, "ui", "rinswa-ribbon-left.svg"), "r", encoding="utf-8") as f:
    svg_left = f.read()

with open(os.path.join(root, "ui", "rinswa-ribbon-right.svg"), "r", encoding="utf-8") as f:
    svg_right = f.read()

with open(os.path.join(root, "branding", "generated", "about-logo.png"), "rb") as f:
    b64_logo = base64.b64encode(f.read()).decode("utf-8")

b64_svg_left = base64.b64encode(svg_left.encode("utf-8")).decode("utf-8")
b64_svg_right = base64.b64encode(svg_right.encode("utf-8")).decode("utf-8")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Rinswa Browser - Signature Glossy Ribbon Theme Showcase</title>
<style>
  :root {{
    --rinswa-cyan: #00f2fe;
    --rinswa-sky: #00b4d8;
    --rinswa-blue: #0072ff;
    --rinswa-indigo: #6366f1;
    --rinswa-purple: #a855f7;
    --rinswa-magenta: #ec4899;
    --rinswa-coral: #ff758c;
    --rinswa-ribbon-bar: linear-gradient(90deg, #00f2fe, #00b4d8, #0072ff, #6366f1, #a855f7, #ec4899, #ff758c);
    --rinswa-bg-base: #090616;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI Variable Text", "Segoe UI", Roboto, sans-serif;
    user-select: none;
  }}

  body {{
    background: #05030a;
    color: #f8fafc;
    min-height: 100vh;
    padding: 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}

  /* Browser Window Mockup */
  .browser-window {{
    width: 1220px;
    height: 740px;
    background: #080512;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 25px 80px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(255, 255, 255, 0.1);
    display: flex;
    flex-direction: column;
    position: relative;
  }}

  /* Navigation Toolbox Header with Signature Glossy Multicolour Ribbon Background */
  .navigator-toolbox {{
    background-color: #0b0718;
    background-image:
      url("data:image/svg+xml;base64,{b64_svg_left}"),
      url("data:image/svg+xml;base64,{b64_svg_right}"),
      linear-gradient(180deg, #090616 0%, #120b24 50%, #1a1033 100%);
    background-position: left top, right top, center;
    background-repeat: no-repeat, no-repeat, no-repeat;
    background-size: auto 144px, auto 144px, 100% 100%;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    position: relative;
    z-index: 10;
  }}

  /* Tabs Toolbar */
  .tabs-toolbar {{
    display: flex;
    align-items: center;
    height: 42px;
    padding: 6px 12px 0 12px;
    gap: 6px;
  }}

  .tab {{
    display: flex;
    align-items: center;
    gap: 8px;
    height: 34px;
    padding: 0 14px;
    border-radius: 9px;
    font-size: 12px;
    font-weight: 500;
    color: #94a3b8;
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid rgba(255, 255, 255, 0.06);
    position: relative;
    max-width: 220px;
    flex: 1;
    backdrop-filter: blur(12px);
  }}

  .tab.active {{
    color: #ffffff;
    background: rgba(45, 23, 84, 0.88);
    border: 1px solid rgba(168, 85, 247, 0.45);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.25);
  }}

  .tab.active::after {{
    content: "";
    position: absolute;
    bottom: -1px;
    left: 8%;
    right: 8%;
    height: 2.5px;
    background: var(--rinswa-ribbon-bar);
    border-radius: 2px 2px 0 0;
    box-shadow: 0 0 10px rgba(0, 242, 254, 0.8), 0 0 6px rgba(236, 72, 153, 0.8);
  }}

  .tab-icon {{
    width: 16px;
    height: 16px;
    border-radius: 3px;
    flex-shrink: 0;
  }}

  .tab-title {{
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
  }}

  .tab-close {{
    color: #94a3b8;
    font-size: 13px;
    cursor: pointer;
    opacity: 0.7;
  }}

  .btn-newtab {{
    width: 28px;
    height: 28px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #cbd5e1;
    font-size: 16px;
    margin-left: 2px;
  }}

  .window-controls {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-left: auto;
    padding-right: 6px;
  }}

  .win-btn {{
    width: 26px;
    height: 26px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    color: #94a3b8;
  }}

  .win-close {{
    color: #f87171;
  }}

  /* Navigation Bar */
  .nav-bar {{
    display: flex;
    align-items: center;
    height: 44px;
    padding: 0 12px;
    gap: 8px;
  }}

  .nav-btn {{
    width: 30px;
    height: 30px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.06);
    color: #cbd5e1;
    font-size: 13px;
  }}

  .urlbar {{
    flex: 1;
    max-width: 680px;
    height: 32px;
    border-radius: 9999px;
    background: rgba(24, 15, 48, 0.9);
    border: 1px solid rgba(0, 242, 254, 0.65);
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.35), 0 0 16px rgba(0, 242, 254, 0.25);
    display: flex;
    align-items: center;
    padding: 0 12px;
    gap: 8px;
    margin: 0 auto;
  }}

  .urlbar-icon {{
    width: 16px;
    height: 16px;
    border-radius: 4px;
  }}

  .urlbar-text {{
    color: #f8fafc;
    font-size: 12.5px;
    font-weight: 500;
  }}

  .urlbar-highlight {{
    color: #00f2fe;
    font-weight: 600;
  }}

  .toolbar-actions {{
    display: flex;
    align-items: center;
    gap: 6px;
    margin-left: auto;
  }}

  .shield-badge {{
    background: #00f2fe;
    color: #090616;
    font-size: 9px;
    font-weight: 800;
    padding: 1px 4px;
    border-radius: 4px;
    margin-left: -4px;
  }}

  .hamburger-btn {{
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(99, 102, 241, 0.3);
    border: 1px solid rgba(129, 140, 248, 0.5);
    color: #ffffff;
    font-size: 15px;
  }}

  /* Main Browser Body */
  .browser-body {{
    flex: 1;
    display: flex;
    background: #080514;
    position: relative;
    overflow: hidden;
  }}

  /* Web Page Viewport with Rinswa Glow */
  .viewport {{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    background: radial-gradient(circle at 50% 35%, #180d38 0%, #080514 70%);
  }}

  .center-emblem {{
    width: 140px;
    height: 140px;
    filter: drop-shadow(0 0 40px rgba(0, 242, 254, 0.45)) drop-shadow(0 0 60px rgba(236, 72, 153, 0.3));
    margin-bottom: 20px;
  }}

  .brand-title {{
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: var(--rinswa-ribbon-bar);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
  }}

  .brand-tagline {{
    font-size: 14px;
    color: #94a3b8;
    margin-bottom: 24px;
  }}

  .search-dock {{
    width: 520px;
    height: 44px;
    border-radius: 22px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    padding: 0 18px;
    color: #94a3b8;
    font-size: 13.5px;
  }}

  /* Floating App Menu (Hamburger Popup) - Zero Shadow Frosted Glass */
  .app-menu {{
    position: absolute;
    top: 8px;
    right: 14px;
    width: 380px;
    background: linear-gradient(155deg, rgba(28, 19, 54, 0.72) 0%, rgba(14, 10, 28, 0.68) 100%);
    backdrop-filter: blur(32px) saturate(200%);
    -webkit-backdrop-filter: blur(32px) saturate(200%);
    border: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 16px;
    box-shadow: none;
    padding: 8px;
    z-index: 100;
    display: flex;
    flex-direction: column;
    gap: 1px;
  }}

  .menu-header {{
    display: flex;
    align-items: center;
    gap: 10px;
    height: 42px;
    padding: 0 10px;
    font-size: 14px;
    font-weight: 700;
    color: #f8fafc;
    border-bottom: 2px solid transparent;
    border-image: var(--rinswa-ribbon-bar) 1;
    margin-bottom: 6px;
  }}

  .menu-header img {{
    width: 24px;
    height: 24px;
  }}

  .menu-row {{
    display: flex;
    align-items: center;
    height: 30px;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 12.5px;
    font-weight: 500;
    color: #cbd5e1;
    cursor: default;
    transition: background 0.15s ease;
  }}

  .menu-row:hover {{
    background: rgba(99, 102, 241, 0.22);
    color: #ffffff;
  }}

  .menu-icon {{
    width: 15px;
    height: 15px;
    margin-right: 10px;
    opacity: 0.85;
    flex-shrink: 0;
  }}

  .menu-label {{
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}

  .menu-shortcut {{
    margin-left: auto;
    margin-right: 4px;
    color: #818cf8;
    font-size: 11px;
    font-weight: 600;
    flex-shrink: 0;
    white-space: nowrap;
  }}

  .menu-arrow {{
    margin-left: auto;
    margin-right: 4px;
    width: 16px;
    height: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #94a3b8;
    flex-shrink: 0;
  }}

  .menu-separator {{
    height: 1px;
    background: rgba(255, 255, 255, 0.08);
    margin: 4px 6px;
  }}

  /* Zoom row */
  .zoom-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 28px;
    padding: 2px 10px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 8px;
    margin: 2px 0;
    font-size: 12px;
    color: #cbd5e1;
  }}

  .zoom-btns {{
    display: flex;
    align-items: center;
    gap: 4px;
  }}

  .zoom-btn {{
    width: 24px;
    height: 20px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 600;
  }}

  .zoom-level {{
    font-size: 11px;
    font-weight: 600;
    padding: 0 4px;
  }}

  /* Feature Callout Tag */
  .feature-badge {{
    position: absolute;
    bottom: 18px;
    left: 24px;
    background: rgba(13, 18, 30, 0.88);
    border: 1px solid rgba(0, 242, 254, 0.35);
    border-radius: 10px;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
  }}

  .badge-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #00f2fe;
    box-shadow: 0 0 10px #00f2fe;
  }}

  .badge-text {{
    font-size: 12.5px;
    color: #cbd5e1;
  }}

  .badge-text strong {{
    color: #ffffff;
  }}
</style>
</head>
<body>

<div class="browser-window">
  <!-- NAVIGATION TOOLBOX WITH GLOSSY MULTICOLOUR RIBBON THEME -->
  <div class="navigator-toolbox">
    <!-- TABS TOOLBAR -->
    <div class="tabs-toolbar">
      <!-- Active Tab -->
      <div class="tab active">
        <img class="tab-icon" src="data:image/png;base64,{b64_logo}">
        <span class="tab-title">Rinswa Browser - Next-Gen Web</span>
        <span class="tab-close">✕</span>
      </div>

      <!-- Secondary Tab -->
      <div class="tab">
        <span class="tab-icon" style="background:#24292e; border-radius:3px; display:inline-flex; align-items:center; justify-content:center; font-size:10px;">🐙</span>
        <span class="tab-title">deadxfire/Rinswa-browser</span>
        <span class="tab-close">✕</span>
      </div>

      <!-- Third Tab -->
      <div class="tab" style="max-width: 160px;">
        <span class="tab-icon" style="background:#4285f4; border-radius:3px; display:inline-flex; align-items:center; justify-content:center; font-size:10px;">G</span>
        <span class="tab-title">Google Search</span>
        <span class="tab-close">✕</span>
      </div>

      <div class="btn-newtab">+</div>

      <!-- Windows Controls -->
      <div class="window-controls">
        <div class="win-btn">─</div>
        <div class="win-btn">□</div>
        <div class="win-btn win-close">✕</div>
      </div>
    </div>

    <!-- NAVIGATION BAR -->
    <div class="nav-bar">
      <div class="nav-btn">←</div>
      <div class="nav-btn" style="opacity:0.5;">→</div>
      <div class="nav-btn">↻</div>

      <!-- Centered Capsule URL Bar -->
      <div class="urlbar">
        <img class="urlbar-icon" src="data:image/png;base64,{b64_logo}">
        <span style="color:#00f2fe; font-size:12px;">🔒</span>
        <span class="urlbar-text"><span class="urlbar-highlight">https://rinswa.org</span>/welcome</span>
        <span style="margin-left:auto; color:#94a3b8; font-size:13px;">★</span>
      </div>

      <!-- Extensions & Actions -->
      <div class="toolbar-actions">
        <div class="nav-btn" style="position:relative;">
          🛡️<span class="shield-badge">1</span>
        </div>
        <div class="nav-btn">🧩</div>
        <div class="hamburger-btn">☰</div>
      </div>
    </div>
  </div>

  <!-- BROWSER VIEWPORT & FLOATING APP MENU -->
  <div class="browser-body">
    <!-- Viewport Content -->
    <div class="viewport">
      <img class="center-emblem" src="data:image/png;base64,{b64_logo}">
      <h1 class="brand-title">Rinswa Browser</h1>
      <p class="brand-tagline">Signature Glossy Multicolour Ribbon Design • Ultra-Fast • Uncompromising Privacy</p>
      <div class="search-dock">
        <span>Search the web or enter URL...</span>
        <span style="margin-left:auto; color:#00f2fe; font-size:16px;">🔍</span>
      </div>
    </div>

    <!-- FLOATING 380px APP MENU (HAMBURGER POPUP) -->
    <div class="app-menu">
      <!-- Menu Header -->
      <div class="menu-header">
        <img src="data:image/png;base64,{b64_logo}">
        <span>Rinswa Browser</span>
      </div>

      <!-- Menu Rows with Full Shortcuts and Navigation Arrows -->
      <div class="menu-row">
        <span class="menu-icon">📄</span>
        <span class="menu-label">New Tab</span>
        <span class="menu-shortcut">Ctrl+T</span>
      </div>
      <div class="menu-row">
        <span class="menu-icon">🪟</span>
        <span class="menu-label">New Window</span>
        <span class="menu-shortcut">Ctrl+N</span>
      </div>
      <div class="menu-row">
        <span class="menu-icon">🕵️</span>
        <span class="menu-label">New Private Window</span>
        <span class="menu-shortcut">Ctrl+Shift+P</span>
      </div>

      <div class="menu-separator"></div>

      <div class="menu-row">
        <span class="menu-icon">🕒</span>
        <span class="menu-label">History</span>
        <span class="menu-arrow">❯</span>
      </div>
      <div class="menu-row">
        <span class="menu-icon">⭐</span>
        <span class="menu-label">Bookmarks</span>
        <span class="menu-arrow">❯</span>
      </div>
      <div class="menu-row">
        <span class="menu-icon">📑</span>
        <span class="menu-label">Tab groups</span>
        <span class="menu-arrow">❯</span>
      </div>
      <div class="menu-row">
        <span class="menu-icon">📥</span>
        <span class="menu-label">Downloads</span>
        <span class="menu-shortcut">Ctrl+J</span>
      </div>
      <div class="menu-row">
        <span class="menu-icon">🧩</span>
        <span class="menu-label">Extensions and Themes</span>
        <span class="menu-shortcut">Ctrl+Shift+A</span>
      </div>

      <div class="menu-separator"></div>

      <div class="menu-row">
        <span class="menu-icon">🖨️</span>
        <span class="menu-label">Print...</span>
        <span class="menu-shortcut">Ctrl+P</span>
      </div>
      <div class="menu-row">
        <span class="menu-icon">💾</span>
        <span class="menu-label">Save Page As...</span>
        <span class="menu-shortcut">Ctrl+S</span>
      </div>
      <div class="menu-row">
        <span class="menu-icon">🔍</span>
        <span class="menu-label">Find in Page...</span>
        <span class="menu-shortcut">Ctrl+F</span>
      </div>

      <!-- Zoom Row -->
      <div class="zoom-row">
        <span>Zoom</span>
        <div class="zoom-btns">
          <div class="zoom-btn">−</div>
          <span class="zoom-level">100%</span>
          <div class="zoom-btn">+</div>
          <div class="zoom-btn">⛶</div>
        </div>
      </div>

      <div class="menu-row">
        <span class="menu-icon">⚙️</span>
        <span class="menu-label">Settings</span>
      </div>
      <div class="menu-row">
        <span class="menu-icon">🛠️</span>
        <span class="menu-label">More Tools</span>
        <span class="menu-arrow">❯</span>
      </div>
      <div class="menu-row">
        <span class="menu-icon">❓</span>
        <span class="menu-label">Help and Report</span>
        <span class="menu-arrow">❯</span>
      </div>

      <div class="menu-separator"></div>

      <div class="menu-row">
        <span class="menu-icon">🚪</span>
        <span class="menu-label">Exit</span>
        <span class="menu-shortcut">Ctrl+Shift+Q</span>
      </div>
    </div>

    <!-- Live Design Highlight Badge -->
    <div class="feature-badge">
      <div class="badge-dot"></div>
      <div class="badge-text">
        <strong>Glossy Multicolour Ribbon Theme</strong> (Cyan, Blue, Indigo, Purple, Magenta) &bull; <strong>380px Fixed Menu Layout</strong>
      </div>
    </div>
  </div>
</div>

</body>
</html>"""

showcase_html = os.path.join(root, "theme-showcase.html")
with open(showcase_html, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated {showcase_html}")

# Render to PNG screenshot using Headless Chrome
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
screenshot_output = os.path.join(artifacts_dir, "theme_preview.png")

cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--force-device-scale-factor=1",
    f"--window-size=1280,820",
    f"--screenshot={screenshot_output}",
    f"file:///{showcase_html.replace(os.sep, '/')}"
]

print("Executing Chrome headless screenshot...")
res = subprocess.run(cmd, capture_output=True, text=True)
print("Returncode:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)

if os.path.exists(screenshot_output):
    print(f"Successfully generated screenshot: {screenshot_output} ({os.path.getsize(screenshot_output)} bytes)")
else:
    print("Screenshot file not found!")
