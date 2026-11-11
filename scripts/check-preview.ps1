param([string]$BaseUrl = 'http://127.0.0.1:8080')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$previewEnv = Join-Path $projectRoot '.env.preview'
$apiKey = if (Test-Path -LiteralPath $previewEnv) {
    $line = Get-Content -LiteralPath $previewEnv |
        Where-Object { $_ -match '^API_KEY=' } |
        Select-Object -First 1
    if ($line) { $line.Substring('API_KEY='.Length).Trim() }
}
foreach ($route in @('/health', '/ready', '/version', '/typhoons/active')) {
    $headers = @{}
    if ($route -eq '/typhoons/active' -and $apiKey) {
        $headers['X-API-Key'] = $apiKey
    }
    $result = Invoke-WebRequest -UseBasicParsing -Uri ($BaseUrl + $route) -Headers $headers -TimeoutSec 30
    if ($result.StatusCode -ne 200 -or $result.Headers['Content-Type'] -notmatch 'application/json') {
        throw "API check failed: $route"
    }
    Write-Host "OK $route"
}
$page = Invoke-WebRequest -UseBasicParsing -Uri $BaseUrl -TimeoutSec 30
if ($page.Content -notmatch '<div id="root">') { throw 'Dashboard HTML missing' }
$assets = [regex]::Matches($page.Content, '(?:src|href)="(/assets/[^\"]+)"')
if ($assets.Count -eq 0) { throw 'Compiled assets missing' }
foreach ($asset in $assets) {
    $response = Invoke-WebRequest -UseBasicParsing -Uri ($BaseUrl + $asset.Groups[1].Value) -TimeoutSec 30
    if ($response.StatusCode -ne 200 -or $response.Headers['Content-Type'] -match 'text/html') {
        throw 'Compiled asset request returned invalid content'
    }
}
Write-Host 'OK dashboard and compiled assets'
