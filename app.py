import streamlit as st
import pandas as pd
import plotly.express as px
from agents import generate_insights
from utils import clean_data, get_summary
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import io

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="InsightForge AI", layout="wide")
st.markdown("""
<style>

/* ===== Main Background ===== */
.stApp {
    background-color: #f5f7fa;
    color: #1f2937;
}

/* ===== Headers ===== */
h1 {
    color: #1d4ed8;
    font-weight: 700;
}

h2, h3 {
    color: #111827;
    font-weight: 600;
}

/* ===== KPI Cards ===== */
[data-testid="metric-container"] {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e5e7eb;
}

/* ===== Buttons ===== */
.stButton > button {
    background-color: #2874f0;
    color: white;
    border-radius: 8px;
    border: none;
    height: 45px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1d4ed8;
}

/* ===== Selectbox / Multiselect ===== */
div[data-baseweb="select"] > div {
    background-color: #ffffff;
    border-radius: 8px;
    border: 1px solid #d1d5db;
}

/* ===== Dataframe Styling ===== */
[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<div style="padding:25px;background:#2874f0;
border-radius:12px;margin-bottom:20px">
<h1 style="color:white;margin:0;">InsightForge AI</h1>
<p style="color:white;margin:0;">Executive Analytics Dashboard</p>
</div>
""", unsafe_allow_html=True)
st.title("InsightForge AI 🚀")
st.write("AI-Powered Executive Data Dashboard")

uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])

# ------------------- PDF GENERATOR -------------------
def generate_pdf_report(df, ai_text):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Executive Data Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"Total Rows: {len(df)}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("AI Executive Summary:", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(ai_text, styles["Normal"]))
    elements.append(Spacer(1, 0.4 * inch))

    table_data = [df.columns.tolist()] + df.head(10).values.tolist()
    table = Table(table_data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer

# ------------------- MAIN APP -------------------
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df = clean_data(df)

    # -------- SIDEBAR FILTERS --------
    st.sidebar.header("🔎 Filters")
    filtered_df = df.copy()

    if "category" in df.columns:
        selected_category = st.sidebar.multiselect(
            "Select Category",
            df["category"].unique(),
            default=df["category"].unique()
        )
        filtered_df = filtered_df[
            filtered_df["category"].isin(selected_category)
        ]

    if "year" in df.columns:
        selected_years = st.sidebar.multiselect(
            "Select Year",
            sorted(df["year"].unique()),
            default=sorted(df["year"].unique())
        )
        filtered_df = filtered_df[
            filtered_df["year"].isin(selected_years)
        ]

    # -------- RAW DATA PREVIEW --------
    with st.expander("📂 View Cleaned Dataset"):
        st.dataframe(filtered_df)

    numeric_cols = filtered_df.select_dtypes(
        include=['int64','float64']
    ).columns

    # -------- KPI SECTION --------
    st.subheader("📊 Executive KPI Dashboard")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Rows", len(filtered_df))
    with col2:
        st.metric("Total Columns", len(filtered_df.columns))
    with col3:
        st.metric("Numeric Features", len(numeric_cols))

    # -------- VISUALIZATION --------
    st.subheader("📈 Data Visualization")

    if len(numeric_cols) > 0:
        selected_col = st.selectbox(
            "Select metric to visualize",
            numeric_cols
        )

        if "year" in filtered_df.columns and selected_col != "year":
            grouped = filtered_df.groupby(
                "year", as_index=False
            )[selected_col].sum()

            fig = px.line(grouped, x="year", y=selected_col)
        else:
            fig = px.line(filtered_df, y=selected_col)

        st.plotly_chart(fig, use_container_width=True)

    # -------- FULLY AUTOMATED REPORT --------
    if st.button("🚀 Generate Full Executive Report"):

        summary = get_summary(filtered_df)

        with st.spinner("Generating AI Insights..."):
            insights = generate_insights(summary)

        st.subheader("🧠 Executive AI Summary")
        st.write(insights)

        # PDF Download
        pdf_file = generate_pdf_report(filtered_df, insights)

        st.download_button(
            label="📄 Download Executive PDF",
            data=pdf_file,
            file_name="executive_report.pdf",
            mime="application/pdf"
        )

        # Cleaned Dataset Download
        csv = filtered_df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="📊 Download Cleaned Dataset",
            data=csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )