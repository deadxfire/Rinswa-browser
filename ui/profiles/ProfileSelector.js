/**
 * Rinswa Profile Selector Controller
 * Interfaces with Gecko's nsIToolkitProfileService to manage isolated profiles.
 */

document.addEventListener('DOMContentLoaded', () => {
  class ProfileSelector {
    constructor() {
      this.listEl = document.getElementById('profile-list');
      this.init();
    }

    init() {
      this.loadProfiles();
    }

    loadProfiles() {
      // In a real Gecko environment, this queries nsIToolkitProfileService
      // For this architecture demo, we mock the profile return structure.
      const mockProfiles = [
        { id: 'default', name: 'Personal', active: true, avatar: 'P' },
        { id: 'work', name: 'Work', active: false, avatar: 'W' },
        { id: 'dev', name: 'Development', active: false, avatar: 'D' }
      ];

      this.listEl.innerHTML = '';
      
      mockProfiles.forEach(profile => {
        const li = document.createElement('li');
        li.className = 'profile-item';
        li.dataset.active = profile.active;
        li.dataset.id = profile.id;
        
        li.innerHTML = `
          <div class="profile-avatar">${profile.avatar}</div>
          <div class="profile-info">
            <span class="profile-name">${profile.name}</span>
            <span class="profile-status">${profile.active ? 'Current Session' : 'Click to switch'}</span>
          </div>
        `;

        // Don't restart if already active
        if (!profile.active) {
           li.addEventListener('click', () => this.switchProfile(profile.id));
        }
        
        this.listEl.appendChild(li);
      });
    }

    switchProfile(profileId) {
      console.log(`Instructing Gecko to restart with profile: ${profileId}`);
      // In Gecko, switching profiles requires restarting the application instance
      // let appStartup = Components.classes["@mozilla.org/toolkit/app-startup;1"].getService(Components.interfaces.nsIAppStartup);
      // appStartup.quit(appStartup.eForceQuit | appStartup.eRestart);
    }
  }

  window.RinswaProfileSelector = new ProfileSelector();
});
