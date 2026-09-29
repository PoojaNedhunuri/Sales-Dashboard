# ============================================================
# OVERVIEW - DUCKDB DATA LAYER
# ============================================================

import duckdb
import time
from pathlib import Path


# Create DuckDB connection
duck_con = duckdb.connect()


# ============================================================
# PARQUET PATH
# ============================================================

PROCESSED_DIR = Path("data/processed")

VISIT_FILE = PROCESSED_DIR / "dcr_visit_mart.parquet"


# ============================================================
# DCR KPI QUERY
# ============================================================

start_time = time.time()


dcr_kpi = duck_con.execute(
    f"""
    SELECT

        COUNT(*) AS total_visits,

        COUNT(DISTINCT DOCTOR_KEY) AS unique_doctors,

        COUNT(DISTINCT MR_KEY) AS active_employees,

        COUNT(DISTINCT HQ_KEY) AS unique_hqs,

        COUNT(DISTINCT PRODUCT_KEY) AS unique_products

    FROM read_parquet('{VISIT_FILE}')
    """
).df()


query_time = time.time() - start_time


st.caption(
    f"DuckDB KPI execution time: {query_time:.2f} seconds"
)


# ============================================================
# KPI VALUES
# ============================================================

total_visits = int(
    dcr_kpi["total_visits"].iloc[0]
)

unique_doctors = int(
    dcr_kpi["unique_doctors"].iloc[0]
)

active_employees = int(
    dcr_kpi["active_employees"].iloc[0]
)

unique_hqs = int(
    dcr_kpi["unique_hqs"].iloc[0]
)

unique_products = int(
    dcr_kpi["unique_products"].iloc[0]
)


# ============================================================
# KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)


with kpi1:
    st.metric(
        "Total Visits",
        f"{total_visits:,}"
    )


with kpi2:
    st.metric(
        "Unique Doctors",
        f"{unique_doctors:,}"
    )


with kpi3:
    st.metric(
        "Active Employees",
        f"{active_employees:,}"
    )


with kpi4:
    st.metric(
        "Unique HQs",
        f"{unique_hqs:,}"
    )


with kpi5:
    st.metric(
        "Products Detailed",
        f"{unique_products:,}"
    )
