"""Demographics charts: deaths and injuries by age group and gender."""

import plotly.express as px
import streamlit as st

# Two age schemes in the source (2010-2017 and 2018-2024); order by start age.
AGE_ORDER = ["0-5", "6-11", "6-12", "12-17", "13-18", "18-29", "19-25", "26-60", "30-59", "60+"]
GENDER_COLORS = {"Masculino": "#1f77b4", "Femenino": "#e377c2"}


def _grouped_bar(df, title, y_label):
    grouped = df.groupby(["age_group", "gender"], as_index=False)["count"].sum()
    fig = px.bar(grouped, x="age_group", y="count", color="gender",
                 barmode="group", title=title,
                 labels={"age_group": "Age Group", "count": y_label, "gender": "Gender"},
                 category_orders={"age_group": AGE_ORDER},
                 color_discrete_map=GENDER_COLORS)
    st.plotly_chart(fig, width="stretch")


def render_deaths_by_age_gender(df):
    _grouped_bar(df, "Deaths by Age Group and Gender", "Number of Deaths")


def render_injuries_by_age_gender(df):
    _grouped_bar(df, "Injuries by Age Group and Gender", "Number of Injuries")
