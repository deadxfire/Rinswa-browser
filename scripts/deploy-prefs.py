import shutil
import os
import glob

ROOT_DIR = r"c:\Users\arind\OneDrive\Documents\Project\browser"
src = os.path.join(ROOT_DIR, "branding", "pref", "firefox-branding.js")
policies_src = os.path.join(ROOT_DIR, "branding", "distribution", "policies.json")

targets = [
    os.path.join(ROOT_DIR, "mozilla-central", "browser", "branding", "rinswa", "pref", "firefox-branding.js"),
    os.path.join(ROOT_DIR, "rinswa-stable", "browser", "branding", "rinswa", "pref", "firefox-branding.js"),
    os.path.join(ROOT_DIR, "mozilla-central", "obj-rinswa", "dist", "bin", "browser", "defaults", "preferences", "firefox-branding.js"),
    os.path.join(ROOT_DIR, "mozilla-central", "obj-rinswa", "dist", "bin", "browser", "defaults", "preferences", "all-rinswa.js"),
    os.path.join(ROOT_DIR, "rinswa-stable", "obj-rinswa", "dist", "bin", "browser", "defaults", "preferences", "firefox-branding.js"),
    os.path.join(ROOT_DIR, "rinswa-stable", "obj-rinswa", "dist", "bin", "browser", "defaults", "preferences", "all-rinswa.js"),
]

for t in targets:
    os.makedirs(os.path.dirname(t), exist_ok=True)
    shutil.copyfile(src, t)
    print(f"Copied to {t}")

policies_targets = [
    os.path.join(ROOT_DIR, "mozilla-central", "obj-rinswa", "dist", "bin", "distribution", "policies.json"),
    os.path.join(ROOT_DIR, "rinswa-stable", "obj-rinswa", "dist", "bin", "distribution", "policies.json"),
]

for pt in policies_targets:
    if os.path.exists(os.path.dirname(pt)):
        shutil.copyfile(policies_src, pt)
        print(f"Copied policies to {pt}")

user_prefs = """// Rinswa Stable v1.0.1 Web Compatibility & Clean Home Settings
user_pref("general.useragent.compatMode.firefox", true);
user_pref("browser.newtabpage.activity-stream.feeds.section.topstories", false);
user_pref("browser.newtabpage.activity-stream.section.highlights.includePocket", false);
user_pref("browser.newtabpage.activity-stream.showSponsored", false);
user_pref("browser.newtabpage.activity-stream.showSponsoredTopSites", false);
user_pref("browser.newtabpage.activity-stream.feeds.discoverystreamfeed", false);
user_pref("browser.newtabpage.activity-stream.discoverystream.enabled", false);
user_pref("browser.newtabpage.activity-stream.feeds.snippets", false);
user_pref("browser.newtabpage.activity-stream.feeds.topsites", true);
user_pref("browser.newtabpage.activity-stream.showSearch", true);
user_pref("browser.startup.homepage.abouthome_cache.enabled", false);

// Smart Window & Tab Groups
user_pref("browser.smartwindow.enabled", true);
user_pref("browser.smartwindow.firstrun.hasCompleted", true);
user_pref("browser.smartwindow.isDefaultWindow", true);
user_pref("browser.smartwindow.autoTabGrouping.enabled", true);
user_pref("browser.tabs.groups.enabled", true);
user_pref("browser.tabs.groups.smart.enabled", true);
user_pref("browser.tabs.groups.alternateMenu", true);
user_pref("browser.tabs.groups.smart.userEnabled", true);
user_pref("browser.tabs.groups.smart.optin", true);
user_pref("places.semanticHistory.smartwindow.featureGate", true);

// Newtab Wallpapers & Customization
user_pref("browser.newtabpage.activity-stream.newtabWallpapers.enabled", true);
user_pref("browser.newtabpage.activity-stream.newtabWallpapers.customWallpaper.enabled", true);
user_pref("browser.newtabpage.activity-stream.newtabWallpapers.customWallpaper.library.enabled", true);
user_pref("browser.newtabpage.activity-stream.newtabWallpapers.user.enabled", true);
"""

profile_dirs = glob.glob(r"C:\Users\arind\AppData\Roaming\Mozilla\Rinswa\Profiles\*")

user_content_css = """/* Hide enterprise policies managed notice in Settings */
@-moz-document url-prefix("about:preferences") {
  #policies-container-content,
  #policies-container {
    display: none !important;
  }
}

/* AI Window / Chatbot Contrast & Light Mode Fix */
@-moz-document url-prefix("chrome://browser/content/aiwindow/") {
  :root {
    background-color: light-dark(#f8fafc, transparent) !important;
  }
  
  html, body, .ai-window {
    background-color: light-dark(#f8fafc, transparent) !important;
  }

  @media (prefers-color-scheme: light) {
    body,
    .chat-bubble-assistant,
    .chat-bubble-assistant .chat-bubble-inner,
    .assistant-message {
      color: #0f172a !important;
    }
    
    .disclaimer,
    smartwindow-footer,
    .smartwindow-footer-text,
    [data-l10n-id*="mistake"],
    [data-l10n-id*="error"] {
      color: #475569 !important;
    }
  }
}
"""

for p in profile_dirs:
    if os.path.isdir(p):
        user_js = os.path.join(p, "user.js")
        with open(user_js, "w", encoding="utf-8") as f:
            f.write(user_prefs)
        print(f"Updated {user_js}")
        
        chrome_dir = os.path.join(p, "chrome")
        os.makedirs(chrome_dir, exist_ok=True)
        user_content_path = os.path.join(chrome_dir, "userContent.css")
        with open(user_content_path, "w", encoding="utf-8") as f:
            f.write(user_content_css)
        print(f"Updated {user_content_path}")

print("All preferences deployed!")

