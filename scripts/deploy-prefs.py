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

user_prefs = """// Rinswa Stable Web Compatibility & Clean Home Settings
user_pref("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:157.0) Gecko/20100101 Firefox/157.0");
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

// Low RAM & High-Efficiency Performance Tuning (Chromium-level ~200MB Startup)
// 1. Process limits & eliminate prelaunch process overhead
user_pref("dom.ipc.processCount", 2);
user_pref("dom.ipc.processCount.webIsolated", 1);
user_pref("dom.ipc.processPrelaunch.enabled", false);
user_pref("dom.ipc.processPrelaunch.fission.enabled", false);
user_pref("browser.tabs.remote.warmup.enabled", false);
user_pref("browser.tabs.remote.warmup.maxTabs", 0);

// 2. On-demand lazy session restore (prevents mass-loading restored & pinned tabs at startup)
user_pref("browser.sessionstore.restore_on_demand", true);
user_pref("browser.sessionstore.restore_pinned_tabs_on_demand", true);
user_pref("browser.sessionstore.restore_tabs_lazily", true);
user_pref("browser.newtabpage.activity-stream.prerender", false);

// 3. Proactive Tab Unloading / Sleeping for inactive tabs
user_pref("browser.tabs.unloadOnLowMemory", true);
user_pref("browser.tabs.min_inactive_duration_before_unload", 60000); // 1 minute
user_pref("browser.tabs.unloadTabInContextMenu", true);
user_pref("browser.tabs.fadeOutExplicitlyUnloadedTabs", true);
user_pref("browser.tabs.fadeOutUnloadedTabs", true);

// 4. BFCache (Back-Forward Cache) Limits
user_pref("browser.sessionhistory.max_total_viewers", 1);
user_pref("browser.sessionhistory.max_entries", 10);

// 5. Cap Network Memory Cache (forces network cache to use fast disk instead of bloating RAM)
user_pref("browser.cache.memory.enable", true);
user_pref("browser.cache.memory.capacity", 16384); // 16 MB max
user_pref("browser.cache.memory.max_entry_size", 2048); // 2 MB max entry
user_pref("browser.cache.disk.max_chunks_memory_usage", 5120); // 5 MB
user_pref("browser.cache.disk.max_priority_chunks_memory_usage", 5120); // 5 MB

// 6. Image Surface Cache Optimization (aggressively expires decoded image bitmaps)
user_pref("image.mem.discardable", true);
user_pref("image.mem.animated.discardable", true);
user_pref("image.mem.surfacecache.max_size_kb", 40960); // 40 MB max (down from 256 MB)
user_pref("image.mem.surfacecache.min_expiration_ms", 10000); // 10s expiration

// 7. SpiderMonkey JS Heap Compacting & Responsive GC
user_pref("javascript.options.compact_on_user_inactive", true);
user_pref("javascript.options.compact_on_user_inactive_delay", 5000); // 5s idle delay
user_pref("javascript.options.gc_on_memory_pressure", true);
user_pref("javascript.options.gc_delay", 500);
user_pref("javascript.options.mem.gc_compacting", true);
user_pref("javascript.options.mem.gc_per_zone", true);
user_pref("javascript.options.mem.high_water_mark", 64);

// 8. Media Cache Memory Optimization (prevents video streams buffering deeply into RAM)
user_pref("media.memory_cache_max_size", 2048); // 2 MB
user_pref("media.memory_caches_combined_limit_kb", 32768); // 32 MB combined max

// 9. Session Store I/O and Memory Churn
user_pref("browser.sessionstore.interval", 30000); // 30s interval

// 10. Disable unnecessary background prefetching & speculative connections
user_pref("network.prefetch-next", false);
user_pref("network.dns.disablePrefetch", true);
user_pref("network.http.speculative-parallel-limit", 0);
user_pref("browser.places.speculativeConnect.enabled", false);

// 11. Disable accessibility tree duplication unless requested
user_pref("accessibility.force_disabled", 1);

// 12. GPU / Canvas cache sizing
user_pref("gfx.canvas.accelerated.cache-items", 512);
user_pref("gfx.canvas.accelerated.cache-size", 64);

// 13. Stylesheet and theme custom properties
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);
user_pref("svg.context-properties.content.enabled", true);
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

