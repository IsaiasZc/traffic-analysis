"""One cached loader per processed CSV. Loaders only read CSVs — no Excel."""

import pandas as pd
import streamlit as st

from config import CSV_PATHS


def _load(key, required_cols):
    """Read one CSV and validate columns. Returns None (section skipped) on error
    so the rest of the dashboard keeps working (SC-006)."""
    path = CSV_PATHS[key]
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"Processed CSV not found: {path}. Run scripts/prepare_data.py first.")
        return None
    for col in required_cols:
        if col not in df.columns:
            st.warning(f"CSV '{path}' missing required column: '{col}'. Section skipped.")
            return None
    return df


@st.cache_data
def load_accidents():
    return _load("accidents", ["año", "departamento", "count"])


@st.cache_data
def load_types():
    return _load("types", ["año", "departamento", "tipo_accidente", "count"])


@st.cache_data
def load_causes():
    return _load("causes", ["año", "departamento", "causa", "count"])


@st.cache_data
def load_dayofweek():
    return _load("dayofweek", ["año", "departamento", "dia_semana", "count"])


@st.cache_data
def load_timeslots():
    return _load("timeslots", ["año", "departamento", "franja", "count"])


@st.cache_data
def load_deaths_demographics():
    return _load("deaths_demographics", ["año", "gender", "age_group", "count"])


@st.cache_data
def load_injuries_demographics():
    return _load("injuries_demographics", ["año", "gender", "age_group", "count"])


@st.cache_data
def load_license():
    return _load("license", ["año", "license_type", "count"])


@st.cache_data
def load_vehicles_by_region():
    return _load("vehicles_by_region", ["año", "departamento", "tipo_vehiculo", "count"])
