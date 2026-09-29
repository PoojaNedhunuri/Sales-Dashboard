# ============================================================
# OVERVIEW - DUCKDB DATA LAYER
# ============================================================

import streamlit as st
import pandas as pd
import duckdb
import time
from pathlib import Path


# paths
PROCESSED_DIR = Path("data/processed")


# parquet files
VISIT_FILE = PROCESSED_DIR / "dcr_visit_mart.parquet"


# Parquet paths
VISIT_FILE = PROCESSED_DIR / "dcr_visit_mart.parquet"
DOCTOR_FILE = PROCESSED_DIR / "dcr_doctor_mart.parquet"
MR_FILE = PROCESSED_DIR / "dcr_mr_mart.parquet"


# ============================================================
# OVERVIEW FILTER INPUTS
# (keep your existing filters above this section)
# ============================================================


# ============================================================
# DCR KPI QUERY
# ============================================================

start_time = time.time()


dcr_kpi = duck_con.execute(f"""

SELECT

    COUNT(*) AS total_visits,

    COUNT(DISTINCT DOCTOR_KEY) AS unique_doctors,

    COUNT(DISTINCT MR_KEY) AS active_employees,

    COUNT(DISTINCT HQ_KEY) AS unique_hqs,

    COUNT(DISTINCT PRODUCT_KEY) AS unique_products


FROM read_parquet('{VISIT_FILE}')


""").df()


query_time = time.time() - start_time


st.caption(
    f"DuckDB KPI execution time: {query_time:.2f} seconds"
)


# Extract KPI values

total_visits = int(dcr_kpi.loc[0, "total_visits"])

unique_doctors = int(dcr_kpi.loc[0, "unique_doctors"])

active_employees = int(dcr_kpi.loc[0, "active_employees"])

unique_hqs = int(dcr_kpi.loc[0, "unique_hqs"])

unique_products = int(dcr_kpi.loc[0, "unique_products"])



# ============================================================
# KPI CARDS
# ============================================================


kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)


with kpi1:
    st.metric(
        "Total Visits",
        format_indian_number(total_visits)
    )


with kpi2:
    st.metric(
        "Unique Doctors",
        format_indian_number(unique_doctors)
    )


with kpi3:
    st.metric(
        "Active Employees",
        format_indian_number(active_employees)
    )


with kpi4:
    st.metric(
        "Unique HQs",
        format_indian_number(unique_hqs)
    )


with kpi5:
    st.metric(
        "Products Detailed",
        format_indian_number(unique_products)
    )
