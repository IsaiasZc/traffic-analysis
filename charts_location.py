"""Location charts: department ranking and vehicle types by region."""

import plotly.express as px
import streamlit as st


def render_department_ranking(df):
    ranked = df.groupby("departamento", as_index=False)["count"].sum()
    ranked = ranked.sort_values("count", ascending=True)  # largest on top
    fig = px.bar(ranked, x="count", y="departamento", orientation="h",
                 title="Accident Count by Department",
                 labels={"count": "Number of Accidents", "departamento": "Department"})
    fig.update_layout(height=max(400, 25 * len(ranked)))
    st.plotly_chart(fig, width="stretch")


def render_vehicle_by_region(df):
    grouped = df.groupby(["departamento", "tipo_vehiculo"], as_index=False)["count"].sum()
    fig = px.bar(grouped, x="departamento", y="count", color="tipo_vehiculo",
                 title="Vehicle Types by Department",
                 labels={"departamento": "Department", "count": "Number of Vehicles",
                         "tipo_vehiculo": "Vehicle Type"})
    fig.update_layout(barmode="stack", xaxis_tickangle=-45)
    st.plotly_chart(fig, width="stretch")
