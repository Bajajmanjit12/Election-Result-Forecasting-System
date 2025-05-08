import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta
import plotly.express as px

st.set_page_config(page_title="Election Forecast App", layout="wide")
st.markdown("""
    <style>
        .main {font-size:18px;}
        h1, h2, h3, h4, h5, h6 {color: #003366;}
        .stTabs [data-baseweb="tab"] {font-size: 18px; padding: 1rem;}
        .stTabs [data-baseweb="tab"]:hover {background-color: #f0f2f6;}
        .css-1v0mbdj.ef3psqc12 {padding-top: 2rem;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🗳 Election Forecast Dashboard</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Election CSV (e.g., consit2019.csv)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    st.subheader("📂 Uploaded Dataset")
    st.dataframe(df)

    constituencies = df['Constituency'].unique()
    selected_const = st.selectbox("Select Constituency", constituencies)
    const_data = df[df['Constituency'] == selected_const].iloc[0]

    past_votes_lead = 6000
    past_votes_trail = 4000
    alpha_prior = past_votes_lead + 1
    beta_prior = past_votes_trail + 1

    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Survey & Forecast", "Advanced Analysis", "Geographic View"])

    with tab1:
        st.subheader(f"📌 Overview - {selected_const}")
        st.markdown(f"*Leading Candidate:* {const_data['Leading Candidate']} ({const_data['Leading Party']})")
        st.markdown(f"*Trailing Candidate:* {const_data['Trailing Candidate']} ({const_data['Trailing Party']})")
        st.markdown(f"*Vote Margin:* {const_data['Margin']}")

    with tab2:
        st.subheader("🗳 Survey Input")
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            survey_lead = st.number_input(f"{const_data['Leading Candidate']} Votes", 0, 1000, 58)
        with col2:
            survey_trail = st.number_input(f"{const_data['Trailing Candidate']} Votes", 0, 1000, 42)
        with col3:
            n_simulations = st.slider("Simulations", 1000, 50000, 10000, step=1000)

        alpha_post = alpha_prior + survey_lead
        beta_post = beta_prior + survey_trail
        samples = beta.rvs(alpha_post, beta_post, size=n_simulations)

        prob_lead = np.mean(samples > 0.5)
        prob_trail = 1 - prob_lead

        st.subheader("📈 Forecast Results")
        pie_fig = px.pie(
            names=[const_data['Leading Candidate'], const_data['Trailing Candidate']],
            values=[prob_lead, prob_trail],
            title="Winning Probability",
            color_discrete_sequence=["#1f77b4", "#ff7f0e"]
        )
        st.plotly_chart(pie_fig, use_container_width=True)

        st.subheader("📊 Survey Vote Comparison")
        bar_fig = px.bar(
            x=[const_data['Leading Candidate'], const_data['Trailing Candidate']],
            y=[survey_lead, survey_trail],
            labels={'x': 'Candidate', 'y': 'Votes'},
            color=[const_data['Leading Candidate'], const_data['Trailing Candidate']],
        )
        st.plotly_chart(bar_fig, use_container_width=True)

        st.subheader("🔵 Posterior Distribution")
        x_vals = np.linspace(0, 1, 1000)
        y_vals = beta.pdf(x_vals, alpha_post, beta_post)
        fig, ax = plt.subplots(figsize=(4, 3))  # 👈 Reduced size here
        ax.plot(x_vals, y_vals)
        ax.axvline(0.5, color='red', linestyle='--')
        ax.set_title("Posterior Probability (Leading Candidate)", fontsize=12)
        ax.tick_params(axis='both', labelsize=10)
        st.pyplot(fig)


    with tab3:
        st.subheader("📌 Sensitivity Analysis")
        sens_lead = st.slider("Lead Votes", 0, 1000, value=survey_lead, key="sens_lead")
        sens_trail = st.slider("Trail Votes", 0, 1000, value=survey_trail, key="sens_trail")
        sens_sim = st.slider("Simulations", 1000, 50000, value=n_simulations, step=1000, key="sens_sim")

        alpha_post_sens = alpha_prior + sens_lead
        beta_post_sens = beta_prior + sens_trail
        sens_samples = beta.rvs(alpha_post_sens, beta_post_sens, size=sens_sim)

        # Removed outdated and static percentage display

    with tab4:
        st.subheader("🗺 Geographic Visualization")
        geo_df = df.copy()

        # Generate fake coordinates if needed
        if 'Latitude' not in geo_df.columns or 'Longitude' not in geo_df.columns:
            st.warning("🌍 Latitude/Longitude not found — generating random coordinates for map.")
            np.random.seed(42)
            geo_df['Latitude'] = np.random.uniform(20, 30, size=len(geo_df))
            geo_df['Longitude'] = np.random.uniform(70, 90, size=len(geo_df))

        fig_map = px.scatter_mapbox(
            geo_df,
            lat="Latitude",
            lon="Longitude",
            hover_name="Constituency",
            hover_data=["Leading Candidate", "Leading Party", "Margin"],
            color="Leading Party",
            zoom=4,
            height=600
        )
        fig_map.update_layout(mapbox_style="carto-positron")
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)
