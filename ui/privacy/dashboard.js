/**
 * Rinswa Privacy Dashboard Controller
 * Bridges the HTML UI with Gecko's Tracking Protection API and SitePermissions API.
 */

document.addEventListener('DOMContentLoaded', () => {
  class PrivacyDashboard {
    constructor() {
      this.elements = {
        trackers: document.getElementById('trackers-blocked-count'),
        cookies: document.getElementById('cookies-blocked-count'),
        permissionsList: document.getElementById('permissions-list'),
        etpToggle: document.getElementById('etp-site-toggle')
      };
      
      this.init();
    }

    init() {
      this.fetchStats();
      this.fetchPermissions();
      this.setupListeners();
    }

    fetchStats() {
      // In a real Gecko environment, this queries Services.contentBlocking.getLog()
      // For this architecture demo, we mock the stats return.
      const mockTrackers = Math.floor(Math.random() * 45) + 5;
      const mockCookies = Math.floor(Math.random() * 120) + 12;

      this.elements.trackers.textContent = mockTrackers;
      this.elements.cookies.textContent = mockCookies;
    }

    fetchPermissions() {
      // Mocking Gecko's SitePermissions API retrieval for the active tab
      const mockPermissions = [
        { id: 'camera', label: 'Camera', state: 'Blocked' },
        { id: 'location', label: 'Location', state: 'Allowed' }
      ];

      this.elements.permissionsList.innerHTML = '';
      if (mockPermissions.length === 0) {
        this.elements.permissionsList.innerHTML = '<li><span style="color:var(--text-secondary)">No special permissions</span></li>';
      } else {
        mockPermissions.forEach(p => {
          const li = document.createElement('li');
          const isAllowed = p.state === 'Allowed';
          li.innerHTML = `
            <span>${p.label}</span>
            <span style="color: ${isAllowed ? 'var(--secure)' : 'var(--text-secondary)'}">${p.state}</span>
          `;
          this.elements.permissionsList.appendChild(li);
        });
      }
    }

    setupListeners() {
      this.elements.etpToggle.addEventListener('change', (e) => {
        const isEnabled = e.target.checked;
        
        // Translates to: SitePermissions.set(activeURI, "trackingprotection", isEnabled ? SitePermissions.DEFAULT : SitePermissions.BLOCK)
        console.log(`Enhanced Tracking Protection for site set to: ${isEnabled}`);
        
        if (isEnabled) {
          this.fetchStats(); // simulate refetching blocking stats upon reload
        } else {
          this.elements.trackers.textContent = '0';
          this.elements.cookies.textContent = '0';
        }
      });
    }
  }

  // Expose to window for testing/debugging
  window.RinswaPrivacyDashboard = new PrivacyDashboard();
});
