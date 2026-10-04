/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Rinswa Branding Preferences - Official Stable v1.0.0
pref("startup.homepage_override_url", "");
pref("startup.homepage_welcome_url", "");
pref("startup.homepage_welcome_url.additional", "");
pref("app.update.channel", "release");
pref("app.update.interval", 86400);
pref("app.update.promptWaitTime", 86400);
pref("app.update.url.manual", "https://github.com/mozilla-firefox/firefox/releases");
pref("app.update.url.details", "https://github.com/mozilla-firefox/firefox/releases");
pref("app.update.checkInstallTime.days", 2);
pref("app.update.badgeWaitTime", 0);
pref("devtools.selfxss.count", 5);

// Web Compatibility: Ensure Firefox compatibility token is included in the User-Agent header
// so major search engines and web apps (Google, YouTube, Cloudflare) serve modern rich interfaces
pref("general.useragent.compatMode.firefox", true);
