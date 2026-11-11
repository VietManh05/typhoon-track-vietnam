param(
    [int]$Port = 8011
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$python = Join-Path $root ".venv\Scripts\python.exe"
$database = Join-Path $root "data\operational\dashboard-runtime.db"
$databaseUrl = "sqlite:///$(($database -replace '\\', '/'))"
$baseUrl = "http://127.0.0.1:$Port"
$stormId = "WP-DASH-RUNTIME"
$server = $null

Remove-Item $database -Force -ErrorAction SilentlyContinue
$env:APP_ENV = "development"
$env:OPERATIONAL_DATABASE_URL = $databaseUrl
$env:CACHE_ENABLED = "false"
$env:ALLOW_BASELINE = "true"
$env:REQUIRE_API_KEY = "false"
$env:TYPHOON_BASE_URL = $baseUrl
$env:TYPHOON_EXPECT_STORM_ID = $stormId

try {
    $arguments = @("-m", "uvicorn", "typhoon_vn.api.app:app", "--host", "127.0.0.1", "--port", $Port)
    $server = Start-Process -FilePath $python -ArgumentList $arguments -WorkingDirectory $root -PassThru -NoNewWindow

    $ready = $false
    for ($attempt = 1; $attempt -le 30; $attempt++) {
        if ($server.HasExited) {
            throw "Uvicorn exited before becoming healthy (exit $($server.ExitCode))"
        }
        try {
            $health = Invoke-RestMethod -Uri "$baseUrl/health" -TimeoutSec 1
            if ($health.status -eq "ok") {
                $ready = $true
                break
            }
        } catch {
            Start-Sleep -Milliseconds 250
        }
    }
    if (-not $ready) {
        throw "Dashboard API did not become healthy at $baseUrl"
    }

    $now = [DateTime]::UtcNow
    $fixes = @(
        @{ offset = -18; lat = 13.0; lon = 115.0; wind = 25.0; pressure = 990.0 },
        @{ offset = -12; lat = 13.25; lon = 115.4; wind = 27.0; pressure = 988.0 },
        @{ offset = -6; lat = 13.5; lon = 115.8; wind = 29.0; pressure = 986.0 },
        @{ offset = 0; lat = 13.75; lon = 116.2; wind = 31.0; pressure = 984.0 }
    ) | ForEach-Object {
        @{
            timestamp = $now.AddHours($_.offset).ToString("yyyy-MM-ddTHH:mm:ssZ")
            lat = $_.lat
            lon = $_.lon
            wind_ms = $_.wind
            pressure_hpa = $_.pressure
            intensity = "TS"
            source = "local-runtime-fixture"
        }
    }
    $body = @{
        storm_id = $stormId
        name = "Dashboard runtime fixture"
        observations = $fixes
    } | ConvertTo-Json -Depth 5

    $stored = Invoke-RestMethod -Method Post -Uri "$baseUrl/observations" -ContentType "application/json" -Body $body
    if ($stored.status -ne "stored" -or $stored.forecast_ids.Count -lt 1) {
        throw "Observation-to-forecast seed failed"
    }

    & $python (Join-Path $PSScriptRoot "verify_dashboard_http.py")
    if ($LASTEXITCODE -ne 0) {
        throw "Dashboard HTTP verification failed with exit code $LASTEXITCODE"
    }
} finally {
    if ($null -ne $server -and -not $server.HasExited) {
        Stop-Process -Id $server.Id -Force
        $server.WaitForExit()
    }
    $databaseFiles = @(
        $database,
        "$database-shm",
        "$database-wal",
        "$database-journal"
    )
    for ($attempt = 1; $attempt -le 10; $attempt++) {
        Remove-Item $databaseFiles -Force -ErrorAction SilentlyContinue
        if (-not ($databaseFiles | Where-Object { Test-Path $_ })) {
            break
        }
        Start-Sleep -Milliseconds 100
    }
    $leftovers = @($databaseFiles | Where-Object { Test-Path $_ })
    if ($leftovers.Count -gt 0) {
        throw "Could not clean runtime database files: $($leftovers -join ', ')"
    }
}
