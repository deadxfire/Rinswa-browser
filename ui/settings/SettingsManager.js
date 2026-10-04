/**
 * Rinswa SettingsManager
 * Acts as a clean bridge between the modern Rinswa Settings UI and Gecko's XPCOM libpref system.
 * Prevents hardcoding preferences in UI components.
 */

export class SettingsManager {
  constructor(schema) {
    this.schema = schema;
    this.prefs = Components.classes["@mozilla.org/preferences-service;1"]
                           .getService(Components.interfaces.nsIPrefBranch);
  }

  /** Retrieves setting value, handling mappings and defaults */
  get(settingId) {
    const spec = this.schema.settings[settingId];
    if (!spec) throw new Error(`Unknown setting: ${settingId}`);

    let val;
    try {
      switch (spec.type) {
        case "boolean": val = this.prefs.getBoolPref(spec.geckoPref); break;
        case "integer": val = this.prefs.getIntPref(spec.geckoPref); break;
        case "string":  val = this.prefs.getStringPref(spec.geckoPref); break;
      }
    } catch (e) {
      val = spec.default;
    }

    // Handle inverse/custom mappings (e.g. hardware acceleration boolean inversion)
    if (spec.valueMap) {
      const entry = Object.entries(spec.valueMap).find(([k, v]) => v === val);
      return entry ? (entry[0] === 'true' ? true : (entry[0] === 'false' ? false : entry[0])) : val;
    }
    return val;
  }

  /** Sets setting value with validation */
  set(settingId, value) {
    const spec = this.schema.settings[settingId];
    if (!spec) throw new Error(`Unknown setting: ${settingId}`);

    // Validation Check
    if (spec.validation && !spec.validation.includes(value)) {
      throw new Error(`Invalid value for ${settingId}`);
    }

    let writeValue = value;
    if (spec.valueMap) {
       writeValue = spec.valueMap[value.toString()];
    }

    // Immediate persistence
    switch (spec.type) {
      case "boolean": this.prefs.setBoolPref(spec.geckoPref, writeValue); break;
      case "integer": this.prefs.setIntPref(spec.geckoPref, writeValue); break;
      case "string":  this.prefs.setStringPref(spec.geckoPref, writeValue); break;
    }
  }

  /** Clears user preference, reverting to Mozilla/Rinswa default */
  reset(settingId) {
    const spec = this.schema.settings[settingId];
    if (!spec) return;
    if (this.prefs.prefHasUserValue(spec.geckoPref)) {
      this.prefs.clearUserPref(spec.geckoPref);
    }
  }

  /** Resets an entire category (e.g. for a "Reset Defaults" button) */
  resetAllInCategory(category) {
    Object.keys(this.schema.settings).forEach(id => {
      if (this.schema.settings[id].category === category) {
        this.reset(id);
      }
    });
  }
}
