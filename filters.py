"""Single filter function shared by every chart section.

Each dimension is applied only when the column exists in the table AND the
user picked a value — so charts from tables lacking a dimension are simply
not affected (per-table filter scope, data-model.md).
"""


def apply_filters(df, dept=None, year_range=None, gender=None,
                  license_types=None, accident_types=None):
    if dept and "departamento" in df.columns:
        df = df[df["departamento"].isin(dept)]
    if year_range and "año" in df.columns:
        df = df[df["año"].between(year_range[0], year_range[1])]
    if gender and gender != "All" and "gender" in df.columns:
        df = df[df["gender"] == gender]
    if license_types and "license_type" in df.columns:
        df = df[df["license_type"].isin(license_types)]
    if accident_types and "tipo_accidente" in df.columns:
        df = df[df["tipo_accidente"].isin(accident_types)]
    return df.copy()
