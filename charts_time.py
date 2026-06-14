"""Time-based charts: yearly trend, time slots, day of week."""

import plotly.express as px
import streamlit as st

DAY_ORDER = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO", "DOMINGO"]


def render_yearly_trend(df):
    """Accidents per year. Replaces the planned hourly chart — the ONSV source
    has no hour-level data, only time bands (see render_timeslot_chart)."""
    yearly = df.groupby("año", as_index=False)["count"].sum()
    fig = px.bar(yearly, x="año", y="count",
                 title="Accidents by Year",
                 labels={"año": "Year", "count": "Number of Accidents"})
    st.plotly_chart(fig, width="stretch")


def render_timeslot_chart(df):
    """Accidents per time band. Source uses 4 bands for 2008-2014 and
    12 two-hour bands from 2015 on — bands shown depend on year filter."""
    slots = df.groupby("franja", as_index=False)["count"].sum()
    slots = slots.sort_values("franja", key=lambda s: s.str[:2].astype(int))
    fig = px.bar(slots, x="franja", y="count",
                 title="Accidents by Time Slot",
                 labels={"franja": "Time Slot", "count": "Number of Accidents"})
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, width="stretch")


def render_dayofweek_chart(df):
    days = df.groupby("dia_semana", as_index=False)["count"].sum()
    fig = px.bar(days, x="dia_semana", y="count",
                 title="Accidents by Day of Week",
                 labels={"dia_semana": "Day of Week", "count": "Number of Accidents"},
                 category_orders={"dia_semana": DAY_ORDER})
    st.plotly_chart(fig, width="stretch")
