"""Generate Rinswa Smart Tab Manager icons with signature ribbon aesthetics"""
import os
import math
from PIL import Image, ImageDraw

out_dir = r"c:\Users\arind\OneDrive\Documents\Project\browser\extensions\smart-tabs\icons"
os.makedirs(out_dir, exist_ok=True)

sizes = [16, 32, 48, 128]

for size in sizes:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    pad = max(1, size // 10)
    w = size - 2 * pad
    h = size - 2 * pad
    radius = max(2, size // 6)
    
    # Draw glossy rounded container with dark glass
    # Top card (folder/tab stack)
    # Background glass tab back
    back_y = pad
    draw.rounded_rectangle(
        [pad + size//8, back_y, pad + w, back_y + h * 0.75],
        radius=radius,
        fill=(99, 102, 241, 180),
        outline=(168, 85, 247, 220),
        width=max(1, size // 32)
    )
    
    # Middle glass tab
    mid_y = pad + size // 10
    draw.rounded_rectangle(
        [pad + size//16, mid_y, pad + w - size//16, mid_y + h * 0.78],
        radius=radius,
        fill=(0, 114, 255, 210),
        outline=(0, 242, 254, 240),
        width=max(1, size // 32)
    )
    
    # Fore glass tab with Rinswa ribbon gradient
    fore_y = pad + size // 5
    draw.rounded_rectangle(
        [pad, fore_y, pad + w - size//8, pad + h],
        radius=radius,
        fill=(15, 10, 35, 245),
        outline=(0, 242, 254, 255),
        width=max(1, size // 24)
    )
    
    # Draw glowing neon ribbon bar at bottom of front card
    bar_h = max(2, size // 14)
    bar_y = pad + h - bar_h - max(1, size // 20)
    bar_w = w - size//8 - 2 * max(1, size // 16)
    bar_x = pad + max(1, size // 16)
    
    for i in range(int(bar_w)):
        ratio = i / max(1, bar_w)
        # Gradient: Cyan (0,242,254) -> Blue (0,114,255) -> Purple (168,85,247) -> Pink (236,72,153)
        if ratio < 0.33:
            r = int(0 + (0 - 0) * (ratio / 0.33))
            g = int(242 + (114 - 242) * (ratio / 0.33))
            b = 255
        elif ratio < 0.66:
            sub = (ratio - 0.33) / 0.33
            r = int(0 + (168 - 0) * sub)
            g = int(114 + (85 - 114) * sub)
            b = int(255 + (247 - 255) * sub)
        else:
            sub = (ratio - 0.66) / 0.34
            r = int(168 + (236 - 168) * sub)
            g = int(85 + (72 - 85) * sub)
            b = int(247 + (153 - 247) * sub)
        draw.line([(bar_x + i, bar_y), (bar_x + i, bar_y + bar_h)], fill=(r, g, b, 255), width=1)
        
    # Draw sparkles or clean tab indicators inside fore card if size >= 32
    if size >= 32:
        tab_dot_r = max(1, size // 30)
        dot_y = fore_y + size // 10
        dot_x = pad + size // 10
        draw.ellipse([dot_x - tab_dot_r, dot_y - tab_dot_r, dot_x + tab_dot_r, dot_y + tab_dot_r], fill=(0, 242, 254, 255))
        draw.line([dot_x + tab_dot_r * 3, dot_y, dot_x + size // 3, dot_y], fill=(248, 250, 252, 220), width=max(1, size // 30))
        
    out_file = os.path.join(out_dir, f"icon-{size}.png")
    img.save(out_file, "PNG")
    print(f"Generated {out_file}")

# Also generate icon.svg for clean scalable vector
svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" fill="none">
  <defs>
    <linearGradient id="ribbon" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f2fe"/>
      <stop offset="35%" stop-color="#0072ff"/>
      <stop offset="70%" stop-color="#a855f7"/>
      <stop offset="100%" stop-color="#ec4899"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e1346"/>
      <stop offset="100%" stop-color="#0d0822"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>
  <!-- Back Tab -->
  <rect x="28" y="14" width="86" height="72" rx="14" fill="#6366f1" fill-opacity="0.3" stroke="#a855f7" stroke-width="2"/>
  <!-- Middle Tab -->
  <rect x="20" y="26" width="88" height="74" rx="14" fill="#0072ff" fill-opacity="0.4" stroke="#00f2fe" stroke-width="2"/>
  <!-- Front Tab -->
  <rect x="12" y="38" width="94" height="76" rx="14" fill="url(#cardGrad)" stroke="#00f2fe" stroke-width="2.5" filter="url(#glow)"/>
  <!-- Tab item lines -->
  <circle cx="28" cy="56" r="4" fill="#00f2fe"/>
  <rect x="40" y="53" width="46" height="6" rx="3" fill="#f8fafc" fill-opacity="0.9"/>
  <circle cx="28" cy="74" r="4" fill="#a855f7"/>
  <rect x="40" y="71" width="36" height="6" rx="3" fill="#94a3b8" fill-opacity="0.8"/>
  <!-- Ribbon stripe bottom -->
  <rect x="22" y="96" width="74" height="6" rx="3" fill="url(#ribbon)"/>
</svg>"""

with open(os.path.join(out_dir, "icon.svg"), "w", encoding="utf-8") as f:
    f.write(svg_content)
print("Generated icon.svg")
