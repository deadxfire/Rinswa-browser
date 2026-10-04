# Rinswa branding asset generator.
# Extracts the largest image from branding/icons/default.ico and renders every
# PNG size the Firefox branding directory needs into branding/generated/.

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$root   = Split-Path -Parent $PSScriptRoot
$icoPath = Join-Path $root 'branding\icons\default.ico'
$outDir  = Join-Path $root 'branding\generated'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

# --- Read the ICO directory and pick the largest entry -----------------------
$bytes = [System.IO.File]::ReadAllBytes($icoPath)
$count = [BitConverter]::ToUInt16($bytes, 4)
$best = $null
for ($i = 0; $i -lt $count; $i++) {
    $o = 6 + 16 * $i
    $w = if ($bytes[$o] -eq 0) { 256 } else { $bytes[$o] }
    $entry = [pscustomobject]@{
        Width  = $w
        Size   = [BitConverter]::ToUInt32($bytes, $o + 8)
        Offset = [BitConverter]::ToUInt32($bytes, $o + 12)
    }
    if (-not $best -or $entry.Width -gt $best.Width) { $best = $entry }
}

$isPng = $bytes[$best.Offset] -eq 0x89 -and $bytes[$best.Offset + 1] -eq 0x50
if ($isPng) {
    $ms = New-Object System.IO.MemoryStream(, $bytes[$best.Offset..($best.Offset + $best.Size - 1)])
    $source = [System.Drawing.Bitmap]::FromStream($ms)
} else {
    $source = (New-Object System.Drawing.Icon($icoPath, $best.Width, $best.Width)).ToBitmap()
}
Write-Host "Source icon: $($source.Width)x$($source.Height) (png=$isPng)"

function Save-Resized([int]$w, [int]$h, [string]$name) {
    $bmp = New-Object System.Drawing.Bitmap($w, $h, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.InterpolationMode  = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.SmoothingMode      = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $g.PixelOffsetMode    = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
    $g.Clear([System.Drawing.Color]::Transparent)
    $side = [Math]::Min($w, $h)
    $g.DrawImage($source, [int](($w - $side) / 2), [int](($h - $side) / 2), $side, $side)
    $g.Dispose()
    $bmp.Save((Join-Path $outDir $name), [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()
}

foreach ($s in 16, 22, 24, 32, 48, 64, 128, 256) { Save-Resized $s $s "default$s.png" }
Save-Resized 192 192 'about-logo.png'
Save-Resized 384 384 'about-logo@2x.png'
Save-Resized 192 192 'about-logo-private.png'
Save-Resized 384 384 'about-logo-private@2x.png'
Save-Resized 192 192 'about.png'
Save-Resized 150 150 'VisualElements_150.png'
Save-Resized 70  70  'VisualElements_70.png'
Save-Resized 150 150 'PrivateBrowsing_150.png'
Save-Resized 70  70  'PrivateBrowsing_70.png'

$source.Dispose()
Write-Host "Rinswa branding assets written to $outDir"
