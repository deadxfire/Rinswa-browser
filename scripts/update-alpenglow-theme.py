import json
import os

manifest_data = {
    "manifest_version": 2,
    "browser_specific_settings": {
        "gecko": {
            "id": "firefox-alpenglow@mozilla.org"
        }
    },
    "name": "Rinswa Glossy Ribbon",
    "description": "Signature Glossy Multicolour Ribbon Theme for Rinswa Browser.",
    "author": "Rinswa",
    "version": "1.6.0",
    "icons": {"32": "icon.svg"},
    "theme": {
        "images": {
            "additional_backgrounds": [
                "background-noodles-right.svg",
                "background-noodles-left.svg",
                {"linear-gradient": "to bottom, #090616 0%, #160e2e 50%"}
            ]
        },
        "properties": {
            "additional_backgrounds_alignment": ["right top", "left top", "right top"],
            "additional_backgrounds_tiling": ["no-repeat", "no-repeat", "repeat-x"],
            "additional_backgrounds_size": ["auto", "auto", "auto 144px"],
            "zap_gradient": "linear-gradient(90deg, #00f2fe 0%, #0072ff 25%, #6366f1 50%, #a855f7 75%, #ec4899 100%)"
        },
        "colors": {
            "frame": "#0e0822",
            "toolbar": "hsla(260, 48%, 14%, .96)",
            "button_background_active": "hsla(255, 100%, 94%, .24)",
            "button_background_hover": "hsla(255, 100%, 94%, .12)",
            "icons": "#a5b4fc",
            "icons_attention": "#00f2fe",
            "toolbar_text": "#f8fafc",
            "toolbar_vertical_separator": "rgba(255, 255, 255, 0.15)",
            "toolbar_field": "hsla(260, 40%, 18%, 1)",
            "toolbar_field_focus": "hsla(260, 45%, 15%, .98)",
            "toolbar_field_text": "#ffffff",
            "toolbar_field_text_focus": "#ffffff",
            "toolbar_field_border": "transparent",
            "toolbar_field_border_focus": "#00f2fe",
            "toolbar_field_highlight": "rgba(0, 242, 254, 0.32)",
            "toolbar_top_separator": "transparent",
            "toolbar_bottom_separator": "rgba(255, 255, 255, 0.1)",
            "bookmark_text": "#f8fafc",
            "tab_selected": "rgb(45, 23, 84)",
            "tab_text": "#ffffff",
            "tab_background_text": "#94a3b8",
            "tab_background_separator": "rgba(255, 255, 255, 0.1)",
            "tab_line": "#00f2fe",
            "tab_loading": "#00f2fe",
            "ntp_background": "#090616",
            "ntp_text": "#f8fafc",
            "popup": "hsla(260, 45%, 15%, 1)",
            "popup_text": "#f8fafc",
            "popup_border": "rgba(168, 85, 247, 0.35)",
            "popup_highlight": "rgba(99, 102, 241, 0.2)",
            "popup_highlight_text": "#ffffff",
            "popup_icon": "#a5b4fc",
            "sidebar": "hsla(260, 45%, 15%, 1)",
            "sidebar_text": "#f8fafc",
            "sidebar_border": "rgba(255, 255, 255, 0.1)",
            "sidebar_highlight": "#00f2fe",
            "sidebar_highlight_text": "#ffffff",
            "focus_outline": "#00f2fe"
        }
    },
    "dark_theme": {
        "images": {
            "additional_backgrounds": [
                "background-noodles-right-dark.svg",
                "background-noodles-left-dark.svg",
                {"linear-gradient": "to bottom, #090616 0%, #160e2e 50%"}
            ]
        },
        "properties": {
            "additional_backgrounds_alignment": ["right top", "left top", "right top"],
            "additional_backgrounds_tiling": ["no-repeat", "no-repeat", "repeat-x"],
            "additional_backgrounds_size": ["auto", "auto", "auto 144px"],
            "zap_gradient": "linear-gradient(90deg, #00f2fe 0%, #0072ff 25%, #6366f1 50%, #a855f7 75%, #ec4899 100%)"
        },
        "colors": {
            "frame": "#0e0822",
            "toolbar": "hsla(260, 48%, 14%, .96)",
            "button_background_active": "hsla(255, 100%, 94%, .24)",
            "button_background_hover": "hsla(255, 100%, 94%, .12)",
            "icons": "#a5b4fc",
            "icons_attention": "#00f2fe",
            "toolbar_text": "#f8fafc",
            "toolbar_vertical_separator": "rgba(255, 255, 255, 0.15)",
            "toolbar_field": "hsla(260, 40%, 18%, 1)",
            "toolbar_field_focus": "hsla(260, 45%, 15%, .98)",
            "toolbar_field_text": "#ffffff",
            "toolbar_field_text_focus": "#ffffff",
            "toolbar_field_border": "transparent",
            "toolbar_field_border_focus": "#00f2fe",
            "toolbar_field_highlight": "rgba(0, 242, 254, 0.32)",
            "toolbar_top_separator": "transparent",
            "toolbar_bottom_separator": "rgba(255, 255, 255, 0.1)",
            "bookmark_text": "#f8fafc",
            "tab_selected": "rgb(45, 23, 84)",
            "tab_text": "#ffffff",
            "tab_background_text": "#94a3b8",
            "tab_background_separator": "rgba(255, 255, 255, 0.1)",
            "tab_line": "#00f2fe",
            "tab_loading": "#00f2fe",
            "ntp_background": "#090616",
            "ntp_text": "#f8fafc",
            "popup": "hsla(260, 45%, 15%, 1)",
            "popup_text": "#f8fafc",
            "popup_border": "rgba(168, 85, 247, 0.35)",
            "popup_highlight": "rgba(99, 102, 241, 0.2)",
            "popup_highlight_text": "#ffffff",
            "popup_icon": "#a5b4fc",
            "sidebar": "hsla(260, 45%, 15%, 1)",
            "sidebar_text": "#f8fafc",
            "sidebar_border": "rgba(255, 255, 255, 0.1)",
            "sidebar_highlight": "#00f2fe",
            "sidebar_highlight_text": "#ffffff",
            "focus_outline": "#00f2fe"
        }
    }
}

root = r"c:\Users\arind\OneDrive\Documents\Project\browser"
dirs = [
    os.path.join(root, "rinswa-stable", "browser", "themes", "addons", "alpenglow"),
    os.path.join(root, "mozilla-central", "browser", "themes", "addons", "alpenglow"),
    os.path.join(root, "rinswa-stable", "obj-rinswa", "dist", "bin", "browser", "chrome", "browser", "content", "builtin-themes", "alpenglow"),
]

for d in dirs:
    if os.path.exists(d):
        p = os.path.join(d, "manifest.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2)
        print("Updated manifest in", d)

print("Alpenglow manifest update complete!")
