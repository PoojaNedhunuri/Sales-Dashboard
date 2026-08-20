from pathlib import Path 
import pandas as pd
import plotly.express as px
import streamlit as st
import re
import altair as alt
import plotly.graph_objects as go


# =========================================================

# PAGE CONFIGURATION

# =========================================================
 
st.set_page_config(

    page_title="Sales & Field Force Intelligence",

    page_icon="📈",

    layout="wide",

    initial_sidebar_state="expanded",

)
 
 
# =========================================================

# FILE PATHS

# =========================================================
 
PROCESSED_DIR = Path("data/processed")
 
SALES_FILE = (

    PROCESSED_DIR

    / "sales_month_brand_performance_new_test.parquet"

)
 
MR_FILE = (

    PROCESSED_DIR

    / "dcr_mr_mart.parquet"

)
 
DOCTOR_FILE = (

    PROCESSED_DIR

    / "dcr_doctor_mart.parquet"

)
 
VISIT_FILE = (

    PROCESSED_DIR

    / "dcr_visit_mart.parquet"

)
 
PRODUCT_FILE = (

    PROCESSED_DIR

    / "dcr_product_mart.parquet"

)

TARGET_FILE = (

    PROCESSED_DIR

    / "sales_target_performance_new.parquet"

)
 
# =========================================================

# STANDARD DASHBOARD COLUMN NAMES

# =========================================================
 
MONTH_COLUMN = "MONTH_START"

YEAR_COLUMN = "FINANCIAL_YEAR"

QUARTER_COLUMN = "FINANCIAL_QUARTER"

MONTH_LABEL_COLUMN = "MONTH_LABEL"
 
REGION_COLUMN = "REGION_KEY"

STATE_COLUMN = "STATE_KEY"

HQ_COLUMN = "HQ_KEY"

BRAND_COLUMN = "BRAND_KEY"
 
MR_COLUMN = "MR_KEY"

DOCTOR_COLUMN = "DOCTOR_KEY"

VISIT_COLUMN = "VISIT_KEY"

PRODUCT_COLUMN = "PRODUCT_KEY"
 
 
# =========================================================

# PROFESSIONAL DASHBOARD CSS

# =========================================================
 
st.markdown(

    """
<style>
 
        /* ---------- Application background ---------- */
 
        .stApp {

            background:

                radial-gradient(

                    circle at 8% 4%,

                    rgba(37, 99, 235, 0.10),

                    transparent 25%

                ),

                radial-gradient(

                    circle at 92% 12%,

                    rgba(14, 165, 233, 0.08),

                    transparent 24%

                ),

                linear-gradient(

                    135deg,

                    #F8FAFC 0%,

                    #F1F5F9 50%,

                    #F8FAFC 100%

                );

        }
 
        .block-container {

            max-width: 1550px;

            padding-top: 0.5rem;

            padding-bottom: 3rem;

        }
 
 
        /* ---------- Sidebar ---------- */
 
        [data-testid="stSidebar"] {

            background:

                linear-gradient(

                    180deg,

                    rgba(255, 255, 255, 0.99),

                    rgba(248, 250, 252, 0.99)

                );
 
            border-right:

                1px solid rgba(148, 163, 184, 0.24);

        }
 
        [data-testid="stSidebar"] h2 {

            color: #0F172A;

            font-weight: 750;

            letter-spacing: -0.3px;

        }
 
        [data-testid="stSidebar"] label {

            color:#2563EB;

            font-weight: 700;

        }
 
 
        /* ---------- Main header ---------- */
 
        .dashboard-header {

            position: relative;

            overflow: hidden;
 
            padding: 28px 32px;

            margin-bottom: 18px;
 
            border-radius: 24px;
 
            background:

                linear-gradient(

                    130deg,

                    #0F172A 0%,

                    #1E3A8A 52%,

                    #2563EB 100%

                );
 
            border:

                1px solid rgba(255, 255, 255, 0.18);
 
            box-shadow:

                0 20px 45px rgba(15, 23, 42, 0.18),

                inset 0 1px 0 rgba(255, 255, 255, 0.22);

        }
 
        .dashboard-header::before {

            content: "";

            position: absolute;
 
            width: 300px;

            height: 300px;
 
            top: -190px;

            right: -80px;
 
            border-radius: 50%;
 
            background:

                rgba(255, 255, 255, 0.10);

        }
 
        .dashboard-header::after {

            content: "";

            position: absolute;
 
            width: 190px;

            height: 190px;
 
            bottom: -135px;

            left: 42%;
 
            border-radius: 50%;
 
            background:

                rgba(56, 189, 248, 0.18);

        }
 
        .dashboard-title {

            position: relative;

            z-index: 1;
 
            margin: 0;
 
            color: #FFFFFF;

            font-size: 31px;

            font-weight: 780;

            letter-spacing: -0.7px;

        }
 
        .dashboard-subtitle {

            position: relative;

            z-index: 1;
 
            margin-top: 7px;

            margin-bottom: 0;
 
            color: rgba(255, 255, 255, 0.78);

            font-size: 14px;

        }
 
 
        /* ---------- Active filter summary ---------- */
 
        .filter-summary {

            padding: 14px 17px;

            margin-bottom: 20px;
 
            border-radius: 16px;
 
            background:

                linear-gradient(

                    135deg,

                    rgba(255, 255, 255, 0.94),

                    rgba(239, 246, 255, 0.86)

                );
 
            border:

                1px solid rgba(96, 165, 250, 0.24);
 
            box-shadow:

                0 8px 22px rgba(15, 23, 42, 0.05),

                inset 0 1px 0 rgba(255, 255, 255, 0.90);

        }
 
        .filter-summary-title {

            color: #475569;

            font-size: 11px;

            font-weight: 750;
 
            margin-bottom: 8px;
 
            text-transform: uppercase;

            letter-spacing: 0.8px;

        }
 
        .filter-chip {

            display: inline-block;
 
            padding: 6px 11px;

            margin: 3px 5px 3px 0;
 
            border-radius: 999px;
 
            color: #1D4ED8;

            background:

                linear-gradient(

                    135deg,

                    #EFF6FF,

                    #DBEAFE

                );
 
            border: 1px solid #BFDBFE;
 
            font-size: 12px;

            font-weight: 650;

        }
 
        .filter-chip-empty {

            display: inline-block;
 
            padding: 6px 11px;
 
            border-radius: 999px;
 
            color: #64748B;

            background: #F1F5F9;
 
            border: 1px solid #E2E8F0;
 
            font-size: 12px;

            font-weight: 600;

        }
 
 
        /* ---------- Section headings ---------- */
 
        .section-header {
        position: relative;
 
        margin-top: 10px;
        margin-bottom: 16px;
 
        padding:
            0 0 12px 0;
 
        background: transparent;
 
        border: none;
        border-radius: 0;
 
        box-shadow: none;
 
        overflow: visible;
    }
 
 
    /* -----------------------------------------------------
       BOTTOM DIVIDER
    ----------------------------------------------------- */
 
    .section-header::after {
        content: "";
 
        position: absolute;
 
        left: 0;
        right: 0;
        bottom: 0;
 
        width: 100%;
        height: 1px;
 
        background:
            linear-gradient(
                90deg,
                rgba(37, 99, 235, 0.55) 0%,
                rgba(96, 165, 250, 0.20) 35%,
                rgba(226, 232, 240, 0.65) 70%,
                transparent 100%
            );
 
        border-radius: 999px;
 
        pointer-events: none;
    }
 
 
    /* =====================================================
       SECTION TITLE
    ===================================================== */
 
    .section-title {
        position: relative;
 
        margin: 0;
 
        color: #163A5F;
 
        font-size: 20px;
        font-weight: 800;
 
        line-height: 1.2;
 
        letter-spacing: -0.40px;
    }
 
 
    /* Remove previous title underline */
    .section-title::after {
        display: none;
        content: none;
    }
 
 
    /* =====================================================
       CAPTION
    ===================================================== */
 
    .section-caption {
        position: relative;
 
        margin-top: 5px;
        margin-bottom: 0;
 
        color: #2563EB;
 
        font-size: 12px;
        font-weight: 500;
 
        line-height: 1.4;
 
        letter-spacing: 0;
    }
 
 
    /* =====================================================
       RESPONSIVE
    ===================================================== */
 
    @media (max-width: 900px) {
 
        .section-header {
            margin-top: 24px;
            margin-bottom: 14px;
        }
 
        .section-title {
            font-size: 18px;
        }
 
        .section-caption {
            font-size: 10px;
        }
    }
 
 
    /* ---------- KPI cards ---------- */
    /* =====================================================
       KPI CARD
    ===================================================== */
 
    [data-testid="stMetric"] {
        position: relative !important;
 
        width: 100%;
 
        height: 118px;
        min-height: 118px;
        max-height: 118px;
 
        box-sizing: border-box;
 
        display: flex;
        flex-direction: column;
 
        padding: 15px 16px 12px;
 
        overflow: hidden;
 
        border-radius: 16px;
 
        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.80) 0%,
                rgba(248,250,252,0.70) 55%,
                rgba(239,246,255,0.66) 100%
            );
 
        border:
            1px solid rgba(255,255,255,0.72);
 
        box-shadow:
            0 10px 28px rgba(15,23,42,0.07),
            0 2px 8px rgba(37,99,235,0.035),
            inset 0 1px 0 rgba(255,255,255,0.95);
 
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
    }
 
 
    /* =====================================================
       BLUE TOP ACCENT
    ===================================================== */
 
    [data-testid="stMetric"]::before {
        content: "";
 
        position: absolute;
 
        top: 0;
        left: 0;
        right: 0;
 
        height: 3px;
 
        border-radius:
            0 0 999px 999px;
 
        background:
            linear-gradient(
                90deg,
                #2563EB,
                #38BDF8,
                #6366F1
            );
 
    }
 
    /* =====================================================

    KPI HELP ICON — BESIDE KPI TITLE

    ===================================================== */
    
    [data-testid="stMetric"] {

        position: relative !important;

    }
    
    
    /* Label row */

    [data-testid="stMetricLabel"] {

        position: relative !important;
    
        display: flex !important;

        align-items: center !important;

        justify-content: flex-start !important;
    
        gap: 5px !important;
    
        flex-wrap: nowrap !important;

        white-space: nowrap !important;
    
        width: 100% !important;

    }
    
    
    /* KPI title */

    [data-testid="stMetricLabel"] p {

        margin: 0 !important;

        padding: 0 !important;
    
        white-space: nowrap !important;

    }
    
    
    /* Help / tooltip button */

    [data-testid="stMetric"] [data-testid="stMetricLabel"] button {
    
        /* IMPORTANT — remove absolute positioning */

        position: relative !important;
    
        top: auto !important;

        right: auto !important;
    
        width: 15px !important;

        height: 15px !important;

        min-width: 15px !important;
    
        margin: 0 0 0 3px !important;

        padding: 0 !important;
    
        display: inline-flex !important;

        align-items: center !important;

        justify-content: center !important;
    
        flex-shrink: 0 !important;

    }
    
    
    /* Help icon size */

    [data-testid="stMetric"]

    [data-testid="stMetricLabel"]

    button svg {
    
        width: 11px !important;

        height: 11px !important;

    }
 
 
    /* =====================================================
       KPI TITLE — SINGLE LINE
    ===================================================== */
 
    [data-testid="stMetric"] {
        padding-top: 11px !important;
    }
 
    [data-testid="stMetricLabel"] {
        margin-top: 0 !important;
        margin-bottom: 6px !important;
 
        min-height: 18px !important;
        height: 18px !important;
        color: #163A5F !important;
        display: flex !important;
        align-items: center !important;
    }
 
    [data-testid="stMetricLabel"] p {
        margin: 0 !important;
        padding: 0 !important;
 
        line-height: 0.75 !important;
 
        white-space: nowrap !important;
    }
 
    
 
    
 
    /* =====================================================
       KPI VALUE
    ===================================================== */
 
    [data-testid="stMetricValue"] {
        min-height: 25px;
        height: 36px;
 
        display: flex;
        align-items: center;
 
        margin: 0 !important;
 
        color: #0F172A;
 
        font-size: 30px;
        font-weight: 820;
 
        line-height: 1.0;
 
        letter-spacing: -0.6px;
 
        white-space: nowrap;
    }
 
 
    /* =====================================================
       DELTA
    ===================================================== */
 
    [data-testid="stMetricDelta"] {
        margin-top: auto !important;
 
        min-height: 20px;
        height: 20px;
 
        display: flex;
        align-items: center;
 
        overflow: hidden;
 
        font-size: 11px;
        font-weight: 700;
 
        line-height: 1;
 
        white-space: nowrap;
    }
 
 
    [data-testid="stMetricDelta"] > div {
        max-width: 100%;
 
        overflow: hidden;
 
        white-space: nowrap;
 
        text-overflow: ellipsis;
    }
 
 
    [data-testid="stMetricDelta"] svg {
        width: 9px !important;
        height: 9px !important;
    }
 
 
    /* =====================================================
       ROW ALIGNMENT
    ===================================================== */
 
    [data-testid="stHorizontalBlock"] {
        align-items: stretch;
    }
 
 
    [data-testid="column"] {
        height: 100%;
    }    
 
    /* =====================================================
       TRACEABILITY — LARGE KPI STYLE CARD
    ===================================================== */
 
    .st-key-traceability_card
    [data-testid="stVerticalBlockBorderWrapper"] {
 
        position: relative;
 
        overflow: hidden;
 
        padding: 13px 16px 12px;
 
        border-radius: 16px !important;
 
        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.80) 0%,
                rgba(248,250,252,0.70) 55%,
                rgba(239,246,255,0.66) 100%
            ) !important;
 
        border:
            1px solid rgba(
                148,
                163,
                184,
                0.22
            ) !important;
 
        box-shadow:
            0 10px 28px rgba(15,23,42,0.07),
            inset 0 1px 0 rgba(255,255,255,0.95);
    }
 
 
    /* Same blue accent as KPI cards */
 
    .st-key-traceability_card
    [data-testid="stVerticalBlockBorderWrapper"]::before {
 
        content: "";
 
        position: absolute;
 
        top: 0;
        left: 14px;
        right: 14px;
 
        height: 3px;
 
        border-radius:
            0 0 999px 999px;
 
        background:
            linear-gradient(
                90deg,
                #1D4ED8,
                #3B82F6,
                #60A5FA
            );
 
        box-shadow:
            0 1px 6px rgba(37,99,235,0.22);
    }
 
 
    /* =====================================================
       TRACEABILITY HEADER
    ===================================================== */
 
    .trace-card-title {
        color: #163A5F;
 
        font-size: 17px;
        font-weight: 750;
 
        line-height: 1.2;
 
        white-space: nowrap;
 
        margin: 0;
    }
 
 
    .trace-card-caption {
        color: #64748B;
 
        font-size: 14px;
        font-weight: 500;
 
        margin-top: 3px;
        margin-bottom: 1px;
 
        white-space: nowrap;
    }
 
 
    /* =====================================================
       TRACEABILITY VALUES
    ===================================================== */
 
    .trace-value-area {
        height: 155px;
 
        display: flex;
        flex-direction: column;
        justify-content: center;
 
        padding-left: 3px;
    }
 
 
    .trace-item {
        position: relative;
 
        padding-left: 10px;
    }
 
 
    .trace-item::before {
        content: "";
 
        position: absolute;
 
        left: 0;
        top: 1px;
        bottom: 1px;
 
        width: 3px;
 
        border-radius: 999px;
    }
 
 
    .trace-item.traceable::before {
        background: #2563EB;
    }
 
 
    .trace-item.untraced::before {
        background: #F59E0B;
    }
 
 
    .trace-label {
        color: #64748B;
 
        font-size: 12px;
        font-weight: 750;
 
        letter-spacing: 0.3px;
 
        text-transform: uppercase;
 
        white-space: nowrap;
    }
 
 
    .trace-value {
        margin-top: 3px;
 
        color: #163A5F;
 
        font-size: 25px;
        font-weight: 800;
 
        line-height: 1;
    }
 
 
    .trace-share {
        margin-top: 3px;
 
        font-size: 13px;
        font-weight: 700;
    }
 
 
    .trace-share.blue {
        color: #2563EB;
    }
 
 
    .trace-share.orange {
        color: #D97706;
    }
 
 
    .trace-divider {
        height: 1px;
 
        margin: 12px 0;
 
        background:
            linear-gradient(
                90deg,
                rgba(148,163,184,0.32),
                transparent
            );
    }
        .traceability-kpi-card {
        position: relative;
 
        width: 100%;
 
        height: 248px;
        min-height: 248px;
        max-height: 248px;
 
        box-sizing: border-box;
 
        overflow: hidden;
 
        padding: 15px 16px 13px;
 
        border-radius: 16px;
 
        /* SAME GLASS BACKGROUND AS KPI */
        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.80) 0%,
                rgba(248,250,252,0.70) 55%,
                rgba(239,246,255,0.66) 100%
            );
 
        /* IMPORTANT:
           Same subtle KPI border — not dark grey
        */
        border:
            1px solid rgba(
                148,
                163,
                184,
                0.18
            );
 
        box-shadow:
            0 10px 28px rgba(15,23,42,0.07),
            0 2px 8px rgba(37,99,235,0.035),
            inset 0 1px 0 rgba(255,255,255,0.95);
 
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
    }
 
 
    /* =====================================================
       SAME BLUE TOP ACCENT AS KPI CARDS
    ===================================================== */
 
    .traceability-kpi-card::before {
        content: "";
 
        position: absolute;
 
        top: 0;
 
        left: 14px;
        right: 14px;
 
        height: 3px;
 
        border-radius:
            0 0 999px 999px;
 
        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.92),
                rgba(245,249,255,0.88),
                rgba(235,244,255,0.82)
            );
 
        box-shadow:
            0 1px 6px rgba(
                37,
                99,
                235,
                0.20
            );
    }
 
 
    /* =====================================================
       TITLE
    ===================================================== */
 
    .traceability-title {
        margin: 0;
 
        color: #163A5F;
 
        font-size: 10px;
        font-weight: 750;
 
        line-height: 1.2;
 
        white-space: nowrap;
    }
 
 
    .traceability-caption {
        margin-top: 3px;
 
        color: #64748B;
 
        font-size: 8px;
        font-weight: 500;
 
        line-height: 1.25;
 
        white-space: nowrap;
    }
 
 
    /* =====================================================
       VALUES
    ===================================================== */
 
    .traceability-values {
        height: 200px;
 
        display: flex;
        flex-direction: column;
        justify-content: center;
 
        padding-left: 2px;
    }
 
 
    .traceability-item {
        position: relative;
 
        padding-left: 10px;
    }
 
 
    .traceability-item::before {
        content: "";
 
        position: absolute;
 
        left: 0;
        top: 2px;
        bottom: 2px;
 
        width: 3px;
 
        border-radius: 999px;
    }
 
 
    .traceability-item.traceable::before {
        background: #2563EB;
    }
 
 
    .traceability-item.untraced::before {
        background: #F59E0B;
    }
 
 
    .traceability-label {
        color: #64748B;
 
        font-size: 7px;
        font-weight: 750;
 
        letter-spacing: 0.3px;
 
        text-transform: uppercase;
 
        white-space: nowrap;
    }
 
 
    .traceability-value {
        margin-top: 3px;
 
        color: #163A5F;
 
        font-size: 16px;
        font-weight: 800;
 
        line-height: 1;
    }
 
 
    .traceability-share {
        margin-top: 3px;
 
        font-size: 8px;
        font-weight: 700;
    }
 
 
    .traceability-share.blue {
        color: #2563EB;
    }
 
 
    .traceability-share.orange {
        color: #D97706;
    }
 
 
    .traceability-divider {
        height: 1px;
 
        margin: 11px 0;
 
        background:
            linear-gradient(
                90deg,
                rgba(148,163,184,0.30),
                transparent
            );
    }
 
        /* ---------- Buttons ---------- */
 
        .stButton > button {

            width: 100%;
 
            border: none;

            border-radius: 12px;
 
            color: #FFFFFF;

            font-weight: 650;
 
            background:

                linear-gradient(

                    135deg,

                    #2563EB,

                    #1D4ED8

                );
 
            box-shadow:

                0 8px 18px rgba(37, 99, 235, 0.22);

        }
 
        .stButton > button:hover {

            color: #FFFFFF;
 
            border: none;
 
            background:

                linear-gradient(

                    135deg,

                    #1D4ED8,

                    #1E40AF

                );

        }
 
 
        /* ---------- Charts and tables ---------- */
        /* =========================================================
    PROFESSIONAL DATAFRAME - BLUE THEME
    ========================================================= */
    [data-testid="stDataFrame"]::before {
        content: "";
 
        position: absolute;
 
        top: 0;
        left: 0;
        right: 0;
 
        height: 3px;
 
        border-radius:
            16px 16px 4px 4px;
 
        background:
            linear-gradient(
                90deg,
                #2563EB,
                #38BDF8,
                #6366F1
            );
        z-index: 2;
 
    }
    
    [data-testid="stDataFrame"] {
    
        overflow: hidden;
    
        border-radius: 16px;
    
        background:
            linear-gradient(
                145deg,
                rgba(255, 255, 255, 0.98),
                rgba(248, 250, 252, 0.96)
            );
    
        border:
            1px solid rgba(96, 165, 250, 0.22);
    
        box-shadow:
            0 10px 28px rgba(15, 23, 42, 0.06),
            inset 0 1px 0 rgba(255, 255, 255, 0.95);
    
    }
    
    
    /* =========================================================
    DATAFRAME HEADER
    ========================================================= */

    
    [data-testid="stDataFrame"] [role="columnheader"] {
    
        background: #EFF6FF !important;
    
        color: #1E3A5F !important;
    
        font-size: 12px;
    
        font-weight: 800;
    
        letter-spacing: 0.2px;
    
        border-bottom:
            1px solid rgba(59, 130, 246, 0.22);
    
    }
    
    
    /* =========================================================
    DATAFRAME BODY CELLS
    ========================================================= */
    
    [data-testid="stDataFrame"] [role="gridcell"] {
    
        color: #334155;
    
        font-size: 13px;
    
        font-weight: 500;
    
        background: rgba(255, 255, 255, 0.96);
    
        border-bottom:
            1px solid rgba(226, 232, 240, 0.75);
    
    }
    
    
    /* =========================================================
    ROW HOVER
    ========================================================= */
    
    [data-testid="stDataFrame"] [role="row"]:hover
    [role="gridcell"] {
    
        background:
            linear-gradient(
                135deg,
                rgba(239, 246, 255, 0.95),
                rgba(248, 250, 252, 0.98)
            );
    
    }
    
    
    /* =========================================================
    FIRST COLUMN - SLIGHTLY STRONGER
    ========================================================= */
    
    [data-testid="stDataFrame"]
    [role="row"]
    [role="gridcell"]:first-child {
    
        font-weight: 650;
    
        color: #1E3A8A;
    
    }
    
    
    /* =========================================================
    DATAFRAME SCROLL AREA
    ========================================================= */
    
    [data-testid="stDataFrame"] ::-webkit-scrollbar {
    
        width: 8px;
    
        height: 8px;
    
    }
    
    
    [data-testid="stDataFrame"] ::-webkit-scrollbar-thumb {
    
        background: rgba(96, 165, 250, 0.45);
    
        border-radius: 10px;
    
    }
    
    
    [data-testid="stDataFrame"] ::-webkit-scrollbar-track {
    
        background: rgba(241, 245, 249, 0.8);
    
    }

 
        hr {

            border-color:

                rgba(148, 163, 184, 0.22);

        }
    /* =========================================================

   RADIO BUTTON GROUP - PROFESSIONAL BLUE THEME

   ========================================================= */
 
div[role="radiogroup"] {
 
    background:

        linear-gradient(

            145deg,

            rgba(255, 255, 255, 0.98),

            rgba(239, 246, 255, 0.92)

        );
 
    border:

        1px solid rgba(59, 130, 246, 0.18);
 
    border-radius: 14px;
 
    padding: 8px 12px;
 
    box-shadow:

        0 6px 16px rgba(15, 23, 42, 0.05);
 
    width: fit-content;

}
 
 
/* Radio labels */
 
div[role="radiogroup"] label {
 
    color: #334155 !important;
 
    font-weight: 600 !important;
 
    margin-right: 8px;

}
 
 
/* Selected radio circle */
 
div[role="radiogroup"] input[type="radio"]:checked {
 
    accent-color: #2563EB;

}
/* =========================================================
   SEARCH INPUT - PROFESSIONAL BLUE THEME
   ========================================================= */
 
[data-testid="stTextInput"] {
 
    max-width: 420px;
}
 
 
[data-testid="stTextInput"] input {
 
    background: #FFFFFF !important;
 
    color: #0F172A !important;
 
    border:
        1px solid rgba(59, 130, 246, 0.28) !important;
 
    border-radius: 12px !important;
 
    padding: 10px 14px !important;
 
    box-shadow:
        0 5px 14px rgba(15, 23, 42, 0.05) !important;
}
 
 
/* Placeholder */
 
[data-testid="stTextInput"] input::placeholder {
 
    color: #64748B !important;
 
    opacity: 0.9;
}
 
 
/* Blue focus effect */
 
[data-testid="stTextInput"] input:focus {
 
    border-color: #3B82F6 !important;
 
    box-shadow:
        0 0 0 3px rgba(59, 130, 246, 0.12),
        0 6px 16px rgba(15, 23, 42, 0.06) !important;
 
    outline: none !important;
}
 
    </style>

    """,

    unsafe_allow_html=True,

)
 
 
# =========================================================

# HELPER: STANDARDIZE DIMENSION COLUMNS

# =========================================================

def clean_key(series: pd.Series) -> pd.Series:
 
    return (
        series.astype("string")
        .str.strip()
        .str.upper()
        .str.replace(r"\s+", " ", regex=True)
        .str.replace(r"\.0$", "", regex=True)
        .replace(
            {
                "": pd.NA,
                "NAN": pd.NA,
                "NONE": pd.NA,
                "<NA>": pd.NA,
                "NULL": pd.NA,
            }
        )
    )

def format_indian_number(value):

    value = int(round(value))
 
    sign = "-" if value < 0 else ""

    value = str(abs(value))
 
    if len(value) <= 3:

        return sign + value
 
    last_three = value[-3:]

    remaining = value[:-3]
 
    parts = []
 
    while len(remaining) > 2:

        parts.insert(0, remaining[-2:])

        remaining = remaining[:-2]
 
    if remaining:

        parts.insert(0, remaining)
 
    return sign + ",".join(parts) + "," + last_three
 

def standardize_columns(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
 
    dataframe = dataframe.copy()
 
    rename_map = {}
 
    if (
        REGION_COLUMN not in dataframe.columns
        and "STANDARD_REGION" in dataframe.columns
    ):
        rename_map["STANDARD_REGION"] = REGION_COLUMN
 
    if (
        STATE_COLUMN not in dataframe.columns
        and "STANDARD_STATE" in dataframe.columns
    ):
        rename_map["STANDARD_STATE"] = STATE_COLUMN
 
    if (
        HQ_COLUMN not in dataframe.columns
        and "STANDARD_HQ" in dataframe.columns
    ):
        rename_map["STANDARD_HQ"] = HQ_COLUMN
 
    if (
        BRAND_COLUMN not in dataframe.columns
        and "BrandName" in dataframe.columns
    ):
        rename_map["BrandName"] = BRAND_COLUMN
 
    if (
        BRAND_COLUMN not in dataframe.columns
        and "BRAND_NAME" in dataframe.columns
    ):
        rename_map["BRAND_NAME"] = BRAND_COLUMN
 
    if (
        PRODUCT_COLUMN not in dataframe.columns
        and "STANDARD_MATERIAL_NAME" in dataframe.columns
    ):
        rename_map[
            "STANDARD_MATERIAL_NAME"
        ] = PRODUCT_COLUMN
 
    dataframe = dataframe.rename(
    columns=rename_map
    )
    for column in [
        REGION_COLUMN,
        STATE_COLUMN,
        HQ_COLUMN,
        BRAND_COLUMN,
        PRODUCT_COLUMN,
    ]:
        if column in dataframe.columns:
            dataframe[column] = clean_key(
                dataframe[column]
            )
    
    return dataframe
 
# =========================================================

# HELPER: CREATE DASHBOARD DATE COLUMNS

# =========================================================
 
def add_date_columns(

    dataframe: pd.DataFrame,

) -> pd.DataFrame:
 
    dataframe = dataframe.copy()
 
    dataframe[MONTH_COLUMN] = pd.to_datetime(

        dataframe[MONTH_COLUMN],

        errors="coerce",

    )
 
    month_number = dataframe[

        MONTH_COLUMN

    ].dt.month
 
    calendar_year = dataframe[

        MONTH_COLUMN

    ].dt.year
 
    financial_year_start = calendar_year.where(

        month_number >= 4,

        calendar_year - 1,

    ).astype("Int64")
 
    quarter_number = (

        ((month_number - 4) % 12) // 3

        + 1

    ).astype("Int64")
 
    dataframe[YEAR_COLUMN] = (

        "FY"

        + financial_year_start.astype("string")

        + "-"

        + (financial_year_start + 1)

        .astype("string")

        .str[-2:]

    )
 
    dataframe[QUARTER_COLUMN] = (
        dataframe[YEAR_COLUMN]

        + " Q"

        + quarter_number.astype("string")

    )
 
    dataframe[MONTH_LABEL_COLUMN] = (

        dataframe[MONTH_COLUMN]

        .dt.strftime("%b %Y")

        .astype("string")

    )
 
    return dataframe
 
 
# =========================================================

# HELPER: VALIDATE REQUIRED COLUMNS

# =========================================================
 
def validate_columns(

    dataframe: pd.DataFrame,

    required_columns: list[str],

    mart_name: str,

) -> None:
 
    missing_columns = [

        column

        for column in required_columns

        if column not in dataframe.columns

    ]
 
    if missing_columns:

        raise KeyError(

            f"{mart_name} is missing columns: "

            f"{missing_columns}. "

            f"Available columns: "

            f"{dataframe.columns.tolist()}"

        )
 
 
# =========================================================

# HELPER: FILTER OPTIONS

# =========================================================
 
def get_options(

    dataframe: pd.DataFrame,

    column: str,

) -> list[str]:
 
    if column not in dataframe.columns:

        return []
 
    values = (

        dataframe[column]

        .dropna()

        .astype("string")

        .str.strip()

    )
 
    values = values[

        values.ne("")
& values.ne("<NA>")

    ]
 
    return sorted(

        values.unique().tolist()

    )
 
 
# =========================================================

# HELPER: APPLY DASHBOARD FILTERS

# =========================================================
 
def apply_filters(

    dataframe: pd.DataFrame,

    selected_years: list[str],

    selected_quarters: list[str],

    selected_months: list[str],

    selected_regions: list[str],

    selected_states: list[str],

    selected_hqs: list[str],

    selected_brands: list[str],

    selected_products: list[str],

) -> pd.DataFrame:
 
    mask = pd.Series(

        True,

        index=dataframe.index,

    )
 
    if selected_years:

        mask &= dataframe[

            YEAR_COLUMN

        ].isin(selected_years)
 
    if selected_quarters:

        mask &= dataframe[

            QUARTER_COLUMN

        ].isin(selected_quarters)
 
    if selected_months:

        mask &= dataframe[

            MONTH_LABEL_COLUMN

        ].isin(selected_months)
 
    if selected_regions:

        mask &= dataframe[

            REGION_COLUMN

        ].isin(selected_regions)
 
    if selected_states:

        mask &= dataframe[

            STATE_COLUMN

        ].isin(selected_states)
 
    if selected_hqs:

        mask &= dataframe[

            HQ_COLUMN

        ].isin(selected_hqs)
 
    if selected_brands:

        mask &= dataframe[

            BRAND_COLUMN

        ].isin(selected_brands)

    if selected_products:

        mask &= dataframe[

            PRODUCT_COLUMN

        ].isin(selected_products)
 
    return dataframe.loc[mask]

# =========================================================

# HELPER: APPLY TARGET FILTERS

#

# Target mart grain:

# Month + HQ + Brand

#

# Product filter cannot be applied because the target mart

# does not contain product-level targets.

# =========================================================
 
def apply_target_filters(

    dataframe: pd.DataFrame,

    selected_years: list[str],

    selected_quarters: list[str],

    selected_months: list[str],

    selected_regions: list[str],

    selected_states: list[str],

    selected_hqs: list[str],

    selected_brands: list[str],

) -> pd.DataFrame:
 
    mask = pd.Series(

        True,

        index=dataframe.index,

    )
 
    if selected_years:

        mask &= dataframe[

            YEAR_COLUMN

        ].isin(selected_years)
 
    if selected_quarters:

        mask &= dataframe[

            QUARTER_COLUMN

        ].isin(selected_quarters)
 
    if selected_months:

        mask &= dataframe[

            MONTH_LABEL_COLUMN

        ].isin(selected_months)
 
    if selected_regions:

        mask &= dataframe[

            REGION_COLUMN

        ].isin(selected_regions)
 
    if selected_states:

        mask &= dataframe[

            STATE_COLUMN

        ].isin(selected_states)
 
    if selected_hqs:

        mask &= dataframe[

            HQ_COLUMN

        ].isin(selected_hqs)
 
    if selected_brands:

        mask &= dataframe[

            BRAND_COLUMN

        ].isin(selected_brands)
 
    return dataframe.loc[mask]
 
 
 
# =========================================================

# HELPER: KPI FORMATTING

# =========================================================
def format_currency(value: float) -> str:
    """Format numbers using Indian currency units."""
 
    value = 0 if pd.isna(value) else value
 
    if abs(value) >= 10_000_000:
        return f"{value / 10_000_000:,.2f} Cr"
 
    if abs(value) >= 100_000:
        return f"{value / 100_000:,.2f} L"
 
    if abs(value) >= 1_000:
        return f"{value / 1_000:,.2f} K"
 
    return f"{value:,.0f}"
 
 
def safe_percentage(
    numerator: float,
    denominator: float,
) -> float:
    if denominator == 0:
        return 0.0
 
    return numerator / denominator * 100
 
 
def safe_sum(
    dataframe: pd.DataFrame,
    column: str,
) -> float:
    if column not in dataframe.columns:
        return 0.0
 
    return dataframe[column].fillna(0).sum()
 
 
 
# =========================================================

# HELPER: ACTIVE FILTER CHIP

# =========================================================
 
def create_filter_chip(

    label: str,

    values: list[str],

    maximum_display: int = 3,

) -> str:
 
    if not values:

        return ""
 
    displayed_values = values[

        :maximum_display

    ]
 
    value_text = ", ".join(

        map(str, displayed_values)

    )
 
    remaining_count = (

        len(values)

        - maximum_display

    )
 
    if remaining_count > 0:

        value_text += (

            f" +{remaining_count} more"

        )
 
    return (

        '<span class="filter-chip">'

        f"{label}: {value_text}"

        "</span>"

    )
 
 
# =========================================================

# LOAD AND PREPARE DATA

# =========================================================
 
@st.cache_data(

    show_spinner="Loading dashboard data..."

)

def load_data():
 
    sales = pd.read_parquet(

        SALES_FILE

    )

    target = pd.read_parquet(

        TARGET_FILE

    )

    mr = pd.read_parquet(

        MR_FILE

    )
 
    doctor = pd.read_parquet(

        DOCTOR_FILE

    )
 
    visit = pd.read_parquet(

        VISIT_FILE

    )
 
    product = pd.read_parquet(

        PRODUCT_FILE

    )
 
    marts = {

        "sales": sales,

        "target": target,

        "mr": mr,

        "doctor": doctor,

        "visit": visit,

        "product": product,

    }
 
    prepared_marts = {}
 
    for mart_name, mart in marts.items():
 
        mart = standardize_columns(

            mart

        )
 
        mart = add_date_columns(

            mart

        )
 
        prepared_marts[mart_name] = mart
 
    return (

        prepared_marts["sales"],

        prepared_marts["target"],

        prepared_marts["mr"],

        prepared_marts["doctor"],

        prepared_marts["visit"],

        prepared_marts["product"],

    )
 
 
(

    sales_mart,

    target_mart,

    mr_mart,

    doctor_mart,

    visit_mart,

    product_mart,

) = load_data()
 
 
# =========================================================

# VALIDATE COLUMNS

# =========================================================
 
common_dimension_columns = [

    MONTH_COLUMN,

    YEAR_COLUMN,

    QUARTER_COLUMN,

    MONTH_LABEL_COLUMN,

    REGION_COLUMN,

    STATE_COLUMN,

    HQ_COLUMN,

    BRAND_COLUMN,

    PRODUCT_COLUMN,

]
 
validate_columns(

    sales_mart,

    common_dimension_columns

    + [

        "GROSS_REVENUE",

        "RETURN_AMOUNT",

        "NET_REVENUE",

        "NET_QUANTITY",

        "TRACEABLE_REVENUE",

        "UNTRACED_REVENUE",

    ],

    "Sales mart",

)

validate_columns(
    target_mart,
    [
        MONTH_COLUMN,
        YEAR_COLUMN,
        QUARTER_COLUMN,
        MONTH_LABEL_COLUMN,
        REGION_COLUMN,
        STATE_COLUMN,
        HQ_COLUMN,
        BRAND_COLUMN,
        "TARGET_SALES",
        "TARGET_QUANTITY",
    ],
    "Target mart",
)
 
validate_columns(

    mr_mart,

    common_dimension_columns

    + [MR_COLUMN],

    "MR mart",

)
 
validate_columns(

    doctor_mart,

    common_dimension_columns

    + [DOCTOR_COLUMN, "SPECIALISATION_KEY"],

    "Doctor mart",

)
 
validate_columns(

    visit_mart,

    common_dimension_columns

    + [VISIT_COLUMN, "DOCTOR_KEY", "MR_KEY"],

    "Visit mart",

)
 
validate_columns(

    product_mart,

    common_dimension_columns,

    "Product mart",

)
 
 
# =========================================================

# DASHBOARD HEADER

# =========================================================
 
st.html(
    """
    <div class="dashboard-header">
        <p class="dashboard-title">
            Sales & Field Force Intelligence
        </p>
        <p class="dashboard-subtitle">
            Integrated analysis of revenue performance,
            sales traceability and field-force execution
        </p>
    </div>
    """
)
 
 
# =========================================================

# FILTER SOURCE

# =========================================================
 
filter_source = product_mart
 
 
# =========================================================

# RESET FILTER CALLBACK

# =========================================================
 
FILTER_KEYS = [

    "year_filter",

    "quarter_filter",

    "month_filter",

    "region_filter",

    "state_filter",

    "hq_filter",

    "brand_filter",

    "product_filter",

]
 
 
def reset_filters() -> None:
 
    for key in FILTER_KEYS:

        st.session_state[key] = []
 
 
# =========================================================

# SIDEBAR FILTERS

# =========================================================
 
st.sidebar.markdown(

    "## Dashboard Filters"

)

st.sidebar.button(

    "Reset All Filters",

    use_container_width=True,

    on_click=reset_filters,

)



 
# ---------------------------------------------------------
# FINANCIAL YEAR
# ---------------------------------------------------------
 
year_options = get_options(
    filter_source,
    YEAR_COLUMN,
)
 
selected_years = st.sidebar.multiselect(
    "Financial Year",
    options=year_options,
    key="year_filter",
    placeholder="All financial years",
)
 
 
# ---------------------------------------------------------
# FINANCIAL QUARTER
# Display only Q1, Q2, Q3, Q4
# ---------------------------------------------------------
 
quarter_source = filter_source.copy()
 
if selected_years:
    quarter_source = quarter_source[
        quarter_source[
            YEAR_COLUMN
        ]
        .astype("string")
        .isin(selected_years)
    ]
 
 
quarter_options = (
    quarter_source[
        QUARTER_COLUMN
    ]
    .dropna()
    .astype("string")
    .str.extract(
        r"(Q[1-4])",
        expand=False,
    )
    .dropna()
    .unique()
    .tolist()
)
 
quarter_options = sorted(
    quarter_options,
    key=lambda quarter: int(quarter[1]),
)
 
 
selected_quarters = st.sidebar.multiselect(
    "Financial Quarter",
    options=quarter_options,
    key="quarter_filter",
    placeholder="All quarters",
)
 
 
# ---------------------------------------------------------
# BUILD FULL QUARTER KEYS FOR FILTERING
# Example:
# Displayed option = Q2
# Internal key     = FY2025-26 Q2
# ---------------------------------------------------------
 
selected_quarter_keys = []
 
if selected_quarters:
 
    quarter_number = (
        quarter_source[
            QUARTER_COLUMN
        ]
        .astype("string")
        .str.extract(
            r"(Q[1-4])",
            expand=False,
        )
    )
 
    selected_quarter_keys = (
        quarter_source.loc[
            quarter_number.isin(selected_quarters),
            QUARTER_COLUMN,
        ]
        .dropna()
        .astype("string")
        .unique()
        .tolist()
    )
 
 
# ---------------------------------------------------------
# MONTH
# Display only after quarter selection
# ---------------------------------------------------------
 
selected_months = []
 
if selected_quarter_keys:
 
    month_source = quarter_source[
        quarter_source[
            QUARTER_COLUMN
        ]
        .astype("string")
        .isin(selected_quarter_keys)
    ].copy()
 
    month_options = (
        month_source[
            [
                MONTH_COLUMN,
                MONTH_LABEL_COLUMN,
            ]
        ]
        .dropna(
            subset=[
                MONTH_COLUMN,
                MONTH_LABEL_COLUMN,
            ]
        )
        .drop_duplicates()
        .sort_values(MONTH_COLUMN)
        [MONTH_LABEL_COLUMN]
        .astype("string")
        .tolist()
    )
 
    selected_months = st.sidebar.multiselect(
        "Month",
        options=month_options,
        key="month_filter",
        placeholder="All months",
    )
 
 
# ---------------------------------------------------------

# REGION

# ---------------------------------------------------------
 
region_source = quarter_source
 
if selected_quarter_keys:

    region_source = region_source[

        region_source[

            QUARTER_COLUMN

        ].isin(selected_quarter_keys)

    ]
 
if selected_months:

    region_source = region_source[

        region_source[

            MONTH_LABEL_COLUMN

        ].isin(selected_months)

    ]
 
region_options = get_options(

    region_source,

    REGION_COLUMN,

)
 
selected_regions = st.sidebar.multiselect(

    "Region",

    options=region_options,

    key="region_filter",

    placeholder="All regions",

)
 
 
# ---------------------------------------------------------

# STATE

# ---------------------------------------------------------
 
state_source = region_source
 
if selected_regions:

    state_source = state_source[

        state_source[

            REGION_COLUMN

        ].isin(selected_regions)

    ]
 
state_options = get_options(

    state_source,

    STATE_COLUMN,

)
 
selected_states = st.sidebar.multiselect(

    "State",

    options=state_options,

    key="state_filter",

    placeholder="All states",

)
 
 
# ---------------------------------------------------------

# HQ

# ---------------------------------------------------------
 
hq_source = state_source
 
if selected_states:

    hq_source = hq_source[

        hq_source[

            STATE_COLUMN

        ].isin(selected_states)

    ]
 
hq_options = get_options(

    hq_source,

    HQ_COLUMN,

)
 
selected_hqs = st.sidebar.multiselect(

    "HQ",

    options=hq_options,

    key="hq_filter",

    placeholder="All HQs",

)
 
 
# ---------------------------------------------------------

# BRAND

# ---------------------------------------------------------

dcr_brand_source = hq_source.copy()
 
if selected_hqs:

    dcr_brand_source = dcr_brand_source[

        dcr_brand_source[

            HQ_COLUMN

        ].isin(selected_hqs)

    ]
 
 
# ---------------------------------------------------------

# SALES BRAND SOURCE

# Apply the same filters up to HQ

# ---------------------------------------------------------
 
sales_brand_source = sales_mart.copy()
 
if selected_years:

    sales_brand_source = sales_brand_source[

        sales_brand_source[

            YEAR_COLUMN

        ].isin(selected_years)

    ]
 
if selected_quarter_keys:

    sales_brand_source = sales_brand_source[

        sales_brand_source[

            QUARTER_COLUMN

        ].isin(selected_quarter_keys)

    ]
 
if selected_months:

    sales_brand_source = sales_brand_source[

        sales_brand_source[

            MONTH_LABEL_COLUMN

        ].isin(selected_months)

    ]
 
if selected_regions:

    sales_brand_source = sales_brand_source[

        sales_brand_source[

            REGION_COLUMN

        ].isin(selected_regions)

    ]
 
if selected_states:

    sales_brand_source = sales_brand_source[

        sales_brand_source[

            STATE_COLUMN

        ].isin(selected_states)

    ]
 
if selected_hqs:

    sales_brand_source = sales_brand_source[

        sales_brand_source[

            HQ_COLUMN

        ].isin(selected_hqs)

    ]
 
 
# ---------------------------------------------------------

# GET DCR BRANDS

# ---------------------------------------------------------
 
dcr_brand_options = get_options(

    dcr_brand_source,

    BRAND_COLUMN,

)
 
 
# ---------------------------------------------------------

# GET SALES BRANDS

# ---------------------------------------------------------
 
sales_brand_options = get_options(

    sales_brand_source,

    BRAND_COLUMN,

)
 
 
# ---------------------------------------------------------

# UNION = DCR BRANDS + SALES BRANDS

# ---------------------------------------------------------
 
brand_options = sorted(

    set(dcr_brand_options)

    | set(sales_brand_options)

)

brand_options= [
    brand
    for brand in brand_options
    if str(brand).strip().upper() != "ASRA"
]
 
 
selected_brands = st.sidebar.multiselect(

    "Brand",

    options=brand_options,

    key="brand_filter",

    placeholder="All brands",

)
 
# ---------------------------------------------------------

# PRODUCT

# ---------------------------------------------------------
 
product_source = dcr_brand_source
 
if selected_brands:

    product_source = product_source[

        product_source[

            BRAND_COLUMN

        ].isin(selected_brands)

    ]

product_options = get_options(

    product_source,

    PRODUCT_COLUMN,

)

selected_products = st.sidebar.multiselect(

    "Product",

    options=product_options,

    key="product_filter",

    placeholder="All products",

)

st.sidebar.divider()
 

 
 
# =========================================================

# ACTIVE FILTER SUMMARY

# Main dashboard only — not in sidebar

# =========================================================
 
filter_selections = {

    "Year": selected_years,

    "Quarter": selected_quarter_keys,

    "Month": selected_months,

    "Region": selected_regions,

    "State": selected_states,

    "HQ": selected_hqs,

    "Brand": selected_brands,

    "Product": selected_products,

}
 
active_filter_count = sum(

    bool(values)

    for values in filter_selections.values()

)
 
filter_chips = []
 
for label, values in filter_selections.items():
 
    chip = create_filter_chip(

        label,

        values,

    )
 
    if chip:

        filter_chips.append(chip)
 
 
if filter_chips:
 
    filter_summary_html = "".join(

        filter_chips

    )
 
else:
 
    filter_summary_html = (

        '<span class="filter-chip-empty">'

        "Full Business Overview · All Regions, HQs and Brands"

        "</span>"

    )
 
 
st.html(
    f"""
    <div class="filter-summary">
        <div class="filter-summary-title">
            Current View · {active_filter_count}
            active filter{"s" if active_filter_count != 1 else ""}
         </div>
        {filter_summary_html}
    </div>
    """
)
 
 
# =========================================================

# APPLY FILTERS TO ALL MARTS

# =========================================================
 
filter_arguments = (

    selected_years,

    selected_quarter_keys,

    selected_months,

    selected_regions,

    selected_states,

    selected_hqs,

    selected_brands,

    selected_products,

)
 
filtered_sales = apply_filters(

    sales_mart,

    *filter_arguments,

)

filtered_target = apply_target_filters(
    target_mart,
    selected_years,
    selected_quarter_keys,
    selected_months,
    selected_regions,
    selected_states,
    selected_hqs,
    selected_brands,
)    
 
filtered_mr = apply_filters(

    mr_mart,

    *filter_arguments,

)
 
filtered_doctor = apply_filters(

    doctor_mart,

    *filter_arguments,

)
 
filtered_visit = apply_filters(

    visit_mart,

    *filter_arguments,

)
 
filtered_product = apply_filters(

    product_mart,

    *filter_arguments,

)
 
 
# =========================================================

# REVENUE KPI CALCULATIONS

# =========================================================
 
gross_revenue = safe_sum(
    filtered_sales,
    "GROSS_REVENUE",
)
 
return_amount = safe_sum(
    filtered_sales,
    "RETURN_AMOUNT",
)
 
net_revenue = safe_sum(
    filtered_sales,
    "NET_REVENUE",
)
 
traceable_revenue = safe_sum(
    filtered_sales,
    "TRACEABLE_REVENUE",
)
 
untraced_revenue = safe_sum(
    filtered_sales,
    "UNTRACED_REVENUE",
)
 
net_quantity = safe_sum(
    filtered_sales,
    "NET_QUANTITY",
)
 
traceable_percentage = safe_percentage(

    traceable_revenue,

    net_revenue,

)
 
untraced_percentage = safe_percentage(

    untraced_revenue,

    net_revenue,

)
 
return_percentage = safe_percentage(

    return_amount,

    gross_revenue,

)
 
 
# =========================================================

# FIELD FORCE KPI CALCULATIONS

# =========================================================
 
active_mrs = (

    filtered_mr[

        MR_COLUMN

    ].nunique()

)
 
unique_doctors = (

    filtered_doctor[

        DOCTOR_COLUMN

    ].nunique()

)
 
total_visits = (

    filtered_visit[

        VISIT_COLUMN

    ].nunique()

)
 
brands_detailed = (
    filtered_product.loc[
        filtered_product[
            BRAND_COLUMN
        ]
        .astype("string")
        .str.strip()
        .str.upper()
        .ne("ASRA"),
        BRAND_COLUMN,
    ]
    .dropna()
    .nunique()
)
 
products_detailed = (

    filtered_product[

        PRODUCT_COLUMN

    ].nunique()

)
 
visits_per_mr = (

    total_visits / active_mrs

    if active_mrs > 0

    else 0

)
 
doctors_per_mr = (

    unique_doctors / active_mrs

    if active_mrs > 0

    else 0

)


# ============================================================

# QOQ DELTA CALCULATIONS

# ============================================================

#

# QoQ intentionally ignores:

# Financial Year

# Financial Quarter

# Month

#

# This is required so:

#

# FY2026-27 Q1

#       compares with

# FY2025-26 Q4

#

# Region / State / HQ / Brand / Product

# are still respected.

# ============================================================
 
 
qoq_sales = apply_filters(

    sales_mart,
 
    selected_years=[],

    selected_quarters=[],

    selected_months=[],
 
    selected_regions=selected_regions,

    selected_states=selected_states,

    selected_hqs=selected_hqs,

    selected_brands=selected_brands,

    selected_products=selected_products,

).copy()
 
 
# ============================================================

# AGGREGATE ALL REVENUE KPI VALUES BY FINANCIAL QUARTER

# ============================================================
 
quarterly_sales = (

    qoq_sales

    .groupby(

        QUARTER_COLUMN,

        as_index=False,

        observed=True,

    )

    .agg(

        GROSS_REVENUE=(

            "GROSS_REVENUE",

            "sum",

        ),
 
        RETURN_AMOUNT=(

            "RETURN_AMOUNT",

            "sum",

        ),
 
        NET_REVENUE=(

            "NET_REVENUE",

            "sum",

        ),
 
        NET_QUANTITY=(

            "NET_QUANTITY",

            "sum",

        ),
 
        TRACEABLE_REVENUE=(

            "TRACEABLE_REVENUE",

            "sum",

        ),
 
        UNTRACED_REVENUE=(

            "UNTRACED_REVENUE",

            "sum",

        ),

    )

)
 
 
# ============================================================

# EXTRACT FINANCIAL YEAR AND QUARTER NUMBER

# ============================================================
 
quarterly_sales[

    "FY_START_YEAR"

] = pd.to_numeric(

    quarterly_sales[

        QUARTER_COLUMN

    ]

    .astype("string")

    .str.extract(

        r"FY(\d{4})",

        expand=False,

    ),

    errors="coerce",

)
 
 
quarterly_sales[

    "QUARTER_NUMBER"

] = pd.to_numeric(

    quarterly_sales[

        QUARTER_COLUMN

    ]

    .astype("string")

    .str.extract(

        r"Q([1-4])",

        expand=False,

    ),

    errors="coerce",

)
 
 
# ============================================================

# CREATE TRUE QUARTER ORDER

#

# FY2025-26 Q4

# comes immediately before

# FY2026-27 Q1

# ============================================================
 
quarterly_sales[

    "QUARTER_ORDER"

] = (

    quarterly_sales[

        "FY_START_YEAR"

    ]

    * 4

    +

    quarterly_sales[

        "QUARTER_NUMBER"

    ]

)
 
 
quarterly_sales = (

    quarterly_sales

    .dropna(

        subset=[

            "FY_START_YEAR",

            "QUARTER_NUMBER",

        ]

    )

    .sort_values(

        "QUARTER_ORDER",

        ascending=True,

    )

    .reset_index(drop=True)

)
 
 
# ============================================================

# DEFAULT DELTA VALUES

# ============================================================
 
gross_qoq_growth = None
 
return_qoq_growth = None
 
qoq_growth = None
 
quantity_qoq_growth = None
 
traceable_qoq_growth = None
 
untraced_qoq_growth = None
 
traceable_percentage_delta = None
 
untraced_percentage_delta = None
 
return_percentage_delta = None
 
 
current_quarter_sales = 0.0
 
previous_quarter_sales = 0.0
 
 
current_quarter_label = (

    "Current Quarter"

)
 
previous_quarter_label = (

    "Previous Quarter"

)
 
 
qoq_delta_text = (

    "Previous quarter data not available"

)
 
 
# ============================================================

# HELPER — QOQ GROWTH %

# ============================================================
 
def calculate_qoq_growth(

    current_value,

    previous_value,

):
 
    if (

        previous_value is None

        or pd.isna(previous_value)

        or previous_value == 0

    ):

        return None
 
    return (

        (

            current_value

            - previous_value

        )

        / abs(previous_value)

        * 100

    )
 
 
# ============================================================

# SHORT QUARTER LABEL

#

# FY2026-27 Q1 -> Q1 '27

# FY2025-26 Q4 -> Q4 '26

# ============================================================
 
def short_quarter_label(

    quarter_label: str,

) -> str:
 
    match = re.search(

        r"FY(\d{4})-(\d{2}) Q([1-4])",

        str(quarter_label),

    )
 
    if not match:

        return str(

            quarter_label

        )
 
    end_year = match.group(2)
 
    quarter = match.group(3)
 
    return (

        f"Q{quarter} '{end_year}"

    )
 
 
# ============================================================

# GET CURRENT AND PREVIOUS QUARTER

# ============================================================
 
if len(quarterly_sales) >= 2:
 
    previous_quarter = (

        quarterly_sales.iloc[-2]

    )
 
    current_quarter = (

        quarterly_sales.iloc[-1]

    )
 
 
    # --------------------------------------------------------

    # SHORT QUARTER LABELS

    # --------------------------------------------------------
 
    current_quarter_label = (

        short_quarter_label(

            current_quarter[

                QUARTER_COLUMN

            ]

        )

    )
 
 
    previous_quarter_label = (

        short_quarter_label(

            previous_quarter[

                QUARTER_COLUMN

            ]

        )

    )
 
 
    # ========================================================

    # NET REVENUE

    # ========================================================
 
    current_quarter_sales = (

        current_quarter[

            "NET_REVENUE"

        ]

    )
 
    previous_quarter_sales = (

        previous_quarter[

            "NET_REVENUE"

        ]

    )
 
 
    qoq_growth = (

        calculate_qoq_growth(

            current_quarter_sales,

            previous_quarter_sales,

        )

    )
 
 
    # ========================================================

    # GROSS REVENUE

    # ========================================================
 
    gross_qoq_growth = (

        calculate_qoq_growth(

            current_quarter[

                "GROSS_REVENUE"

            ],

            previous_quarter[

                "GROSS_REVENUE"

            ],

        )

    )
 
 
    # ========================================================

    # RETURN AMOUNT

    # ========================================================
 
    return_qoq_growth = (

        calculate_qoq_growth(

            current_quarter[

                "RETURN_AMOUNT"

            ],

            previous_quarter[

                "RETURN_AMOUNT"

            ],

        )

    )
 
 
    # ========================================================

    # NET QUANTITY

    # ========================================================
 
    quantity_qoq_growth = (

        calculate_qoq_growth(

            current_quarter[

                "NET_QUANTITY"

            ],

            previous_quarter[

                "NET_QUANTITY"

            ],

        )

    )
 
 
    # ========================================================

    # TRACEABLE REVENUE

    # ========================================================
 
    traceable_qoq_growth = (

        calculate_qoq_growth(

            current_quarter[

                "TRACEABLE_REVENUE"

            ],

            previous_quarter[

                "TRACEABLE_REVENUE"

            ],

        )

    )
 
 
    # ========================================================

    # UNTRACED REVENUE

    # ========================================================
 
    untraced_qoq_growth = (

        calculate_qoq_growth(

            current_quarter[

                "UNTRACED_REVENUE"

            ],

            previous_quarter[

                "UNTRACED_REVENUE"

            ],

        )

    )
 
 
    # ========================================================

    # TRACEABLE %

    # Percentage-point change

    # ========================================================
 
    current_traceable_percentage = (

        safe_percentage(

            current_quarter[

                "TRACEABLE_REVENUE"

            ],

            current_quarter[

                "NET_REVENUE"

            ],

        )

    )
 
 
    previous_traceable_percentage = (

        safe_percentage(

            previous_quarter[

                "TRACEABLE_REVENUE"

            ],

            previous_quarter[

                "NET_REVENUE"

            ],

        )

    )
 
 
    traceable_percentage_delta = (

        current_traceable_percentage

        - previous_traceable_percentage

    )
 
 
    # ========================================================

    # UNTRACED %

    # Percentage-point change

    # ========================================================
 
    current_untraced_percentage = (

        safe_percentage(

            current_quarter[

                "UNTRACED_REVENUE"

            ],

            current_quarter[

                "NET_REVENUE"

            ],

        )

    )
 
 
    previous_untraced_percentage = (

        safe_percentage(

            previous_quarter[

                "UNTRACED_REVENUE"

            ],

            previous_quarter[

                "NET_REVENUE"

            ],

        )

    )
 
 
    untraced_percentage_delta = (

        current_untraced_percentage

        - previous_untraced_percentage

    )
 
 
    # ========================================================

    # RETURN %

    #

    # Return Amount / Gross Revenue

    # Percentage-point change

    # ========================================================
 
    current_return_percentage = (

        safe_percentage(

            current_quarter[

                "RETURN_AMOUNT"

            ],

            current_quarter[

                "GROSS_REVENUE"

            ],

        )

    )
 
 
    previous_return_percentage = (

        safe_percentage(

            previous_quarter[

                "RETURN_AMOUNT"

            ],

            previous_quarter[

                "GROSS_REVENUE"

            ],

        )

    )
 
 
    return_percentage_delta = (

        current_return_percentage

        - previous_return_percentage

    )
 
 
    # ========================================================

    # QOQ CONTEXT

    #

    # Q1 '27 ₹18.23 Cr vs Q4 '26 ₹13.17 Cr

    # ========================================================
 
    qoq_delta_text = (

        f"{current_quarter_label} "

        f"₹{format_currency(current_quarter_sales)}"

        f" vs "

        f"{previous_quarter_label} "

        f"₹{format_currency(previous_quarter_sales)}"

    )
 
 

 

selected_view = st.radio(

    "Select View",

    ["Overview", "Doctor Coverage", "Targets vs Achievement", "Forecasting"],

    horizontal=True,
    label_visibility="collapsed",

)
 
 
if selected_view == "Overview": 
# =========================================================

# REVENUE PERFORMANCE

# =========================================================
 
    st.html(
        """
        <div class="section-header">
            <p class="section-title">
                Revenue Performance
            </p>
            <p class="section-caption">
                Executive sales of sales, returns, net revenue and revenue traceability
            </p>
        </div>
        """,
    )
    
    # ============================================================

    # REVENUE PERFORMANCE — EXECUTIVE LAYOUT

    # ============================================================

    
    revenue_left, revenue_right = st.columns(

        [1.72, 1],

        gap="small",

    )
    
    
    # ============================================================

    # LEFT SIDE — KPI CARDS

    # ============================================================
    
    with revenue_left:
    
        # --------------------------------------------------------

        # FIRST ROW

        # Gross | Return | Net Revenue

        # --------------------------------------------------------
    
        revenue_top = st.columns(
            3
        )
    
    
        revenue_top[0].metric(

            label="Gross Revenue",

            value=f"₹{format_currency(gross_revenue)}",
    
            delta=(

                f"{gross_qoq_growth:+.2f}% ."
                f"{current_quarter_label} vs {previous_quarter_label}"

                if gross_qoq_growth is not None

                else None

            ),
    
            delta_color="normal",
    
            help=(

                "Total positive sales value before "

                "returns and credit adjustments."

            ),
    
            border=True,

        )
    
    
        revenue_top[1].metric(

            label="Return Amount",

            value=f"₹{format_currency(return_amount)}",
    
            delta=(
                f"{return_qoq_growth:+.2f}% ."
                f"{current_quarter_label} vs {previous_quarter_label}"
                if return_qoq_growth is not None

                else None

            ),
    
            delta_color="inverse",
    
            help=(

                "Total value of product returns. "

                "A decrease is favourable."

            ),
    
            border=True,

        )
    
    
        revenue_top[2].metric(

            label="Net Revenue",

            value=f"₹{format_currency(net_revenue)}",
    
            delta=(
                f"{qoq_growth:+.2f}% ."
                f"{current_quarter_label} vs {previous_quarter_label}"

                if qoq_growth is not None

                else None

            ),
    
            delta_color="normal",
    
            help=(

                "Revenue remaining after product returns "

                "are deducted from gross revenue."

            ),
    
            border=True,

        )
    
    
        # --------------------------------------------------------

        # SECOND ROW

        # Net Quantity | QoQ Growth | blank

        # --------------------------------------------------------
    
        revenue_bottom = st.columns(

            2,

            gap="medium",

        )
    
    
        revenue_bottom[0].metric(

            label="Net Quantity",

            value=f"{format_indian_number(net_quantity)}",
    
            delta=(
                f"{quantity_qoq_growth:+.2f}% ."
                f"{current_quarter_label} vs {previous_quarter_label}"
                if quantity_qoq_growth is not None

                else None

            ),
    
            delta_color="normal",
    
            help=(

                "Net quantity sold after returned "

                "quantities are deducted."

            ),
    
            border=True,

        )
    
    
        revenue_bottom[1].metric(

            label="QoQ Growth",
    
            value=(

                f"{qoq_growth:.2f}%"

                if qoq_growth is not None

                else "N/A"

            ),
    
            delta=(

                qoq_delta_text

                if qoq_growth is not None

                else None

            ),
    
            delta_color=(

                "normal"

                if qoq_growth is None or qoq_growth >= 0

                else "inverse"

            ),
    
            help=(

                "Net revenue growth compared with "

                "the immediately preceding financial quarter."

            ),
    
            border=True,

        )
    
    
    # ============================================================

    # RIGHT SIDE — TRACEABILITY DONUT

    # ============================================================
    
    with revenue_right:
    
        # ========================================================

        # TRACEABILITY DATA

        # ========================================================
    
        traceability_data = pd.DataFrame(

            {

                "Revenue Type": [

                    "Traceable",

                    "Untraced",

                ],

                "Revenue": [

                    traceable_revenue,

                    untraced_revenue,

                ],

            }

        )
    
    
        total_traceability_revenue = (

            traceability_data["Revenue"].sum()

        )
    
    
        if total_traceability_revenue > 0:
    
            traceability_data["Share"] = (

                traceability_data["Revenue"]

                / total_traceability_revenue

                * 100

            )
    
        else:
    
            traceability_data["Share"] = 0
    
    
        # ========================================================

        # COMPACT DONUT

        # ========================================================
    
        donut = (

            alt.Chart(traceability_data)

            .mark_arc(

                innerRadius=46,

                outerRadius=68,

                cornerRadius=5,

                padAngle=0.025,

            )

            .encode(

                theta=alt.Theta(

                    "Revenue:Q"

                ),
    
                color=alt.Color(

                    "Revenue Type:N",
    
                    scale=alt.Scale(

                        domain=[

                            "Traceable",

                            "Untraced",

                        ],
    
                        range=[

                            "#2563EB",

                            "#F59E0B",

                        ],

                    ),
    
                    legend=None,

                ),
    
                tooltip=[

                    alt.Tooltip(

                        "Revenue Type:N",

                        title="Revenue Type",

                    ),
    
                    alt.Tooltip(

                        "Revenue:Q",

                        title="Revenue",

                        format=",.0f",

                    ),
    
                    alt.Tooltip(

                        "Share:Q",

                        title="Share",

                        format=".2f",

                    ),

                ],

            )

        )
    
    
        # ========================================================

        # CENTER VALUE

        # ========================================================
    
        center_data = pd.DataFrame(

            {

                "label": [

                    "Net Revenue"

                ],
    
                "value": [

                    f"₹{format_currency(net_revenue)}"

                ],

            }

        )
    
    
        center_label = (

            alt.Chart(center_data)

            .mark_text(

                fontSize=13,

                fontWeight=500,

                color="#64748B",

                dy=-7,

            )

            .encode(

                text="label:N"

            )

        )
    
    
        center_value = (

            alt.Chart(center_data)

            .mark_text(

                fontSize=14,

                fontWeight=800,

                color="#163A5F",

                dy=8,

            )

            .encode(

                text="value:N"

            )

        )
    
    
        final_donut = (

            donut

            + center_label

            + center_value

        ).properties(

            height=175,

        )
    
    
        # ========================================================

        # LARGE KPI-STYLE TRACEABILITY CARD

        # ========================================================
    
        with st.container(

            key="traceability_card",

        ):
    
            st.html(

                """
    <div>
    <div class="trace-card-title">

                        Revenue Traceability
    </div>
    
                    <div class="trace-card-caption">

                        Traceable vs untraced revenue mix
    </div>
    </div>

                """

            )
    
    
            donut_col, values_col = st.columns(

                [1.05, 0.95],

                gap="small",

            )
    
    
            # ----------------------------------------------------

            # DONUT

            # ----------------------------------------------------
    
            with donut_col:
    
                st.altair_chart(

                    final_donut,

                    width="stretch",

                )
    
    
            # ----------------------------------------------------

            # VALUES BESIDE DONUT

            # ----------------------------------------------------
    
            with values_col:
    
                st.html(

                    f"""
    <div class="trace-value-area">
    
    
                        <div class="trace-item traceable">
    
                            <div class="trace-label">

                                Traceable Revenue
                                <span

                                        class="trace-tooltip"

                                        title="Portion of net revenue linked to field-force activity through mapped HQ and brand coverage."
                                >

                                        ⓘ
                                </span>
                            </div>
 
    
                            <div class="trace-value">

                                ₹{format_currency(traceable_revenue)}
    </div>
    
                            <div class="trace-share blue">

                                {traceable_percentage:.2f}%
    </div>
    
                        </div>
    
    
                        <div class="trace-divider"></div>
    
    
                        <div class="trace-item untraced">
    
        
                        <div class="trace-label">

                            Untraced Revenue
                            <span

                                    class="trace-tooltip"

                                    title="Portion of net revenue that could not be linked to field-force activity because corresponding HQ or brand coverage was not identified."
                            >

                                    ⓘ
                            </span>
                        </div>
                        <div class="trace-value">

                                ₹{format_currency(untraced_revenue)}
    </div>
                            
    
                            <div class="trace-share orange">

                                {untraced_percentage:.2f}%
    </div>
    
                        </div>
    
    
                    </div>

                    """

                )
    
    # =========================================================

    # FIELD FORCE EFFECTIVENESS

    # =========================================================
    
    st.html(
        """
        <div class="section-header">
            <p class="section-title">
                Field Force Effectiveness
            </p>
            <p class="section-caption">
                MR activity, doctor engagement and product-detailing coverage
            </p>
        </div>
        """
    )
    
    
    field_row_1 = st.columns(5)
    
    field_row_1[0].metric(

        label="Active MRs",

        value=f"{active_mrs:,}",

        help=(

            "Number of unique field representatives with "

            "recorded DCR activity in the selected period."

        ),

        border=True,

    )
    
    field_row_1[1].metric(

        label="Unique Doctors",

        value=f"{format_indian_number(unique_doctors)}",

        help=(

            "Number of distinct doctors covered by the field force "

            "during the selected period."

        ),

        border=True,

    )
    
    field_row_1[2].metric(

        label="Total Visits",

        value=f"{format_indian_number(total_visits)}",

        help=(

            "Total doctor visits recorded by field representatives "

            "during the selected period."

        ),

        border=True,

    )
    
    field_row_1[3].metric(

        label="Brands Detailed",

        value=f"{brands_detailed:,}",

        help=(

            "Number of distinct brands detailed to doctors "

            "during field visits."

        ),

        border=True,

    )
    
    field_row_1[4].metric(

        label="Products Detailed",

        value=f"{products_detailed:,}",

        help=(

            "Number of distinct products detailed to doctors "

            "during field visits."

        ),

        border=True,

    )
    
    
    
    field_row_2 = st.columns(2)
    
    field_row_2[0].metric(

        label="Visits per MR",

        value=f"{visits_per_mr:,.2f}",

        help=(

            "Average number of doctor visits per active MR. "

            "Calculated as Total Visits ÷ Active MRs."

        ),

        border=True,

    )
    
    field_row_2[1].metric(

        label="Doctors per MR",

        value=f"{doctors_per_mr:,.2f}",

        help=(

            "Average number of unique doctors covered per active MR. "

            "Calculated as Unique Doctors ÷ Active MRs."

        ),

        border=True,

    )
 
    
    
    # =========================================================

    # MONTHLY REVENUE TREND

    # =========================================================
    
    st.html(
        """
        <div class="section-header">
            <p class="section-title">
                Monthly Revenue Trend
            </p>
            <p class="section-caption">
                Net, traceable and untraced revenue movement over time
            </p>
        </div>
        """
    )
    
    
    if filtered_sales.empty:
    
        st.info(

            "No revenue data is available for the selected filters."

        )
    
    else:
    
        monthly_revenue = (

            filtered_sales

            .groupby(

                MONTH_COLUMN,

                as_index=False,

                observed=True,

            )

            .agg(

                NET_REVENUE=(

                    "NET_REVENUE",

                    "sum",

                ),

                TRACEABLE_REVENUE=(

                    "TRACEABLE_REVENUE",

                    "sum",

                ),

                UNTRACED_REVENUE=(

                    "UNTRACED_REVENUE",

                    "sum",

                ),

            )

            .sort_values(MONTH_COLUMN)

        )
    
        # =========================================================

        # MONTHLY REVENUE TREND - PROFESSIONAL ALTAIR CHART

        # =========================================================
        
        monthly_revenue_plot = monthly_revenue.melt(

            id_vars=[MONTH_COLUMN],

            value_vars=[

                "NET_REVENUE",

                "TRACEABLE_REVENUE",

                "UNTRACED_REVENUE",

            ],

            var_name="REVENUE_TYPE",

            value_name="REVENUE",

        )

        monthly_revenue_plot["REVENUE_CR"] = (

            monthly_revenue_plot["REVENUE"]

            /10_000_000

        )

        
        
        # ---------------------------------------------------------

        # FRIENDLY SERIES NAMES

        # ---------------------------------------------------------
        
        monthly_revenue_plot["REVENUE_TYPE"] = (

            monthly_revenue_plot["REVENUE_TYPE"]

            .replace(

                {

                    "NET_REVENUE": "Net Revenue",

                    "TRACEABLE_REVENUE": "Traceable Revenue",

                    "UNTRACED_REVENUE": "Untraced Revenue",

                }

            )

        )
        
        
        # ---------------------------------------------------------

        # FORMAT TOOLTIP VALUES USING YOUR format_currency()

        # ---------------------------------------------------------
        
        monthly_revenue_plot["REVENUE_DISPLAY"] = (

            monthly_revenue_plot["REVENUE"]

            .apply(

                lambda value:

                    f"₹{format_currency(value)}"

            )

        )
        
        
        # ---------------------------------------------------------

        # FORMAT MONTH FOR TOOLTIP

        # Example: Mar 2026

        # ---------------------------------------------------------
        
        monthly_revenue_plot["MONTH_DISPLAY"] = (

            pd.to_datetime(

                monthly_revenue_plot[

                    MONTH_COLUMN

                ]

            )

            .dt.strftime("%b %Y")

        )
        
        
        # =========================================================

        # CHART

        # =========================================================
        
        monthly_revenue_chart = (

            alt.Chart(

                monthly_revenue_plot

            )

            .mark_line(

                strokeWidth=2.5,

                point=alt.OverlayMarkDef(

                    size=55,

                    filled=True,

                ),

            )

            .encode(
        
                # -------------------------------------------------

                # X AXIS

                # Explicit month + year

                # -------------------------------------------------
        
                x=alt.X(

                    f"{MONTH_COLUMN}:T",

                    title="Month",
        
                    axis=alt.Axis(

                        format="%b '%y",

                        labelAngle=0,

                        labelOverlap=True,

                        tickCount="month",

                        grid=False,

                    ),

                ),
        
        
                # -------------------------------------------------

                # Y AXIS

                # FIX START AT ZERO

                # Prevents negative values during chart scaling

                # -------------------------------------------------
        
                y=alt.Y(

                    "REVENUE_CR:Q",

                    title="Revenue",
        
                    scale=alt.Scale(

                        zero=True,

                        domainMin=0,

                        nice=True,

                    ),
        
                    axis=alt.Axis(

                        format="~s",

                        labelExpr="datum.value + ' Cr'",

                        grid=True,

                    ),

                ),
        
        
                # -------------------------------------------------

                # SERIES

                # -------------------------------------------------
        
                color=alt.Color(

                    "REVENUE_TYPE:N",

                    title=None,
        
                    scale=alt.Scale(

                        domain=[

                            "Net Revenue",

                            "Traceable Revenue",

                            "Untraced Revenue",

                        ],
        
                        range=[

                            "#2563EB",

                            "#38BDF8",

                            "#F59E0B",

                        ],

                    ),

                ),
        
        
                # -------------------------------------------------

                # TOOLTIP

                # -------------------------------------------------
        
                tooltip=[

                    alt.Tooltip(

                        "MONTH_DISPLAY:N",

                        title="Month",

                    ),
        
                    alt.Tooltip(

                        "REVENUE_TYPE:N",

                        title="Revenue Type",

                    ),
        
                    alt.Tooltip(

                        "REVENUE_DISPLAY:N",

                        title="Revenue",

                    ),

                ],

            )

            .properties(

                height=360,

            )

            .interactive(

                bind_y=False

            )

        )
        
        
        st.altair_chart(

            monthly_revenue_chart,

            use_container_width=True,

        )
 
    
    
    # =========================================================

    # BRAND-WISE REVENUE

    # =========================================================
    
    st.html(
        """
        <div class="section-header">
            <p class="section-title">
                Top 15 Brands Revenue Composition
            </p>
            <p class="section-caption">
                Traceable and untraced revenue contribution by brand
            </p>
        </div>
        """
    )
    
    
    if filtered_sales.empty:
    
        st.info(

            "No brand performance data is available."

        )
    
    else:
    
        brand_performance = (

            filtered_sales

            .groupby(

                BRAND_COLUMN,

                as_index=False,

                observed=True,

            )

            .agg(

                NET_REVENUE=(

                    "NET_REVENUE",

                    "sum",

                ),

                TRACEABLE_REVENUE=(

                    "TRACEABLE_REVENUE",

                    "sum",

                ),

                UNTRACED_REVENUE=(

                    "UNTRACED_REVENUE",

                    "sum",

                ),

            )

            .sort_values(

                "NET_REVENUE",

                ascending=False,

            )

            .head(15)

        )
    
        # =========================================================

        # PREPARE VALUES

        # =========================================================
        
        brand_performance["TRACEABLE_CR"] = (

            brand_performance["TRACEABLE_REVENUE"]

            / 10_000_000

        )
        
        brand_performance["UNTRACED_CR"] = (

            brand_performance["UNTRACED_REVENUE"]

            / 10_000_000

        )
        
        brand_performance["TOTAL_CR"] = (

            brand_performance["NET_REVENUE"]

            / 10_000_000

        )
        
        brand_performance["TOTAL_DISPLAY"] = (

            brand_performance["NET_REVENUE"]

            .apply(

                lambda value:

                    f"₹{format_currency(value)}"

            )

        )
        
        
        # =========================================================

        # PREPARE STACKED CHART DATA

        # =========================================================
        
        brand_chart_data = (

            brand_performance[

                [

                    BRAND_COLUMN,

                    "TRACEABLE_CR",

                    "UNTRACED_CR",

                    "TOTAL_CR",

                    "TOTAL_DISPLAY",

                ]

            ]

            .melt(

                id_vars=[

                    BRAND_COLUMN,

                    "TOTAL_CR",

                    "TOTAL_DISPLAY",

                ],
        
                value_vars=[

                    "TRACEABLE_CR",

                    "UNTRACED_CR",

                ],
        
                var_name="REVENUE_TYPE",

                value_name="REVENUE_CR",

            )

        )
        
        brand_chart_data["REVENUE_TYPE"] = (

            brand_chart_data[

                "REVENUE_TYPE"

            ]

            .replace(

                {

                    "TRACEABLE_CR":

                        "Traceable Revenue",
        
                    "UNTRACED_CR":

                        "Untraced Revenue",

                }

            )

        )
        
        brand_chart_data["REVENUE_VALUE"] = (

            brand_chart_data["REVENUE_CR"]

            * 10_000_000

        )
        
        brand_chart_data["REVENUE_DISPLAY"] = (

            brand_chart_data["REVENUE_VALUE"]

            .apply(

                lambda value:

                    f"₹{format_currency(value)}"

            )

        )
        
        
        # =========================================================

        # STACKED BARS

        # =========================================================
        
        bars = (

            alt.Chart(

                brand_chart_data

            )

            .mark_bar()

            .encode(
        
                x=alt.X(

                    f"{BRAND_COLUMN}:N",

                    title="Brand",

                    sort=brand_performance[

                        BRAND_COLUMN

                    ].tolist(),
        
                    axis=alt.Axis(

                        labelAngle=-45,

                        labelLimit=120,

                        titlePadding=14,

                    ),

                ),
        
                y=alt.Y(

                    "REVENUE_CR:Q",

                    title="Revenue",

                    stack="zero",
        
                    scale=alt.Scale(

                        zero=True,

                        domainMin=0,

                        nice=True,

                    ),
        
                    axis=alt.Axis(

                        labelExpr=(

                            "datum.value == 0 "

                            "? '0' "

                            ": datum.value + ' Cr'"

                        ),

                        grid=True,

                        titlePadding=12,

                    ),

                ),
        
                color=alt.Color(

                    "REVENUE_TYPE:N",

                    title=None,
        
                    scale=alt.Scale(

                        domain=[

                            "Traceable Revenue",

                            "Untraced Revenue",

                        ],
        
                        range=[

                            "#2563EB",

                            "#60A5FA",

                        ],

                    ),

                ),
        
                tooltip=[

                    alt.Tooltip(

                        f"{BRAND_COLUMN}:N",

                        title="Brand",

                    ),
        
                    alt.Tooltip(

                        "REVENUE_TYPE:N",

                        title="Revenue Type",

                    ),
        
                    alt.Tooltip(

                        "REVENUE_DISPLAY:N",

                        title="Revenue",

                    ),
        
                    alt.Tooltip(

                        "TOTAL_DISPLAY:N",

                        title="Total Revenue",

                    ),

                ],

            )

        )
        
        
        # =========================================================

        # TOTAL LABELS ABOVE BAR

        # =========================================================
        
        total_labels = (

            alt.Chart(

                brand_performance

            )

            .mark_text(

                dy=-8,

                fontSize=11,

                fontWeight=700,

                color="#163A5F",

            )

            .encode(
        
                x=alt.X(

                    f"{BRAND_COLUMN}:N",

                    sort=brand_performance[

                        BRAND_COLUMN

                    ].tolist(),

                ),
        
                y=alt.Y(

                    "TOTAL_CR:Q"

                ),
        
                text=alt.Text(

                    "TOTAL_DISPLAY:N"

                ),

            )

        )
        
        
        # =========================================================

        # COMBINE

        # =========================================================
        
        brand_revenue_chart = (

            bars

            + total_labels

        ).properties(

            height=400

        )
        
        
        st.altair_chart(

            brand_revenue_chart,

            use_container_width=True,

        )
 
    
    
    # =========================================================

    # HQ PERFORMANCE TABLE

    # =========================================================
    
    st.html(
        """
        <div class="section-header">
            <p class="section-title">
                HQ Performance Overview
            </p>
            <p class="section-caption">
                Revenue and field-force activity comparison by HQ
            </p>
        </div>
        """
    )
    
    
    if filtered_sales.empty:
    
        st.info(

            "No HQ performance data is available."

        )
    
    else:
    
        hq_revenue = (

            filtered_sales

            .groupby(

                HQ_COLUMN,

                as_index=False,

                observed=True,

            )

            .agg(

                NET_REVENUE=(

                    "NET_REVENUE",

                    "sum",

                ),

                TRACEABLE_REVENUE=(

                    "TRACEABLE_REVENUE",

                    "sum",

                ),

                UNTRACED_REVENUE=(

                    "UNTRACED_REVENUE",

                    "sum",

                ),

            )

        )
    
        hq_mrs = (

            filtered_mr

            .groupby(

                HQ_COLUMN,

                as_index=False,

                observed=True,

            )

            .agg(

                ACTIVE_MRS=(

                    MR_COLUMN,

                    "nunique",

                )

            )

        )
    
        hq_doctors = (

            filtered_doctor

            .groupby(

                HQ_COLUMN,

                as_index=False,

                observed=True,

            )

            .agg(

                UNIQUE_DOCTORS=(

                    DOCTOR_COLUMN,

                    "nunique",

                )

            )

        )
    
        hq_visits = (

            filtered_visit

            .groupby(

                HQ_COLUMN,

                as_index=False,

                observed=True,

            )

            .agg(

                TOTAL_VISITS=(

                    VISIT_COLUMN,

                    "nunique",

                )

            )

        )
    
        hq_performance = (

            hq_revenue

            .merge(

                hq_mrs,

                on=HQ_COLUMN,

                how="left",

            )

            .merge(

                hq_doctors,

                on=HQ_COLUMN,

                how="left",

            )

            .merge(

                hq_visits,

                on=HQ_COLUMN,

                how="left",

            )

        )
    
        count_columns = [

            "ACTIVE_MRS",

            "UNIQUE_DOCTORS",

            "TOTAL_VISITS",

        ]
    
        hq_performance[

            count_columns

        ] = (

            hq_performance[

                count_columns

            ]

            .fillna(0)

            .astype(int)

        )
    
        hq_performance[

            "TRACEABLE_PERCENTAGE"

        ] = (

            hq_performance.apply(

                lambda row: safe_percentage(

                    row["TRACEABLE_REVENUE"],

                    row["NET_REVENUE"],

                ),

                axis=1,

            )

        )
    
        hq_performance = (

            hq_performance

            .sort_values(

                "NET_REVENUE",

                ascending=False,

            )

        )
    
        # =========================================================

        # TRUE TOTALS FROM FILTERED SOURCE DATA

        # =========================================================
        
        total_net_revenue = safe_sum(

            filtered_sales,

            "NET_REVENUE",

        )
        
        total_traceable_revenue = safe_sum(

            filtered_sales,

            "TRACEABLE_REVENUE",

        )
        
        total_untraced_revenue = safe_sum(

            filtered_sales,

            "UNTRACED_REVENUE",

        )
        
        
        # True unique MRs across complete filtered data

        total_active_mrs = (

            filtered_mr[

                MR_COLUMN

            ]

            .dropna()

            .nunique()

        )
        
        
        # True unique doctors across complete filtered data

        total_unique_doctors = (

            filtered_doctor[

                DOCTOR_COLUMN

            ]

            .dropna()

            .nunique()

        )
        
        
        # Total visits from complete filtered visit data

        total_visits = (

            filtered_visit[

                VISIT_COLUMN

            ]

            .dropna()

            .nunique()

        )
        
        
        # =========================================================

        # TRUE OVERALL TRACEABLE %

        # =========================================================
        
        total_traceable_percentage = safe_percentage(

            total_traceable_revenue,

            total_net_revenue,

        )
 
        total_row = pd.DataFrame(

            {

                HQ_COLUMN: [

                    "TOTAL"

                ],
        
                "NET_REVENUE": [

                    total_net_revenue

                ],
        
                "TRACEABLE_REVENUE": [

                    total_traceable_revenue

                ],
        
                "UNTRACED_REVENUE": [

                    total_untraced_revenue

                ],
        
                "ACTIVE_MRS": [

                    total_active_mrs

                ],
        
                "UNIQUE_DOCTORS": [

                    total_unique_doctors

                ],
        
                "TOTAL_VISITS": [

                    total_visits

                ],
        
                "TRACEABLE_PERCENTAGE": [

                    total_traceable_percentage

                ],

            }

        )
        
        
        hq_performance_display = pd.concat(

            [

                hq_performance,

                total_row,

            ],

            ignore_index=True,

        )
        
        
        # =========================================================

        # HQ PERFORMANCE TABLE

        # =========================================================
        
        st.dataframe(

            hq_performance_display,
        
            use_container_width=True,
        
            hide_index=True,
        
            column_config={
        
                HQ_COLUMN:

                    st.column_config.TextColumn(

                        "HQ",
        
                        help=(

                            "Standardised Head Quarter used to combine "

                            "sales and field-force activity."

                        ),

                    ),
        
        
                "NET_REVENUE":

                    st.column_config.NumberColumn(

                        "Net Revenue",
        
                        help=(

                            "Net sales revenue for the HQ after "

                            "returns and credit adjustments."

                        ),
        
                        format="₹ %.0f",

                    ),
        
        
                "TRACEABLE_REVENUE":

                    st.column_config.NumberColumn(

                        "Traceable Revenue",
        
                        help=(

                            "Portion of net revenue linked to field-force "

                            "activity through mapped HQ and brand coverage."

                        ),
        
                        format="₹ %.0f",

                    ),
        
        
                "UNTRACED_REVENUE":

                    st.column_config.NumberColumn(

                        "Untraced Revenue",
        
                        help=(

                            "Portion of net revenue that could not be linked "

                            "to corresponding field-force HQ and brand coverage."

                        ),
        
                        format="₹ %.0f",

                    ),
        
        
                "ACTIVE_MRS":

                    st.column_config.NumberColumn(

                        "Active MRs",
        
                        help=(

                            "Number of active field representatives "

                            "with recorded DCR activity for the HQ."

                        ),
        
                        format="%d",

                    ),
        
        
                "UNIQUE_DOCTORS":

                    st.column_config.NumberColumn(

                        "Unique Doctors",
        
                        help=(

                            "Number of distinct doctors covered by "

                            "field representatives in the HQ."

                        ),
        
                        format="%d",

                    ),
        
        
                "TOTAL_VISITS":

                    st.column_config.NumberColumn(

                        "Total Visits",
        
                        help=(

                            "Total doctor visits recorded by the "

                            "field force for the HQ."

                        ),
        
                        format="%d",

                    ),
        
        
                "TRACEABLE_PERCENTAGE":

                    st.column_config.NumberColumn(

                        "Traceable %",
        
                        help=(

                            "Percentage of HQ net revenue that is traceable "

                            "to field-force activity. Calculated as "

                            "Traceable Revenue ÷ Net Revenue × 100."

                        ),
        
                        format="%.2f%%",

                    ),

            },

        )
       
 
    # =========================================================

    # HQ SALES DRILL-DOWN

    # =========================================================
    
    st.html(

        """
    <div class="section-header">
    <p class="section-title">

                HQ Sales Drill-down
    </p>
    <p class="section-caption">

                Sales office and HQ-code breakdown within the selected standard HQ
    </p>
    </div>

        """

    )
    
    # ---------------------------------------------------------

    # STANDARD HQ SELECTION

    # ---------------------------------------------------------
    
    drilldown_hq_options = (

        filtered_sales[HQ_COLUMN]

        .dropna()

        .astype("string")

        .sort_values()

        .unique()

        .tolist()

    )
    
    
    selected_drilldown_hq = st.selectbox(

        "Select HQ",

        options=drilldown_hq_options,

        key="hq_sales_drilldown",

    )
    
    # ---------------------------------------------------------

    # SALES OFFICE BREAKDOWN

    # ---------------------------------------------------------
    
    hq_sales_drilldown = (

        filtered_sales.loc[

            filtered_sales[

                HQ_COLUMN

            ].eq(selected_drilldown_hq)

        ]

        .groupby(

            [

                "SALES_HQ",

                "HQ_CODE",

            ],

            as_index=False,

            observed=True,

            dropna=False,

        )

        .agg(

            PRIMARY_SALES=(

                "NET_REVENUE",

                "sum",

            ),
    
            GROSS_REVENUE=(

                "GROSS_REVENUE",

                "sum",

            ),
    
            RETURN_AMOUNT=(

                "RETURN_AMOUNT",

                "sum",

            ),

        )

        .sort_values(

            "PRIMARY_SALES",

            ascending=False,

        )

    )
    
    hq_total_sales = (

        hq_sales_drilldown[

            "PRIMARY_SALES"

        ].sum()

    )
    
    
    hq_sales_drilldown[

        "SALES_SHARE"

    ] = (

        hq_sales_drilldown[

            "PRIMARY_SALES"

        ]

        .div(

            hq_total_sales

            if hq_total_sales != 0

            else 1

        )

        .mul(100)

    )
    
    st.dataframe(

        hq_sales_drilldown,

        use_container_width=True,

        hide_index=True,
    
        column_config={
    
            "SALES_HQ":

                st.column_config.TextColumn(

                    "Sales HQ"

                ),
    
            "HQ_CODE":

                st.column_config.TextColumn(

                    "HQ Code"

                ),
    
            "PRIMARY_SALES":

                st.column_config.NumberColumn(

                    "Primary Sales",

                    format="₹ %.0f",

                ),
    
            "GROSS_REVENUE":

                st.column_config.NumberColumn(

                    "Gross Revenue",

                    format="₹ %.0f",

                ),
    
            "RETURN_AMOUNT":

                st.column_config.NumberColumn(

                    "Returns",

                    format="₹ %.0f",

                ),
    
            "SALES_SHARE":

                st.column_config.NumberColumn(

                    "Share",

                    format="%.1f%%",

                ),

        },

    )
 
    
    # ============================================================

    # QUARTERLY SALES TREND

    # ============================================================
    
    quarterly_sales_trend = (

        filtered_sales.groupby(

            [

                "FINANCIAL_YEAR",

                "FINANCIAL_QUARTER",

            ],

            as_index=False,

            dropna=False,

        )

        .agg(

            PRIMARY_SALES=(

                "NET_REVENUE",

                "sum",

            )

        )

    )
    
    
    # Quarter sorting

    quarter_order = {

        "Q1": 1,

        "Q2": 2,

        "Q3": 3,

        "Q4": 4,

    }
    
    quarterly_sales_trend["QUARTER_NUMBER"] = (

        quarterly_sales_trend["FINANCIAL_QUARTER"]

        .map(quarter_order)

    )
    
    
    # Create a complete quarter label

    quarterly_sales_trend["QUARTER_LABEL"] = (

        quarterly_sales_trend["FINANCIAL_QUARTER"]

    )
    
    
    # Sort chronologically

    quarterly_sales_trend = (

        quarterly_sales_trend.sort_values(

            [

                "FINANCIAL_YEAR",

                "QUARTER_NUMBER",

            ]

        )

        .reset_index(drop=True)

    )
    
    
    # Values in crores

    quarterly_sales_trend["SALES_CR"] = (

        quarterly_sales_trend["PRIMARY_SALES"] / 1_00_00_000

    )
    
    quarterly_sales_trend["VALUE_LABEL"] = (

        quarterly_sales_trend["SALES_CR"]

        .map(lambda value: f"₹{value:,.2f} Cr")

    )
    
    
    # ============================================================

    # DISPLAY CHART

    # ============================================================
    st.html(
        """
        <div class="section-header">
            <p class="section-title">
                Quarterly Sales Trend
            </p>
            <p class="section-caption">
                Revenue and field-force activity comparison by HQ
            </p>
        </div>
        """
    )
    
    fig = px.line(

        quarterly_sales_trend,

        x="QUARTER_LABEL",

        y="SALES_CR",

        markers=True,

        text="VALUE_LABEL",

        custom_data=[

            "PRIMARY_SALES",

        ],

    )
    
    fig.update_traces(

        mode="lines+markers+text",

        textposition="top center",

        line=dict(width=3),

        marker=dict(size=10),

        hovertemplate=(

            "<b>%{x}</b><br>"

            "Primary Sales: ₹%{customdata[0]:,.0f}"

            "<extra></extra>"

        ),

    )
    
    fig.update_layout(

        xaxis_title="Financial Quarter",

        yaxis_title="Primary Sales (₹ Cr)",

        hovermode="x unified",

        showlegend=False,

        margin=dict(

            l=20,

            r=20,

            t=40,

            b=20,

        ),

    )
    
    fig.update_yaxes(

        tickprefix="₹",

        ticksuffix=" Cr",

        rangemode="tozero",

    )
    
    st.plotly_chart(

        fig,

        use_container_width=True,

    )
    pass

## Doctor Details

elif selected_view == "Doctor Coverage":
       
 
    st.html(

        """
    <div class="section-header">
    <p class="section-title">

                    Doctor Coverage Intelligence
    </p>
    <p class="section-caption">

                    Doctor reach, field activity and primary sales analysis
    </p>
    </div>

            """

        )
    
    
        # =====================================================

        # KPI CALCULATIONS

        # =====================================================
    
    unique_doctors_coverage = (

        filtered_doctor[

            DOCTOR_COLUMN

        ]

        .dropna()

        .nunique()

    )

    total_visits_coverage = (

        filtered_visit[

            VISIT_COLUMN

        ]

        .dropna()

        .nunique()

    )

    active_mrs_coverage = (

        filtered_mr[

            MR_COLUMN

        ]

        .dropna()

        .nunique()

    )

    primary_sales_coverage = safe_sum(

        filtered_sales,

        "NET_REVENUE",

    )

    visits_per_doctor = (

        total_visits_coverage

        / unique_doctors_coverage

        if unique_doctors_coverage > 0

        else 0

    )


    # =====================================================

    # KPI CARDS

    # =====================================================

    doctor_kpis = st.columns(5)

    doctor_kpis[0].metric(

        label="Unique Doctors",

        value=f"{format_indian_number(unique_doctors)}",

        help=(

            "Number of distinct doctors covered by the field force "

            "within the selected filters and period."

        ),

        border=True,

    )
    
    doctor_kpis[1].metric(

        label="Total Visits",

        value=f"{format_indian_number(total_visits)}",

        help=(

            "Total doctor visits recorded by field representatives "

            "within the selected filters and period."

        ),

        border=True,

    )
    
    doctor_kpis[2].metric(

        label="Active MRs",

        value=f"{format_indian_number(active_mrs)}",

        help=(

            "Number of unique Medical Representatives with recorded "

            "field activity within the selected filters and period."

        ),

        border=True,

    )
    
    doctor_kpis[3].metric(

        label="Primary Sales",

        value=f"₹{format_currency(primary_sales_coverage)}",

        help=(

            "Total primary sales associated with the selected geography "

            "and period, shown alongside doctor coverage activity."

        ),

        border=True,

    )
    
    doctor_kpis[4].metric(

        label="Visits / Doctor",

        value=f"{visits_per_doctor:,.2f}",

        help=(

            "Average number of visits per covered doctor. "

            "Calculated as Total Visits ÷ Unique Doctors."

        ),

        border=True,

    )
    
    # =====================================================

    # SPECIALISATION COVERAGE

    # =====================================================

    st.html(

        """
    <div class="section-header">
    <p class="section-title">

                    Unique Doctors by Specialisation
    </p>
    <p class="section-caption">

                    Doctor coverage distribution across DCR categories
    </p>
    </div>

            """

        )
    
    # =========================================================
    # SPECIALISATION + GRADE PERFORMANCE
    # =========================================================
    
    SPECIALISATION_COLUMN = "SPECIALISATION_KEY"
    GRADE_COLUMN = "GRADE"
    
    # ---------------------------------------------------------
    # 1. DOCTOR LOOKUP
    # One doctor + HQ + specialisation + grade
    # ---------------------------------------------------------
    
    doctor_lookup = (
        filtered_doctor[
            [
                HQ_COLUMN,
                DOCTOR_COLUMN,
                SPECIALISATION_COLUMN,
                GRADE_COLUMN,
            ]
        ]
        .dropna(
            subset=[
                HQ_COLUMN,
                DOCTOR_COLUMN,
                SPECIALISATION_COLUMN,
            ]
        )
        .drop_duplicates()
    )
    
    
    # ---------------------------------------------------------
    # 2. UNIQUE DOCTORS BY SPECIALISATION + GRADE
    # ---------------------------------------------------------
    
    specialisation_grade = (
        doctor_lookup
        .groupby(
            [
                SPECIALISATION_COLUMN,
                GRADE_COLUMN,
            ],
            as_index=False,
            observed=True,
        )
        .agg(
            UNIQUE_DOCTORS=(
                DOCTOR_COLUMN,
                "nunique",
            )
        )
    )
    
    
    # ---------------------------------------------------------
    # 3. PIVOT GRADES INTO COLUMNS
    #
    # Example:
    # CORE | FOUR V | GENERAL | VIP | VVIP
    # ---------------------------------------------------------
    
    grade_pivot = (
        specialisation_grade
        .pivot_table(
            index=SPECIALISATION_COLUMN,
            columns=GRADE_COLUMN,
            values="UNIQUE_DOCTORS",
            aggfunc="sum",
            fill_value=0,
        )
        .reset_index()
    )
    
    
    # Remove pivot column name
    grade_pivot.columns.name = None
    
    
    # ---------------------------------------------------------
    # 4. TOTAL UNIQUE DOCTORS PER SPECIALISATION
    # ---------------------------------------------------------
    
    specialisation_doctors = (
        doctor_lookup
        .groupby(
            SPECIALISATION_COLUMN,
            as_index=False,
            observed=True,
        )
        .agg(
            UNIQUE_DOCTORS=(
                DOCTOR_COLUMN,
                "nunique",
            )
        )
    )
    
    
    # =========================================================
    # 5. VISITS BY SPECIALISATION
    # =========================================================
    
    # Doctor → specialisation lookup
    doctor_specialisation_lookup = (
        doctor_lookup[
            [
                DOCTOR_COLUMN,
                SPECIALISATION_COLUMN,
            ]
        ]
        .drop_duplicates(
            subset=[
                DOCTOR_COLUMN,
                SPECIALISATION_COLUMN,
            ]
        )
    )
    
    
    visit_with_specialisation = (
        filtered_visit
        .merge(
            doctor_specialisation_lookup,
            on=DOCTOR_COLUMN,
            how="left",
        )
    )
    
    
    specialisation_visits = (
        visit_with_specialisation
        .dropna(
            subset=[
                SPECIALISATION_COLUMN
            ]
        )
        .groupby(
            SPECIALISATION_COLUMN,
            as_index=False,
            observed=True,
        )
        .agg(
            VISITS=(
                VISIT_COLUMN,
                "nunique",
            )
        )
    )
    
    
    # =========================================================
    # 6. PRIMARY SALES ALLOCATION
    #
    # Sales does NOT contain specialisation.
    # Therefore allocate HQ sales based on doctor share
    # within each HQ.
    # =========================================================
    
    
    # ---------------------------------------------------------
    # Doctors per HQ + specialisation
    # ---------------------------------------------------------
    
    hq_specialisation_doctors = (
        doctor_lookup
        .groupby(
            [
                HQ_COLUMN,
                SPECIALISATION_COLUMN,
            ],
            as_index=False,
            observed=True,
        )
        .agg(
            SPECIALISATION_DOCTORS=(
                DOCTOR_COLUMN,
                "nunique",
            )
        )
    )
    
    
    # ---------------------------------------------------------
    # Total doctors per HQ
    # ---------------------------------------------------------
    
    hq_total_doctors = (
        doctor_lookup
        .groupby(
            HQ_COLUMN,
            as_index=False,
            observed=True,
        )
        .agg(
            HQ_TOTAL_DOCTORS=(
                DOCTOR_COLUMN,
                "nunique",
            )
        )
    )
    
    
    hq_specialisation_doctors = (
        hq_specialisation_doctors
        .merge(
            hq_total_doctors,
            on=HQ_COLUMN,
            how="left",
        )
    )
    
    
    # ---------------------------------------------------------
    # Doctor share inside HQ
    # ---------------------------------------------------------
    
    hq_specialisation_doctors[
        "DOCTOR_SHARE"
    ] = (
        hq_specialisation_doctors[
            "SPECIALISATION_DOCTORS"
        ]
        .div(
            hq_specialisation_doctors[
                "HQ_TOTAL_DOCTORS"
            ]
            .replace(0, pd.NA)
        )
        .fillna(0)
    )
    
    
    # ---------------------------------------------------------
    # Primary sales per HQ
    # ---------------------------------------------------------
    
    hq_sales = (
        filtered_sales
        .groupby(
            HQ_COLUMN,
            as_index=False,
            observed=True,
        )
        .agg(
            HQ_PRIMARY_SALES=(
                "NET_REVENUE",
                "sum",
            )
        )
    )
    
    
    # ---------------------------------------------------------
    # Merge and allocate
    # ---------------------------------------------------------
    
    hq_specialisation_sales = (
        hq_specialisation_doctors
        .merge(
            hq_sales,
            on=HQ_COLUMN,
            how="left",
        )
    )
    
    
    hq_specialisation_sales[
        "PRIMARY_SALES"
    ] = (
        hq_specialisation_sales[
            "HQ_PRIMARY_SALES"
        ]
        .fillna(0)
        *
        hq_specialisation_sales[
            "DOCTOR_SHARE"
        ]
    )
    
    
    # ---------------------------------------------------------
    # Sum allocated sales by specialisation
    # ---------------------------------------------------------
    
    specialisation_sales = (
        hq_specialisation_sales
        .groupby(
            SPECIALISATION_COLUMN,
            as_index=False,
            observed=True,
        )
        .agg(
            PRIMARY_SALES=(
                "PRIMARY_SALES",
                "sum",
            )
        )
    )
    
    
    # =========================================================
    # 7. FINAL DATAFRAME
    # =========================================================
    
    specialisation_performance = (
        grade_pivot
    
        .merge(
            specialisation_doctors,
            on=SPECIALISATION_COLUMN,
            how="outer",
        )
    
        .merge(
            specialisation_visits,
            on=SPECIALISATION_COLUMN,
            how="outer",
        )
    
        .merge(
            specialisation_sales,
            on=SPECIALISATION_COLUMN,
            how="outer",
        )
    )

    # =========================================================

    # 8. SPECIALISATION SHARE

    # =========================================================
    
    total_unique_doctors = (

        specialisation_performance[

            "UNIQUE_DOCTORS"

        ].sum()

    )
    
    
    specialisation_performance[

        "SHARE_PERCENTAGE"

    ] = (

        specialisation_performance[

            "UNIQUE_DOCTORS"

        ]

        .div(

            total_unique_doctors

            if total_unique_doctors != 0

            else 1

        )

        .mul(100)

    )
    
    
    
    # ---------------------------------------------------------
    # Fill numeric blanks
    # ---------------------------------------------------------
    
    numeric_columns = (
        specialisation_performance
        .select_dtypes(
            include="number"
        )
        .columns
    )
    
    specialisation_performance[
        numeric_columns
    ] = (
        specialisation_performance[
            numeric_columns
        ]
        .fillna(0)
    )
    
    
    # ---------------------------------------------------------
    # Ensure doctor/visit counts 
    # ---------------------------------------------------------
    
    count_columns = [
        column
        for column in specialisation_performance.columns
        if column not in [
            SPECIALISATION_COLUMN,
            "PRIMARY_SALES",
            "SHARE_PERCENTAGE",
        ]
    ]
    
    specialisation_performance[
        count_columns
    ] = (
        specialisation_performance[
            count_columns
        ]
        .astype(int)
    )
    
    
    # ---------------------------------------------------------
    # Sort by doctor coverage
    # ---------------------------------------------------------
    
    specialisation_performance = (
        specialisation_performance
        .sort_values(
            "UNIQUE_DOCTORS",
            ascending=False,
        )
        .reset_index(drop=True)
    )
    # =========================================================
    # TOTAL ROW
    # =========================================================
    
    # Grade columns created dynamically by grade_pivot
    grade_columns = [
        column
        for column in grade_pivot.columns
        if column != SPECIALISATION_COLUMN
    ]
    
    
    # ---------------------------------------------------------
    # True total unique doctors
    # Do not simply sum specialisation rows
    # ---------------------------------------------------------
    
    total_doctors_specialisation = (
        doctor_lookup[
            DOCTOR_COLUMN
        ]
        .nunique()
    )
    
    
    # ---------------------------------------------------------
    # True total visits
    # ---------------------------------------------------------
    
    total_visits_specialisation = (
        visit_with_specialisation[
            VISIT_COLUMN
        ]
        .nunique()
    )
    
    
    # ---------------------------------------------------------
    # Total allocated primary sales
    # ---------------------------------------------------------
    
    total_sales_specialisation = (
        specialisation_performance[
            "PRIMARY_SALES"
        ]
        .sum()
    )
    
    
    # ---------------------------------------------------------
    # Build total row
    # ---------------------------------------------------------
    
    total_row_data = {
        SPECIALISATION_COLUMN: "TOTAL",
        "UNIQUE_DOCTORS": total_doctors_specialisation,
        "VISITS": total_visits_specialisation,
        "PRIMARY_SALES": total_sales_specialisation,
        "SHARE_PERCENTAGE": 100.0 if total_doctors_specialisation > 0 else 0.0,
    }
    
    
    # ---------------------------------------------------------
    # Grade totals
    # Uses actual unique doctors from doctor_lookup
    # ---------------------------------------------------------
    
    for grade_column in grade_columns:
    
        total_row_data[
            grade_column
        ] = (
            doctor_lookup.loc[
                doctor_lookup[
                    GRADE_COLUMN
                ].eq(
                    grade_column
                ),
                DOCTOR_COLUMN,
            ]
            .nunique()
        )
    
    
    specialisation_total_row = pd.DataFrame(
        [
            total_row_data
        ]
    )
    
    
    # ---------------------------------------------------------
    # Append TOTAL to bottom
    # ---------------------------------------------------------
    
    specialisation_performance_display = pd.concat(
        [
            specialisation_performance,
            specialisation_total_row,
        ],
        ignore_index=True,
    )
    
    
    # =========================================================
    # COLUMN CONFIG + TOOLTIPS
    # =========================================================
    
    specialisation_column_config = {
    
        SPECIALISATION_COLUMN:
            st.column_config.TextColumn(
                "Specialisation",
                help=(
                    "Standardised doctor specialisation used "
                    "for doctor coverage analysis."
                ),
            ),
    
    
        "UNIQUE_DOCTORS":
            st.column_config.NumberColumn(
                "Unique Doctors",
                help=(
                    "Number of distinct doctors covered within "
                    "this specialisation."
                ),
                format="%d",
            ),
    
    
        "VISITS":
            st.column_config.NumberColumn(
                "Visits",
                help=(
                    "Total field-force visits recorded for doctors "
                    "within this specialisation."
                ),
                format="%d",
            ),
    
    
        "PRIMARY_SALES":
            st.column_config.NumberColumn(
                "Primary Sales",
                help=(
                    "Primary sales allocated to this specialisation "
                    "based on its doctor share within each HQ."
                ),
                format="₹ %.0f",
            ),
    
    
        "SHARE_PERCENTAGE":
            st.column_config.NumberColumn(
                "Doctor's Share %",
                help=(
                    "Percentage contribution of this specialisation "
                    "to total covered doctors."
                ),
                format="%.1f%%",
            ),
    }
    
    
    # =========================================================
    # ADD DYNAMIC TOOLTIPS FOR ALL GRADE COLUMNS
    # CORE, FOUR V, GENERAL (B), VIP (A), VVIP (A+), etc.
    # =========================================================
    
    for grade_column in grade_columns:
    
        specialisation_column_config[
            grade_column
        ] = st.column_config.NumberColumn(
            grade_column,
    
            help=(
                f"Number of unique doctors classified as "
                f"{grade_column} within this specialisation."
            ),
    
            format="%d",
        )
    
    
    # =========================================================
    # DISPLAY
    # =========================================================
    
    st.dataframe(
        specialisation_performance_display,
    
        use_container_width=True,
    
        hide_index=True,
    
        column_config=specialisation_column_config,
    )

    # =========================================================
    # DOCTOR GRADE MIX
    # =========================================================
    st.html(

        """
    <div class="section-header">
    <p class="section-title">

                    Doctor Grade Mix
    </p>
    <p class="section-caption">

                    Distribution of unique doctors across priority grades
    </p>
    </div>

            """

        )
    grade_mix = (
        filtered_doctor
        .dropna(
            subset=[
                "GRADE",
                DOCTOR_COLUMN,
            ]
        )
        .groupby(
            "GRADE",
            as_index=False,
            observed=True,
        )
        .agg(
            UNIQUE_DOCTORS=(
                DOCTOR_COLUMN,
                "nunique",
            )
        )
    )
    
    
    # ---------------------------------------------------------
    # Calculate share
    # ---------------------------------------------------------
    
    total_grade_doctors = (
        grade_mix["UNIQUE_DOCTORS"].sum()
    )
    
    grade_mix["SHARE"] = (
        grade_mix["UNIQUE_DOCTORS"]
        .div(
            total_grade_doctors
            if total_grade_doctors > 0
            else 1
        )
        .mul(100)
    )
    
    
    # =========================================================
    # DONUT CHART
    # =========================================================
    
    if grade_mix.empty:
    
        st.info(
            "No doctor grade data is available "
            "for the selected filters."
        )
    
    else:
    
        fig_grade_mix = px.pie(
            grade_mix,
            names="GRADE",
            values="UNIQUE_DOCTORS",
            hole=0.55,
            custom_data=[
                "SHARE",
            ],
        )
    
    
        fig_grade_mix.update_traces(
    
            textposition="outside",
    
            texttemplate=(
                "%{label}<br>"
                "%{customdata[0]:.1f}%"
            ),
    
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Unique Doctors: %{value:,}<br>"
                "Share: %{customdata[0]:.1f}%"
                "<extra></extra>"
            ),
        )
    
    
        fig_grade_mix.update_layout(
    
            legend_title_text="Grade",
    
            margin=dict(
                l=30,
                r=30,
                t=70,
                b=80,
            ),
    
            height=430,
        )
    
    
        st.plotly_chart(
            fig_grade_mix,
            use_container_width=True,
        )
 

    # =========================================================
    # HQ BASED DOCTOR COVERAGE
    # =========================================================
    
    st.html(

        """
    <div class="section-header">
    <p class="section-title">

                    Doctors and Sales by HQ
    </p>
    <p class="section-caption">

                    Doctor coverage distribution across DCR categories
    </p>
    </div>

            """

        )
    
    # ---------------------------------------------------------
    # 1. DOCTORS + VISITS + ACTIVE MRs BY HQ
    # ---------------------------------------------------------
    
    hq_activity = (
        filtered_visit
        .dropna(
            subset=[
                HQ_COLUMN,
            ]
        )
        .groupby(
            HQ_COLUMN,
            as_index=False,
            observed=True,
        )
        .agg(
            DOCTORS_COVERED=(
                DOCTOR_COLUMN,
                "nunique",
            ),
    
            VISITS=(
                VISIT_COLUMN,
                "nunique",
            ),
    
            ACTIVE_MRS=(
                MR_COLUMN,
                "nunique",
            ),
        )
    )
    
    
    # =========================================================
    # 2. PRIMARY SALES BY HQ
    # =========================================================
    
    hq_sales = (
        filtered_sales
        .dropna(
            subset=[
                HQ_COLUMN,
            ]
        )
        .groupby(
            HQ_COLUMN,
            as_index=False,
            observed=True,
        )
        .agg(
            PRIMARY_SALES=(
                "NET_REVENUE",
                "sum",
            )
        )
    )
    
    
    # =========================================================
    # 3. MERGE ACTIVITY + SALES
    # =========================================================
    
    hq_doctor_coverage = (
        hq_activity
        .merge(
            hq_sales,
            on=HQ_COLUMN,
            how="outer",
        )
    )
    
    
    # =========================================================
    # 4. CLEAN NULL VALUES
    # =========================================================
    
    hq_doctor_coverage[
        [
            "DOCTORS_COVERED",
            "VISITS",
            "ACTIVE_MRS",
        ]
    ] = (
        hq_doctor_coverage[
            [
                "DOCTORS_COVERED",
                "VISITS",
                "ACTIVE_MRS",
            ]
        ]
        .fillna(0)
        .astype(int)
    )
    
    
    hq_doctor_coverage[
        "PRIMARY_SALES"
    ] = (
        hq_doctor_coverage[
            "PRIMARY_SALES"
        ]
        .fillna(0)
    )
    
    
    # =========================================================
    # 5. PRIMARY SALES SHARE
    # =========================================================
    
    total_hq_sales = (
        hq_doctor_coverage[
            "PRIMARY_SALES"
        ]
        .sum()
    )
    
    
    hq_doctor_coverage[
        "SALES_SHARE"
    ] = (
        hq_doctor_coverage[
            "PRIMARY_SALES"
        ]
        .div(
            total_hq_sales
            if total_hq_sales != 0
            else 1
        )
        * 100
    )
    
    
    # =========================================================
    # 6. VISITS PER DOCTOR
    # =========================================================
    
    hq_doctor_coverage[
        "VISITS_PER_DOCTOR"
    ] = (
        hq_doctor_coverage[
            "VISITS"
        ]
        .div(
            hq_doctor_coverage[
                "DOCTORS_COVERED"
            ]
            .replace(
                0,
                pd.NA,
            )
        )
        .fillna(0)
    )
    
    
    # =========================================================
    # 7. DOCTORS PER MR
    # =========================================================
    
    hq_doctor_coverage[
        "DOCTORS_PER_MR"
    ] = (
        hq_doctor_coverage[
            "DOCTORS_COVERED"
        ]
        .div(
            hq_doctor_coverage[
                "ACTIVE_MRS"
            ]
            .replace(
                0,
                pd.NA,
            )
        )
        .fillna(0)
    )
    
    
    # =========================================================
    # 8. SALES PER DOCTOR
    # =========================================================
    
    hq_doctor_coverage[
        "SALES_PER_DOCTOR"
    ] = (
        hq_doctor_coverage[
            "PRIMARY_SALES"
        ]
        .div(
            hq_doctor_coverage[
                "DOCTORS_COVERED"
            ]
            .replace(
                0,
                pd.NA,
            )
        )
        .fillna(0)
    )
    
    
    # =========================================================
    # 9. SORT
    # =========================================================
    
    hq_doctor_coverage = (
        hq_doctor_coverage
        .sort_values(
            "PRIMARY_SALES",
            ascending=False,
        )
        .reset_index(drop=True)
    )
    
    
    # =========================================================

    # 10. TOTAL ROW

    # =========================================================
    
    # True unique doctors across the filtered dataset

    total_hq_doctors = (

        filtered_doctor[

            DOCTOR_COLUMN

        ]

        .nunique()

    )
    
    # True unique visits across the filtered dataset

    total_hq_visits = (

        filtered_visit[

            VISIT_COLUMN

        ]

        .nunique()

    )
    
    # True unique active MRs across the filtered dataset

    total_hq_mrs = (

        filtered_visit[

            MR_COLUMN

        ]

        .nunique()

    )
    
    # Total primary sales

    total_hq_primary_sales = (

        hq_doctor_coverage[

            "PRIMARY_SALES"

        ]

        .sum()

    )
    
    # Overall sales share

    total_hq_sales_share = (

        100.0

        if total_hq_primary_sales != 0

        else 0.0

    )
    
    # Overall visits per doctor

    total_hq_visits_per_doctor = (

        total_hq_visits

        / total_hq_doctors

        if total_hq_doctors != 0

        else 0

    )
    
    # Overall doctors per MR

    total_hq_doctors_per_mr = (

        total_hq_doctors

        / total_hq_mrs

        if total_hq_mrs != 0

        else 0

    )
    
    # Overall sales per doctor

    total_hq_sales_per_doctor = (

        total_hq_primary_sales

        / total_hq_doctors

        if total_hq_doctors != 0

        else 0

    )
    
    
    hq_doctor_total_row = pd.DataFrame(

        [

            {

                HQ_COLUMN: "TOTAL",
    
                "DOCTORS_COVERED":

                    total_hq_doctors,
    
                "PRIMARY_SALES":

                    total_hq_primary_sales,
    
                "VISITS":

                    total_hq_visits,
    
                "ACTIVE_MRS":

                    total_hq_mrs,
    
                "SALES_SHARE":

                    total_hq_sales_share,
    
                "VISITS_PER_DOCTOR":

                    total_hq_visits_per_doctor,
    
                "DOCTORS_PER_MR":

                    total_hq_doctors_per_mr,
    
                "SALES_PER_DOCTOR":

                    total_hq_sales_per_doctor,

            }

        ]

    )
    
    
    # =========================================================

    # APPEND TOTAL AT BOTTOM

    # =========================================================
    
    hq_doctor_coverage_display = pd.concat(

        [

            hq_doctor_coverage,

            hq_doctor_total_row,

        ],

        ignore_index=True,

    )
    
    
    # =========================================================

    # COLUMN CONFIG + TOOLTIPS

    # =========================================================
    
    hq_doctor_column_config = {
    
        HQ_COLUMN:

            st.column_config.TextColumn(

                "HQ",

                help=(

                    "Standardised HQ used to compare doctor coverage, "

                    "field-force activity and primary sales."

                ),

            ),
    
    
        "DOCTORS_COVERED":

            st.column_config.NumberColumn(

                "Doctors Covered",

                help=(

                    "Number of distinct doctors covered by the field force "

                    "within this HQ."

                ),

                format="%d",

            ),
    
    
        "PRIMARY_SALES":

            st.column_config.NumberColumn(

                "Primary Sales",

                help=(

                    "Total primary sales recorded for this HQ "

                    "within the selected filters and period."

                ),

                format="₹ %.0f",

            ),
    
    
        "VISITS":

            st.column_config.NumberColumn(

                "Visits",

                help=(

                    "Total unique doctor visits recorded by the field force "

                    "within this HQ."

                ),

                format="%d",

            ),
    
    
        "ACTIVE_MRS":

            st.column_config.NumberColumn(

                "Active MRs",

                help=(

                    "Number of unique Medical Representatives with "

                    "recorded field activity in this HQ."

                ),

                format="%d",

            ),
    
    
        "SALES_SHARE":

            st.column_config.NumberColumn(

                "Sales Share",

                help=(

                    "Percentage contribution of this HQ's primary sales "

                    "to total primary sales under the selected filters."

                ),

                format="%.1f%%",

            ),
    
    
        "VISITS_PER_DOCTOR":

            st.column_config.NumberColumn(

                "Visits / Doctor",

                help=(

                    "Average number of visits per covered doctor in the HQ. "

                    "Calculated as Visits ÷ Doctors Covered."

                ),

                format="%.2f",

            ),
    
    
        "DOCTORS_PER_MR":

            st.column_config.NumberColumn(

                "Doctors / MR",

                help=(

                    "Average number of covered doctors per active MR in the HQ. "

                    "Calculated as Doctors Covered ÷ Active MRs."

                ),

                format="%.2f",

            ),
    
    
        "SALES_PER_DOCTOR":

            st.column_config.NumberColumn(

                "Sales / Doctor",

                help=(

                    "Average HQ primary sales per covered doctor. "

                    "Calculated as Primary Sales ÷ Doctors Covered. "

                    "This is an HQ-level association, not doctor-attributed sales."

                ),

                format="₹ %.0f",

            ),

    }
    
    
    # =========================================================

    # DISPLAY

    # =========================================================
    
    st.dataframe(

        hq_doctor_coverage_display[

            [

                HQ_COLUMN,

                "DOCTORS_COVERED",

                "PRIMARY_SALES",

                "VISITS",

                "ACTIVE_MRS",

                "SALES_SHARE",

                "VISITS_PER_DOCTOR",

                "DOCTORS_PER_MR",

                "SALES_PER_DOCTOR",

            ]

        ],
    
        use_container_width=True,

        hide_index=True,
    
        column_config=hq_doctor_column_config,

    )
    
    # =========================================================

    # DOCTOR-LEVEL DETAILING & ASSOCIATED SALES

    # =========================================================
    
    st.html(

        """
    <div class="section-header">
    <p class="section-title">

                Doctor-Level Detailing & Sales
    </p>
    <p class="section-caption">

                Doctor visits, brand detailing and associated HQ sales

                for the selected period
    </p>
    </div>

        """

    )
    
    # =========================================================
    # 1. LOAD DETAIL SECTION
    # =========================================================
    
    show_doctor_detail = st.toggle(
        "Load Doctor-Level Details",
        value=False,
        key="load_doctor_detail",
    )
    
    
    if show_doctor_detail:
    
        # =====================================================
        # 2. DOCTOR SEARCH / SELECTION
        # =====================================================
    
        doctor_options = (
            filtered_doctor[
                [
                    DOCTOR_COLUMN,
                    "DOCTOR_NAME",
                ]
            ]
            .dropna(
                subset=[
                    DOCTOR_COLUMN,
                    "DOCTOR_NAME",
                ]
            )
            .drop_duplicates()
            .sort_values(
                "DOCTOR_NAME"
            )
        )
    
    
        # Create friendly display:
        # Doctor Name | Doctor Code
        doctor_options[
            "DOCTOR_DISPLAY"
        ] = (
            doctor_options[
                "DOCTOR_NAME"
            ].astype("string")
            + " | "
            + doctor_options[
                DOCTOR_COLUMN
            ].astype("string")
        )
    
    
        selected_doctor_display = st.selectbox(
            "Search Doctor",
            options=[
                None
            ]
            + doctor_options[
                "DOCTOR_DISPLAY"
            ].tolist(),
            index=0,
            placeholder="Type or select a doctor...",
            key="doctor_detail_search",
        )
    
    
        # =====================================================
        # 3. ONLY RUN HEAVY CODE AFTER DOCTOR IS SELECTED
        # =====================================================
    
        if selected_doctor_display is None:
    
            st.info(
                "Select a doctor to load doctor-level detailing."
            )
    
        else:
    
            with st.spinner(
                "Loading doctor-level details..."
            ):
    
                # -------------------------------------------------
                # FIND SELECTED DOCTOR CODE
                # -------------------------------------------------
    
                selected_doctor_code = (
                    doctor_options.loc[
                        doctor_options[
                            "DOCTOR_DISPLAY"
                        ].eq(
                            selected_doctor_display
                        ),
                        DOCTOR_COLUMN,
                    ]
                    .iloc[0]
                )
    
    
                # =================================================
                # 4. FILTER FIRST
                # =================================================
    
                detail_doctor = (
                    filtered_doctor.loc[
                        filtered_doctor[
                            DOCTOR_COLUMN
                        ].eq(
                            selected_doctor_code
                        )
                    ]
                    .copy()
                )
    
    
                detail_visit = (
                    filtered_visit.loc[
                        filtered_visit[
                            DOCTOR_COLUMN
                        ].eq(
                            selected_doctor_code
                        )
                    ]
                    .copy()
                )
    
    
                # =================================================
                # 5. DOCTOR MASTER
                # =================================================
    
                SPECIALISATION_COLUMN = (
                    "SPECIALISATION_KEY"
                )
    
                GRADE_COLUMN = "GRADE"
    
                DOCTOR_NAME_COLUMN = (
                    "DOCTOR_NAME"
                )
    
    
                doctor_master = (
                    detail_doctor[
                        [
                            DOCTOR_COLUMN,
                            DOCTOR_NAME_COLUMN,
                            HQ_COLUMN,
                            SPECIALISATION_COLUMN,
                            GRADE_COLUMN,
                        ]
                    ]
                    .drop_duplicates()
                )
    
    
                # =================================================
                # 6. TOTAL VISITS
                # =================================================
    
                doctor_visits = (
                    detail_visit
                    .groupby(
                        DOCTOR_COLUMN,
                        as_index=False,
                        observed=True,
                    )
                    .agg(
                        TOTAL_VISITS=(
                            VISIT_COLUMN,
                            "nunique",
                        )
                    )
                )
    
    
                # =================================================
                # 7. BRAND DETAILING COUNT
                # =================================================
    
                doctor_brand_detail = (
                    detail_visit
                    .dropna(
                        subset=[
                            BRAND_COLUMN,
                            VISIT_COLUMN,
                        ]
                    )
                    .groupby(
                        [
                            DOCTOR_COLUMN,
                            BRAND_COLUMN,
                        ],
                        as_index=False,
                        observed=True,
                    )
                    .agg(
                        DETAILING_COUNT=(
                            VISIT_COLUMN,
                            "nunique",
                        )
                    )
                )
    
    
                # =================================================
                # 8. DOCTOR + MONTH + HQ + BRAND
                # =================================================
    
                doctor_brand_month = (
                    detail_visit[
                        [
                            DOCTOR_COLUMN,
                            MONTH_COLUMN,
                            HQ_COLUMN,
                            BRAND_COLUMN,
                        ]
                    ]
                    .dropna(
                        subset=[
                            MONTH_COLUMN,
                            HQ_COLUMN,
                            BRAND_COLUMN,
                        ]
                    )
                    .drop_duplicates()
                )
    
    
                # =================================================
                # 9. SALES MONTH + HQ + BRAND
                # =================================================
    
                # Restrict sales only to the selected doctor's
                # HQ / months / brands before grouping.
    
                detail_hqs = (
                    doctor_brand_month[
                        HQ_COLUMN
                    ]
                    .dropna()
                    .unique()
                )
    
                detail_months = (
                    doctor_brand_month[
                        MONTH_COLUMN
                    ]
                    .dropna()
                    .unique()
                )
    
                detail_brands = (
                    doctor_brand_month[
                        BRAND_COLUMN
                    ]
                    .dropna()
                    .unique()
                )
    
    
                detail_sales = (
                    filtered_sales.loc[
                        filtered_sales[
                            HQ_COLUMN
                        ].isin(
                            detail_hqs
                        )
    &
                        filtered_sales[
                            MONTH_COLUMN
                        ].isin(
                            detail_months
                        )
    &
                        filtered_sales[
                            BRAND_COLUMN
                        ].isin(
                            detail_brands
                        )
                    ]
                    .copy()
                )
    
    
                sales_brand_month = (
                    detail_sales
                    .groupby(
                        [
                            MONTH_COLUMN,
                            HQ_COLUMN,
                            BRAND_COLUMN,
                        ],
                        as_index=False,
                        observed=True,
                    )
                    .agg(
                        ASSOCIATED_SALES=(
                            "NET_REVENUE",
                            "sum",
                        )
                    )
                )
    
    
                # =================================================
                # 10. MATCH DOCTOR DETAILING WITH SALES
                # =================================================
    
                doctor_brand_sales = (
                    doctor_brand_month
                    .merge(
                        sales_brand_month,
                        on=[
                            MONTH_COLUMN,
                            HQ_COLUMN,
                            BRAND_COLUMN,
                        ],
                        how="left",
                    )
                )
    
    
                doctor_brand_sales[
                    "ASSOCIATED_SALES"
                ] = (
                    doctor_brand_sales[
                        "ASSOCIATED_SALES"
                    ]
                    .fillna(0)
                )
    
    
                doctor_brand_sales = (
                    doctor_brand_sales
                    .groupby(
                        [
                            DOCTOR_COLUMN,
                            BRAND_COLUMN,
                        ],
                        as_index=False,
                        observed=True,
                    )
                    .agg(
                        ASSOCIATED_SALES=(
                            "ASSOCIATED_SALES",
                            "sum",
                        )
                    )
                )
    
    
                # =================================================
                # 11. BRAND SUMMARY
                # =================================================
    
                doctor_brand_summary = (
                    doctor_brand_detail
                    .merge(
                        doctor_brand_sales,
                        on=[
                            DOCTOR_COLUMN,
                            BRAND_COLUMN,
                        ],
                        how="left",
                    )
                )
    
    
                doctor_brand_summary[
                    "ASSOCIATED_SALES"
                ] = (
                    doctor_brand_summary[
                        "ASSOCIATED_SALES"
                    ]
                    .fillna(0)
                )
    
    
                # =================================================
                # 12. BUILD BRAND TEXT
                # =================================================
    
                doctor_brand_summary[
                    "BRAND_DETAIL_TEXT"
                ] = (
                    doctor_brand_summary[
                        BRAND_COLUMN
                    ].astype("string")
                    + " ×"
                    + doctor_brand_summary[
                        "DETAILING_COUNT"
                    ]
                    .astype(int)
                    .astype("string")
                    + " · ₹"
                    + doctor_brand_summary[
                        "ASSOCIATED_SALES"
                    ]
                    .apply(
                        format_currency
                    )
                )
    
    
                doctor_brand_text = (
                    doctor_brand_summary
                    .sort_values(
                        "DETAILING_COUNT",
                        ascending=False,
                    )
                    .groupby(
                        DOCTOR_COLUMN,
                        as_index=False,
                        observed=True,
                    )
                    .agg(
                        BRANDS_DETAILED=(
                            "BRAND_DETAIL_TEXT",
                            " │ ".join,
                        )
                    )
                )
    
    
                # =================================================
                # 13. BRAND COUNT
                # =================================================
    
                doctor_brand_count = (
                    doctor_brand_summary
                    .groupby(
                        DOCTOR_COLUMN,
                        as_index=False,
                        observed=True,
                    )
                    .agg(
                        BRANDS_COUNT=(
                            BRAND_COLUMN,
                            "nunique",
                        )
                    )
                )
    
    
                # =================================================
                # 14. PRODUCT COUNT
                # =================================================
    
                doctor_product_count = (
                    detail_visit
                    .dropna(
                        subset=[
                            PRODUCT_COLUMN
                        ]
                    )
                    .groupby(
                        DOCTOR_COLUMN,
                        as_index=False,
                        observed=True,
                    )
                    .agg(
                        PRODUCTS_DETAILED=(
                            PRODUCT_COLUMN,
                            "nunique",
                        )
                    )
                )
    
    
                # =================================================
                # 15. ASSOCIATED SALES TOTAL
                # =================================================
    
                doctor_sales_total = (
                    doctor_brand_sales
                    .groupby(
                        DOCTOR_COLUMN,
                        as_index=False,
                        observed=True,
                    )
                    .agg(
                        ASSOCIATED_HQ_SALES=(
                            "ASSOCIATED_SALES",
                            "sum",
                        )
                    )
                )
    
    
                # =================================================
                # 16. FINAL TABLE
                # =================================================
    
                doctor_detail = (
                    doctor_master
    
                    .merge(
                        doctor_visits,
                        on=DOCTOR_COLUMN,
                        how="left",
                    )
    
                    .merge(
                        doctor_brand_count,
                        on=DOCTOR_COLUMN,
                        how="left",
                    )
    
                    .merge(
                        doctor_product_count,
                        on=DOCTOR_COLUMN,
                        how="left",
                    )
    
                    .merge(
                        doctor_brand_text,
                        on=DOCTOR_COLUMN,
                        how="left",
                    )
    
                    .merge(
                        doctor_sales_total,
                        on=DOCTOR_COLUMN,
                        how="left",
                    )
                )
    
    
                # =================================================
                # 17. CLEAN VALUES
                # =================================================
    
                for column in [
                    "TOTAL_VISITS",
                    "BRANDS_COUNT",
                    "PRODUCTS_DETAILED",
                ]:
    
                    doctor_detail[
                        column
                    ] = (
                        doctor_detail[
                            column
                        ]
                        .fillna(0)
                        .astype(int)
                    )
    
    
                doctor_detail[
                    "ASSOCIATED_HQ_SALES"
                ] = (
                    doctor_detail[
                        "ASSOCIATED_HQ_SALES"
                    ]
                    .fillna(0)
                )
    
    
                doctor_detail[
                    "BRANDS_DETAILED"
                ] = (
                    doctor_detail[
                        "BRANDS_DETAILED"
                    ]
                    .fillna("—")
                )
    
    
                # =================================================
                # 18. DISPLAY
                # =================================================
    
                doctor_display = (
                    doctor_detail[
                        [
                            DOCTOR_NAME_COLUMN,
                            SPECIALISATION_COLUMN,
                            GRADE_COLUMN,
                            HQ_COLUMN,
                            "TOTAL_VISITS",
                            "BRANDS_COUNT",
                            "PRODUCTS_DETAILED",
                            "BRANDS_DETAILED",
                            "ASSOCIATED_HQ_SALES",
                        ]
                    ]
                    .rename(
                        columns={
                            DOCTOR_NAME_COLUMN:
                                "DOCTOR",
    
                            SPECIALISATION_COLUMN:
                                "SPECIALISATION",
    
                            GRADE_COLUMN:
                                "GRADE",
    
                            HQ_COLUMN:
                                "HQ",
    
                            "TOTAL_VISITS":
                                "TOTAL VISITS",
    
                            "BRANDS_COUNT":
                                "BRANDS",
    
                            "PRODUCTS_DETAILED":
                                "PRODUCTS",
    
                            "BRANDS_DETAILED":
                                "BRAND DETAILING",
    
                            "ASSOCIATED_HQ_SALES":
                                "ASSOCIATED HQ SALES",
                        }
                    )
                )
    
    
                st.dataframe(
                    doctor_display,
                    use_container_width=True,
                    hide_index=True,
                    row_height=85,
                    column_config={
    
                        "DOCTOR":
                            st.column_config.TextColumn(
                                "Doctor",
                            ),
    
                        "SPECIALISATION":
                            st.column_config.TextColumn(
                                "Specialisation",
                            ),
    
                        "GRADE":
                            st.column_config.TextColumn(
                                "Grade",
                            ),
    
                        "HQ":
                            st.column_config.TextColumn(
                                "HQ",
                            ),
    
                        "TOTAL VISITS":
                            st.column_config.NumberColumn(
                                "Total Visits",
                                format="%d",
                            ),
    
                        "BRANDS":
                            st.column_config.NumberColumn(
                                "Brands",
                                format="%d",
                            ),
    
                        "PRODUCTS":
                            st.column_config.NumberColumn(
                                "Products",
                                format="%d",
                            ),
    
                        "BRAND DETAILING":
                            st.column_config.TextColumn(
                                "Brand Detailing",
                                width="large",
                            ),
    
                        "ASSOCIATED HQ SALES":
                            st.column_config.NumberColumn(
                                "Associated HQ Sales",
                                format="₹ %.0f",
                            ),
                    },
                )
    
## Targets VS Acievement

elif selected_view == "Targets vs Achievement":
    # =========================================================

    # DYNAMIC TARGET PERFORMANCE

    # =========================================================
    
    
    # ---------------------------------------------------------

    # 1. TARGET PERIOD SOURCE

    #

    # IMPORTANT:

    # Apply ONLY time filters here.

    #

    # Region / State / HQ / Brand must NOT decide

    # which months belong to the target period.

    # ---------------------------------------------------------
    
    target_period_source = apply_target_filters(

        target_mart,
    
        selected_years=selected_years,

        selected_quarters=selected_quarter_keys,

        selected_months=selected_months,
    
        selected_regions=[],

        selected_states=[],

        selected_hqs=[],

        selected_brands=[],

    )
    
    
    # ---------------------------------------------------------

    # 2. TARGET UNDER ALL CURRENT FILTERS

    #

    # This determines the actual target amount.

    # ---------------------------------------------------------
    
    filtered_target = apply_target_filters(

        target_mart,
    
        selected_years=selected_years,

        selected_quarters=selected_quarter_keys,

        selected_months=selected_months,
    
        selected_regions=selected_regions,

        selected_states=selected_states,

        selected_hqs=selected_hqs,

        selected_brands=selected_brands,

    )
    
    
    # ---------------------------------------------------------

    # 3. FIND THE TARGET TIME PERIOD

    # ---------------------------------------------------------
    
    target_months = (

        target_period_source[

            MONTH_COLUMN

        ]

        .dropna()

        .drop_duplicates()

    )
    
    
    # ---------------------------------------------------------

    # 4. SALES IN SAME TARGET PERIOD

    #

    # filtered_sales already contains:

    # Region / State / HQ / Brand filters

    #

    # Now restrict ONLY by target time period.

    # ---------------------------------------------------------
    
    if target_months.empty:
    
        filtered_sales_for_target = (

            filtered_sales.iloc[0:0].copy()

        )
    
    else:
    
        filtered_sales_for_target = (

            filtered_sales.loc[

                filtered_sales[

                    MONTH_COLUMN

                ].isin(target_months)

            ]

            .copy()

        )
    
    
    # ---------------------------------------------------------

    # 5. KPI VALUES

    # ---------------------------------------------------------
    
    actual_sales_for_target = safe_sum(

        filtered_sales_for_target,

        "NET_REVENUE",

    )
    
    target_sales = safe_sum(

        filtered_target,

        "TARGET_SALES",

    )
    
    target_quantity = safe_sum(

        filtered_target,

        "TARGET_QUANTITY",

    )
    
    
    target_available = (

        not filtered_target.empty

        and target_sales != 0

    )
    
    
    # ---------------------------------------------------------

    # 6. TARGET PERFORMANCE

    # ---------------------------------------------------------
    
    if target_available:
    
        target_achievement_percentage = safe_percentage(

            actual_sales_for_target,

            target_sales,

        )
    
        sales_variance = (

            actual_sales_for_target

            - target_sales

        )
    
        target_gap = max(

            target_sales

            - actual_sales_for_target,

            0,

        )
    
        target_surplus = max(

            actual_sales_for_target

            - target_sales,

            0,

        )
    
        target_status = (

            "Achieved"

            if actual_sales_for_target >= target_sales

            else "Below Target"

        )
    
    else:
    
        target_achievement_percentage = None

        sales_variance = None

        target_gap = None

        target_surplus = None

        target_status = "Target Unavailable"
    # =========================================================
    # TARGET PERFORMANCE
    # =========================================================

    st.html(
        """
    <div class="section-header">
    <p class="section-title">
                Target Performance
    </p>
    <p class="section-caption">
                Sales achievement against planned revenue targets
    </p>
    </div>
        """
    )

    if selected_products:
 
        st.warning(
            "Target KPIs are not available for the Product filter "
            "because targets are maintained at Month + HQ + Brand level."
        )
    
    else:
    
        # =====================================================
        # DYNAMIC GAP / SURPLUS
        # =====================================================
    
        if actual_sales_for_target >= target_sales:
    
            variance_label = "Target Surplus"
            variance_value = target_surplus
            variance_delta = "Above Target"
            variance_delta_color = "normal"
    
        else:
    
            variance_label = "Target Gap"
            variance_value = target_gap
            variance_delta = "Below Target"
            variance_delta_color = "inverse"
    
    
        # =====================================================
        # KPI CARDS
        # =====================================================
    
        # =========================================================

        # TARGET KPI CARDS

        # =========================================================
        
        target_row = st.columns(

            4,

            gap="medium",

        )
        
        
        # ---------------------------------------------------------

        # 1. SALES IN TARGET PERIOD

        # ---------------------------------------------------------
        
        target_row[0].metric(

            label="Sales in Target Period",
        
            value=f"₹{format_currency(actual_sales_for_target)}",
        
            help=(

                "Actual primary sales achieved only for the months "

                "where corresponding target data is available."

            ),
        
            border=True,

        )
        
        
        # ---------------------------------------------------------

        # 2. TARGET

        # ---------------------------------------------------------
        
        target_row[1].metric(

            label="Target",
        
            value=f"₹{format_currency(target_sales)}",
        
            help=(

                "Planned sales target for the target period under "

                "the currently selected filters."

            ),
        
            border=True,

        )
        
        
        # ---------------------------------------------------------

        # 3. TARGET ACHIEVEMENT

        # ---------------------------------------------------------
        
        target_row[2].metric(

            label="Target Achievement",
        
            value=f"{target_achievement_percentage:.2f}%",
        
            help=(

                "Percentage of the target achieved. "

                "Calculated as Sales in Target Period ÷ Target × 100."

            ),
        
            border=True,

        )
        
        
        # ---------------------------------------------------------

        # 4. DYNAMIC TARGET GAP / SURPLUS

        # ---------------------------------------------------------
        
        if actual_sales_for_target >= target_sales:
        
            target_difference = (

                actual_sales_for_target

                - target_sales

            )
        
            target_difference_label = (

                "Target Surplus"

            )
        
            target_difference_delta = (

                "Above Target"

            )
        
            target_difference_color = (

                "normal"

            )
        
        else:
        
            target_difference = (

                target_sales

                - actual_sales_for_target

            )
        
            target_difference_label = (

                "Target Gap"

            )
        
            target_difference_delta = (

                "Below Target"

            )
        
            target_difference_color = (

                "inverse"

            )
        
        
        target_row[3].metric(

            label=target_difference_label,
        
            value=f"₹{format_currency(target_difference)}",
        
            delta=target_difference_delta,
        
            delta_color=target_difference_color,
        
            help=(

                "Difference between actual sales and target. "

                "Shown as Target Gap when sales are below target "

                "and Target Surplus when sales exceed target."

            ),
        
            border=True,

        )
 
    # =========================================================

    # SALES AND TARGET PERFORMANCE TABLE

    #

    # Sales: all available years under current filters

    # Target: only where target records are available

    #

    # Views:

    # Brand | State | HQ | Region

    # =========================================================
    
    st.html(

        """
    <div class="section-header">
    <p class="section-title">

                Sales Performance
    </p>
    <p class="section-caption">

                Primary sales and target achievement under the current filters
    </p>
    </div>

        """

    )
    
    
    if selected_products:
    
        st.warning(

            "The target comparison table is unavailable when a Product "

            "filter is selected because targets are maintained at "

            "Month + HQ + Brand level."

        )
    
    else:
    
        # -----------------------------------------------------

        # SELECT VIEW

        # -----------------------------------------------------
    
        performance_view = st.radio(

            "Performance View",

            options=[

                "Brand",

                "State",

                "HQ",

                "Region",

            ],

            horizontal=True,

            label_visibility="collapsed",

            key="performance_table_view",

        )
    
        dimension_map = {

            "Brand": BRAND_COLUMN,

            "State": STATE_COLUMN,

            "HQ": HQ_COLUMN,

            "Region": REGION_COLUMN,

        }
    
        selected_dimension = dimension_map[

            performance_view

        ]
    
    
        # -----------------------------------------------------

        # SEARCH

        # -----------------------------------------------------
    
        performance_search = st.text_input(

            "Search",

            placeholder=(

                f"Search {performance_view.lower()}..."

            ),

            label_visibility="collapsed",

            key="performance_table_search",

        )
    
    
        # =====================================================

        # SALES PERFORMANCE DATA

        #

        # PRIMARY_SALES:

        #   Uses ALL sales available under current filters.

        #

        # TARGET:

        #   Uses target rows available under current filters.

        #

        # COMPARABLE_SALES:

        #   Sales only for Month + HQ + Brand combinations

        #   where a corresponding target exists.

        #

        # ACHIEVEMENT:

        #   COMPARABLE_SALES / TARGET

        # =====================================================
 
 
        # -----------------------------------------------------

        # 1. PRIMARY SALES

        # All available sales under current dashboard filters

        # -----------------------------------------------------
 
        sales_by_dimension = (

            filtered_sales.loc[

                filtered_sales[

                    selected_dimension

                ].notna()

            ]

            .groupby(

                selected_dimension,

                as_index=False,

                observed=True,

            )

            .agg(

                PRIMARY_SALES=(

                    "NET_REVENUE",

                    "sum",

                )

            )

        )
 
 
        # -----------------------------------------------------

        # 2. TARGET DATA

        #

        # IMPORTANT:

        # Apply the SAME dashboard time/business filters.

        #

        # Do NOT use the globally overwritten filtered_target

        # because the old code forces FY2025-26.

        # -----------------------------------------------------
 
        performance_target = apply_target_filters(

            target_mart,
 
            selected_years=selected_years,

            selected_quarters=selected_quarter_keys,

            selected_months=selected_months,
 
            selected_regions=selected_regions,

            selected_states=selected_states,

            selected_hqs=selected_hqs,

            selected_brands=selected_brands,

        )
 
 
        target_by_dimension = (

            performance_target.loc[

                performance_target[

                    selected_dimension

                ].notna()

            ]

            .groupby(

                selected_dimension,

                as_index=False,

                observed=True,

            )

            .agg(

                TARGET=(

                    "TARGET_SALES",

                    "sum",

                )

            )

        )
 
 
        # -----------------------------------------------------

        # 3. FIND TARGET COVERAGE

        #

        # Target mart grain:

        # Month + HQ + Brand

        #

        # Only sales matching an actual target record should

        # participate in Achievement %.

        # -----------------------------------------------------
 
        target_coverage_keys = (

            performance_target[

                [

                    MONTH_COLUMN,

                    HQ_COLUMN,

                    BRAND_COLUMN,

                ]

            ]

            .dropna(

                subset=[

                    MONTH_COLUMN,

                    HQ_COLUMN,

                    BRAND_COLUMN,

                ]

            )

            .drop_duplicates()

        )
 
 
        # -----------------------------------------------------

        # 4. COMPARABLE SALES

        #

        # This does NOT replace Primary Sales.

        # It is only used internally for Achievement %.

        # -----------------------------------------------------
 
        if target_coverage_keys.empty:
 
            comparable_sales_by_dimension = pd.DataFrame(

                columns=[

                    selected_dimension,

                    "COMPARABLE_SALES",

                ]

            )
 
        else:
 
            comparable_sales_rows = (

                filtered_sales.merge(

                    target_coverage_keys,

                    on=[

                        MONTH_COLUMN,

                        HQ_COLUMN,

                        BRAND_COLUMN,

                    ],

                    how="inner",

                )

            )
 
 
            comparable_sales_by_dimension = (

                comparable_sales_rows.loc[

                    comparable_sales_rows[

                        selected_dimension

                    ].notna()

                ]

                .groupby(

                    selected_dimension,

                    as_index=False,

                    observed=True,

                )

                .agg(

                    COMPARABLE_SALES=(

                        "NET_REVENUE",

                        "sum",

                    )

                )

            )
 
 
        # -----------------------------------------------------

        # 5. MERGE

        # -----------------------------------------------------
 
        performance_table = (

            sales_by_dimension

            .merge(

                target_by_dimension,

                on=selected_dimension,

                how="outer",

                validate="one_to_one",

            )

            .merge(

                comparable_sales_by_dimension,

                on=selected_dimension,

                how="left",

                validate="one_to_one",

            )

        )
 
 
        # -----------------------------------------------------

        # 6. CLEAN VALUES

        # -----------------------------------------------------
 
        performance_table[

            selected_dimension

        ] = clean_key(

            performance_table[

                selected_dimension

            ]

        )
 
 
        performance_table[

            "PRIMARY_SALES"

        ] = pd.to_numeric(

            performance_table[

                "PRIMARY_SALES"

            ],

            errors="coerce",

        ).fillna(0)
 
 
        performance_table[

            "TARGET"

        ] = pd.to_numeric(

            performance_table[

                "TARGET"

            ],

            errors="coerce",

        ).fillna(0)
 
 
        performance_table[

            "COMPARABLE_SALES"

        ] = pd.to_numeric(

            performance_table[

                "COMPARABLE_SALES"

            ],

            errors="coerce",

        ).fillna(0)
 
 
        # -----------------------------------------------------

        # 7. ACHIEVEMENT %

        #

        # IMPORTANT:

        # Comparable Sales / Target

        #

        # NOT:

        # Primary Sales / Target

        # -----------------------------------------------------
 
        performance_table[

            "ACHIEVEMENT_PERCENTAGE"

        ] = (

            performance_table[

                "COMPARABLE_SALES"

            ]

            .div(

                performance_table[

                    "TARGET"

                ].replace(

                    0,

                    pd.NA,

                )

            )

            .mul(100)

        )
 
    
        # -----------------------------------------------------

        # SHARE %

        #

        # Share of current filtered Primary Sales

        # -----------------------------------------------------
    
        total_primary_sales = performance_table[

            "PRIMARY_SALES"

        ].sum()
    
        if total_primary_sales != 0:
    
            performance_table[

                "SHARE_PERCENTAGE"

            ] = (

                performance_table[

                    "PRIMARY_SALES"

                ]

                / total_primary_sales

                * 100

            )
    
        else:
    
            performance_table[

                "SHARE_PERCENTAGE"

            ] = 0.0
    
    
        # -----------------------------------------------------

        # SEARCH FILTER

        # -----------------------------------------------------
    
        if performance_search:
    
            performance_table = performance_table[

                performance_table[

                    selected_dimension

                ]

                .astype("string")

                .str.contains(

                    performance_search,

                    case=False,

                    na=False,

                )

            ]
        # -----------------------------------------------------

        # TOTAL VALUES

        # -----------------------------------------------------
 
        total_sales_value = (

            performance_table[

                "PRIMARY_SALES"

            ].sum()

        )
 
 
        total_comparable_sales_value = (

            performance_table[

                "COMPARABLE_SALES"

            ].sum()

        )
 
 
        total_target_value = (

            performance_table[

                "TARGET"

            ].sum()

        )
 
 
        if total_target_value != 0:
 
            total_achievement_value = safe_percentage(

                total_comparable_sales_value,

                total_target_value,

            )
 
        else:
 
            total_achievement_value = pd.NA
 

    
    
        # -----------------------------------------------------

        # SORT AND RANK

        # -----------------------------------------------------
    
        performance_table = (

            performance_table

            .sort_values(

                by="PRIMARY_SALES",

                ascending=False,

            )

            .reset_index(drop=True)

        )
    
        performance_table.insert(

            0,

            "RANK",

            range(

                1,

                len(performance_table) + 1,

            ),

        )
    
    
        # -----------------------------------------------------

        # FORMAT CURRENCY

        # -----------------------------------------------------
    
        performance_table[

            "PRIMARY_SALES_DISPLAY"

        ] = performance_table[

            "PRIMARY_SALES"

        ].apply(

            lambda value:

                f"₹{format_currency(value)}"

        )
    
        performance_table[

            "TARGET_DISPLAY"

        ] = performance_table[

            "TARGET"

        ].apply(

            lambda value:

                (

                    f"₹{format_currency(value)}"

                    if value != 0

                    else "—"

                )

        )
        # -----------------------------------------------------
        # REMOVE UNMAPPED ROWS FROM SALES PERFORMANCE TABLE
        # -----------------------------------------------------
        
        performance_table = performance_table[
            ~performance_table[selected_dimension]
            .astype("string")
            .str.upper()
            .str.contains("UNMAPPED", na=False)
        ].copy()

        # -----------------------------------------------------
        # ADD TOTAL ROW
        # -----------------------------------------------------
        
        total_row = pd.DataFrame(
            {
                "RANK": [pd.NA],
        
                selected_dimension: [
                    "TOTAL"
                ],
        
                "PRIMARY_SALES": [
                    total_sales_value
                ],

                "COMPARABLE_SALES": [
                    total_comparable_sales_value
                ],
        
                "TARGET": [
                    total_target_value
                ],
        
                "ACHIEVEMENT_PERCENTAGE": [
                    total_achievement_value
                ],
        
                "SHARE_PERCENTAGE": [
                    100.0
                ],
        
                "PRIMARY_SALES_DISPLAY": [
                    f"₹{format_currency(total_sales_value)}"
                ],
        
                "TARGET_DISPLAY": [
                    (
                        f"₹{format_currency(total_target_value)}"
                        if total_target_value != 0
                        else "—"
                    )
                ],
            }
        )
        
        
        performance_table = pd.concat(
            [
                performance_table,
                total_row,
            ],
            ignore_index=True,
        )
    
    
        # -----------------------------------------------------

        # DISPLAY TABLE

        # -----------------------------------------------------

        performance_display = performance_table[

            [

                "RANK",

                selected_dimension,

                "PRIMARY_SALES_DISPLAY",

                "TARGET_DISPLAY",

                "ACHIEVEMENT_PERCENTAGE",

                "SHARE_PERCENTAGE",

            ]

        ].rename(

            columns={

                "RANK": "#",

                selected_dimension:

                    performance_view.upper(),

                "PRIMARY_SALES_DISPLAY":

                    "PRIMARY SALES",

                "TARGET_DISPLAY":

                    "TARGET",

                "ACHIEVEMENT_PERCENTAGE":

                    "TARGET ACH %",

                "SHARE_PERCENTAGE":

                    "SHARE",

            }

        )
    
    
        if performance_display.empty:
    
            st.info(

                "No sales or target records are available "

                "for the selected filters."

            )
    
        else:
    
            st.dataframe(

                performance_display,

                use_container_width=True,

                hide_index=True,

                height=500,

                column_config={

                    "#":

                        st.column_config.NumberColumn(

                            "#",

                            format="%d",

                            width="small",

                        ),
    
                    performance_view.upper():

                        st.column_config.TextColumn(

                            performance_view.upper(),

                            width="medium",

                        ),
    
                    "PRIMARY SALES":

                        st.column_config.TextColumn(

                            "PRIMARY SALES",

                            width="medium",

                        ),
    
                    "TARGET":

                        st.column_config.TextColumn(

                            "TARGET",

                            width="medium",

                        ),
    
                    "TARGET ACH %":

                        st.column_config.NumberColumn(

                            "TARGET ACH %",

                            format="%.1f%%",

                        ),
    
                    "SHARE":

                        st.column_config.NumberColumn(

                            "SHARE",

                            format="%.1f%%",

                        ),

                },

            )
    # =========================================================
    # CUMULATIVE TARGET VS CUMULATIVE SALES
    # =========================================================
    
    st.html(
        """
    <div class="section-header">
    <p class="section-title">
                Cumulative Target vs Cumulative Sales
    </p>
    <p class="section-caption">
                Year-to-date sales progress against cumulative target trajectory
    </p>
    </div>
        """
    )
    
    
    # ---------------------------------------------------------
    # 1. MONTHLY TARGET
    # ---------------------------------------------------------
    
    monthly_target = (
        filtered_target
        .groupby(
            MONTH_COLUMN,
            as_index=False,
            observed=True,
        )
        .agg(
            TARGET_SALES=(
                "TARGET_SALES",
                "sum",
            )
        )
    )
    
    
    # ---------------------------------------------------------
    # 2. MONTHLY SALES
    # ---------------------------------------------------------
    
    monthly_sales = (
        filtered_sales
        .groupby(
            MONTH_COLUMN,
            as_index=False,
            observed=True,
        )
        .agg(
            ACTUAL_SALES=(
                "NET_REVENUE",
                "sum",
            )
        )
    )
    
    
    # ---------------------------------------------------------
    # 3. MERGE TARGET + SALES
    # ---------------------------------------------------------
    
    cumulative_data = (
        monthly_target
        .merge(
            monthly_sales,
            on=MONTH_COLUMN,
            how="outer",
        )
        .sort_values(
            MONTH_COLUMN
        )
        .reset_index(drop=True)
    )
    
    
    cumulative_data[
        [
            "TARGET_SALES",
            "ACTUAL_SALES",
        ]
    ] = (
        cumulative_data[
            [
                "TARGET_SALES",
                "ACTUAL_SALES",
            ]
        ]
        .fillna(0)
    )
    
    
    # ---------------------------------------------------------
    # 4. KEEP ONLY MONTHS UP TO LATEST COMMON PERIOD
    #
    # This avoids showing future target months when sales
    # are not yet available.
    # ---------------------------------------------------------
    
    target_available_months = set(
        monthly_target[
            MONTH_COLUMN
        ].dropna()
    )
    
    sales_available_months = set(
        monthly_sales[
            MONTH_COLUMN
        ].dropna()
    )
    
    common_months = sorted(
        target_available_months
    & sales_available_months
    )
    
    
    if common_months:
    
        latest_common_month = max(
            common_months
        )
    
        cumulative_data = (
            cumulative_data.loc[
                cumulative_data[
                    MONTH_COLUMN
                ]
    <= latest_common_month
            ]
            .copy()
        )
    
    
    # ---------------------------------------------------------
    # 5. CUMULATIVE VALUES
    # ---------------------------------------------------------
    
    cumulative_data[
        "CUMULATIVE_TARGET"
    ] = (
        cumulative_data[
            "TARGET_SALES"
        ]
        .cumsum()
    )
    
    
    cumulative_data[
        "CUMULATIVE_SALES"
    ] = (
        cumulative_data[
            "ACTUAL_SALES"
        ]
        .cumsum()
    )
    
    
    # ---------------------------------------------------------
    # 6. VALUES IN CRORES
    # ---------------------------------------------------------
    
    cumulative_data[
        "CUMULATIVE_TARGET_CR"
    ] = (
        cumulative_data[
            "CUMULATIVE_TARGET"
        ]
        / 10_000_000
    )
    
    
    cumulative_data[
        "CUMULATIVE_SALES_CR"
    ] = (
        cumulative_data[
            "CUMULATIVE_SALES"
        ]
        / 10_000_000
    )
    
    
    # ---------------------------------------------------------
    # 7. MONTH LABEL
    # ---------------------------------------------------------
    
    cumulative_data[
        "MONTH_LABEL"
    ] = (
        pd.to_datetime(
            cumulative_data[
                MONTH_COLUMN
            ]
        )
        .dt.strftime(
            "%b '%y"
        )
    )
    
    
    # ---------------------------------------------------------
    # 8. TOOLTIP DISPLAY VALUES
    # ---------------------------------------------------------
    
    cumulative_data[
        "TARGET_DISPLAY"
    ] = (
        cumulative_data[
            "CUMULATIVE_TARGET"
        ]
        .apply(
            lambda value:
                f"₹{format_currency(value)}"
        )
    )
    
    
    cumulative_data[
        "SALES_DISPLAY"
    ] = (
        cumulative_data[
            "CUMULATIVE_SALES"
        ]
        .apply(
            lambda value:
                f"₹{format_currency(value)}"
        )
    )
    
    
    # ---------------------------------------------------------
    # 9. BUILD CHART
    # ---------------------------------------------------------
    
    if cumulative_data.empty:
    
        st.info(
            "No target and sales data is available "
            "for the selected filters."
        )
    
    else:
    
        fig_cumulative = go.Figure()
    
    
        # TARGET LINE
        fig_cumulative.add_trace(
            go.Scatter(
                x=cumulative_data[
                    "MONTH_LABEL"
                ],
    
                y=cumulative_data[
                    "CUMULATIVE_TARGET_CR"
                ],
    
                mode="lines+markers",
    
                name="Cumulative Target",
    
                customdata=cumulative_data[
                    [
                        "TARGET_DISPLAY",
                    ]
                ],
    
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Cumulative Target: "
                    "%{customdata[0]}"
                    "<extra></extra>"
                ),
            )
        )
    
    
        # SALES LINE
        fig_cumulative.add_trace(
            go.Scatter(
                x=cumulative_data[
                    "MONTH_LABEL"
                ],
    
                y=cumulative_data[
                    "CUMULATIVE_SALES_CR"
                ],
    
                mode="lines+markers",
    
                name="Cumulative Sales",
    
                customdata=cumulative_data[
                    [
                        "SALES_DISPLAY",
                    ]
                ],
    
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Cumulative Sales: "
                    "%{customdata[0]}"
                    "<extra></extra>"
                ),
            )
        )
    
    
        # -----------------------------------------------------
        # 10. LAYOUT
        # -----------------------------------------------------
    
        fig_cumulative.update_layout(
    
            height=430,
    
            hovermode="x unified",
    
            legend_title_text="",
    
            xaxis_title="Month",
    
            yaxis_title="Cumulative Value (₹ Cr)",
    
            margin=dict(
                l=30,
                r=20,
                t=30,
                b=40,
            ),
        )
    
    
        fig_cumulative.update_yaxes(
            ticksuffix=" Cr",
            rangemode="tozero",
        )
    
    
        st.plotly_chart(
            fig_cumulative,
            use_container_width=True,
        )
    
    # =========================================================

    # FIELD EMPLOYEE SCORECARD

    # =========================================================
    
    st.html(

        """
    <div class="section-header">
    <p class="section-title">

                Field Employee Scorecard
    </p>
    <p class="section-caption">

                Target and achievement attributed to field employees

                based on their visit contribution within each HQ
    </p>
    </div>

        """

    )
    
    
    # =========================================================

    # 1. LAZY LOAD

    # =========================================================
    
    show_mr_scorecard = st.toggle(

        "Load Field Employee Scorecard",

        value=False,

        key="load_mr_scorecard",

    )
    
    
    if show_mr_scorecard:
    
        MR_NAME_COLUMN = "MR_NAME"
    
    
        # =====================================================

        # 2. BUILD SEARCH OPTIONS

        # =====================================================

        #

        # Uses MR mart only.

        # This is lightweight compared with building the full

        # target/sales allocation for all employees.

        # =====================================================
    
        mr_options = (

            filtered_mr[

                [

                    MR_COLUMN,

                    MR_NAME_COLUMN,

                ]

            ]

            .dropna(

                subset=[

                    MR_COLUMN,

                    MR_NAME_COLUMN,

                ]

            )

            .drop_duplicates()

            .sort_values(

                MR_NAME_COLUMN

            )

            .reset_index(drop=True)

        )
    
    
        # Example:

        # KARTHIK A V | MR00123

        mr_options[

            "MR_DISPLAY"

        ] = (

            mr_options[

                MR_NAME_COLUMN

            ]

            .astype("string")

            .str.strip()

            + " | "

            + mr_options[

                MR_COLUMN

            ]

            .astype("string")

            .str.strip()

        )
    
    
        # =====================================================

        # 3. SEARCH / SELECT MR

        # =====================================================
    
        selected_mr_display = st.selectbox(

            "Search Field Employee",

            options=[

                None

            ]

            + mr_options[

                "MR_DISPLAY"

            ].tolist(),

            index=0,

            placeholder=(

                "Search by employee name or MR key..."

            ),

            key="mr_scorecard_search",

        )
    
    
        # =====================================================

        # 4. DO NOT RUN HEAVY LOGIC UNTIL MR IS SELECTED

        # =====================================================
    
        if selected_mr_display is None:
    
            st.info(

                "Select a field employee to load "

                "target and achievement details."

            )
    
        else:
    
            # -------------------------------------------------

            # Resolve selected MR

            # -------------------------------------------------
    
            selected_mr_row = (

                mr_options.loc[

                    mr_options[

                        "MR_DISPLAY"

                    ].eq(

                        selected_mr_display

                    )

                ]

                .iloc[0]

            )
    
    
            selected_mr_key = (

                selected_mr_row[

                    MR_COLUMN

                ]

            )
    
    
            selected_mr_name = (

                selected_mr_row[

                    MR_NAME_COLUMN

                ]

            )
    
    
            with st.spinner(

                f"Loading scorecard for {selected_mr_name}..."

            ):
    
                # =============================================

                # 5. FILTER MR DATA FIRST

                # =============================================
    
                selected_mr_data = (

                    filtered_mr.loc[

                        filtered_mr[

                            MR_COLUMN

                        ].eq(

                            selected_mr_key

                        )

                    ]

                    .copy()

                )
    
    
                selected_mr_visits = (

                    filtered_visit.loc[

                        filtered_visit[

                            MR_COLUMN

                        ].eq(

                            selected_mr_key

                        )

                    ]

                    .copy()

                )
    
    
                # =============================================

                # 6. VISITS BY HQ FOR THIS MR

                # =============================================
    
                mr_hq_visits = (

                    selected_mr_visits

                    .dropna(

                        subset=[

                            HQ_COLUMN,

                            VISIT_COLUMN,

                        ]

                    )

                    .groupby(

                        HQ_COLUMN,

                        as_index=False,

                        observed=True,

                    )

                    .agg(

                        MR_VISITS=(

                            VISIT_COLUMN,

                            "nunique",

                        )

                    )

                )
    
    
                # =============================================

                # 7. TOTAL VISITS BY HQ

                # =============================================

                #

                # Needed to calculate this MR's share of HQ visits.

                # =================================================
    
                relevant_hqs = (

                    mr_hq_visits[

                        HQ_COLUMN

                    ]

                    .dropna()

                    .unique()

                )
    
    
                hq_total_visits = (

                    filtered_visit.loc[

                        filtered_visit[

                            HQ_COLUMN

                        ].isin(

                            relevant_hqs

                        )

                    ]

                    .groupby(

                        HQ_COLUMN,

                        as_index=False,

                        observed=True,

                    )

                    .agg(

                        HQ_TOTAL_VISITS=(

                            VISIT_COLUMN,

                            "nunique",

                        )

                    )

                )
    
    
                mr_hq_performance = (

                    mr_hq_visits

                    .merge(

                        hq_total_visits,

                        on=HQ_COLUMN,

                        how="left",

                    )

                )
    
    
                # =============================================

                # 8. MR VISIT SHARE

                # =============================================
    
                mr_hq_performance[

                    "VISIT_SHARE"

                ] = (

                    mr_hq_performance[

                        "MR_VISITS"

                    ]

                    .div(

                        mr_hq_performance[

                            "HQ_TOTAL_VISITS"

                        ]

                        .replace(

                            0,

                            pd.NA,

                        )

                    )

                    .fillna(0)

                )
    
    
                # =============================================

                # 9. HQ TARGET

                # =============================================
    
                hq_target = (

                    filtered_target.loc[

                        filtered_target[

                            HQ_COLUMN

                        ].isin(

                            relevant_hqs

                        )

                    ]

                    .groupby(

                        HQ_COLUMN,

                        as_index=False,

                        observed=True,

                    )

                    .agg(

                        HQ_TARGET=(

                            "TARGET_SALES",

                            "sum",

                        )

                    )

                )
    
    
                # =============================================

                # 10. HQ SALES

                # =============================================
    
                hq_sales = (

                    filtered_sales.loc[

                        filtered_sales[

                            HQ_COLUMN

                        ].isin(

                            relevant_hqs

                        )

                    ]

                    .groupby(

                        HQ_COLUMN,

                        as_index=False,

                        observed=True,

                    )

                    .agg(

                        HQ_SALES=(

                            "NET_REVENUE",

                            "sum",

                        )

                    )

                )
    
    
                # =============================================

                # 11. MERGE HQ TARGET + SALES

                # =============================================
    
                mr_hq_performance = (

                    mr_hq_performance

                    .merge(

                        hq_target,

                        on=HQ_COLUMN,

                        how="left",

                    )

                    .merge(

                        hq_sales,

                        on=HQ_COLUMN,

                        how="left",

                    )

                )
    
    
                mr_hq_performance[

                    [

                        "HQ_TARGET",

                        "HQ_SALES",

                    ]

                ] = (

                    mr_hq_performance[

                        [

                            "HQ_TARGET",

                            "HQ_SALES",

                        ]

                    ]

                    .fillna(0)

                )
    
    
                # =============================================

                # 12. ALLOCATE TARGET + SALES BY VISIT SHARE

                # =============================================
    
                mr_hq_performance[

                    "ALLOCATED_TARGET"

                ] = (

                    mr_hq_performance[

                        "HQ_TARGET"

                    ]

                    * mr_hq_performance[

                        "VISIT_SHARE"

                    ]

                )
    
    
                mr_hq_performance[

                    "ALLOCATED_SALES"

                ] = (

                    mr_hq_performance[

                        "HQ_SALES"

                    ]

                    * mr_hq_performance[

                        "VISIT_SHARE"

                    ]

                )
    
    
                # =============================================

                # 13. TOTAL SCORECARD VALUES

                # =============================================
    
                total_visits = (

                    mr_hq_performance[

                        "MR_VISITS"

                    ].sum()

                )
    
    
                allocated_target = (

                    mr_hq_performance[

                        "ALLOCATED_TARGET"

                    ].sum()

                )
    
    
                allocated_sales = (

                    mr_hq_performance[

                        "ALLOCATED_SALES"

                    ].sum()

                )
    
    
                achievement_pct = (

                    safe_percentage(

                        allocated_sales,

                        allocated_target,

                    )

                    if allocated_target != 0

                    else 0

                )
    
    
                gap_surplus = (

                    allocated_sales

                    - allocated_target

                )
    
    
                status = (

                    "Achiever"

                    if achievement_pct >= 100

                    else "Non-achiever"

                )
    
    
                # =============================================

                # 14. EMPLOYEE CONTEXT

                # =============================================
    
                mr_context = (

                    selected_mr_data[

                        [

                            HQ_COLUMN,

                            REGION_COLUMN,

                        ]

                    ]

                    .drop_duplicates()

                )
    
    
                hq_display = (

                    ", ".join(

                        mr_context[

                            HQ_COLUMN

                        ]

                        .dropna()

                        .astype("string")

                        .unique()

                    )

                )
    
    
                region_display = (

                    ", ".join(

                        mr_context[

                            REGION_COLUMN

                        ]

                        .dropna()

                        .astype("string")

                        .unique()

                    )

                )
    
    
                # =============================================

                # 15. SCORECARD TABLE

                # =============================================
    
                mr_scorecard = pd.DataFrame(

                    {

                        "FIELD EMPLOYEE": [

                            selected_mr_name

                        ],
    
                        "MR KEY": [

                            selected_mr_key

                        ],
    
                        "HQ": [

                            hq_display

                        ],
    
                        "REGION": [

                            region_display

                        ],
    
                        "VISITS": [

                            total_visits

                        ],
    
                        "TARGET": [

                            allocated_target

                        ],
    
                        "ACHIEVED": [

                            allocated_sales

                        ],
    
                        "ACHIEVEMENT %": [

                            achievement_pct

                        ],
    
                        "GAP / SURPLUS": [

                            gap_surplus

                        ],
    
                        "STATUS": [

                            status

                        ],

                    }

                )
    
    
                # =============================================

                # 16. DISPLAY

                # =============================================
    
                st.dataframe(

                    mr_scorecard,

                    use_container_width=True,

                    hide_index=True,
    
                    column_config={
    
                        "FIELD EMPLOYEE":

                            st.column_config.TextColumn(

                                "Field Employee",

                                width="medium",

                            ),
    
                        "MR KEY":

                            st.column_config.TextColumn(

                                "MR Key",

                                width="small",

                            ),
    
                        "HQ":

                            st.column_config.TextColumn(

                                "HQ",

                            ),
    
                        "REGION":

                            st.column_config.TextColumn(

                                "Region",

                            ),
    
                        "VISITS":

                            st.column_config.NumberColumn(

                                "Visits",

                                format="%d",

                            ),
    
                        "TARGET":

                            st.column_config.NumberColumn(

                                "Target",

                                format="₹ %.0f",

                            ),
    
                        "ACHIEVED":

                            st.column_config.NumberColumn(

                                "Achieved",

                                format="₹ %.0f",

                            ),
    
                        "ACHIEVEMENT %":

                            st.column_config.NumberColumn(

                                "Achievement %",

                                format="%.1f%%",

                            ),
    
                        "GAP / SURPLUS":

                            st.column_config.NumberColumn(

                                "Gap / Surplus",

                                format="₹ %.0f",

                            ),
    
                        "STATUS":

                            st.column_config.TextColumn(

                                "Status",

                            ),

                    },

                )

elif selected_view == "Forecasting":
    # =========================================================

    # FORECASTING - 3 MONTH WEIGHTED MOVING AVERAGE (WMA)

    # =========================================================
    
    st.html(

        """
    <div class="section-header">
    <p class="section-title">

                Sales Forecast & Outlook
    </p>
    <p class="section-caption">

                3-month weighted moving average forecast with greater

                emphasis on recent sales performance
    </p>
    </div>

        """

    )
    
    
    # =========================================================

    # 1. BUILD FORECAST SOURCE

    #

    # IMPORTANT:

    # Ignore FY / Quarter / Month filters for model history.

    #

    # Keep:

    # Region

    # State

    # HQ

    # Brand

    # Product

    # =========================================================
    
    forecast_sales = apply_filters(

        sales_mart,
    
        [],                     # FY

        [],                     # Quarter

        [],                     # Month
    
        selected_regions,

        selected_states,

        selected_hqs,

        selected_brands,

        selected_products,

    )
    
    
    # =========================================================

    # 2. MONTHLY SALES

    # =========================================================
    
    monthly_forecast_sales = (

        forecast_sales

        .groupby(

            MONTH_COLUMN,

            as_index=False,

            observed=True,

        )

        .agg(

            ACTUAL_SALES=(

                "NET_REVENUE",

                "sum",

            )

        )

        .dropna(

            subset=[

                MONTH_COLUMN

            ]

        )

        .sort_values(

            MONTH_COLUMN

        )

        .reset_index(drop=True)

    )
    
    
    # Ensure date

    monthly_forecast_sales[

        MONTH_COLUMN

    ] = pd.to_datetime(

        monthly_forecast_sales[

            MONTH_COLUMN

        ]

    )
    
    
    # =========================================================

    # 3. CHECK MINIMUM HISTORY

    # =========================================================
    
    if len(monthly_forecast_sales) < 3:
    
        st.info(

            "At least 3 months of sales history are required "

            "to generate the WMA forecast."

        )
    
    else:
    
        # =====================================================

        # 4. WMA CONFIGURATION

        #

        # Oldest → newest

        #

        # Month -2 = 20%

        # Month -1 = 30%

        # Latest   = 50%

        # =====================================================
    
        WMA_WEIGHTS = [

            0.20,

            0.30,

            0.50,

        ]
    
    
        # =====================================================

        # 5. LATEST ACTUAL MONTH

        # =====================================================
    
        latest_actual_month = (

            monthly_forecast_sales[

                MONTH_COLUMN

            ].max()

        )
        latest_actual_sales = (
            monthly_forecast_sales.loc[
                monthly_forecast_sales[
                    MONTH_COLUMN
                ].eq(
                    latest_actual_month
                ),
                "ACTUAL_SALES",
            ]
            .iloc[0]
        )
        previous_3_month_sales = (
            monthly_forecast_sales[
                "ACTUAL_SALES"
            ]
            .tail(3)
            .sum()
        )
    
    
        # =====================================================

        # 6. DETERMINE CURRENT FINANCIAL YEAR

        #

        # Apr → Mar

        # =====================================================
    
        if latest_actual_month.month >= 4:
    
            fy_start_year = (

                latest_actual_month.year

            )
    
            fy_end_year = (

                latest_actual_month.year

                + 1

            )
    
        else:
    
            fy_start_year = (

                latest_actual_month.year

                - 1

            )
    
            fy_end_year = (

                latest_actual_month.year

            )
    
    
        current_forecast_fy = (

            f"FY{fy_start_year}-"

            f"{str(fy_end_year)[-2:]}"

        )
    
    
        fy_start_date = pd.Timestamp(

            year=fy_start_year,

            month=4,

            day=1,

        )
    
    
        fy_end_date = pd.Timestamp(

            year=fy_end_year,

            month=3,

            day=1,

        )
    
    
        # =====================================================

        # 7. ACTUAL SALES IN CURRENT FY

        # =====================================================
    
        actual_current_fy = (

            monthly_forecast_sales.loc[

                (

                    monthly_forecast_sales[

                        MONTH_COLUMN

                    ]
    >= fy_start_date

                )
    &

                (

                    monthly_forecast_sales[

                        MONTH_COLUMN

                    ]
    <= latest_actual_month

                )

            ]

            .copy()

        )
    
    
        ytd_sales = (

            actual_current_fy[

                "ACTUAL_SALES"

            ].sum()

        )
    
    
        # =====================================================

        # 8. CURRENT 3-MONTH WMA RUN RATE

        # =====================================================
    
        latest_three_sales = (

            monthly_forecast_sales[

                "ACTUAL_SALES"

            ]

            .tail(3)

            .tolist()

        )
    
    
        current_wma_run_rate = sum(

            value * weight
    
            for value, weight in zip(

                latest_three_sales,

                WMA_WEIGHTS,

            )

        )
    
    
        # =====================================================

        # 9. RECURSIVE FORECAST UNTIL FY END

        #

        # Example:

        #

        # Jul forecast uses Apr/May/Jun actual

        #

        # Aug forecast uses

        # May/Jun/Jul forecast

        #

        # etc.

        # =====================================================
    
        history_values = (

            monthly_forecast_sales[

                "ACTUAL_SALES"

            ]

            .astype(float)

            .tolist()

        )
    
    
        forecast_rows = []
    
        forecast_month = (

            latest_actual_month

            + pd.DateOffset(months=1)

        )
    
    
        while forecast_month <= fy_end_date:
    
            last_three = (

                history_values[-3:]

            )
    
    
            forecast_value = sum(

                value * weight
    
                for value, weight in zip(

                    last_three,

                    WMA_WEIGHTS,

                )

            )
    
    
            forecast_rows.append(

                {

                    MONTH_COLUMN:

                        forecast_month,
    
                    "FORECAST_SALES":

                        forecast_value,

                }

            )
    
    
            # Recursive forecast

            history_values.append(

                forecast_value

            )
    
    
            forecast_month = (

                forecast_month

                + pd.DateOffset(months=1)

            )
    
    
        forecast_df = pd.DataFrame(

            forecast_rows

        )
    
    
        # =====================================================

        # 10. NEXT QUARTER FORECAST

        #

        # First 3 future months

        # =====================================================
    
        next_quarter_forecast = (

            forecast_df[

                "FORECAST_SALES"

            ]

            .head(3)

            .sum()

        )
    
    
        # =====================================================

        # 11. FORECAST FULL FY SALES

        #

        # Actual YTD

        # +

        # Forecast remaining months

        # =====================================================
    
        remaining_forecast_sales = (

            forecast_df[

                "FORECAST_SALES"

            ].sum()

        )
    
    
        forecast_fy_sales = (

            ytd_sales

            + remaining_forecast_sales

        )
    
        # ============================================================

        # FORECAST KPI CALCULATIONS

        # ============================================================
        
        
        # ============================================================

        # HELPER — FINANCIAL QUARTER LABEL

        # ============================================================
        
        def get_fy_quarter_label(date_value):
        
            month = date_value.month

            year = date_value.year
        
            if month in [4, 5, 6]:

                quarter = 1

                fy_end_year = year + 1
        
            elif month in [7, 8, 9]:

                quarter = 2

                fy_end_year = year + 1
        
            elif month in [10, 11, 12]:

                quarter = 3

                fy_end_year = year + 1
        
            else:

                quarter = 4

                fy_end_year = year
        
            return (

                f"Q{quarter} "

                f"'{str(fy_end_year)[-2:]}"

            )
        
        
        # ============================================================

        # 1. LATEST COMPLETED / AVAILABLE ACTUAL QUARTER

        # ============================================================
        
        latest_actual_quarter_label = (

            get_fy_quarter_label(

                latest_actual_month

            )

        )
        
        
        # Determine months belonging to latest actual quarter
        
        if latest_actual_month.month in [4, 5, 6]:
        
            latest_quarter_months = [4, 5, 6]
        
        elif latest_actual_month.month in [7, 8, 9]:
        
            latest_quarter_months = [7, 8, 9]
        
        elif latest_actual_month.month in [10, 11, 12]:
        
            latest_quarter_months = [10, 11, 12]
        
        else:
        
            latest_quarter_months = [1, 2, 3]
        
        
        # Actual sales for latest quarter
        
        latest_actual_quarter_sales = (

            monthly_forecast_sales.loc[

                (

                    monthly_forecast_sales[

                        MONTH_COLUMN

                    ].dt.year

                    ==

                    latest_actual_month.year

                )
        &

                (

                    monthly_forecast_sales[

                        MONTH_COLUMN

                    ].dt.month.isin(

                        latest_quarter_months

                    )

                ),

                "ACTUAL_SALES",

            ]

            .sum()

        )
        
        
        # ============================================================

        # 2. NEXT FORECAST QUARTER LABEL

        # ============================================================
        
        if not forecast_df.empty:
        
            first_forecast_month = (

                forecast_df[

                    MONTH_COLUMN

                ].min()

            )
        
            next_forecast_quarter_label = (

                get_fy_quarter_label(

                    first_forecast_month

                )

            )
        
        else:
        
            first_forecast_month = None

            next_forecast_quarter_label = "Next Quarter"
        
        
        # ============================================================

        # KPI 1 DELTA

        # PROJECTED NEXT QUARTER

        #

        # Example:

        # Q2 '27 Forecast vs Q1 '27 Actual

        # ============================================================
        
        if latest_actual_quarter_sales > 0:
        
            projected_qtr_change_pct = (

                (

                    next_quarter_forecast

                    - latest_actual_quarter_sales

                )

                / latest_actual_quarter_sales

                * 100

            )
        
            projected_qtr_delta = (

                f"{projected_qtr_change_pct:+.1f}% "

                f"{next_forecast_quarter_label} "

                f"vs {latest_actual_quarter_label}"

            )
        
        else:
        
            projected_qtr_change_pct = None

            projected_qtr_delta = "No quarter comparison"
        
        
        # ============================================================

        # KPI 2

        # CURRENT QUARTERLY RUN RATE

        #

        # Current monthly WMA pace × 3

        # ============================================================
        
        current_quarterly_run_rate = (

            current_wma_run_rate

            * 3

        )
        
        
        # Compare current quarterly pace with latest actual quarter
        
        if latest_actual_quarter_sales > 0:
        
            quarterly_run_rate_change_pct = (

                (

                    current_quarterly_run_rate

                    - latest_actual_quarter_sales

                )

                / latest_actual_quarter_sales

                * 100

            )
        
            quarterly_run_rate_delta = (

                f"{quarterly_run_rate_change_pct:+.1f}% "

                f"vs {latest_actual_quarter_label}"

            )
        
        else:
        
            quarterly_run_rate_change_pct = None

            quarterly_run_rate_delta = "No quarter comparison"
        
        
        # ============================================================

        # KPI 3

        # FORECAST QUARTERLY AVERAGE

        # ============================================================
        
        forecast_quarterly_average = (

            forecast_fy_sales

            / 4

        )
        
        
        # ============================================================

        # PREVIOUS FY SALES

        #

        # Example:

        # Current forecast FY = FY2026-27

        # Previous FY = Apr 2025 → Mar 2026

        # ============================================================
        
        previous_fy_start = pd.Timestamp(

            year=fy_start_year - 1,

            month=4,

            day=1,

        )
        
        
        previous_fy_end = pd.Timestamp(

            year=fy_start_year,

            month=3,

            day=1,

        )
        
        
        previous_fy_sales_df = (

            monthly_forecast_sales.loc[

                (

                    monthly_forecast_sales[

                        MONTH_COLUMN

                    ]
        >= previous_fy_start

                )
        &

                (

                    monthly_forecast_sales[

                        MONTH_COLUMN

                    ]
        <= previous_fy_end

                )

            ]

        )
        
        
        previous_fy_sales = (

            previous_fy_sales_df[

                "ACTUAL_SALES"

            ]

            .sum()

        )
        
        
        previous_fy_month_count = (

            previous_fy_sales_df[

                MONTH_COLUMN

            ]

            .nunique()

        )
        
        
        # ============================================================

        # PREVIOUS FY LABEL

        # ============================================================
        
        previous_fy_label = (

            f"FY{str(fy_start_year - 1)[-2:]}"

            f"-{str(fy_start_year)[-2:]}"

        )
        
        
        # ============================================================

        # PREVIOUS FY QUARTERLY AVERAGE

        #

        # Only compare as a full FY if all 12 months exist.

        # ============================================================
        
        if (

            previous_fy_sales > 0

            and previous_fy_month_count == 12

        ):
        
            previous_fy_quarterly_average = (

                previous_fy_sales

                / 4

            )
        
        
            forecast_qtr_avg_change_pct = (

                (

                    forecast_quarterly_average

                    - previous_fy_quarterly_average

                )

                / previous_fy_quarterly_average

                * 100

            )
        
        
            forecast_qtr_avg_delta = (

                f"{forecast_qtr_avg_change_pct:+.1f}% "

                f"vs {previous_fy_label} avg"

            )
        
        else:
        
            previous_fy_quarterly_average = None

            forecast_qtr_avg_change_pct = None
        
            forecast_qtr_avg_delta = (

                "Prior full FY unavailable"

            )
        
        
        # ============================================================

        # KPI 4 DELTA

        # FORECAST FY SALES VS PREVIOUS FY ACTUAL

        # ============================================================
        
        if (

            previous_fy_sales > 0

            and previous_fy_month_count == 12

        ):
        
            forecast_fy_change_pct = (

                (

                    forecast_fy_sales

                    - previous_fy_sales

                )

                / previous_fy_sales

                * 100

            )
        
        
            forecast_fy_delta = (

                f"{forecast_fy_change_pct:+.1f}% "

                f"vs {previous_fy_label}"

            )
        
        else:
        
            forecast_fy_change_pct = None
        
            forecast_fy_delta = (

                "Prior full FY unavailable"

            )
        # ============================================================

        # FORECAST KPI CARDS

        # ============================================================
        
        forecast_kpis = st.columns(

            3,

            gap="medium",

        )
        
        
        # ============================================================

        # 1. PROJECTED NEXT QUARTER

        # ============================================================
        
        forecast_kpis[0].metric(

            label="Projected Next Quarter",
        
            value=(

                f"₹{format_currency(next_quarter_forecast)}"

            ),
        
            delta=projected_qtr_delta,
        
            help=(

                "Forecast sales for the next financial quarter. "

                "The delta compares the next-quarter forecast "

                "with actual sales from the latest quarter."

            ),

        )
        
        
        
        
        # ============================================================

        # 3. FORECAST QUARTERLY AVERAGE

        # ============================================================
        
        forecast_kpis[1].metric(

            label="Forecast Quarterly Average",
        
            value=(

                f"₹{format_currency(forecast_quarterly_average)}"

            ),
        
            delta=forecast_qtr_avg_delta,
        
            help=(

                "Average quarterly sales expected for the "

                "forecast financial year. Calculated as forecast "

                "FY sales divided by four. The delta compares it "

                "with the previous full financial year's "

                "quarterly average."

            ),

        )
        
        
        # ============================================================

        # 4. FORECAST FY SALES

        # ============================================================
        
        forecast_kpis[2].metric(

            label=f"Forecast {current_forecast_fy} Sales",
        
            value=(

                f"₹{format_currency(forecast_fy_sales)}"

            ),
        
            delta=forecast_fy_delta,
        
            help=(

                "Expected full-year sales based on actual sales "

                "already achieved plus forecast sales for the "

                "remaining months. The delta compares the forecast "

                "with actual sales from the previous full FY."

            ),

        )
        
        
 
    # =========================================================

    # FORECASTING TABLE + TARGET / ACHIEVED / WMA CHART

    # =========================================================
    
    st.html(

        """
    <div class="section-header">
    <p class="section-title">

                Monthly Sales Forecast Performance
    </p>
    <p class="section-caption">

                Actual primary sales, available targets and 3-month

                weighted moving average forecast
    </p>
    </div>

        """

    )

    
    
    
    # =========================================================

    # 1. SALES SOURCE

    #

    # Forecast should use full historical timeline.

    # Ignore FY / Quarter / Month filters.

    # Keep business filters.

    # =========================================================
    
    forecast_sales_source = apply_filters(

        sales_mart,
    
        [],                     # FY

        [],                     # Quarter

        [],                     # Month
    
        selected_regions,

        selected_states,

        selected_hqs,

        selected_brands,

        selected_products,

    )
    
    
    # =========================================================

    # 2. MONTHLY ACTUAL SALES

    # =========================================================
    
    actual_monthly = (

        forecast_sales_source

        .dropna(

            subset=[

                MONTH_COLUMN

            ]

        )

        .groupby(

            MONTH_COLUMN,

            as_index=False,

            observed=True,

        )

        .agg(

            ACTUAL_SALES=(

                "NET_REVENUE",

                "sum",

            )

        )

        .sort_values(

            MONTH_COLUMN

        )

        .reset_index(drop=True)

    )
    
    
    actual_monthly[

        MONTH_COLUMN

    ] = pd.to_datetime(

        actual_monthly[

            MONTH_COLUMN

        ]

    )
    
    
    # =========================================================

    # 3. ALL AVAILABLE TARGETS

    #

    # Do NOT restrict to current forecast FY.

    # This allows FY2025-26 target to appear even if

    # FY2026-27 target has not yet been loaded.

    # =========================================================
    
    target_chart_source = apply_target_filters(

        target_mart,
    
        selected_years=[],          # all FYs

        selected_quarters=[],

        selected_months=[],
    
        selected_regions=selected_regions,

        selected_states=selected_states,

        selected_hqs=selected_hqs,

        selected_brands=selected_brands,

    )
    
    
    target_monthly = (

        target_chart_source

        .dropna(

            subset=[

                MONTH_COLUMN

            ]

        )

        .groupby(

            MONTH_COLUMN,

            as_index=False,

            observed=True,

        )

        .agg(

            TARGET_SALES=(

                "TARGET_SALES",

                "sum",

            )

        )

        .sort_values(

            MONTH_COLUMN

        )

        .reset_index(drop=True)

    )
    
    
    target_monthly[

        MONTH_COLUMN

    ] = pd.to_datetime(

        target_monthly[

            MONTH_COLUMN

        ]

    )
    
    
    # =========================================================

    # 4. BUILD 3-MONTH WMA FORECAST

    # =========================================================
    
    WMA_WEIGHTS = [

        0.20,

        0.30,

        0.50,

    ]
    
    
    if len(actual_monthly) < 3:
    
        st.warning(

            "At least 3 months of sales history are required "

            "to generate the WMA forecast."

        )
    
    else:
    
        # -----------------------------------------------------

        # Latest actual month

        # -----------------------------------------------------
    
        latest_actual_month = (

            actual_monthly[

                MONTH_COLUMN

            ].max()

        )

    
        # -----------------------------------------------------

        # Determine FY end

        #

        # Latest = Jun 2026

        # FY end = Mar 2027

        # -----------------------------------------------------
    
        if latest_actual_month.month >= 4:
    
            fy_end_year = (

                latest_actual_month.year

                + 1

            )
    
        else:
    
            fy_end_year = (

                latest_actual_month.year

            )
    
    
        fy_end_date = pd.Timestamp(

            year=fy_end_year,

            month=3,

            day=1,

        )
    
    
        # -----------------------------------------------------

        # Historical values

        # -----------------------------------------------------
    
        history_values = (

            actual_monthly[

                "ACTUAL_SALES"

            ]

            .astype(float)

            .tolist()

        )
    
    
        forecast_rows = []
    
    
        forecast_month = (

            latest_actual_month

            + pd.DateOffset(

                months=1

            )

        )
    
    
        # -----------------------------------------------------

        # Recursive WMA

        # -----------------------------------------------------
    
        while forecast_month <= fy_end_date:
    
            last_three = (

                history_values[-3:]

            )
    
    
            forecast_value = sum(

                value * weight
    
                for value, weight in zip(

                    last_three,

                    WMA_WEIGHTS,

                )

            )
    
    
            forecast_rows.append(

                {

                    MONTH_COLUMN:

                        forecast_month,
    
                    "FORECAST_SALES":

                        forecast_value,

                }

            )
    
    
            history_values.append(

                forecast_value

            )
    
    
            forecast_month = (

                forecast_month

                + pd.DateOffset(

                    months=1

                )

            )
    
    
        forecast_df = pd.DataFrame(

            forecast_rows

        )
    
    
        forecast_df[

            MONTH_COLUMN

        ] = pd.to_datetime(

            forecast_df[

                MONTH_COLUMN

            ]

        )
    
    
        # =====================================================

        # 5. BUILD MASTER MONTHLY TABLE

        # =====================================================
    
        forecast_performance_table = (

            actual_monthly
    
            .merge(

                target_monthly,

                on=MONTH_COLUMN,

                how="outer",

            )
    
            .merge(

                forecast_df,

                on=MONTH_COLUMN,

                how="outer",

            )
    
            .sort_values(

                MONTH_COLUMN

            )
    
            .reset_index(

                drop=True

            )

        )
    
    
        # =====================================================

        # 6. GAP / SURPLUS

        #

        # Calculate only where target AND actual exist.

        # =====================================================
    
        forecast_performance_table[

            "GAP_SURPLUS"

        ] = pd.NA
    
    
        comparable_mask = (

            forecast_performance_table[

                "TARGET_SALES"

            ].notna()
    &

            forecast_performance_table[

                "ACTUAL_SALES"

            ].notna()

        )
    
    
        forecast_performance_table.loc[

            comparable_mask,

            "GAP_SURPLUS"

        ] = (

            forecast_performance_table.loc[

                comparable_mask,

                "ACTUAL_SALES"

            ]

            -

            forecast_performance_table.loc[

                comparable_mask,

                "TARGET_SALES"

            ]

        )
    
    
        forecast_performance_table[

            "GAP_SURPLUS"

        ] = pd.to_numeric(

            forecast_performance_table[

                "GAP_SURPLUS"

            ],

            errors="coerce",

        )
    
    
        # =====================================================

        # 7. ACHIEVEMENT %

        # =====================================================
    
        forecast_performance_table[

            "ACHIEVEMENT_PERCENTAGE"

        ] = pd.NA
    
    
        achievement_mask = (

            comparable_mask
    &

            forecast_performance_table[

                "TARGET_SALES"

            ].ne(0)

        )
    
    
        forecast_performance_table.loc[

            achievement_mask,

            "ACHIEVEMENT_PERCENTAGE"

        ] = (

            forecast_performance_table.loc[

                achievement_mask,

                "ACTUAL_SALES"

            ]

            /

            forecast_performance_table.loc[

                achievement_mask,

                "TARGET_SALES"

            ]

            * 100

        )
    
    
        forecast_performance_table[

            "ACHIEVEMENT_PERCENTAGE"

        ] = pd.to_numeric(

            forecast_performance_table[

                "ACHIEVEMENT_PERCENTAGE"

            ],

            errors="coerce",

        )
    
    
        # =====================================================

        # 8. MONTH LABEL

        # =====================================================
    
        forecast_performance_table[

            "MONTH"

        ] = (

            forecast_performance_table[

                MONTH_COLUMN

            ]

            .dt.strftime(

                "%b %Y"

            )

        )
    
    
        # -----------------------------------------------------

        # Mark future rows

        # -----------------------------------------------------
    
        future_mask = (

            forecast_performance_table[

                "ACTUAL_SALES"

            ].isna()
    &

            forecast_performance_table[

                "FORECAST_SALES"

            ].notna()

        )
    
    
        forecast_performance_table.loc[

            future_mask,

            "MONTH"

        ] = (

            forecast_performance_table.loc[

                future_mask,

                "MONTH"

            ]

            + " · Forecast"

        )
    
    
        # =====================================================

        # 9. SEARCH

        # =====================================================
    
        forecast_search = st.text_input(

            "Search Month",

            placeholder=(

                "Search month, e.g. Apr 2025..."

            ),

            key="forecast_month_search",

        )
    
    
        filtered_forecast_table = (

            forecast_performance_table

            .copy()

        )
    
    
        if forecast_search:
    
            search_value = (

                forecast_search

                .strip()

                .upper()

            )
    
    
            filtered_forecast_table = (

                filtered_forecast_table.loc[

                    filtered_forecast_table[

                        "MONTH"

                    ]

                    .astype("string")

                    .str.upper()

                    .str.contains(

                        search_value,

                        na=False,

                        regex=False,

                    )

                ]

                .copy()

            )
    
    
        # =====================================================

        # 10. TOTALS

        # =====================================================
    
        total_target = (

            filtered_forecast_table[

                "TARGET_SALES"

            ]

            .dropna()

            .sum()

        )
    
    
        total_achieved = (

            filtered_forecast_table[

                "ACTUAL_SALES"

            ]

            .dropna()

            .sum()

        )
    
    
        total_forecast = (

            filtered_forecast_table[

                "FORECAST_SALES"

            ]

            .dropna()

            .sum()

        )
    
    
        # -----------------------------------------------------

        # Comparable totals

        #

        # Achievement should NOT compare months where

        # target is unavailable.

        # -----------------------------------------------------
    
        comparable_rows = (

            filtered_forecast_table.loc[

                filtered_forecast_table[

                    "TARGET_SALES"

                ].notna()
    &

                filtered_forecast_table[

                    "ACTUAL_SALES"

                ].notna()

            ]

        )
    
    
        comparable_target = (

            comparable_rows[

                "TARGET_SALES"

            ].sum()

        )
    
    
        comparable_achieved = (

            comparable_rows[

                "ACTUAL_SALES"

            ].sum()

        )
    
    
        total_gap_surplus = (

            comparable_achieved

            - comparable_target

        )
    
    
        total_achievement_pct = (

            (

                comparable_achieved

                / comparable_target

                * 100

            )
    
            if comparable_target != 0
    
            else None

        )
    
    
        # =====================================================

        # 11. FORMAT FUNCTION

        # =====================================================
    
        def display_currency(value):
    
            if pd.isna(value):
    
                return "—"
    
            return (

                f"₹{format_currency(float(value))}"

            )
    
    
        # =====================================================

        # 12. DISPLAY TABLE

        # =====================================================
    
        forecast_display = pd.DataFrame(

            {

                "MONTH":

                    filtered_forecast_table[

                        "MONTH"

                    ],
    
                "TARGET":

                    filtered_forecast_table[

                        "TARGET_SALES"

                    ]

                    .apply(

                        display_currency

                    ),
    
                "FORECAST (WMA)":

                    filtered_forecast_table[

                        "FORECAST_SALES"

                    ]

                    .apply(

                        display_currency

                    ),
    
                "ACHIEVED":

                    filtered_forecast_table[

                        "ACTUAL_SALES"

                    ]

                    .apply(

                        display_currency

                    ),
    
                "ACH %":

                    filtered_forecast_table[

                        "ACHIEVEMENT_PERCENTAGE"

                    ]

                    .apply(

                        lambda value:

                            (

                                f"{value:.1f}%"

                                if pd.notna(value)

                                else "—"

                            )

                    ),
    
                "GAP / SURPLUS":

                    filtered_forecast_table[

                        "GAP_SURPLUS"

                    ]

                    .apply(

                        lambda value:

                            (

                                (

                                    "+"

                                    if value >= 0

                                    else "-"

                                )

                                +

                                f"₹{

                                    format_currency(

                                        abs(value)

                                    )

                                }"

                            )
    
                            if pd.notna(value)
    
                            else "—"

                    ),

            }

        )
    
    
        # =====================================================

        # 13. TOTAL ROW

        # =====================================================
    
        total_row = pd.DataFrame(

            {

                "MONTH": [

                    "TOTAL"

                ],
    
                "TARGET": [

                    display_currency(

                        total_target

                    )

                ],
    
                "FORECAST (WMA)": [

                    display_currency(

                        total_forecast

                    )

                ],
    
                "ACHIEVED": [

                    display_currency(

                        total_achieved

                    )

                ],
    
                "ACH %": [

                    (

                        f"{total_achievement_pct:.1f}%"
    
                        if total_achievement_pct

                        is not None
    
                        else "—"

                    )

                ],
    
                "GAP / SURPLUS": [

                    (

                        "+"

                        if total_gap_surplus >= 0

                        else "-"

                    )

                    +

                    f"₹{

                        format_currency(

                            abs(total_gap_surplus)

                        )

                    }"

                ],

            }

        )
    
    
        forecast_display = pd.concat(

            [

                forecast_display,

                total_row,

            ],

            ignore_index=True,

        )
    
    
        st.dataframe(

            forecast_display,
    
            use_container_width=True,
    
            hide_index=True,
    
            height=560,
    
            column_config={
    
                "MONTH":

                    st.column_config.TextColumn(

                        "Month",

                        width="medium",

                    ),
    
                "TARGET":

                    st.column_config.TextColumn(

                        "Target",

                    ),
    
                "FORECAST (WMA)":

                    st.column_config.TextColumn(

                        "Forecast (WMA)",

                    ),
    
                "ACHIEVED":

                    st.column_config.TextColumn(

                        "Achieved",

                    ),
    
                "ACH %":

                    st.column_config.TextColumn(

                        "Ach %",

                    ),
    
                "GAP / SURPLUS":

                    st.column_config.TextColumn(

                        "Gap / Surplus",

                    ),

            },

        )

        
    
    
        # =====================================================

        # 14. CHART DATA IN CRORES

        # =====================================================
    
        chart_data = (

            forecast_performance_table

            .copy()

        )
    
    
        chart_data[

            "ACTUAL_CR"

        ] = (

            chart_data[

                "ACTUAL_SALES"

            ]

            / 10_000_000

        )
    
    
        chart_data[

            "TARGET_CR"

        ] = (

            chart_data[

                "TARGET_SALES"

            ]

            / 10_000_000

        )
    
    
        chart_data[

            "FORECAST_CR"

        ] = (

            chart_data[

                "FORECAST_SALES"

            ]

            / 10_000_000

        )
    
    
        # =====================================================

        # 15. CONNECT FORECAST TO LAST ACTUAL

        # =====================================================
    
        last_actual = (

            actual_monthly

            .sort_values(

                MONTH_COLUMN

            )

            .iloc[-1]

        )
    
    
        forecast_line = pd.concat(

            [

                pd.DataFrame(

                    {

                        MONTH_COLUMN: [

                            last_actual[

                                MONTH_COLUMN

                            ]

                        ],
    
                        "FORECAST_SALES": [

                            last_actual[

                                "ACTUAL_SALES"

                            ]

                        ],
    
                        "FORECAST_CR": [

                            last_actual[

                                "ACTUAL_SALES"

                            ]

                            / 10_000_000

                        ],

                    }

                ),
    
                forecast_df.assign(

                    FORECAST_CR=(

                        forecast_df[

                            "FORECAST_SALES"

                        ]

                        / 10_000_000

                    )

                ),

            ],
    
            ignore_index=True,

        )
    
    
        # =====================================================

        # 16. COMBINED CHART

        # =====================================================
    
        st.html(

            """
    <div class="section-header">
    <p class="section-title">

                    Sales, Target & Forecast — Monthly
    </p>
    <p class="section-caption">

                    Actual primary sales compared with available targets,

                    with 3-month WMA projected into future months
    </p>
    </div>

            """

        )
    
    
        fig_sales_forecast = go.Figure()
    
    
        # -----------------------------------------------------

        # ACHIEVED

        # -----------------------------------------------------
    
        fig_sales_forecast.add_trace(

            go.Bar(

                x=chart_data[

                    MONTH_COLUMN

                ],
    
                y=chart_data[

                    "ACTUAL_CR"

                ],
    
                name="Achieved",
    
                customdata=chart_data[

                    [

                        "ACTUAL_SALES",

                    ]

                ],
    
                hovertemplate=(

                    "<b>%{x|%b %Y}</b><br>"

                    "Achieved: ₹%{customdata[0]:,.0f}"

                    "<extra></extra>"

                ),

            )

        )
    
    
        # -----------------------------------------------------

        # TARGET

        # -----------------------------------------------------
    
        fig_sales_forecast.add_trace(

            go.Scatter(

                x=chart_data[

                    MONTH_COLUMN

                ],
    
                y=chart_data[

                    "TARGET_CR"

                ],
    
                mode="lines+markers",
    
                name="Target",
    
                connectgaps=False,
    
                customdata=chart_data[

                    [

                        "TARGET_SALES",

                    ]

                ],
    
                hovertemplate=(

                    "<b>%{x|%b %Y}</b><br>"

                    "Target: ₹%{customdata[0]:,.0f}"

                    "<extra></extra>"

                ),

            )

        )
    
    
        # -----------------------------------------------------

        # WMA FORECAST

        # -----------------------------------------------------
    
        fig_sales_forecast.add_trace(

            go.Scatter(

                x=forecast_line[

                    MONTH_COLUMN

                ],
    
                y=forecast_line[

                    "FORECAST_CR"

                ],
    
                mode="lines+markers",
    
                name="WMA Forecast",
    
                line=dict(

                    dash="dash",

                    width=3,

                ),
    
                customdata=forecast_line[

                    [

                        "FORECAST_SALES",

                    ]

                ],
    
                hovertemplate=(

                    "<b>%{x|%b %Y}</b><br>"

                    "WMA Forecast: ₹%{customdata[0]:,.0f}"

                    "<extra></extra>"

                ),

            )

        )
    
    
        # =====================================================

        # 17. CHART LAYOUT

        # =====================================================
    
        fig_sales_forecast.update_layout(
    
            height=470,
    
            hovermode="x unified",
    
            bargap=0.35,
    
            legend=dict(

                orientation="h",

                yanchor="bottom",

                y=1.02,

                xanchor="left",

                x=0,

            ),
    
            xaxis_title="Month",
    
            yaxis_title="Primary Sales (₹ Cr)",
    
            margin=dict(

                l=30,

                r=20,

                t=60,

                b=40,

            ),

        )
    
    
        fig_sales_forecast.update_yaxes(

            ticksuffix=" Cr",

            rangemode="tozero",

        )
    
    
        fig_sales_forecast.update_xaxes(

            dtick="M1",

            tickformat="%b '%y",

        )
    
    
        st.plotly_chart(

            fig_sales_forecast,

            use_container_width=True,

        )

# # =========================================================

# # MODEL BACKTEST

# # 3-MONTH WMA VS HOLT'S LINEAR TREND

# # =========================================================

# from statsmodels.tsa.holtwinters import Holt


# st.html(

#     """
# <div class="section-header">
# <p class="section-title">

#             Forecast Model Validation
# </p>
# <p class="section-caption">

#             Historical walk-forward test comparing 3-month WMA

#             with Holt's Linear Trend
# </p>
# </div>

#     """

# )


# # =========================================================

# # 1. FULL HISTORICAL SALES SOURCE

# #

# # Ignore FY / Quarter / Month filters for model history.

# # Keep business filters.

# # =========================================================

# model_test_sales = apply_filters(

#     sales_mart,

#     [],                     # FY

#     [],                     # Quarter

#     [],                     # Month

#     selected_regions,

#     selected_states,

#     selected_hqs,

#     selected_brands,

#     selected_products,

# )


# # =========================================================

# # 2. MONTHLY ACTUAL SALES

# # =========================================================

# model_monthly = (

#     model_test_sales

#     .dropna(

#         subset=[

#             MONTH_COLUMN

#         ]

#     )

#     .groupby(

#         MONTH_COLUMN,

#         as_index=False,

#         observed=True,

#     )

#     .agg(

#         ACTUAL_SALES=(

#             "NET_REVENUE",

#             "sum",

#         )

#     )

#     .sort_values(

#         MONTH_COLUMN

#     )

#     .reset_index(drop=True)

# )


# model_monthly[

#     MONTH_COLUMN

# ] = pd.to_datetime(

#     model_monthly[

#         MONTH_COLUMN

#     ]

# )


# # =========================================================

# # 3. CHECK HISTORY

# # =========================================================

# MIN_TRAIN_MONTHS = 6


# if len(model_monthly) <= MIN_TRAIN_MONTHS:

#     st.warning(

#         "At least 7 months of sales history are required "

#         "to compare the forecasting models."

#     )

# else:

#     actual_values = (

#         model_monthly[

#             "ACTUAL_SALES"

#         ]

#         .astype(float)

#         .tolist()

#     )


#     months = (

#         model_monthly[

#             MONTH_COLUMN

#         ]

#         .tolist()

#     )


#     # WMA weights:

#     # oldest → newest

#     WMA_WEIGHTS = [

#         0.20,

#         0.30,

#         0.50,

#     ]


#     test_results = []


#     # =====================================================

#     # 4. WALK-FORWARD BACKTEST

#     # =====================================================

#     #

#     # Example:

#     #

#     # Train Apr-Sep 2025

#     # Predict Oct 2025

#     #

#     # Then:

#     # Train Apr-Oct 2025

#     # Predict Nov 2025

#     #

#     # Continue until latest actual month.

#     # =====================================================

#     for i in range(

#         MIN_TRAIN_MONTHS,

#         len(actual_values)

#     ):

#         history = (

#             actual_values[:i]

#         )


#         actual = (

#             actual_values[i]

#         )


#         prediction_month = (

#             months[i]

#         )


#         # =================================================

#         # A. 3-MONTH WMA

#         # =================================================

#         last_three = (

#             history[-3:]

#         )


#         wma_prediction = sum(

#             value * weight

#             for value, weight in zip(

#                 last_three,

#                 WMA_WEIGHTS,

#             )

#         )


#         # =================================================

#         # B. HOLT'S LINEAR TREND

#         # =================================================

#         try:

#             holt_model = Holt(

#                 history,

#                 initialization_method=(

#                     "estimated"

#                 ),

#             ).fit(

#                 optimized=True

#             )


#             holt_prediction = float(

#                 holt_model.forecast(1)[0]

#             )


#         except Exception:

#             holt_prediction = None


#         # =================================================

#         # STORE RESULTS

#         # =================================================

#         test_results.append(

#             {

#                 "MONTH":

#                     prediction_month,

#                 "ACTUAL":

#                     actual,

#                 "WMA_PREDICTION":

#                     wma_prediction,

#                 "HOLT_PREDICTION":

#                     holt_prediction,

#             }

#         )


#     backtest_df = pd.DataFrame(

#         test_results

#     )


#     # =====================================================

#     # 5. REMOVE FAILED HOLT ROWS

#     # =====================================================

#     valid_backtest = (

#         backtest_df

#         .dropna(

#             subset=[

#                 "ACTUAL",

#                 "WMA_PREDICTION",

#                 "HOLT_PREDICTION",

#             ]

#         )

#         .copy()

#     )


#     if valid_backtest.empty:

#         st.warning(

#             "Model comparison could not be calculated."

#         )

#     else:

#         # =================================================

#         # 6. ABSOLUTE ERROR

#         # =================================================

#         valid_backtest[

#             "WMA_ERROR"

#         ] = (

#             valid_backtest[

#                 "ACTUAL"

#             ]

#             -

#             valid_backtest[

#                 "WMA_PREDICTION"

#             ]

#         ).abs()


#         valid_backtest[

#             "HOLT_ERROR"

#         ] = (

#             valid_backtest[

#                 "ACTUAL"

#             ]

#             -

#             valid_backtest[

#                 "HOLT_PREDICTION"

#             ]

#         ).abs()


#         # =================================================

#         # 7. MAE

#         # =================================================

#         wma_mae = (

#             valid_backtest[

#                 "WMA_ERROR"

#             ].mean()

#         )


#         holt_mae = (

#             valid_backtest[

#                 "HOLT_ERROR"

#             ].mean()

#         )


#         # =================================================

#         # 8. SELECT BETTER MODEL

#         # =================================================

#         if holt_mae < wma_mae:

#             best_model = (

#                 "Holt's Linear Trend"

#             )

#             best_mae = (

#                 holt_mae

#             )

#             mae_improvement = (

#                 (

#                     wma_mae

#                     - holt_mae

#                 )

#                 / wma_mae

#                 * 100

#             )

#         elif wma_mae < holt_mae:

#             best_model = (

#                 "3-Month WMA"

#             )

#             best_mae = (

#                 wma_mae

#             )

#             mae_improvement = (

#                 (

#                     holt_mae

#                     - wma_mae

#                 )

#                 / holt_mae

#                 * 100

#             )

#         else:

#             best_model = (

#                 "Both Equal"

#             )

#             best_mae = (

#                 wma_mae

#             )

#             mae_improvement = 0


#         # =================================================

#         # 9. KPI DISPLAY

#         # =================================================

#         model_cols = st.columns(4)


#         model_cols[0].metric(

#             "WMA MAE",

#             f"₹{format_currency(wma_mae)}",

#             help=(

#                 "Average absolute forecast error "

#                 "for the 3-month weighted moving average."

#             ),

#         )


#         model_cols[1].metric(

#             "Holt MAE",

#             f"₹{format_currency(holt_mae)}",

#             help=(

#                 "Average absolute forecast error "

#                 "for Holt's Linear Trend."

#             ),

#         )


#         model_cols[2].metric(

#             "Best Model",

#             best_model,

#         )


#         model_cols[3].metric(

#             "MAE Improvement",

#             f"{mae_improvement:.1f}%",

#             help=(

#                 "Percentage reduction in MAE compared "

#                 "with the less accurate model."

#             ),

#         )


#         # =================================================

#         # 10. FORMAT TEST TABLE

#         # =================================================

#         validation_display = (

#             valid_backtest[

#                 [

#                     "MONTH",

#                     "ACTUAL",

#                     "WMA_PREDICTION",

#                     "WMA_ERROR",

#                     "HOLT_PREDICTION",

#                     "HOLT_ERROR",

#                 ]

#             ]

#             .copy()

#         )


#         validation_display[

#             "MONTH"

#         ] = (

#             validation_display[

#                 "MONTH"

#             ]

#             .dt.strftime(

#                 "%b %Y"

#             )

#         )


#         # Convert monetary values to display format

#         for column in [

#             "ACTUAL",

#             "WMA_PREDICTION",

#             "WMA_ERROR",

#             "HOLT_PREDICTION",

#             "HOLT_ERROR",

#         ]:

#             validation_display[

#                 column

#             ] = (

#                 validation_display[

#                     column

#                 ]

#                 .apply(

#                     lambda value:

#                         f"₹{format_currency(value)}"

#                 )

#             )


#         validation_display = (

#             validation_display.rename(

#                 columns={

#                     "ACTUAL":

#                         "ACTUAL SALES",

#                     "WMA_PREDICTION":

#                         "WMA FORECAST",

#                     "WMA_ERROR":

#                         "WMA ERROR",

#                     "HOLT_PREDICTION":

#                         "HOLT FORECAST",

#                     "HOLT_ERROR":

#                         "HOLT ERROR",

#                 }

#             )

#         )


#         # =================================================

#         # 11. DISPLAY VALIDATION TABLE

#         # =================================================

#         with st.expander(

#             "View Model Backtest Details"

#         ):

#             st.dataframe(

#                 validation_display,

#                 use_container_width=True,

#                 hide_index=True,

#             )


#         # =================================================

#         # 12. FINAL RECOMMENDATION

#         # =================================================

#         st.info(

#             f"Based on walk-forward historical validation, "

#             f"**{best_model}** has the lower MAE "

#             f"(₹{format_currency(best_mae)}). "

#             f"Use this model for the forward forecast."

#         )

    