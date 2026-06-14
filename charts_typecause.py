"""Accident type, cause, and license category charts."""

import plotly.express as px
import streamlit as st


def _horizontal_bar(df, group_col, title, y_label):
    grouped = df.groupby(group_col, as_index=False)["count"].sum()
    grouped = grouped.sort_values("count", ascending=True)  # largest on top
    fig = px.bar(grouped, x="count", y=group_col, orientation="h",
                 title=title,
                 labels={"count": "Number of Accidents", group_col: y_label})
    fig.update_layout(height=max(400, 25 * len(grouped)))
    st.plotly_chart(fig, width="stretch")


def render_accident_type_chart(df):
    _horizontal_bar(df, "tipo_accidente", "Accidents by Type", "Accident Type")


def render_cause_chart(df):
    _horizontal_bar(df, "causa", "Accidents by Cause", "Cause")


def render_license_chart(df):
    grouped = df.groupby("license_type", as_index=False)["count"].sum()
    grouped = grouped.sort_values("count", ascending=True)
    fig = px.bar(grouped, x="count", y="license_type", orientation="h",
                 title="Drivers Involved by License Category",
                 labels={"count": "Number of Drivers Involved",
                         "license_type": "License Category"})
    st.plotly_chart(fig, width="stretch")
