# Peru Traffic Accident Analysis Dashboard

## Overview

As a software engineer, I set out to build a data-driven web dashboard that transforms a large, multi-sheet government dataset into an interactive exploration tool. The goal was to practice the full data pipeline: raw data cleaning, CSV-based storage, modular Python architecture, and interactive visualization — skills that transfer directly to production analytics work.

The dataset is Peru's national road accident registry published by the ONSV (Observatorio Nacional de Seguridad Vial), covering 2008–2024 across all departments of Peru. It includes accident counts, deaths, injuries, causes, vehicle types, driver license categories, and victim demographics broken down by age and gender.

Data source: [ONSV Datos Abiertos](https://www.onsv.gob.pe/datosabiertos)

The purpose of this software is to help citizens and researchers identify high-risk locations, time patterns, and demographic vulnerabilities in Peru's road network — turning raw government numbers into actionable insight through filters and interactive charts.

[Traffic Analysis](https://youtu.be/5_6i1km0cDI)

## Data Analysis Results

**Q: Which department has the most road accidents?**
A: Lima consistently ranks as the highest-accident department, followed by Arequipa and La Libertad.

**Q: What time of day has the most accidents?**
A: Accidents peak between 18:00 and 20:00 (evening rush hour), with a secondary peak around 08:00–10:00.

**Q: Which day of the week is most dangerous?**
A: Fridays and Saturdays show the highest accident counts, likely due to weekend travel and nightlife.

**Q: What are the most common accident types and causes?**
A: Rear-end collisions are the most frequent type. Excessive speed and driver inattention are the leading causes.

**Q: Which age group and gender are most affected by deaths and injuries?**
A: Males aged 19–25 represent the highest share of both deaths and injuries across all years.

**Q: Which license category is most associated with accidents?**
A: Drivers with a "Licencia Particular" (private license) are involved in the majority of recorded accidents.

## Development Environment

- **Editor**: Visual Studio Code
- **Dependency management**: uv (fast Python package manager)
- **Version control**: Git
- **Runtime**: Python 3.13

**Libraries used:**
- `streamlit` — dashboard UI and local web server
- `pandas` — data loading, filtering, and aggregation
- `plotly` — interactive charts (bar, grouped bar, stacked bar)
- `openpyxl` — one-time Excel-to-CSV conversion (data prep only, not used at runtime)

## Useful Websites

* [Streamlit Documentation](https://docs.streamlit.io)
* [Plotly Python Documentation](https://plotly.com/python/)
* [Pandas Documentation](https://pandas.pydata.org/docs/)
* [ONSV Datos Abiertos](https://www.onsv.gob.pe/datosabiertos)
* [uv Documentation](https://docs.astral.sh/uv/)

## Future Work

* Add map visualization — choropleth map of Peru shaded by accident density per department
* Add year-over-year trend line chart to show whether accidents are increasing or decreasing nationally
* Add CSV export so users can download filtered data directly from the dashboard
* Add mobile-responsive layout (currently desktop-only)
* Automate the data prep script to pull the latest ONSV Excel release instead of requiring manual download
