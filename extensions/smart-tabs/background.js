/**
 * Rinswa Smart Tab Manager & Clean Tabs - Background Engine
 * High-performance tab categorization, duplicate detection, sleep management & workspaces.
 */

// Category definition matrix
const SMART_CATEGORIES = {
  work: {
    id: "work",
    name: "WORK",
    icon: "💼",
    color: "#6366f1",
    gradient: "linear-gradient(135deg, #6366f1 0%, #00f2fe 100%)",
    rules: [
      "laravel", "github.com", "gitlab.com", "stackoverflow.com", "stackexchange.com",
      "docs.", "documentation", "developer.mozilla.org", "rust-lang.org", "python.org",
      "flutter.dev", "docker.com", "postman.co", "aws.amazon.com", "cloud.google.com",
      "console.azure.com", "chatgpt.com", "claude.ai", "deepseek.com", "huggingface.co",
      "codepen.io", "npmjs.com", "packagist.org", "jira", "atlassian", "linear.app",
      "trello.com", "notion.so", "figma.com", "localhost", "127.0.0.1", "dev.to"
    ]
  },
  shopping: {
    id: "shopping",
    name: "SHOPPING",
    icon: "🛍️",
    color: "#f59e0b",
    gradient: "linear-gradient(135deg, #f59e0b 0%, #ff758c 100%)",
    rules: [
      "amazon.", "flipkart.com", "ebay.com", "walmart.com", "myntra.com",
      "aliexpress.com", "target.com", "bestbuy.com", "etsy.com", "shopify.com",
      "store.", "shop.", "cart", "checkout", "product-review", "price", "deal"
    ]
  },
  personal: {
    id: "personal",
    name: "PERSONAL",
    icon: "💬",
    color: "#10b981",
    gradient: "linear-gradient(135deg, #10b981 0%, #00b4d8 100%)",
    rules: [
      "mail.google.com", "gmail.com", "outlook.live.com", "web.whatsapp.com", "whatsapp.com",
      "twitter.com", "x.com", "reddit.com", "instagram.com", "facebook.com",
      "linkedin.com", "telegram.org", "discord.com", "slack.com", "messages.google.com"
    ]
  },
  media: {
    id: "media",
    name: "MEDIA & STREAMING",
    icon: "🎬",
    color: "#ec4899",
    gradient: "linear-gradient(135deg, #ec4899 0%, #a855f7 100%)",
    rules: [
      "youtube.com", "youtu.be", "netflix.com", "spotify.com", "twitch.tv",
      "primevideo.com", "disneyplus.com", "soundcloud.com", "vimeo.com", "music.youtube.com"
    ]
  },
  docs: {
    id: "docs",
    name: "DOCS & RESEARCH",
    icon: "📚",
    color: "#00b4d8",
    gradient: "linear-gradient(135deg, #00b4d8 0%, #0072ff 100%)",
    rules: [
      "wikipedia.org", "arxiv.org", "medium.com", "substack.com", "w3schools.com",
      "geeksforgeeks.org", "readthedocs.io", "git-scm.com", "news.ycombinator.com"
    ]
  }
};

/**
 * Normalizes URL for duplicate detection by ignoring hash and tracking parameters
 */
function normalizeUrl(rawUrl) {
  if (!rawUrl) return "";
  try {
    const url = new URL(rawUrl);
    // Ignore common tracking query parameters
    const trackingParams = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "ref", "fbclid", "gclid"];
    trackingParams.forEach(p => url.searchParams.delete(p));
    // Remove hash
    url.hash = "";
    return url.origin + url.pathname + (url.search ? url.search : "");
  } catch (e) {
    return rawUrl.split("#")[0];
  }
}

/**
 * Categorize a single tab based on URL and Title heuristics
 */
function classifyTab(tab) {
  const url = (tab.url || "").toLowerCase();
  const title = (tab.title || "").toLowerCase();

  for (const catId of Object.keys(SMART_CATEGORIES)) {
    const cat = SMART_CATEGORIES[catId];
    for (const rule of cat.rules) {
      if (url.includes(rule) || title.includes(rule)) {
        return cat;
      }
    }
  }

  // Fallback: extract domain name
  try {
    const domain = new URL(tab.url).hostname.replace(/^www\./, "");
    return {
      id: "other",
      name: domain.toUpperCase(),
      icon: "🌐",
      color: "#94a3b8",
      gradient: "linear-gradient(135deg, #64748b 0%, #94a3b8 100%)",
      domain: domain
    };
  } catch (e) {
    return {
      id: "other",
      name: "OTHER",
      icon: "🌐",
      color: "#94a3b8",
      gradient: "linear-gradient(135deg, #64748b 0%, #94a3b8 100%)"
    };
  }
}

/**
 * Performs deep audit across all open tabs
 */
async function auditTabs() {
  const tabs = await browser.tabs.query({ currentWindow: true });
  const totalTabs = tabs.length;

  const urlMap = new Map();
  const duplicates = [];
  const staleTabs = [];
  const domainCounts = {};
  const categoryGroups = {};
  const now = Date.now();
  const STALE_THRESHOLD_MS = 24 * 60 * 60 * 1000; // 24 hours inactive

  let youtubeCount = 0;
  let docsCount = 0;

  for (const tab of tabs) {
    // 1. Duplicate detection
    const normUrl = normalizeUrl(tab.url);
    if (normUrl && !normUrl.startsWith("about:")) {
      if (urlMap.has(normUrl)) {
        duplicates.push({
          duplicateTab: tab,
          originalTab: urlMap.get(normUrl)
        });
      } else {
        urlMap.set(normUrl, tab);
      }
    }

    // 2. Inactive / Stale tab detection
    const isStale = (tab.lastAccessed && (now - tab.lastAccessed > STALE_THRESHOLD_MS) && !tab.active);
    if (isStale) {
      staleTabs.push(tab);
    }

    // 3. Domain clustering
    try {
      const host = new URL(tab.url).hostname.replace(/^www\./, "");
      if (host) {
        domainCounts[host] = (domainCounts[host] || 0) + 1;
        if (host.includes("youtube.com") || host.includes("youtu.be")) {
          youtubeCount++;
        }
      }
    } catch (e) {}

    // 4. Category classification
    const cat = classifyTab(tab);
    if (!categoryGroups[cat.id]) {
      categoryGroups[cat.id] = {
        meta: cat,
        tabs: []
      };
    }
    categoryGroups[cat.id].tabs.push(tab);

    if (cat.id === "docs") {
      docsCount++;
    }
  }

  // Find biggest domain cluster
  let maxClusterDomain = "";
  let maxClusterCount = 0;
  for (const [dom, count] of Object.entries(domainCounts)) {
    if (count > maxClusterCount && count > 1) {
      maxClusterCount = count;
      maxClusterDomain = dom;
    }
  }

  return {
    totalTabs,
    duplicatesCount: duplicates.length,
    duplicates,
    staleCount: staleTabs.length,
    staleTabs,
    domainCluster: maxClusterCount > 1 ? { domain: maxClusterDomain, count: maxClusterCount } : null,
    youtubeCount,
    docsCount,
    categoryGroups,
    rawTabs: tabs
  };
}

/**
 * Clean tabs automatically:
 * - Closes duplicate copies
 * - Puts inactive tabs to sleep
 * - Contiguously reorders tabs in strip by group
 */
async function cleanTabsAutomatically() {
  const audit = await auditTabs();
  let closedCount = 0;
  let hibernatedCount = 0;

  // 1. Close duplicates
  if (audit.duplicates.length > 0) {
    const idsToClose = audit.duplicates.map(d => d.duplicateTab.id);
    await browser.tabs.remove(idsToClose);
    closedCount = idsToClose.length;
  }

  // 2. Hibernate inactive tabs
  const remainingTabs = await browser.tabs.query({ currentWindow: true });
  const idsToDiscard = [];
  for (const t of remainingTabs) {
    if (!t.active && !t.pinned && !t.discarded) {
      idsToDiscard.push(t.id);
    }
  }
  if (idsToDiscard.length > 0) {
    try {
      await browser.tabs.discard(idsToDiscard);
      hibernatedCount = idsToDiscard.length;
    } catch (e) {}
  }

  // 3. Contiguously arrange tabs by category
  await groupTabsInStrip();

  return {
    closedDuplicates: closedCount,
    hibernatedTabs: hibernatedCount,
    memoryFreedEstimateMB: (closedCount * 120) + (hibernatedCount * 65)
  };
}

/**
 * Reorders tabs in strip so related categories sit contiguously together
 */
async function groupTabsInStrip() {
  const tabs = await browser.tabs.query({ currentWindow: true });
  // Sort tabs by category order
  const catOrder = ["work", "shopping", "personal", "media", "docs", "other"];
  
  const categorized = tabs.slice().sort((a, b) => {
    const catA = classifyTab(a);
    const catB = classifyTab(b);
    const indexA = catOrder.indexOf(catA.id);
    const indexB = catOrder.indexOf(catB.id);
    return (indexA === -1 ? 99 : indexA) - (indexB === -1 ? 99 : indexB);
  });

  // Move tabs sequentially
  for (let i = 0; i < categorized.length; i++) {
    const t = categorized[i];
    if (!t.pinned) {
      try {
        await browser.tabs.move(t.id, { index: i });
      } catch (e) {}
    }
  }
}

/**
 * Discard / Sleep tabs
 */
async function sleepTabs(tabIds) {
  if (!tabIds || tabIds.length === 0) return 0;
  try {
    await browser.tabs.discard(tabIds);
    return tabIds.length;
  } catch (e) {
    return 0;
  }
}

/**
 * Workspaces Management (Save & Restore)
 */
async function saveWorkspace(name, icon, color, tabIds) {
  const tabs = await browser.tabs.query({ currentWindow: true });
  const targetTabs = tabIds ? tabs.filter(t => tabIds.includes(t.id)) : tabs;

  const workspace = {
    id: "ws_" + Date.now(),
    name: name || "Workspace " + new Date().toLocaleDateString(),
    icon: icon || "📁",
    color: color || "#6366f1",
    createdAt: Date.now(),
    tabs: targetTabs.map(t => ({
      url: t.url,
      title: t.title,
      favIconUrl: t.favIconUrl
    }))
  };

  const stored = await browser.storage.local.get({ workspaces: [] });
  const workspaces = stored.workspaces || [];
  workspaces.unshift(workspace);
  await browser.storage.local.set({ workspaces });
  return workspace;
}

async function restoreWorkspace(workspaceId, newWindow = false) {
  const stored = await browser.storage.local.get({ workspaces: [] });
  const workspace = (stored.workspaces || []).find(w => w.id === workspaceId);
  if (!workspace || !workspace.tabs.length) return false;

  if (newWindow) {
    const firstUrl = workspace.tabs[0].url;
    const win = await browser.windows.create({ url: firstUrl });
    for (let i = 1; i < workspace.tabs.length; i++) {
      await browser.tabs.create({ windowId: win.id, url: workspace.tabs[i].url, active: false });
    }
  } else {
    for (const t of workspace.tabs) {
      await browser.tabs.create({ url: t.url, active: false });
    }
  }
  return true;
}

async function listWorkspaces() {
  const stored = await browser.storage.local.get({ workspaces: [] });
  return stored.workspaces || [];
}

async function deleteWorkspace(workspaceId) {
  const stored = await browser.storage.local.get({ workspaces: [] });
  const workspaces = (stored.workspaces || []).filter(w => w.id !== workspaceId);
  await browser.storage.local.set({ workspaces });
  return true;
}

// Message Dispatcher
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "auditTabs") {
    auditTabs().then(sendResponse);
    return true;
  }
  if (message.action === "cleanAutomatically") {
    cleanTabsAutomatically().then(sendResponse);
    return true;
  }
  if (message.action === "groupTabsInStrip") {
    groupTabsInStrip().then(sendResponse);
    return true;
  }
  if (message.action === "sleepTabs") {
    sleepTabs(message.tabIds).then(sendResponse);
    return true;
  }
  if (message.action === "saveWorkspace") {
    saveWorkspace(message.name, message.icon, message.color, message.tabIds).then(sendResponse);
    return true;
  }
  if (message.action === "restoreWorkspace") {
    restoreWorkspace(message.workspaceId, message.newWindow).then(sendResponse);
    return true;
  }
  if (message.action === "listWorkspaces") {
    listWorkspaces().then(sendResponse);
    return true;
  }
  if (message.action === "deleteWorkspace") {
    deleteWorkspace(message.workspaceId).then(sendResponse);
    return true;
  }
});
