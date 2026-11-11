$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot
if (-not (Test-Path -LiteralPath '.env.preview')) {
    $secretBytes = New-Object byte[] 32
    $random = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try { $random.GetBytes($secretBytes) } finally { $random.Dispose() }
    $previewKey = [BitConverter]::ToString($secretBytes).Replace('-', '').ToLowerInvariant()
    [System.IO.File]::WriteAllText((Join-Path $projectRoot '.env.preview'), "API_KEY=$previewKey`n", (New-Object System.Text.UTF8Encoding($false)))
}
docker compose --env-file .env.preview -f docker-compose.preview.yml up -d --build
if ($LASTEXITCODE -ne 0) { throw 'Docker preview failed to start. Check Docker Desktop and compose logs.' }
Write-Host 'Dashboard: http://127.0.0.1:8080'
