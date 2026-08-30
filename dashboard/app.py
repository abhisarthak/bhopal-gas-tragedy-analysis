import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# CHART THEME
# ============================================================

plt.rcParams.update({
    "figure.facecolor": "#0E1117",
    "axes.facecolor": "#0E1117",
    "axes.edgecolor": "#444444",
    "axes.labelcolor": "#E0E0E0",
    "text.color": "#E0E0E0",
    "xtick.color": "#CFCFCF",
    "ytick.color": "#CFCFCF",
    "grid.color": "#444444",
    "grid.alpha": 0.4,
    "axes.titlecolor": "#FFFFFF"
})

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Bhopal Gas Disaster | Decision Analysis",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"
IMAGES_DIR = BASE_DIR / "images"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    scenario_df = pd.read_csv(
        RESULTS_DIR / "scenario_analysis.csv"
    )

    summary_df = pd.read_csv(
        RESULTS_DIR / "simulation_summary.csv"
    )

    agent_df = pd.read_csv(
        RESULTS_DIR / "agent_exposure_results.csv"
    )

    return scenario_df, summary_df, agent_df


scenario_df, summary_df, agent_df = load_data()

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚨 Simulation Dashboard")

st.sidebar.markdown(
    """
    **Integrated Industrial Disaster Simulation**

    This dashboard analyzes the impact of emergency
    response delays on population exposure and risk.
    """
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Executive Overview",
        "📊 Emergency Response Analysis",
        "🗺️ Population Risk Analysis",
        "📈 Scenario Comparison",
        "🎯 Decision Insights"
    ]
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "🏠 Executive Overview":

    # --------------------------------------------------------
    # CALCULATIONS
    # --------------------------------------------------------

    total_population = len(agent_df)

    best_scenario = scenario_df.loc[
        scenario_df["average_exposure"].idxmin()
    ]

    worst_scenario = scenario_df.loc[
        scenario_df["average_exposure"].idxmax()
    ]

    best_risk_population = int(
        best_scenario["high_critical_risk_population"]
    )

    worst_risk_population = int(
        worst_scenario["high_critical_risk_population"]
    )

    risk_difference = (
        worst_risk_population - best_risk_population
    )

    exposure_reduction = scenario_df[
        "exposure_reduction_vs_40min_%"
    ].max()

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.title(
        "🚨 Bhopal Gas Disaster: Emergency Response Decision Analysis"
    )

    st.markdown(
        """
        ### Agent-Based Simulation of Population Exposure,
        Gas Dispersion and Emergency Evacuation

        **Decision Intelligence Dashboard for Evaluating the
        Impact of Emergency Response Delays**
        """
    )

    st.markdown("---")

    # --------------------------------------------------------
    # KPI METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Population Simulated",
        f"{total_population:,}"
    )

    col2.metric(
        "Best Scenario Risk Population",
        f"{best_risk_population:,}",
        f"{best_scenario['alarm_delay_min']:.0f} min alarm delay"
    )

    col3.metric(
        "Worst Scenario Risk Population",
        f"{worst_risk_population:,}",
        f"{worst_scenario['alarm_delay_min']:.0f} min alarm delay"
    )

    col4.metric(
        "Maximum Exposure Reduction",
        f"{exposure_reduction:.1f}%"
    )

    st.markdown("---")

    # ============================================================
    # KEY DECISION IMPACT
    # ============================================================

    st.subheader("⚠️ Key Decision Impact")

    impact_col1, impact_col2, impact_col3 = st.columns([2, 1, 1])

    with impact_col1:
        st.warning(
            f"""
            **Emergency response delays can significantly increase population risk.**

            A delay from **{int(best_scenario['alarm_delay_min'])} minutes**
            to **{int(worst_scenario['alarm_delay_min'])} minutes**
            increases the High/Critical Risk Population by:

            # {risk_difference:,} additional people
            """
        )

    with impact_col2:
        st.metric(
            "Risk Population Increase",
            f"{risk_difference:,} people"
        )

    with impact_col3:

        exposure_increase = (
            (
                worst_scenario["average_exposure"]
                - best_scenario["average_exposure"]
            )
            / best_scenario["average_exposure"]
            * 100
        )

        st.metric(
            "Exposure Increase",
            f"{exposure_increase:.1f}%"
        )

    st.markdown("---")

    # ============================================================
    # PROJECT OVERVIEW
    # ============================================================

    col1, col2 = st.columns([1.2, 1])

    with col1:

        st.subheader("Simulation Objective")

        st.write(
            """
            The simulation evaluates how delays in emergency alarms
            influence population exposure and the number of people
            classified under high or critical risk.

            Multiple emergency response scenarios are simulated,
            ranging from immediate alarm activation to a
            40-minute response delay.
            """
        )

        st.subheader("Key Decision Question")

        st.info(
            """
            **How much can rapid emergency warning reduce
            population exposure and high-risk population levels
            during an industrial gas release?**
            """
        )

    with col2:

        st.subheader("Scenario Summary")

        st.dataframe(
            scenario_df[
                [
                    "alarm_delay_min",
                    "average_exposure",
                    "high_critical_risk_population"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )
# ============================================================
# EMERGENCY RESPONSE ANALYSIS
# ============================================================

elif page == "📊 Emergency Response Analysis":

    # --------------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------------

    st.title("📊 Emergency Response Impact Analysis")

    st.markdown(
        """
        Evaluate how delays in emergency alarm activation affect
        population exposure and the High/Critical Risk Population.
        """
    )

    st.markdown("---")

    # --------------------------------------------------------
    # KEY CALCULATIONS
    # --------------------------------------------------------

    best_scenario = scenario_df.loc[
        scenario_df["average_exposure"].idxmin()
    ]

    worst_scenario = scenario_df.loc[
        scenario_df["average_exposure"].idxmax()
    ]

    risk_difference = (
        worst_scenario["high_critical_risk_population"]
        - best_scenario["high_critical_risk_population"]
    )

    exposure_increase = (
        (
            worst_scenario["average_exposure"]
            - best_scenario["average_exposure"]
        )
        / best_scenario["average_exposure"]
        * 100
    )

    risk_percentage_increase = (
        risk_difference
        / best_scenario["high_critical_risk_population"]
        * 100
    )

    # --------------------------------------------------------
    # KPI METRICS
    # --------------------------------------------------------

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "Best Alarm Delay",
        f"{best_scenario['alarm_delay_min']:.0f} min"
    )

    metric2.metric(
        "Worst Alarm Delay",
        f"{worst_scenario['alarm_delay_min']:.0f} min"
    )

    metric3.metric(
        "Additional People at High Risk",
        f"{int(risk_difference):,}"
    )

    metric4.metric(
        "Exposure Increase",
        f"{exposure_increase:.1f}%"
    )

    st.markdown("---")

    # ========================================================
    # DATA FOR CHARTS
    # ========================================================

    alarm_delay = scenario_df["alarm_delay_min"].tolist()

    average_exposure = scenario_df["average_exposure"].tolist()

    high_risk_population = (
        scenario_df[
            "high_critical_risk_population"
        ].tolist()
    )

    # ========================================================
    # TWO MAIN CHARTS
    # ========================================================

    st.subheader("📈 Impact of Emergency Response Delays")

    chart_col1, chart_col2 = st.columns(2)

    # --------------------------------------------------------
    # CHART 1 — POPULATION EXPOSURE
    # --------------------------------------------------------

    with chart_col1:

        fig_exposure, ax_exposure = plt.subplots(
            figsize=(7, 4)
        )

        ax_exposure.plot(
            alarm_delay,
            average_exposure,
            marker="o",
            linewidth=2.5,
            markersize=7
        )

        ax_exposure.set_title(
            "Alarm Delay vs Population Exposure",
            fontsize=13,
            pad=12
        )

        ax_exposure.set_xlabel(
            "Alarm Delay (Minutes)"
        )

        ax_exposure.set_ylabel(
            "Average Cumulative Exposure"
        )

        ax_exposure.grid(
            True,
            alpha=0.25
        )

        ax_exposure.spines["top"].set_visible(False)
        ax_exposure.spines["right"].set_visible(False)

        plt.tight_layout()

        st.pyplot(fig_exposure)

        plt.close(fig_exposure)

    # --------------------------------------------------------
    # CHART 2 — HIGH / CRITICAL RISK POPULATION
    # --------------------------------------------------------

    with chart_col2:

        import numpy as np

        fig_risk, ax_risk = plt.subplots(
            figsize=(7, 4)
        )

        # Even categorical positions
        x_pos = np.arange(len(alarm_delay))

        bars = ax_risk.bar(
            x_pos,
            high_risk_population,
            width=0.60,
            color="#ff6b6b"
        )

        ax_risk.set_xticks(x_pos)

        ax_risk.set_xticklabels(
            [f"{x} min" for x in alarm_delay]
        )

        ax_risk.set_title(
            "Growth of High/Critical Risk Population",
            fontsize=13,
            pad=12
        )

        ax_risk.set_xlabel(
            "Alarm Delay"
        )

        ax_risk.set_ylabel(
            "High/Critical Risk Population"
        )

        ax_risk.grid(
            axis="y",
            alpha=0.25
        )

        ax_risk.set_axisbelow(True)

        ax_risk.spines["top"].set_visible(False)
        ax_risk.spines["right"].set_visible(False)

        # Value labels
        for bar, value in zip(
            bars,
            high_risk_population
        ):

            ax_risk.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 15,
                f"{int(value)}",
                ha="center",
                va="bottom",
                fontsize=9
            )

        # Space above highest bar
        ax_risk.set_ylim(
            0,
            max(high_risk_population) * 1.12
        )

        plt.tight_layout()

        st.pyplot(fig_risk)

        plt.close(fig_risk)

    st.markdown("---")

    # ========================================================
    # DECISION IMPACT CHART
    # ========================================================

    st.subheader("⚠️ Additional Population at Risk")

    risk_increase = (
        scenario_df["high_critical_risk_population"]
        - scenario_df[
            "high_critical_risk_population"
        ].min()
    )

    fig_impact, ax_impact = plt.subplots(
        figsize=(10, 4.5)
    )

    ax_impact.plot(
        alarm_delay,
        risk_increase,
        marker="o",
        linewidth=2.5,
        markersize=7
    )

    ax_impact.fill_between(
        alarm_delay,
        risk_increase,
        alpha=0.20
    )

    ax_impact.set_title(
        "Additional Population at Risk Compared with Immediate Alarm",
        fontsize=14,
        pad=12
    )

    ax_impact.set_xlabel(
        "Alarm Delay (Minutes)"
    )

    ax_impact.set_ylabel(
        "Additional High/Critical Risk Population"
    )

    ax_impact.grid(
        True,
        alpha=0.25
    )

    ax_impact.spines["top"].set_visible(False)
    ax_impact.spines["right"].set_visible(False)

    plt.tight_layout()

    st.pyplot(fig_impact)

    plt.close(fig_impact)

    st.markdown("---")

    # ========================================================
    # DECISION INSIGHT
    # ========================================================

    st.subheader("🚨 Key Decision Insight")

    insight_col1, insight_col2 = st.columns([1.6, 1])

    with insight_col1:

        st.warning(
            f"""
            ### Emergency Response Recommendation

            Delaying the emergency alarm from
            **{int(best_scenario['alarm_delay_min'])} minutes**
            to **{int(worst_scenario['alarm_delay_min'])} minutes**
            increases the High/Critical Risk Population from
            **{int(best_scenario['high_critical_risk_population']):,}**
            to **{int(worst_scenario['high_critical_risk_population']):,} people**.

            **Impact:** An additional **{int(risk_difference):,} people**
            enter the High/Critical Risk category.

            Rapid emergency warning is therefore a critical
            controllable factor for reducing disaster impact.
            """
        )

    with insight_col2:

        st.metric(
            "Risk Increase",
            f"{risk_percentage_increase:.1f}%"
        )

        st.metric(
            "Additional People at Risk",
            f"{int(risk_difference):,}"
        )    

    
   

    
    
    
    
# ============================================================
# POPULATION RISK ANALYSIS
# ============================================================

elif page == "🗺️ Population Risk Analysis":

    st.title("🗺️ Population Exposure and Risk Distribution")

    if "risk_level" in agent_df.columns:

        risk_counts = (
            agent_df["risk_level"]
            .value_counts()
            .reset_index()
        )

        risk_counts.columns = [
            "Risk Level",
            "Population"
        ]

        col1, col2 = st.columns([1, 1.2])

        with col1:

            st.subheader("Risk Distribution")

            st.dataframe(
                risk_counts,
                use_container_width=True,
                hide_index=True
            )

        with col2:

            fig, ax = plt.subplots(figsize=(8, 5))

            ax.bar(
                risk_counts["Risk Level"],
                risk_counts["Population"]
            )

            ax.set_xlabel("Risk Category")
            ax.set_ylabel("Population")
            ax.set_title("Population Risk Classification")

            st.pyplot(fig)

    else:

        st.warning(
            "Risk classification data is not available in the exported dataset."
        )


# ============================================================
# SCENARIO COMPARISON
# ============================================================

elif page == "📈 Scenario Comparison":

    st.title("📈 Emergency Response Scenario Comparison")

    st.subheader("Scenario Results")

    st.dataframe(
        scenario_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    metric = st.selectbox(
        "Select Metric",
        [
            "average_exposure",
            "high_critical_risk_population",
            "exposure_reduction_vs_40min_%",
            "risk_reduction_vs_40min_%"
        ]
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(
        scenario_df["alarm_delay_min"].astype(str),
        scenario_df[metric]
    )

    ax.set_xlabel("Alarm Delay (minutes)")
    ax.set_ylabel(metric.replace("_", " ").title())

    ax.set_title(
        f"{metric.replace('_', ' ').title()} by Alarm Delay"
    )

    st.pyplot(fig)


# ============================================================
# DECISION INSIGHTS
# ============================================================

elif page == "🎯 Decision Insights":

    st.title("🎯 Decision Intelligence Insights")

    best_scenario = scenario_df.loc[
        scenario_df["average_exposure"].idxmin()
    ]

    worst_scenario = scenario_df.loc[
        scenario_df["average_exposure"].idxmax()
    ]

    st.subheader("Key Findings")

    st.success(
        f"""
**Best Emergency Response Scenario**

Alarm Delay: **{best_scenario['alarm_delay_min']} minutes**

Average Exposure: **{best_scenario['average_exposure']:.6f}**
"""
    )

    st.error(
        f"""
**Worst Emergency Response Scenario**

Alarm Delay: **{worst_scenario['alarm_delay_min']} minutes**

Average Exposure: **{worst_scenario['average_exposure']:.6f}**
"""
    )

    st.markdown("---")

    st.subheader("Operational Recommendation")

    st.info(
        """
The simulation demonstrates that rapid emergency warning
significantly reduces cumulative population exposure and
limits the growth of the high/critical-risk population.

**Decision Recommendation:**

Industrial emergency response systems should prioritize:

1. Rapid hazard detection
2. Immediate public warning systems
3. Predefined evacuation protocols
4. Real-time emergency response coordination
"""
    )

    st.markdown("---")

    st.subheader("Decision Impact")

    risk_difference = (
        worst_scenario["high_critical_risk_population"]
        - best_scenario["high_critical_risk_population"]
    )

    st.metric(
        "Additional High/Critical Risk Population Due to Delay",
        f"{int(risk_difference):,} people"
    )