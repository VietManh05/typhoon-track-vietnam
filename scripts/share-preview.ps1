$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
& "$PSScriptRoot/check-preview.ps1"
docker compose --env-file .env.preview -f docker-compose.preview.yml -f docker-compose.share.yml up -d --no-deps tunnel
if ($LASTEXITCODE -ne 0) { throw 'Could not start public preview tunnel' }
Write-Host 'Public demo only. Keep this computer and Docker running. The URL changes when the tunnel is recreated.'
Write-Host 'Find your https://...trycloudflare.com URL below (retry the logs command after a few seconds if needed):'
docker compose --env-file .env.preview -f docker-compose.preview.yml -f docker-compose.share.yml logs --tail=30 tunnel
Write-Host 'Stop sharing: docker compose --env-file .env.preview -f docker-compose.preview.yml -f docker-compose.share.yml stop tunnel'
