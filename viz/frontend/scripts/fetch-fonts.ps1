<#
  Self-host Vietnamese-capable webfonts (WOFF2 only, used weights only).

  Downloads Be Vietnam Pro (UI text, full Vietnamese coverage) and
  JetBrains Mono (tabular numerals) from the official Google Fonts CSS API,
  keeping only the `vietnamese` + `latin` unicode-range subsets.

  Output:
    public/fonts/*.woff2          - font binaries
    src/styles/fonts.css          - generated @font-face declarations

  Usage (from viz/frontend):
    powershell -ExecutionPolicy Bypass -File scripts/fetch-fonts.ps1
#>
[CmdletBinding()]
param(
  [string]$CssApi = 'https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap'
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$fontDir = Join-Path $root 'public\fonts'
$cssOut = Join-Path $root 'src\styles\fonts.css'

New-Item -ItemType Directory -Force -Path $fontDir | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $cssOut) | Out-Null

# A modern browser UA is required for Google Fonts to return woff2 sources.
$ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

Write-Host 'Fetching font CSS from Google Fonts...' -ForegroundColor Cyan
$css = (Invoke-WebRequest -Uri $CssApi -UserAgent $ua -UseBasicParsing -TimeoutSec 30).Content

# Subsets we keep: Vietnamese coverage + basic Latin.
$wanted = @('vietnamese', 'latin')

function Get-Subset([string]$unicodeRange) {
  # Vietnamese subset always includes the Latin Extended Additional block.
  if ($unicodeRange -match 'U\+0102') { return 'vietnamese' }
  # Basic Latin subset starts exactly at U+0000-00FF.
  if ($unicodeRange -match '^\s*U\+0000-00FF') { return 'latin' }
  # Everything else (latin-ext, cyrillic, cyrillic-ext, greek...) is not needed.
  return 'other'
}

$blocks = [regex]::Matches($css, '(?s)@font-face\s*\{(.*?)\}')
Write-Host ("Parsed {0} @font-face blocks." -f $blocks.Count)

$faces = New-Object System.Collections.Generic.List[string]
$downloaded = 0

foreach ($block in $blocks) {
  $body = $block.Groups[1].Value
  $family = [regex]::Match($body, "font-family:\s*'([^']+)'").Groups[1].Value
  $weight = [regex]::Match($body, 'font-weight:\s*(\d+)').Groups[1].Value
  $url = [regex]::Match($body, 'url\((https://[^)]+\.woff2)\)').Groups[1].Value
  $range = [regex]::Match($body, 'unicode-range:\s*([^;]+);').Groups[1].Value.Trim()

  if (-not $family -or -not $weight -or -not $url) { continue }

  $subset = Get-Subset $range
  if ($wanted -notcontains $subset) { continue }

  $slug = ($family -replace '\s+', '') + '-' + $weight + '-' + $subset + '.woff2'
  $dest = Join-Path $fontDir $slug

  if (-not (Test-Path $dest)) {
    Invoke-WebRequest -Uri $url -OutFile $dest -UserAgent $ua -UseBasicParsing -TimeoutSec 60
  }
  $downloaded++

  $faces.Add(@"
@font-face {
  font-family: '$family';
  font-style: normal;
  font-weight: $weight;
  font-display: swap;
  src: url('/fonts/$slug') format('woff2');
  unicode-range: $range;
}
"@)
}

$header = @'
/* ------------------------------------------------------------------
   Self-hosted webfonts - GENERATED FILE, do not edit by hand.
   Regenerate with: powershell -ExecutionPolicy Bypass -File scripts/fetch-fonts.ps1
   Families: Be Vietnam Pro (UI), JetBrains Mono (tabular data)
   Subsets: vietnamese, latin  |  Weights: 400/500/600/700, 400/500
   ------------------------------------------------------------------ */
'@

Set-Content -Path $cssOut -Value ($header + "`n" + ($faces -join "`n")) -Encoding utf8

Write-Host ("Done. {0} faces, files in {1}" -f $downloaded, $fontDir) -ForegroundColor Green
Get-ChildItem $fontDir | Select-Object Name, @{n = 'KB'; e = { [math]::Round($_.Length / 1KB, 1) } } | Format-Table -AutoSize
