"""Summary metric cards (FR-001)."""

import streamlit as st


def render_summary_metrics(accidents, deaths, injuries):
    """Four st.metric cards. Deaths/injuries come from their own tables
    (source data is pre-aggregated; demographics coverage is 2010-2024)."""
    if accidents is None or accidents.empty:
        st.info("No data available")
        return
    top_dept = accidents.groupby("departamento")["count"].sum().idxmax()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Accidents", f"{int(accidents['count'].sum()):,}")
    col2.metric("Total Deaths", _total(deaths))
    col3.metric("Total Injuries", _total(injuries))
    col4.metric("Top Department", top_dept)


def _total(df):
    if df is None or df.empty:
        return "No data"
    return f"{int(df['count'].sum()):,}"
