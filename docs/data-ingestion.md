# Phase 1 data ingestion

## Scope and safety

The pipeline preserves downloaded objects as raw evidence. It never rewrites a
source file in place, and writes a SHA-256 checksum plus URL, response metadata,
parser name, version, and download time into `data/raw/lineage/`. Raw input is
not automatically clean or training-ready; validation and unit conversion are
Phase 2 work.

Do not download, redistribute, or scrape a source unless its current terms
permit the intended use. Do not put an API token, unlicensed data, or raw file
into Git.

## Source catalogue

| Source | Role | Acquisition method | Constraint |
| --- | --- | --- | --- |
| CMA-BST | Annual WP best track, 1949 onward (official page verified through 2025) | `fetch cma` builds `CHYYYYBST.txt` URLs | Retain CMA citation |
| IBTrACS v4r01 | Primary normalised track source | `fetch ibtracs` | Updated frequently; retain checksum |
| JMA RSMC | WP cross-check (official archive currently spans 1951–2026) | `fetch jma` | Public all-years ZIP archive |
| JTWC | WP cross-check | `fetch jtwc --manifest` | Approved URLs only |
| NCHMF | Vietnam-local bulletin observations | Approved CSV export | Authorised archive required |
| PCTT | Provincial impact labels | Approved CSV export | Licence review required |
| GADM 4.1 | Vietnam admin boundaries | `fetch gadm` | Academic/non-commercial terms; no redistribution without permission |
| GSHHG | Coastline for landfall analysis | `fetch gshhg --url ...` | Explicit release URL required |
| NOAA OISST v2.1 | Daily SST field | `fetch oisst --date YYYY-MM-DD` | NetCDF retained raw |
| ERA5 | MSLP, pressure-level winds, humidity | Bounded CDS API request | Account and terms required |
| GFS | Optional operational field | `fetch gfs` | Not a reanalysis substitute |

## Install and fetch

Use Python 3.11. The current workspace only has Python 3.14 and is deliberately
rejected by the project metadata.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
Copy-Item .env.example .env
python -m pip install -e ".[ingestion]"

# Full published CMA interval bounded at the latest verified annual release.
python -m typhoon_vn.ingestion.cli fetch cma --start-year 1949 --end-year 2025
python -m typhoon_vn.ingestion.cli fetch ibtracs
python -m typhoon_vn.ingestion.cli fetch jma
python -m typhoon_vn.ingestion.cli fetch oisst --date 2025-09-01
```

No source is fetched without an explicit command. Each download retries transient
errors up to four times, then fails on a HTTP 4xx error or a checksum mismatch.
Use `--data-root <safe-path>` to write elsewhere.

JTWC archive layout can change, so create a reviewed UTF-8 manifest with one
official URL per line:

```powershell
python -m typhoon_vn.ingestion.cli fetch jtwc --manifest docs/jtwc-urls.txt
```

For an authorised local source export, parse it to the canonical raw schema:

```powershell
python -m typhoon_vn.ingestion.cli parse nchmf `
  --input data/raw/downloads/nchmf/bulletins.csv `
  --source-url "https://archive.example/record"
```

NCHMF columns are `timestamp,storm_id,latitude,longitude,wind_kt,pressure_hpa,name`.
PCTT records use `storm_id,province,impact_type,severity,event_time,reference`.
Preserve original source documents and their URLs; do not use a fragile blind web
scrape. Input timestamps should carry an offset; convert known Vietnam-local
times to UTC in the authorised export and keep the original record as evidence.

## Storage and reconciliation

```text
data/raw/observations/source=<source>/year=<UTC year>/part-00000.parquet
data/raw/impact_labels/part-00000.parquet
data/raw/lineage/<source>/<timestamp>-<checksum>.json
```

The schema contains source/source storm IDs, canonical ID, UTC time, coordinates,
source wind value/unit, pressure, URL, SHA-256, source version, and contributors.
ATCF-shaped IDs are generated only when source evidence establishes them; other
IDs are deliberately unresolved. A merge requires the same resolved ID, time
separation no greater than three hours, and location separation no greater than
75 km. IBTrACS wins priority over JTWC, JMA, CMA, then NCHMF; conflicts are kept
as metadata and never averaged.

HTTP acceptance tests use deterministic fake responses for 200, 404, 429,
timeout, empty payload and checksum behaviour. Full history is only fetched by
an explicit operator command; tests never scrape or mirror upstream archives.

## Environment fields and scheduling

OISST raw NetCDF is cached by UTC day. ERA5 retrieval is deliberately bounded
and requires a configured CDS API account; the project never stores a token in
Git. Optional GFS downloads record their run cycle and lead hour. Sampling fields
at storm locations and computing SST gradients/wind shear are Phase 2 work.

[`infra/scheduler/typhoon-data.cron`](../infra/scheduler/typhoon-data.cron)
provides daily June-November updates and weekly out-of-season updates. Set
`PROJECT_DIR`, run a non-interactive Python 3.11 environment, and send output to
the deployment logging system. Do not schedule an unbounded ERA5 backfill.

## Authoritative sources

- [CMA best-track dataset](https://tcdata.typhoon.org.cn/zjljsjj.html)
- [NOAA IBTrACS v4r01](https://www.ncei.noaa.gov/products/international-best-track-archive)
- [JMA RSMC best-track archive](https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/besttrack.html)
- [JTWC best-track information](https://www.metoc.navy.mil/jtwc/jtwc.html?best-tracks)
- [NOAA OISST v2.1](https://www.ncei.noaa.gov/products/optimum-interpolation-sst)
