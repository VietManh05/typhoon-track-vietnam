# Classical baselines

PersistenceForecaster consumes physical latitude/longitude as the first two features of a (batch, time, features) tensor. Time slots are a regular grid (default six hours). A mask selects the last two valid positions; missing slots retain their elapsed time. Forecast horizons are measured from the last valid observation, including when the input has trailing padding.

Motion per time step = displacement / difference in selected time indices. Longitude displacement uses the short wrapped difference; predictions wrap to [-180, 180). This is linear motion in coordinate degrees, not a geodesic constant-bearing trajectory. Irregular timestamps must first be mapped to the regular input grid.

Example: (10,100) at 00:00 and (12,102) at 12:00 with 06:00 masked gives (13,103) at +6h, not (14,104). Stationary inputs remain stationary. CLIPERForecaster is a damped-persistence proxy, not an operational CLIPER implementation.

Run `python -m pytest tests/test_baselines.py tests/test_evaluation.py -q`. Tests include stationary/linear motion, east/west antimeridian crossings, masked gaps, mixed batches and shared damped motion. Functional correctness is not a meteorological skill claim.
