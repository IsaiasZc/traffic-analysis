# config.py — processed CSV paths used by the dashboard at runtime.
# NO Excel paths, NO sheet names here (those live in scripts/prepare_data.py).

CSV_PATHS = {
    "accidents":             "data/processed/accidents.csv",
    "types":                 "data/processed/types.csv",
    "causes":                "data/processed/causes.csv",
    "dayofweek":             "data/processed/dayofweek.csv",
    "timeslots":             "data/processed/timeslots.csv",
    "deaths_demographics":   "data/processed/deaths_demographics.csv",
    "injuries_demographics": "data/processed/injuries_demographics.csv",
    "license":               "data/processed/license.csv",
    "vehicles_by_region":    "data/processed/vehicles_by_region.csv",
}
