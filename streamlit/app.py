import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Nassau Candy Factory Optimization",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_dashboard_data():

    recommendations = pd.read_csv(
        PROCESSED_DIR / "dashboard_recommendations.csv"
    )

    scenarios = pd.read_csv(
        PROCESSED_DIR / "dashboard_what_if.csv"
    )

    risk_impact = pd.read_csv(
        PROCESSED_DIR / "dashboard_risk_impact.csv"
    )

    kpis = pd.read_csv(
        PROCESSED_DIR / "optimization_kpis.csv"
    )

    raw_data = pd.read_csv(
        DATA_DIR / "Nassau Candy Distributor.csv"
    )

    return (
        recommendations,
        scenarios,
        risk_impact,
        kpis,
        raw_data
    )


(
    recommendations,
    scenarios,
    risk_impact,
    kpis,
    raw_data
) = load_dashboard_data()


# ============================================================
# KPI VALUES
# ============================================================

kpi_values = {
    row["KPI"]: row["Value"]
    for _, row in kpis.iterrows()
}

avg_lead_reduction = kpi_values.get(
    "Average Lead Time Reduction", 0
)

profit_stability = kpi_values.get(
    "Profit Impact Stability", 0
)

scenario_confidence = kpi_values.get(
    "Scenario Confidence Score", 0
)

recommendation_coverage = kpi_values.get(
    "Recommendation Coverage", 0
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("🎛️ Optimization Controls")

products = sorted(
    recommendations["Product Name"].dropna().unique()
)

regions = sorted(
    recommendations["Region"].dropna().unique()
)

ship_modes = sorted(
    raw_data["Ship Mode"].dropna().unique()
)


selected_product = st.sidebar.selectbox(
    "Product",
    ["All Products"] + products
)

selected_region = st.sidebar.selectbox(
    "Region",
    ["All Regions"] + regions
)

selected_ship_mode = st.sidebar.selectbox(
    "Ship Mode",
    ["All Ship Modes"] + ship_modes
)

st.sidebar.markdown("---")

st.sidebar.subheader("Optimization Priority")

speed_priority = st.sidebar.slider(
    "Speed Priority",
    min_value=0,
    max_value=100,
    value=70,
    step=10
)

profit_priority = 100 - speed_priority

st.sidebar.write(
    f"🚚 Speed: **{speed_priority}%**"
)

st.sidebar.write(
    f"💰 Profit: **{profit_priority}%**"
)

st.sidebar.info(
    "Profit priority uses profit stability because factory-specific "
    "operating costs are not available in the dataset."
)


# ============================================================
# FILTER RAW BUSINESS CONTEXT
# ============================================================

context_data = raw_data.copy()

if selected_product != "All Products":
    context_data = context_data[
        context_data["Product Name"] == selected_product
    ]

if selected_region != "All Regions":
    context_data = context_data[
        context_data["Region"] == selected_region
    ]

if selected_ship_mode != "All Ship Modes":
    context_data = context_data[
        context_data["Ship Mode"] == selected_ship_mode
    ]


# ============================================================
# FILTER SCENARIO DATA
# ============================================================

filtered_scenarios = scenarios.copy()

if selected_product != "All Products":
    filtered_scenarios = filtered_scenarios[
        filtered_scenarios["Product Name"]
        == selected_product
    ]

if selected_region != "All Regions":
    filtered_scenarios = filtered_scenarios[
        filtered_scenarios["Region"]
        == selected_region
    ]


# ============================================================
# FILTER RECOMMENDATIONS
# ============================================================

filtered_recommendations = recommendations.copy()

if selected_product != "All Products":
    filtered_recommendations = filtered_recommendations[
        filtered_recommendations["Product Name"]
        == selected_product
    ]

if selected_region != "All Regions":
    filtered_recommendations = filtered_recommendations[
        filtered_recommendations["Region"]
        == selected_region
    ]


# ============================================================
# FILTER RISK DATA
# ============================================================

filtered_risk = risk_impact.copy()

if selected_product != "All Products":
    filtered_risk = filtered_risk[
        filtered_risk["Product Name"]
        == selected_product
    ]

if selected_region != "All Regions":
    filtered_risk = filtered_risk[
        filtered_risk["Region"]
        == selected_region
    ]


# ============================================================
# TITLE
# ============================================================

st.title("🏭 Nassau Candy Factory Optimization")

st.markdown(
    "### Factory Reallocation & Shipping Optimization Recommendation System"
)

st.caption(
    "Decision intelligence dashboard for evaluating factory assignments, "
    "shipping efficiency, scenario outcomes, and operational risk."
)


# ============================================================
# SHIP MODE CONTEXT NOTICE
# ============================================================

if selected_ship_mode != "All Ship Modes":

    st.info(
        f"🚚 **Ship Mode Context:** {selected_ship_mode} is selected. "
        "Observed business metrics below are filtered to this ship mode. "
        "Factory scenario predictions remain based on the existing "
        "product-region simulation model."
    )


# ============================================================
# EXECUTIVE PERFORMANCE
# ============================================================

st.markdown("---")
st.subheader("📊 Executive Performance Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Avg Lead Time Reduction",
        f"{avg_lead_reduction:.2f}%"
    )

with col2:
    st.metric(
        "Profit Impact Stability",
        f"{profit_stability:.0f}%"
    )

with col3:
    st.metric(
        "Scenario Confidence",
        f"{scenario_confidence:.2f}%"
    )

with col4:
    st.metric(
        "Recommendation Coverage",
        f"{recommendation_coverage:.2f}%"
    )


# ============================================================
# OBSERVED BUSINESS CONTEXT
# ============================================================

st.markdown("---")
st.subheader("📦 Selected Business Context")

if len(context_data) > 0:

    context_orders = len(context_data)
    context_sales = context_data["Sales"].sum()
    context_profit = context_data["Gross Profit"].sum()

    context_lead = (
        context_data["Ship Date"]
        .notna()
        .sum()
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Observed Orders",
            f"{context_orders:,}"
        )

    with c2:
        st.metric(
            "Observed Sales",
            f"${context_sales:,.2f}"
        )

    with c3:
        st.metric(
            "Observed Gross Profit",
            f"${context_profit:,.2f}"
        )

    with c4:
        st.metric(
            "Records Available",
            f"{context_lead:,}"
        )

else:

    st.info(
        "No observed records match the selected filters."
    )


# ============================================================
# OPTIMIZATION FINDING
# ============================================================

st.markdown("---")

beneficial_count = (
    scenarios["Lead Time Reduction %"] > 0
).sum()

alternative_count = (
    scenarios["Scenario Factory"]
    != scenarios["Current Factory"]
).sum()

if beneficial_count == 0:

    st.warning(
        "⚠️ **Optimization Finding:** No alternative factory "
        "assignment produced a predicted lead-time improvement "
        "under the current model assumptions. The system therefore "
        "recommends retaining the current factory assignments."
    )

else:

    st.success(
        f"✅ {beneficial_count} potentially beneficial "
        "factory reassignment scenario(s) identified."
    )


# ============================================================
# FACTORY OPTIMIZATION SIMULATOR
# ============================================================

st.markdown("---")
st.header("🏭 Factory Optimization Simulator")

st.write(
    "Compare predicted shipping performance across available "
    "factory assignments."
)

simulator_data = filtered_scenarios.copy()

if len(simulator_data) > 0:

    if selected_product == "All Products":

        simulator_product = st.selectbox(
            "Select Product",
            sorted(
                simulator_data["Product Name"].unique()
            ),
            key="simulator_product"
        )

        simulator_data = simulator_data[
            simulator_data["Product Name"]
            == simulator_product
        ]

    if selected_region == "All Regions":

        if len(simulator_data) > 0:

            simulator_region = st.selectbox(
                "Select Region",
                sorted(
                    simulator_data["Region"].unique()
                ),
                key="simulator_region"
            )

            simulator_data = simulator_data[
                simulator_data["Region"]
                == simulator_region
            ]

    if len(simulator_data) > 0:

        current_factory = simulator_data[
            "Current Factory"
        ].iloc[0]

        current_lead = simulator_data[
            "Current Avg Lead Time"
        ].iloc[0]

        st.markdown(
            f"""
            **Current Factory:** `{current_factory}`  
            **Current Average Lead Time:** `{current_lead:.2f}`
            """
        )

        chart_data = simulator_data[
            [
                "Scenario Factory",
                "Predicted Lead Time"
            ]
        ].sort_values(
            "Predicted Lead Time"
        )

        fig = px.bar(
            chart_data,
            x="Scenario Factory",
            y="Predicted Lead Time",
            title="Predicted Lead Time by Factory",
            labels={
                "Scenario Factory": "Factory",
                "Predicted Lead Time": "Predicted Lead Time"
            },
            text_auto=".1f"
        )

        fig.update_layout(
            height=450,
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

else:

    st.info(
        "No factory scenario data matches the selected filters."
    )


# ============================================================
# WHAT-IF SCENARIO ANALYSIS
# ============================================================

st.markdown("---")
st.header("🔄 What-If Scenario Analysis")

st.write(
    "Evaluate the predicted impact of assigning a product-region "
    "combination to different factories."
)

what_if_data = filtered_scenarios.copy()

if len(what_if_data) > 0:

    if selected_product == "All Products":

        what_if_product = st.selectbox(
            "Select Product",
            sorted(
                what_if_data["Product Name"].unique()
            ),
            key="what_if_product"
        )

        what_if_data = what_if_data[
            what_if_data["Product Name"]
            == what_if_product
        ]

    if selected_region == "All Regions":

        if len(what_if_data) > 0:

            what_if_region = st.selectbox(
                "Select Region",
                sorted(
                    what_if_data["Region"].unique()
                ),
                key="what_if_region"
            )

            what_if_data = what_if_data[
                what_if_data["Region"]
                == what_if_region
            ]

    if len(what_if_data) > 0:

        current_factory = what_if_data[
            "Current Factory"
        ].iloc[0]

        what_if_data["Factory Status"] = np.where(
            what_if_data["Scenario Factory"]
            == current_factory,
            "Current Factory",
            "Alternative Factory"
        )

        fig = px.bar(
            what_if_data,
            x="Scenario Factory",
            y="Lead Time Reduction %",
            color="Factory Status",
            title="Predicted Lead-Time Change by Factory",
            labels={
                "Scenario Factory": "Factory",
                "Lead Time Reduction %":
                    "Lead Time Reduction (%)"
            },
            text_auto=".2f"
        )

        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color="white"
        )

        fig.update_layout(
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.caption(
            "Positive values indicate predicted improvement. "
            "Negative values indicate predicted deterioration."
        )

        st.dataframe(
            what_if_data[
                [
                    "Scenario Factory",
                    "Predicted Lead Time",
                    "Lead Time Improvement",
                    "Lead Time Reduction %",
                    "Distance km",
                    "Profit Margin %",
                    "Profit Impact Stable"
                ]
            ].sort_values(
                "Predicted Lead Time"
            ),
            use_container_width=True,
            hide_index=True
        )

else:

    st.info(
        "No what-if scenarios match the selected filters."
    )


# ============================================================
# DYNAMIC PRIORITY SCORING
# ============================================================

st.markdown("---")
st.header("⚖️ Priority-Based Scenario Ranking")

st.write(
    "The ranking below changes dynamically according to the "
    "Speed vs Profit priority selected in the sidebar."
)

ranking_data = filtered_scenarios.copy()

if len(ranking_data) > 0:

    # Normalize lead-time reduction.
    lead_min = ranking_data[
        "Lead Time Reduction %"
    ].min()

    lead_max = ranking_data[
        "Lead Time Reduction %"
    ].max()

    if lead_max != lead_min:

        ranking_data["Speed Score"] = (
            (ranking_data["Lead Time Reduction %"] - lead_min)
            / (lead_max - lead_min)
        )

    else:

        ranking_data["Speed Score"] = 0.0

    # Distance score: shorter distance = better score.
    distance_min = ranking_data[
        "Distance km"
    ].min()

    distance_max = ranking_data[
        "Distance km"
    ].max()

    if distance_max != distance_min:

        ranking_data["Distance Score"] = (
            1
            - (
                ranking_data["Distance km"] - distance_min
            )
            / (distance_max - distance_min)
        )

    else:

        ranking_data["Distance Score"] = 1.0

    # Profit stability score.
    ranking_data["Profit Score"] = (
        ranking_data["Profit Impact Stable"]
        .astype(int)
    )

    # Dynamic decision score.
    speed_weight = speed_priority / 100
    profit_weight = profit_priority / 100

    ranking_data["Dynamic Score"] = (
        speed_weight
        * ranking_data["Speed Score"]
        * 100
        +
        profit_weight
        * ranking_data["Profit Score"]
        * 100
    )

    ranking_data = ranking_data.sort_values(
        "Dynamic Score",
        ascending=False
    )

    st.dataframe(
        ranking_data[
            [
                "Product Name",
                "Region",
                "Current Factory",
                "Scenario Factory",
                "Lead Time Reduction %",
                "Distance km",
                "Profit Impact Stable",
                "Dynamic Score"
            ]
        ].head(15),
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No scenarios available for ranking."
    )


# ============================================================
# RECOMMENDATION DASHBOARD
# ============================================================

st.markdown("---")
st.header("💡 Recommendation Dashboard")

st.write(
    "Factory decisions generated from the optimization engine."
)

if len(filtered_recommendations) > 0:

    display_recommendations = (
        filtered_recommendations
        .copy()
        .sort_values(
            "Recommendation Score",
            ascending=False
        )
    )

    st.dataframe(
        display_recommendations[
            [
                "Product Name",
                "Region",
                "Current Factory",
                "Scenario Factory",
                "Lead Time Reduction %",
                "Distance km",
                "Profit Stability Score",
                "Recommendation Score",
                "Recommendation",
                "Status"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    recommendation_counts = (
        display_recommendations[
            "Recommendation"
        ]
        .value_counts()
        .reset_index()
    )

    recommendation_counts.columns = [
        "Recommendation",
        "Count"
    ]

    fig = px.bar(
        recommendation_counts,
        x="Recommendation",
        y="Count",
        title="Recommendation Distribution",
        text="Count"
    )

    fig.update_layout(
        height=400,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "No recommendations match the selected filters."
    )


# ============================================================
# RISK & IMPACT PANEL
# ============================================================

st.markdown("---")
st.header("⚠️ Risk & Impact Panel")

st.write(
    "Identify scenarios with potentially unfavorable "
    "lead-time outcomes."
)

if len(filtered_risk) > 0:

    risk_counts = (
        filtered_risk["Risk Level"]
        .value_counts()
        .reset_index()
    )

    risk_counts.columns = [
        "Risk Level",
        "Count"
    ]

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            risk_counts,
            names="Risk Level",
            values="Count",
            title="Scenario Risk Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        high_risk_count = (
            filtered_risk["Risk Level"]
            == "High Risk"
        ).sum()

        moderate_risk_count = (
            filtered_risk["Risk Level"]
            == "Moderate Risk"
        ).sum()

        st.metric(
            "High-Risk Scenarios",
            high_risk_count
        )

        st.metric(
            "Moderate-Risk Scenarios",
            moderate_risk_count
        )

        if high_risk_count > 0:

            st.error(
                f"⚠️ {high_risk_count} scenario(s) have "
                "predicted lead-time reduction below -10%."
            )

    st.subheader("Highest-Risk Scenarios")

    high_risk_table = (
        filtered_risk[
            filtered_risk["Risk Level"]
            == "High Risk"
        ]
        .sort_values(
            "Lead Time Reduction %"
        )
    )

    st.dataframe(
        high_risk_table[
            [
                "Product Name",
                "Region",
                "Current Factory",
                "Scenario Factory",
                "Lead Time Reduction %",
                "Profit Margin %",
                "Profit Impact Stable"
            ]
        ].head(15),
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No risk scenarios match the selected filters."
    )


# ============================================================
# EXECUTIVE DECISION SUMMARY
# ============================================================

st.markdown("---")
st.header("📌 Executive Decision Summary")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:

    st.subheader("Current Finding")

    st.write(
        f"""
        - **Scenarios evaluated:** {len(scenarios)}
        - **Alternative factory scenarios:** {alternative_count}
        - **Beneficial reassignment scenarios:** {beneficial_count}
        - **Recommendation coverage:** {recommendation_coverage:.2f}%
        """
    )

with summary_col2:

    st.subheader("Decision")

    if beneficial_count == 0:

        st.success(
            """
            **Retain the current factory assignments.**

            Under the current predictive model and geographic assumptions,
            no alternative factory produced a predicted lead-time improvement.
            The system therefore avoids recommending unnecessary factory
            reallocations.
            """
        )

    else:

        st.warning(
            """
            Potentially beneficial reassignment scenarios were identified.
            These should be reviewed with operational constraints before
            execution.
            """
        )


# ============================================================
# MODEL / DATA LIMITATIONS
# ============================================================

with st.expander("ℹ️ Model & Data Assumptions"):

    st.markdown(
        """
        **Important assumptions used by this dashboard:**

        - Factory assignments are inferred from the provided
          product-to-factory mapping.
        - Geographic distances use approximate regional coordinates,
          not exact customer addresses or road routes.
        - Scenario predictions were generated using the Gradient
          Boosting model developed during the optimization analysis.
        - The scenario confidence KPI is a model-performance proxy
          based on R².
        - Factory-specific operating costs are not available, so
          profit impact is treated as stable rather than predicting
          a true factory-level profit change.
        - The dataset contains unusually large order-to-ship date
          intervals; these values are retained as provided.
        - Ship Mode filters affect observed business context, while
          the saved factory scenario predictions remain based on
          the product-region simulation.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Nassau Candy Factory Optimization | "
    "Predictive Modeling + Scenario Simulation + Decision Intelligence"
)

st.caption(
    "Developed as an analytical decision-support system for "
    "factory allocation and shipping optimization."
)