param(
    [switch]$Apply,
    [switch]$IncludeRuntime,
    [switch]$IncludeDependencies,
    [switch]$IncludeResearchScratch
)
$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..')).TrimEnd('\')
$prefix = $root + '\'
$targetPaths = @(Get-ChildItem -LiteralPath $root -Force | Where-Object {
    ($_.PSIsContainer -and ($_.Name -like '.pytest-*' -or $_.Name -eq '.pytest_tmp_phase3_slice' -or $_.Name -eq '.pytest_cache' -or $_.Name -eq '.tmp-video-frames')) -or
    (-not $_.PSIsContainer -and $_.Name -match '^\.tmp-video-frame-\d+\.jpg$')
} | Select-Object -ExpandProperty FullName)
if ($IncludeRuntime) {
    $targetPaths += @(
        '.coverage', '__pycache__', '.env.preview', '.local-server.pid',
        '.local-server.err.log', '.local-server.out.log', '.qa-server.err.log',
        '.qa-server.out.log', '_build_baseline.log', '_pip.log',
        'data/operational/handover-qa.db', 'data/operational/handover-qa2.db',
        'data/operational/handover-qa3.db', 'data/operational/typhoon-local.db'
    ) | ForEach-Object { Join-Path $root $_ }
}
if ($IncludeDependencies) {
    $targetPaths += @('node_modules', 'package.json', 'package-lock.json', 'viz/frontend/node_modules') |
        ForEach-Object { Join-Path $root $_ }
}
if ($IncludeResearchScratch) {
    $targetPaths += @(
        'inspect_nchmf.ps1', 'nchmf_kttv.html', 'nchmf_kttv_headers.txt',
        'nchmf_robots.txt', 'nchmf_robots_headers.txt'
    ) | ForEach-Object { Join-Path $root $_ }
}
$targets = @($targetPaths | Where-Object { Test-Path -LiteralPath $_ } | Sort-Object -Unique | ForEach-Object { Get-Item -LiteralPath $_ -Force })
$rows = @()
foreach ($item in $targets) {
    $resolved = [IO.Path]::GetFullPath($item.FullName)
    if (-not $resolved.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) { throw "Outside workspace: $resolved" }
    if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Linked target: $resolved" }
    $children = if ($item.PSIsContainer) { @(Get-ChildItem -LiteralPath $resolved -Recurse -Force) } else { @($item) }
    # Pytest creates 'current' links; archive links as links, never traverse them.
    $files = @($children | Where-Object { -not $_.PSIsContainer -and -not ($_.Attributes -band [IO.FileAttributes]::ReparsePoint) })
    $relative = $resolved.Substring($prefix.Length)
    $rows += [PSCustomObject]@{ Path=$resolved; Relative=$relative; Files=$files.Count; Bytes=($files | Measure-Object Length -Sum).Sum }
}
$rows | Format-Table Relative,Files,Bytes -AutoSize
if (-not $Apply) { Write-Output 'Dry run only. Use -Apply to move these exact targets to an external recovery folder.'; exit 0 }
$active = @(Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^python' -and $_.CommandLine -match 'pytest' })
if ($active.Count) { throw 'A pytest process is active; retry when it finishes.' }
$backup = Join-Path (Split-Path $root -Parent) ('Typhoon_vn-cleanup-backup-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
if (Test-Path -LiteralPath $backup) { throw 'Backup destination already exists.' }
New-Item -ItemType Directory -Path $backup | Out-Null
$rows | Export-Csv -LiteralPath (Join-Path $backup 'manifest.csv') -NoTypeInformation -Encoding UTF8
foreach ($row in $rows) {
    $destination = [IO.Path]::GetFullPath((Join-Path $backup $row.Relative))
    if (-not $destination.StartsWith($backup + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Invalid destination.' }
    $destinationParent = Split-Path $destination -Parent
    if (-not (Test-Path -LiteralPath $destinationParent)) { New-Item -ItemType Directory -Path $destinationParent -Force | Out-Null }
    Move-Item -LiteralPath $row.Path -Destination $destination
    if ((Test-Path -LiteralPath $row.Path) -or -not (Test-Path -LiteralPath $destination)) { throw "Move failed: $($row.Relative)" }
}
Write-Output "Recovery folder: $backup"
Write-Output "Moved targets: $($rows.Count)"
Write-Output "Files: $(($rows | Measure-Object Files -Sum).Sum)"
Write-Output "Bytes: $(($rows | Measure-Object Bytes -Sum).Sum)"
