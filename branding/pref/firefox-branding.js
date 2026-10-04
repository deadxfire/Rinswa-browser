/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Rinswa Branding Preferences - Official Stable v1.0.0
pref("startup.homepage_override_url", "https://deadxfire.github.io/Rinswa-Browser-Support/");
pref("startup.homepage_welcome_url", "https://deadxfire.github.io/Rinswa-Browser-Support/");
pref("startup.homepage_welcome_url.additional", "");
pref("browser.startup.homepage", "https://deadxfire.github.io/Rinswa-Browser-Support/");
pref("app.update.channel", "release");
pref("app.update.interval", 86400);
pref("app.update.promptWaitTime", 86400);
pref("app.update.url", "https://raw.githubusercontent.com/deadxfire/Rinswa-browser/main/update.xml");
pref("app.update.url.manual", "https://github.com/deadxfire/Rinswa-browser/releases");
pref("app.update.url.details", "https://github.com/deadxfire/Rinswa-browser/releases");
pref("app.update.checkInstallTime.days", 2);
pref("app.update.badgeWaitTime", 0);
pref("devtools.selfxss.count", 5);

// Support & Help Links
pref("app.support.baseURL", "https://deadxfire.github.io/Rinswa-Browser-Support/support.html");
pref("app.feedback.baseURL", "https://github.com/deadxfire/Rinswa-browser/issues");

// Web Compatibility: Ensure Firefox compatibility token is included in the User-Agent header
// so major search engines and web apps (Google, YouTube, Cloudflare) serve modern rich interfaces
pref("general.useragent.compatMode.firefox", true);

// Clean Minimal Home Screen: Only Search & Favorites (No News/Stories/Pocket/Sponsored Clutter)
pref("browser.newtabpage.activity-stream.feeds.section.topstories", false);
pref("browser.newtabpage.activity-stream.section.highlights.includePocket", false);
pref("browser.newtabpage.activity-stream.showSponsored", false);
pref("browser.newtabpage.activity-stream.showSponsoredTopSites", false);
pref("browser.newtabpage.activity-stream.feeds.discoverystreamfeed", false);
pref("browser.newtabpage.activity-stream.discoverystream.enabled", false);
pref("browser.newtabpage.activity-stream.feeds.snippets", false);
pref("browser.newtabpage.activity-stream.feeds.topsites", true);
pref("browser.newtabpage.activity-stream.showSearch", true);
pref("browser.startup.homepage.abouthome_cache.enabled", false);

// Auto-enable bundled distribution extensions (uBlock Origin) on first run
pref("extensions.autoDisableScopes", 0);
pref("extensions.enabledScopes", 15);
