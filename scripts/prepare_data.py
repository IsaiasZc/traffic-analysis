"""Offline data preparation: reads the raw ONSV Excel and writes clean CSVs.

This is the ONLY file that touches the raw Excel. Run once before the dashboard:

    uv run python scripts/prepare_data.py

Each ONSV sheet is a wide pivot table: region rows x (year-block x category)
columns, with title/source rows on top. This script melts every sheet to a
long format, normalizes labels, excludes preliminary 2025 data, and writes
one CSV per table to data/processed/.
"""

import unicodedata

import pandas as pd

RAW_EXCEL = "data/raw/PERU_SINIESTROS_2008-2025.xlsx"
OUTPUT_DIR = "data/processed/"
MAX_YEAR = 2024  # 2025 is preliminary — excluded per FR-020

SHEET_MAP = {
    "accidents":             "SINIESTROS AÑO REGIÓN",
    "types":                 "SINIESTROS POR TIPO",
    "causes":                "CAUSAS POR REGIÓN",
    "dayofweek":             "DÍA",
    "timeslots":             "FRANJA HORARIA",
    "deaths_demographics":   "FALLECIDOS",
    "injuries_demographics": "HERIDOS",
    "license":               "CONDUC GENERO EDAD Y LICENCIA",
    "vehicles_by_region":    "VEHICULOS POR TIPO Y REGIÓN",
}

# Label fixes: the source renames some categories across years; merge variants.
TYPE_MAP = {"COLISION": "COLISIÓN"}
CAUSE_MAP = {"FALTA DE LUCES": "FALLA DE LUCES"}
VEHICLE_MAP = {"AUTO": "AUTOMOVIL", "CAMIÓN": "CAMION", "FURGÓN": "FURGON", "OTRO": "OTROS"}
LICENSE_MAP = {
    "LICENCIA PROFESIONAL": "Profesional",
    "LICENCIA PARTICULAR": "Particular",
    "LICENCIA MILITAR": "Militar",
    "SIN LICENCIA": "Sin Licencia",
    "OTROS (NO TIENE LICENCIA O NO CORRESPONDE AL TIPO DE VEHÍCULO)": "Otros",
    "LICENCIA DE VEHÍCULO MENOR": "Otros",
    "LICENCIA EXTRANJERA": "Otros",
    "SE DESCONOCE POR FUGA": "Otros",
}
# Age-group scheme changed over time: 2010-2017 and 2018-2024 use different
# 6-group splits. 2008-2009 only has under/over 18 — excluded (not mappable).
AGE_MAP = {
    "DE 0 A 5 AÑOS": "0-5",
    "DE 6 A 12 AÑOS": "6-12", "DE 6 A 11 AÑOS": "6-11",
    "DE 13 A 18 AÑOS": "13-18", "DE 12 A 17 AÑOS": "12-17",
    "DE 19 A 25 AÑOS": "19-25", "DE 18 A 29 AÑOS": "18-29",
    "DE 26 A 60 AÑOS": "26-60", "DE 30 A 59 AÑOS": "30-59",
    "DE 60 A MÁS AÑOS": "60+",
}
GENDER_MAP = {"MASCULINO": "Masculino", "FEMENINO": "Femenino"}


def strip_accents(text):
    decomposed = unicodedata.normalize("NFD", str(text))
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def clean_region(value):
    # Source has trailing spaces ("LIMA ") and accent inconsistencies
    # ("AMAZÓNAS" vs "AMAZONAS") — normalize so filters match across tables.
    return strip_accents(value).strip().upper()


def read_sheet(key):
    return pd.read_excel(RAW_EXCEL, sheet_name=SHEET_MAP[key], header=None)


def melt_year_region(key):
    """Sheet with region rows x year columns (no category level)."""
    df = read_sheet(key)
    years = df.iloc[3]
    rows, excluded = [], 0
    for r in range(4, len(df)):
        region = df.iat[r, 0]
        if pd.isna(region) or "TOTAL" in str(region).upper():
            continue
        for c in range(1, df.shape[1]):
            if pd.isna(years[c]):
                continue
            count = pd.to_numeric(df.iat[r, c], errors="coerce")
            if pd.isna(count):
                excluded += 1
                continue
            rows.append((int(years[c]), clean_region(region), int(count)))
    print(f"{key}: excluded {excluded} malformed cells")
    return pd.DataFrame(rows, columns=["año", "departamento", "count"])


def melt_year_category(key, cat_row, cat_name, cat_map=None):
    """Sheet with region rows x (year-block x category) columns."""
    df = read_sheet(key)
    years = df.iloc[3].ffill()
    cats = df.iloc[cat_row]
    rows, excluded = [], 0
    for r in range(cat_row + 1, len(df)):
        region = df.iat[r, 0]
        if pd.isna(region) or "TOTAL" in str(region).upper():
            continue
        for c in range(1, df.shape[1]):
            if pd.isna(years[c]) or pd.isna(cats[c]):
                continue
            count = pd.to_numeric(df.iat[r, c], errors="coerce")
            if pd.isna(count):
                excluded += 1
                continue
            cat = str(cats[c]).strip()
            cat = (cat_map or {}).get(cat, cat)
            rows.append((int(years[c]), clean_region(region), cat, int(count)))
    print(f"{key}: excluded {excluded} malformed cells")
    return pd.DataFrame(rows, columns=["año", "departamento", cat_name, "count"])


def melt_demographics(key):
    """Deaths/injuries sheet: gender + age header rows; aggregated over regions."""
    df = read_sheet(key)
    years = df.iloc[3].ffill()
    genders = df.iloc[4].ffill()
    ages = df.iloc[5]
    rows, excluded = [], 0
    for r in range(6, len(df)):
        region = df.iat[r, 0]
        if pd.isna(region) or "TOTAL" in str(region).upper():
            continue
        for c in range(1, df.shape[1]):
            if pd.isna(years[c]) or pd.isna(ages[c]):
                continue
            age = AGE_MAP.get(str(ages[c]).strip())
            count = pd.to_numeric(df.iat[r, c], errors="coerce")
            if age is None or pd.isna(count):
                excluded += 1  # includes 2008-2009 under/over-18 columns
                continue
            gender = GENDER_MAP.get(str(genders[c]).strip().upper())
            rows.append((int(years[c]), gender, age, int(count)))
    print(f"{key}: excluded {excluded} cells (malformed or 2008-2009 age scheme)")
    long_df = pd.DataFrame(rows, columns=["año", "gender", "age_group", "count"])
    return long_df.groupby(["año", "gender", "age_group"], as_index=False)["count"].sum()


def prepare_license():
    """Driver sheet: keep only license-type columns; aggregated over regions."""
    df = melt_year_category("license", cat_row=5, cat_name="license_type")
    df = df[df["license_type"].isin(LICENSE_MAP)]
    df["license_type"] = df["license_type"].map(LICENSE_MAP)
    return df.groupby(["año", "license_type"], as_index=False)["count"].sum()


def main():
    tables = {
        "accidents": melt_year_region("accidents"),
        "types": melt_year_category("types", 4, "tipo_accidente", TYPE_MAP),
        "causes": melt_year_category("causes", 4, "causa", CAUSE_MAP),
        "dayofweek": melt_year_category("dayofweek", 4, "dia_semana"),
        "timeslots": melt_year_category("timeslots", 4, "franja"),
        "deaths_demographics": melt_demographics("deaths_demographics"),
        "injuries_demographics": melt_demographics("injuries_demographics"),
        "license": prepare_license(),
        "vehicles_by_region": melt_year_category("vehicles_by_region", 5, "tipo_vehiculo", VEHICLE_MAP),
    }
    # Day names: strip accents (MIÉRCOLES -> MIERCOLES) for a stable chart order.
    tables["dayofweek"]["dia_semana"] = tables["dayofweek"]["dia_semana"].map(strip_accents)
    # Time bands: "08:00 A 14:00" -> "08:00–14:00" for compact chart labels.
    tables["timeslots"]["franja"] = tables["timeslots"]["franja"].str.replace(" A ", "–")
    for key, table in tables.items():
        table = table[table["año"] <= MAX_YEAR]
        table.to_csv(f"{OUTPUT_DIR}{key}.csv", index=False)
        print(f"wrote {OUTPUT_DIR}{key}.csv ({len(table)} rows)")


if __name__ == "__main__":
    main()
