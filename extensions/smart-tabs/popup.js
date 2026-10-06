/**
 * Rinswa Smart Tab Manager & Clean Tabs - Popup Interface
 */

let currentAudit = null;
let currentWorkspaces = [];

document.addEventListener("DOMContentLoaded", async () => {
  setupNavigation();
  setupSearch();
  setupEventListeners();
  await refreshAudit();
  await loadWorkspaces();
});

/**
 * Tab Navigation (Clean Tabs / Groups / Workspaces)
 */
function setupNavigation() {
  const navTabs = document.querySelectorAll(".nav-tab");
  navTabs.forEach(btn => {
    btn.addEventListener("click", () => {
      navTabs.forEach(t => t.classList.remove("active"));
      document.querySelectorAll(".tab-view").forEach(v => v.classList.remove("active"));
      
      btn.classList.add("active");
      const targetId = btn.getAttribute("data-tab");
      const targetView = document.getElementById(targetId);
      if (targetView) targetView.classList.add("active");
    });
  });
}

/**
 * Event Listeners
 */
function setupEventListeners() {
  // Clean Automatically
  document.getElementById("btn-clean-auto").addEventListener("click", async () => {
    const btn = document.getElementById("btn-clean-auto");
    btn.disabled = true;
    btn.innerHTML = `<span class="btn-icon">⏳</span> Cleaning...`;

    try {
      const res = await browser.runtime.sendMessage({ action: "cleanAutomatically" });
      const statusMsg = document.getElementById("clean-status-message");
      statusMsg.style.display = "block";
      statusMsg.textContent = `⚡ Cleaned! Closed ${res.closedDuplicates} duplicates, hibernated ${res.hibernatedTabs} tabs. Freed ~${res.memoryFreedEstimateMB} MB RAM!`;
      
      setTimeout(async () => {
        statusMsg.style.display = "none";
        btn.disabled = false;
        btn.innerHTML = `<span class="btn-icon">⚡</span> Clean Automatically`;
        await refreshAudit();
      }, 3500);
    } catch (e) {
      btn.disabled = false;
      btn.innerHTML = `<span class="btn-icon">⚡</span> Clean Automatically`;
    }
  });

  // Review Drawer Toggle
  document.getElementById("btn-clean-review").addEventListener("click", () => {
    const drawer = document.getElementById("review-drawer");
    if (drawer.style.display === "none") {
      populateReviewDrawer();
      drawer.style.display = "block";
    } else {
      drawer.style.display = "none";
    }
  });

  document.getElementById("btn-close-review").addEventListener("click", () => {
    document.getElementById("review-drawer").style.display = "none";
  });

  // Apply Review Selections
  document.getElementById("btn-apply-review").addEventListener("click", async () => {
    const drawer = document.getElementById("review-drawer");
    const closeCheckboxes = drawer.querySelectorAll("input.cb-close-tab:checked");
    const sleepCheckboxes = drawer.querySelectorAll("input.cb-sleep-tab:checked");

    const toClose = Array.from(closeCheckboxes).map(cb => parseInt(cb.value, 10));
    const toSleep = Array.from(sleepCheckboxes).map(cb => parseInt(cb.value, 10));

    if (toClose.length > 0) {
      await browser.tabs.remove(toClose);
    }
    if (toSleep.length > 0) {
      try {
        await browser.tabs.discard(toSleep);
      } catch (e) {}
    }

    drawer.style.display = "none";
    await refreshAudit();
  });

  // Quick Action: Group Strip
  document.getElementById("qc-group-strip").addEventListener("click", async () => {
    await browser.runtime.sendMessage({ action: "groupTabsInStrip" });
    await refreshAudit();
  });

  // Quick Action: Sleep Inactive
  const sleepHandler = async () => {
    const tabs = await browser.tabs.query({ currentWindow: true });
    const ids = tabs.filter(t => !t.active && !t.pinned && !t.discarded).map(t => t.id);
    if (ids.length > 0) {
      await browser.tabs.discard(ids);
    }
    await refreshAudit();
  };
  document.getElementById("qc-sleep-all").addEventListener("click", sleepHandler);
  document.getElementById("btn-quick-sleep").addEventListener("click", sleepHandler);

  // Group All Now in Groups tab
  document.getElementById("btn-group-all-now").addEventListener("click", async () => {
    await browser.runtime.sendMessage({ action: "groupTabsInStrip" });
    await refreshAudit();
  });

  // Save Workspace
  document.getElementById("btn-save-workspace").addEventListener("click", async () => {
    const nameInput = document.getElementById("ws-name-input");
    const iconSelect = document.getElementById("ws-icon-select");
    const name = nameInput.value.trim();
    if (!name) return;

    await browser.runtime.sendMessage({
      action: "saveWorkspace",
      name: name,
      icon: iconSelect.value
    });

    nameInput.value = "";
    await loadWorkspaces();
  });
}

/**
 * Refresh Audit Data & Render
 */
async function refreshAudit() {
  try {
    currentAudit = await browser.runtime.sendMessage({ action: "auditTabs" });
  } catch (e) {
    return;
  }
  if (!currentAudit) return;

  // Header badges
  document.getElementById("badge-total-tabs").textContent = `${currentAudit.totalTabs} Tabs`;
  
  // Clean card title
  document.getElementById("audit-main-title").textContent = `You have ${currentAudit.totalTabs} tabs`;

  // Insights list
  const list = document.getElementById("audit-insights-list");
  list.innerHTML = "";

  if (currentAudit.duplicatesCount > 0) {
    const li = document.createElement("li");
    li.className = "clean-insight-item";
    li.innerHTML = `<span class="insight-bullet bullet-red"></span><span><strong>${currentAudit.duplicatesCount} duplicate${currentAudit.duplicatesCount > 1 ? "s" : ""}</strong> detected</span>`;
    list.appendChild(li);
  }

  if (currentAudit.staleCount > 0) {
    const li = document.createElement("li");
    li.className = "clean-insight-item";
    li.innerHTML = `<span class="insight-bullet bullet-amber"></span><span><strong>${currentAudit.staleCount} inactive</strong> for &gt;24 hours</span>`;
    list.appendChild(li);
  }

  if (currentAudit.domainCluster) {
    const li = document.createElement("li");
    li.className = "clean-insight-item";
    li.innerHTML = `<span class="insight-bullet bullet-cyan"></span><span><strong>${currentAudit.domainCluster.count} tabs</strong> from ${escapeHtml(currentAudit.domainCluster.domain)}</span>`;
    list.appendChild(li);
  }

  if (currentAudit.youtubeCount > 0) {
    const li = document.createElement("li");
    li.className = "clean-insight-item";
    li.innerHTML = `<span class="insight-bullet bullet-pink"></span><span><strong>${currentAudit.youtubeCount} YouTube</strong> tab${currentAudit.youtubeCount > 1 ? "s" : ""}</span>`;
    list.appendChild(li);
  }

  if (currentAudit.docsCount > 0) {
    const li = document.createElement("li");
    li.className = "clean-insight-item";
    li.innerHTML = `<span class="insight-bullet bullet-purple"></span><span><strong>${currentAudit.docsCount} documentation</strong> tab${currentAudit.docsCount > 1 ? "s" : ""}</span>`;
    list.appendChild(li);
  }

  if (list.children.length === 0) {
    const li = document.createElement("li");
    li.className = "clean-insight-item";
    li.innerHTML = `<span class="insight-bullet bullet-cyan"></span><span>Tabs are organized and optimal</span>`;
    list.appendChild(li);
  }

  // Footer RAM savings stat
  const savedMB = (currentAudit.duplicatesCount * 120) + (currentAudit.staleCount * 65);
  document.getElementById("footer-ram-stat").textContent = `💾 Recoverable Memory: ~${savedMB} MB`;

  // Render Groups Tab
  renderGroups(currentAudit.categoryGroups);
}

/**
 * Populate Review Drawer with Checklists
 */
function populateReviewDrawer() {
  const wrap = document.getElementById("review-sections-wrap");
  wrap.innerHTML = "";

  if (!currentAudit) return;

  // Duplicates section
  if (currentAudit.duplicates.length > 0) {
    const block = document.createElement("div");
    block.className = "review-group-block";
    block.innerHTML = `
      <div class="review-group-title">
        <span>Duplicates (${currentAudit.duplicates.length})</span>
        <span style="font-size:10px; color:#ef4444;">Will close duplicate copies</span>
      </div>
    `;
    currentAudit.duplicates.forEach(d => {
      const row = document.createElement("div");
      row.className = "review-item-row";
      row.innerHTML = `
        <input type="checkbox" class="cb-close-tab" value="${d.duplicateTab.id}" checked>
        <span class="review-item-title" title="${escapeHtml(d.duplicateTab.url)}">${escapeHtml(d.duplicateTab.title || d.duplicateTab.url)}</span>
      `;
      block.appendChild(row);
    });
    wrap.appendChild(block);
  }

  // Inactive / Stale tabs section
  if (currentAudit.staleTabs.length > 0) {
    const block = document.createElement("div");
    block.className = "review-group-block";
    block.innerHTML = `
      <div class="review-group-title">
        <span>Inactive Tabs (${currentAudit.staleTabs.length})</span>
        <span style="font-size:10px; color:#f59e0b;">Will put to sleep to save RAM</span>
      </div>
    `;
    currentAudit.staleTabs.forEach(t => {
      const row = document.createElement("div");
      row.className = "review-item-row";
      row.innerHTML = `
        <input type="checkbox" class="cb-sleep-tab" value="${t.id}" checked>
        <span class="review-item-title" title="${escapeHtml(t.url)}">${escapeHtml(t.title || t.url)}</span>
      `;
      block.appendChild(row);
    });
    wrap.appendChild(block);
  }

  if (wrap.children.length === 0) {
    wrap.innerHTML = `<div style="text-align:center; padding:12px; color:var(--fg-muted); font-size:12px;">No duplicates or inactive tabs found!</div>`;
  }
}

/**
 * Render Groups View (Work, Shopping, Personal, etc.)
 */
function renderGroups(groupsMap) {
  const container = document.getElementById("groups-container");
  container.innerHTML = "";

  const keys = Object.keys(groupsMap || {});
  document.getElementById("groups-count-tag").textContent = `${keys.length} Categories`;

  keys.forEach(k => {
    const group = groupsMap[k];
    const meta = group.meta;
    const tabs = group.tabs;

    const card = document.createElement("div");
    card.className = "group-card";

    // Header
    const header = document.createElement("div");
    header.className = "group-header";
    header.innerHTML = `
      <div class="group-title-wrap">
        <span class="group-icon">${meta.icon}</span>
        <span class="group-title" style="color:${meta.color};">${meta.name}</span>
        <span class="group-count">(${tabs.length})</span>
      </div>
      <div class="group-actions">
        <button class="btn-mini btn-group-sleep" title="Sleep all tabs in group">💤 Sleep</button>
        <button class="btn-mini btn-group-save-ws" title="Save group as Workspace">💾 Save</button>
      </div>
    `;

    // Sleep button
    header.querySelector(".btn-group-sleep").addEventListener("click", async (e) => {
      e.stopPropagation();
      const ids = tabs.filter(t => !t.active).map(t => t.id);
      if (ids.length) await browser.tabs.discard(ids);
      await refreshAudit();
    });

    // Save as workspace button
    header.querySelector(".btn-group-save-ws").addEventListener("click", async (e) => {
      e.stopPropagation();
      await browser.runtime.sendMessage({
        action: "saveWorkspace",
        name: meta.name,
        icon: meta.icon,
        color: meta.color,
        tabIds: tabs.map(t => t.id)
      });
      await loadWorkspaces();
      // Switch to workspaces tab
      document.querySelector('[data-tab="tab-workspaces"]').click();
    });

    // Tabs list
    const list = document.createElement("div");
    list.className = "group-tabs-list";

    tabs.forEach(t => {
      const row = document.createElement("div");
      row.className = "tab-item-row";
      
      const faviconSrc = t.favIconUrl || "icons/icon-16.png";
      const statusPill = t.discarded ? `<span class="tab-status-pill pill-asleep">Asleep</span>` : (t.active ? `<span class="tab-status-pill pill-active">Active</span>` : "");

      row.innerHTML = `
        <div class="tab-item-left" title="${escapeHtml(t.url)}">
          <img class="tab-favicon" src="${escapeHtml(faviconSrc)}" onerror="this.src='icons/icon-16.png'">
          <span class="tab-title-text">${escapeHtml(t.title || t.url)}</span>
          ${statusPill}
        </div>
        <div class="tab-item-actions">
          <button class="btn-tab-close" title="Close tab">✕</button>
        </div>
      `;

      // Jump to tab
      row.querySelector(".tab-item-left").addEventListener("click", async () => {
        await browser.tabs.update(t.id, { active: true });
        window.close();
      });

      // Close tab
      row.querySelector(".btn-tab-close").addEventListener("click", async (e) => {
        e.stopPropagation();
        await browser.tabs.remove(t.id);
        await refreshAudit();
      });

      list.appendChild(row);
    });

    card.appendChild(header);
    card.appendChild(list);
    container.appendChild(card);
  });
}

/**
 * Load & Render Workspaces
 */
async function loadWorkspaces() {
  try {
    currentWorkspaces = await browser.runtime.sendMessage({ action: "listWorkspaces" });
  } catch (e) {
    currentWorkspaces = [];
  }

  const list = document.getElementById("workspaces-list");
  list.innerHTML = "";

  if (!currentWorkspaces || currentWorkspaces.length === 0) {
    list.innerHTML = `<div style="text-align:center; padding:16px; color:var(--fg-muted); font-size:12px;">No saved workspaces yet. Save a group or open tabs above!</div>`;
    return;
  }

  currentWorkspaces.forEach(ws => {
    const item = document.createElement("div");
    item.className = "workspace-item";
    item.innerHTML = `
      <div class="ws-info">
        <span class="ws-icon">${ws.icon || "📁"}</span>
        <div>
          <div class="ws-name">${escapeHtml(ws.name)}</div>
          <div class="ws-sub">${ws.tabs.length} tabs • Saved ${new Date(ws.createdAt).toLocaleDateString()}</div>
        </div>
      </div>
      <div class="ws-actions">
        <button class="btn-mini btn-ws-restore" style="background:rgba(99,102,241,0.25); color:#38bdf8;">⚡ Restore</button>
        <button class="btn-mini btn-ws-delete" style="color:#ef4444;">✕</button>
      </div>
    `;

    item.querySelector(".btn-ws-restore").addEventListener("click", async () => {
      await browser.runtime.sendMessage({ action: "restoreWorkspace", workspaceId: ws.id, newWindow: false });
      window.close();
    });

    item.querySelector(".btn-ws-delete").addEventListener("click", async () => {
      await browser.runtime.sendMessage({ action: "deleteWorkspace", workspaceId: ws.id });
      await loadWorkspaces();
    });

    list.appendChild(item);
  });
}

/**
 * Search Omnibar Filter
 */
function setupSearch() {
  const input = document.getElementById("tab-search-input");
  const overlay = document.getElementById("search-results-overlay");
  const list = document.getElementById("search-list");
  const countLabel = document.getElementById("search-count-label");
  const clearBtn = document.getElementById("search-clear-btn");

  input.addEventListener("input", () => {
    const query = input.value.trim().toLowerCase();
    if (!query) {
      overlay.style.display = "none";
      clearBtn.style.display = "none";
      return;
    }

    clearBtn.style.display = "block";
    overlay.style.display = "block";
    list.innerHTML = "";

    if (!currentAudit || !currentAudit.rawTabs) return;

    const matches = currentAudit.rawTabs.filter(t => {
      const title = (t.title || "").toLowerCase();
      const url = (t.url || "").toLowerCase();
      return title.includes(query) || url.includes(query);
    });

    countLabel.textContent = `${matches.length} matching tab${matches.length === 1 ? "" : "s"}`;

    matches.forEach(t => {
      const row = document.createElement("div");
      row.className = "tab-item-row";
      const faviconSrc = t.favIconUrl || "icons/icon-16.png";

      row.innerHTML = `
        <div class="tab-item-left">
          <img class="tab-favicon" src="${escapeHtml(faviconSrc)}" onerror="this.src='icons/icon-16.png'">
          <span class="tab-title-text">${escapeHtml(t.title || t.url)}</span>
        </div>
      `;

      row.addEventListener("click", async () => {
        await browser.tabs.update(t.id, { active: true });
        window.close();
      });

      list.appendChild(row);
    });
  });

  clearBtn.addEventListener("click", () => {
    input.value = "";
    overlay.style.display = "none";
    clearBtn.style.display = "none";
    input.focus();
  });
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
