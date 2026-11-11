# User guide

Version: 0.1.0-phase7-local

Typhoon VN is a decision-support application, not an official warning system.

Start the backend as described in [deployment](deployment.md), then open its root URL. The dashboard displays storm observations, forecast tracks and local weather when each source is available. Empty/error states mean unavailable data; they are not evidence that there is no storm.

## NCHMF weather

The NCHMF panel shows temperatures at locations published on the public homepage and links to the source bulletins. Search by location name, check the displayed observation date/time (GMT+7), and open the source link for the complete bulletin. The panel labels cached/stale data. It does not infer wind, pressure, rainfall, storm position, severity or affected regions from missing fields.

API: `GET /api/weather/nchmf`.
Export a snapshot: `python -m typhoon_vn.cli scrape-nchmf --output reports/nchmf-weather.json`.

The export includes source URL, retrieval time, observation time and SHA-256 of the fetched page. Historical archive authorization remains pending; this snapshot does not replace approved training data.

## Forecast interpretation

Forecast horizons are +6/+12/+24/+48/+72 hours where supported. Read model/dataset provenance, issue/valid times and baseline/synthetic labels. A displayed uncertainty radius may be illustrative; consult the model card before interpreting it as calibrated coverage. Use official NCHMF guidance for decisions.

The API documentation at /docs describes validated input units and required fields. Real alert recipients and production deployment are separate operator gates.
