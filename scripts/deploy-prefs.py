import shutil
import os

src = r"c:\Users\arind\OneDrive\Documents\Project\browser\branding\pref\firefox-branding.js"

targets = [
    r"c:\Users\arind\OneDrive\Documents\Project\browser\mozilla-central\browser\branding\rinswa\pref\firefox-branding.js",
    r"c:\Users\arind\OneDrive\Documents\Project\browser\rinswa-stable\browser\branding\rinswa\pref\firefox-branding.js",
    r"c:\Users\arind\OneDrive\Documents\Project\browser\mozilla-central\obj-rinswa\dist\bin\browser\defaults\preferences\firefox-branding.js",
    r"c:\Users\arind\OneDrive\Documents\Project\browser\mozilla-central\obj-rinswa\dist\bin\browser\defaults\preferences\all-rinswa.js",
]

for t in targets:
    os.makedirs(os.path.dirname(t), exist_ok=True)
    shutil.copyfile(src, t)
    print(f"Copied to {t}")

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
"""

profile_dirs = [
    r"C:\Users\arind\AppData\Roaming\Mozilla\Rinswa\Profiles\1d23f8t4.default-default",
    r"C:\Users\arind\AppData\Roaming\Mozilla\Rinswa\Profiles\dws2q43c.default"
]

for p in profile_dirs:
    if os.path.exists(p):
        user_js = os.path.join(p, "user.js")
        with open(user_js, "w", encoding="utf-8") as f:
            f.write(user_prefs)
        print(f"Updated {user_js}")

print("All preferences deployed!")
