import os

prefs_to_add = [
    'user_pref("general.useragent.compatMode.firefox", true);',
    'user_pref("browser.newtabpage.activity-stream.feeds.section.topstories", false);',
    'user_pref("browser.newtabpage.activity-stream.section.highlights.includePocket", false);',
    'user_pref("browser.newtabpage.activity-stream.showSponsored", false);',
    'user_pref("browser.newtabpage.activity-stream.showSponsoredTopSites", false);',
    'user_pref("browser.newtabpage.activity-stream.feeds.discoverystreamfeed", false);',
    'user_pref("browser.newtabpage.activity-stream.discoverystream.enabled", false);',
    'user_pref("browser.newtabpage.activity-stream.feeds.snippets", false);',
    'user_pref("browser.newtabpage.activity-stream.feeds.topsites", true);',
    'user_pref("browser.newtabpage.activity-stream.showSearch", true);',
    'user_pref("browser.startup.homepage.abouthome_cache.enabled", false);',
]

profiles = [
    r"C:\Users\arind\AppData\Roaming\Mozilla\Rinswa\Profiles\1d23f8t4.default-default\prefs.js",
    r"C:\Users\arind\AppData\Roaming\Mozilla\Rinswa\Profiles\dws2q43c.default\prefs.js"
]

for p in profiles:
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        pref_names = [item.split('"')[1] for item in prefs_to_add]
        filtered = [l for l in lines if not any(k in l for k in pref_names)]
        for item in prefs_to_add:
            filtered.append(item + "\n")
        with open(p, "w", encoding="utf-8") as f:
            f.writelines(filtered)
        print("Updated prefs in:", p)

print("Profile prefs.js update completed!")
