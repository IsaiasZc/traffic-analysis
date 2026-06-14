"""Peru Traffic Accidents Dashboard — Streamlit entry point.

Run with: uv run streamlit run app.py
Data: ONSV open data (2008-2024), prepared by scripts/prepare_data.py.
"""

import streamlit as st

from charts_demographics import (
    render_deaths_by_age_gender,
    render_injuries_by_age_gender,
)
from charts_location import render_department_ranking, render_vehicle_by_region
from charts_summary import render_summary_metrics
from charts_time import (
    render_dayofweek_chart,
    render_timeslot_chart,
    render_yearly_trend,
)
from charts_typecause import (
    render_accident_type_chart,
    render_cause_chart,
    render_license_chart,
)
from filters import apply_filters
from loaders import (
    load_accidents,
    load_causes,
    load_dayofweek,
    load_deaths_demographics,
    load_injuries_demographics,
    load_license,
    load_timeslots,
    load_types,
    load_vehicles_by_region,
)

st.set_page_config(page_title="Peru Traffic Accidents", layout="wide")
st.title("Peru Traffic Accidents Dashboard (2008-2024)")
st.markdown(
    "Source: [ONSV open data](https://www.onsv.gob.pe/datosabiertos) - Observatorio Nacional de Seguridad Vial."
)


def show_empty_state():
    st.warning("No data for selected filters.")


def render_section(df, render_fn, description, scope_note):
    """Description + filter scope note + chart, or empty/skip states (FR-009, FR-011, FR-021)."""
    st.markdown(f"**What this shows**: {description}")
    st.caption(f"Filters applied: {scope_note}")
    if df is None:
        return  # loader already showed an error for this table
    if df.empty:
        show_empty_state()
    else:
        render_fn(df)


# --- Load all tables (cached) ---
accidents = load_accidents()
types = load_types()
causes = load_causes()
dayofweek = load_dayofweek()
timeslots = load_timeslots()
deaths = load_deaths_demographics()
injuries = load_injuries_demographics()
license_df = load_license()
vehicles = load_vehicles_by_region()

# --- Sidebar filters ---
st.sidebar.header("Filters")
dept_options = (
    sorted(accidents["departamento"].unique()) if accidents is not None else []
)
dept = st.sidebar.multiselect("Department", options=dept_options)
year_min = int(accidents["año"].min()) if accidents is not None else 2008
year_max = int(accidents["año"].max()) if accidents is not None else 2024
year_range = st.sidebar.slider("Year Range", year_min, year_max, (year_min, year_max))
type_options = sorted(types["tipo_accidente"].unique()) if types is not None else []
accident_types = st.sidebar.multiselect("Accident Type", options=type_options)
gender = st.sidebar.radio("Gender", ["All", "Masculino", "Femenino"])
license_types = st.sidebar.multiselect(
    "License Type",
    options=["Profesional", "Particular", "Militar", "Sin Licencia", "Otros"],
)
st.sidebar.caption(
    "Each filter only affects charts whose data includes that dimension."
)

active = dict(
    dept=dept,
    year_range=year_range,
    gender=gender,
    license_types=license_types,
    accident_types=accident_types,
)


def filtered(df):
    return None if df is None else apply_filters(df, **active)


# --- Summary Metrics ---
st.header("Summary Metrics")
st.markdown(
    "**What this shows**: Overall totals for the selected filters. "
    "Deaths and injuries cover 2010–2024 (earlier years use an incompatible age format)."
)
st.caption(
    "Filters applied: Department & Year Range (accidents); Year Range & Gender (deaths/injuries)"
)
if accidents is None or filtered(accidents).empty:
    show_empty_state()
else:
    render_summary_metrics(filtered(accidents), filtered(deaths), filtered(injuries))

# --- Time Analysis ---
st.header("Time Analysis")
render_section(
    filtered(accidents),
    render_yearly_trend,
    "How the number of accidents has changed year by year.",
    "Department, Year Range",
)
render_section(
    filtered(timeslots),
    render_timeslot_chart,
    "Which times of day concentrate the most accidents "
    "(4 broad bands for 2008–2014; 12 two-hour bands from 2015).",
    "Department, Year Range",
)

# --- Type & Cause ---
st.header("Type & Cause")
render_section(
    filtered(types),
    render_accident_type_chart,
    "Which kinds of accidents happen most often, sorted from most to least common.",
    "Department, Year Range, Accident Type",
)
render_section(
    filtered(causes),
    render_cause_chart,
    "The most frequent causes behind accidents, sorted from most to least common.",
    "Department, Year Range",
)

# --- Location & Region ---
st.header("Location & Region")
render_section(
    filtered(accidents),
    render_department_ranking,
    "Accident counts per department, sorted from highest to lowest risk.",
    "Department, Year Range",
)
render_section(
    filtered(vehicles),
    render_vehicle_by_region,
    "Which vehicle types are involved in accidents in each department.",
    "Department, Year Range",
)

# --- Demographics ---
st.header("Demographics")
st.caption(
    "Department filter does not apply — source data has no regional breakdown here. "
    "Data available from 2010; age groups changed format in 2018."
)
render_section(
    filtered(deaths),
    render_deaths_by_age_gender,
    "Which age groups and genders suffer the most deaths in accidents.",
    "Year Range, Gender",
)
render_section(
    filtered(injuries),
    render_injuries_by_age_gender,
    "Which age groups and genders suffer the most injuries in accidents.",
    "Year Range, Gender",
)

# --- License Categories ---
st.header("License Categories")
render_section(
    filtered(license_df),
    render_license_chart,
    "What kind of driving license the drivers involved in accidents held.",
    "Year Range, License Type",
)

# --- Day of Week ---
st.header("Day of Week")
render_section(
    filtered(dayofweek),
    render_dayofweek_chart,
    "Which days of the week concentrate the most accidents.",
    "Department, Year Range",
)
