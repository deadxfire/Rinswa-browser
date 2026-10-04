"""Generate signature Rinswa glossy ribbon wave SVGs and assets based on Glossy Multicolour Ribbon R Emblem"""
import os
import base64
import json

svg_left = """<svg width="320" height="144" viewBox="0 0 320 144" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Cyan to Royal Blue gradient -->
    <linearGradient id="ribbon-cyan-blue" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f2fe" stop-opacity="0.95"/>
      <stop offset="45%" stop-color="#0072ff" stop-opacity="0.9"/>
      <stop offset="85%" stop-color="#6366f1" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#6366f1" stop-opacity="0"/>
    </linearGradient>

    <!-- Royal Blue to Indigo gradient -->
    <linearGradient id="ribbon-blue-indigo" x1="0%" y1="100%" x2="100%" y2="10%">
      <stop offset="0%" stop-color="#0072ff" stop-opacity="0.9"/>
      <stop offset="50%" stop-color="#6366f1" stop-opacity="0.85"/>
      <stop offset="85%" stop-color="#a855f7" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#a855f7" stop-opacity="0"/>
    </linearGradient>

    <!-- Indigo to Purple & Magenta gradient -->
    <linearGradient id="ribbon-indigo-magenta" x1="5%" y1="100%" x2="95%" y2="0%">
      <stop offset="0%" stop-color="#6366f1" stop-opacity="0.88"/>
      <stop offset="45%" stop-color="#a855f7" stop-opacity="0.82"/>
      <stop offset="80%" stop-color="#ec4899" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#ff758c" stop-opacity="0"/>
    </linearGradient>

    <!-- Vivid Magenta to Peach/Coral flare -->
    <linearGradient id="ribbon-magenta-flare" x1="0%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#ec4899" stop-opacity="0.85"/>
      <stop offset="60%" stop-color="#ff758c" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#ff9a76" stop-opacity="0"/>
    </linearGradient>

    <!-- Deep Cosmic Violet base curve -->
    <linearGradient id="ribbon-cosmic-base" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2d1254" stop-opacity="0.85"/>
      <stop offset="60%" stop-color="#1b0b36" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#0e061e" stop-opacity="0"/>
    </linearGradient>

    <!-- Glossy Specular Sheen -->
    <linearGradient id="ribbon-gloss" x1="10%" y1="100%" x2="90%" y2="10%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.8"/>
      <stop offset="35%" stop-color="#ffffff" stop-opacity="0.25"/>
      <stop offset="70%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- Deep base cosmic shadow/depth wave -->
  <path d="M0 0 C50 14 110 48 145 96 C175 132 210 140 270 144 L0 144 Z" fill="url(#ribbon-cosmic-base)"/>

  <!-- Back Ribbon: Indigo to Magenta sweep -->
  <path d="M0 18 C60 24 125 60 160 108 C185 138 220 142 270 144 L195 144 C155 138 120 120 96 92 C65 56 30 30 0 28 Z" fill="url(#ribbon-indigo-magenta)"/>

  <!-- Middle Ribbon: Blue to Indigo sweep -->
  <path d="M0 48 C52 52 105 84 135 122 C152 140 178 143 215 144 L150 144 C120 140 96 130 78 104 C54 74 25 54 0 52 Z" fill="url(#ribbon-blue-indigo)"/>

  <!-- Fore Ribbon: Electric Cyan to Royal Blue highlight wave -->
  <path d="M0 76 C42 78 82 102 108 132 C120 142 138 144 162 144 L108 144 C86 142 70 134 55 116 C36 92 18 80 0 78 Z" fill="url(#ribbon-cyan-blue)"/>

  <!-- Coral Magenta Accent Flare on the leading crest -->
  <path d="M0 102 C28 104 56 120 74 140 C82 143 92 144 108 144 L62 144 C46 142 34 136 22 126 C12 112 5 106 0 104 Z" fill="url(#ribbon-magenta-flare)"/>

  <!-- Glossy 3D specular highlight curves -->
  <path d="M0 76 C42 78 82 102 108 132 C120 142 138 144 162 144" stroke="url(#ribbon-gloss)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
  <path d="M0 48 C52 52 105 84 135 122 C152 140 178 143 215 144" stroke="url(#ribbon-gloss)" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.75"/>
  <path d="M0 18 C60 24 125 60 160 108 C185 138 220 142 270 144" stroke="url(#ribbon-gloss)" stroke-width="1.2" stroke-linecap="round" fill="none" opacity="0.5"/>
</svg>"""

svg_right = """<svg width="320" height="144" viewBox="0 0 320 144" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Magenta to Purple gradient -->
    <linearGradient id="ribbon-right-magenta" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ec4899" stop-opacity="0.88"/>
      <stop offset="50%" stop-color="#a855f7" stop-opacity="0.82"/>
      <stop offset="85%" stop-color="#6366f1" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#6366f1" stop-opacity="0"/>
    </linearGradient>

    <!-- Indigo to Cyan gradient -->
    <linearGradient id="ribbon-right-cyan" x1="100%" y1="10%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#00f2fe" stop-opacity="0.92"/>
      <stop offset="45%" stop-color="#0072ff" stop-opacity="0.85"/>
      <stop offset="85%" stop-color="#6366f1" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#6366f1" stop-opacity="0"/>
    </linearGradient>

    <!-- Deep Cosmic base -->
    <linearGradient id="ribbon-right-cosmic" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#2d1254" stop-opacity="0.8"/>
      <stop offset="70%" stop-color="#1b0b36" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#0e061e" stop-opacity="0"/>
    </linearGradient>

    <!-- Specular Gloss -->
    <linearGradient id="ribbon-right-gloss" x1="100%" y1="0%" x2="10%" y2="90%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.75"/>
      <stop offset="40%" stop-color="#ffffff" stop-opacity="0.2"/>
      <stop offset="80%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <path d="M320 0 C270 14 210 48 175 96 C145 132 110 140 50 144 L320 144 Z" fill="url(#ribbon-right-cosmic)"/>
  <path d="M320 18 C260 24 195 60 160 108 C135 138 100 142 50 144 L125 144 C165 138 200 120 224 92 C255 56 290 30 320 28 Z" fill="url(#ribbon-right-magenta)"/>
  <path d="M320 52 C268 54 215 86 185 122 C168 140 142 143 105 144 L170 144 C200 140 224 130 242 104 C266 74 295 56 320 54 Z" fill="url(#ribbon-right-cyan)"/>
  <path d="M320 18 C260 24 195 60 160 108 C135 138 100 142 50 144" stroke="url(#ribbon-right-gloss)" stroke-width="2" stroke-linecap="round" fill="none"/>
  <path d="M320 52 C268 54 215 86 185 122 C168 140 142 143 105 144" stroke="url(#ribbon-right-gloss)" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.7"/>
</svg>"""

root = r"c:\Users\arind\OneDrive\Documents\Project\browser"

# Save to ui/
os.makedirs(os.path.join(root, "ui"), exist_ok=True)
with open(os.path.join(root, "ui", "rinswa-ribbon-left.svg"), "w", encoding="utf-8") as f:
    f.write(svg_left)
with open(os.path.join(root, "ui", "rinswa-ribbon-right.svg"), "w", encoding="utf-8") as f:
    f.write(svg_right)

# Save to branding/generated
os.makedirs(os.path.join(root, "branding", "generated"), exist_ok=True)
with open(os.path.join(root, "branding", "generated", "rinswa-ribbon-left.svg"), "w", encoding="utf-8") as f:
    f.write(svg_left)
with open(os.path.join(root, "branding", "generated", "rinswa-ribbon-right.svg"), "w", encoding="utf-8") as f:
    f.write(svg_right)

# Also update the built-in theme (alpenglow) in all 3 locations with Rinswa ribbon art!
alpenglow_dirs = [
    os.path.join(root, "rinswa-stable", "browser", "themes", "addons", "alpenglow"),
    os.path.join(root, "mozilla-central", "browser", "themes", "addons", "alpenglow"),
    os.path.join(root, "rinswa-stable", "obj-rinswa", "dist", "bin", "browser", "chrome", "browser", "content", "builtin-themes", "alpenglow"),
]

for d in alpenglow_dirs:
    if os.path.exists(d):
        with open(os.path.join(d, "background-noodles-left-dark.svg"), "w", encoding="utf-8") as f:
            f.write(svg_left)
        with open(os.path.join(d, "background-noodles-right-dark.svg"), "w", encoding="utf-8") as f:
            f.write(svg_right)
        with open(os.path.join(d, "background-noodles-left.svg"), "w", encoding="utf-8") as f:
            f.write(svg_left)
        with open(os.path.join(d, "background-noodles-right.svg"), "w", encoding="utf-8") as f:
            f.write(svg_right)
        print("Updated ribbon noodles in", d)

print("Ribbon generation and alpenglow update completed successfully!")
