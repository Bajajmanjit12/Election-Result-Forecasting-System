import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta
import plotly.express as px

# Set up Streamlit UI
st.set_page_config(page_title="Election Forecasting App", layout="wide")

st.markdown("<h1 style='text-align: center; font-size: 36px;'>🗳️ Election Result Forecasting using Bayesian Statistics</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Use real election data and Bayesian inference to forecast winning probabilities of candidates!</p>", unsafe_allow_html=True)

# Upload CSV
uploaded_file = st.sidebar.file_uploader("📂 Upload Election CSV File (e.g., consit2019.csv)", type=['csv'])

if uploaded_file:
    # Read and clean CSV
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()  # Remove any extra spaces from column names
    st.sidebar.success("✅ File uploaded!")

    # Show all available constituencies
    constituencies = df['Constituency'].unique()
    selected_const = st.sidebar.selectbox("🏙️ Select a Constituency", constituencies)

    # Filter data for selected constituency
    const_data = df[df['Constituency'] == selected_const].iloc[0]

    # Display past election details
    st.markdown(f"<h2 style='font-size: 28px;'>📜 Past Election Result: {selected_const}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px;'><strong>Leading Candidate:</strong> {const_data['Leading Candidate']} ({const_data['Leading Party']})</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px;'><strong>Trailing Candidate:</strong> {const_data['Trailing Candidate']} ({const_data['Trailing Party']})</p>", unsafe_allow_html=True)
    
    # Safe access to margin column
    margin_column = 'Margin'
    if margin_column in const_data:
        st.markdown(f"<p style='font-size: 18px;'><strong>Vote Margin and Status:</strong> {const_data[margin_column]}</p>", unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ '{margin_column}' column not found in the data.")

    # Inputs: survey data
    st.sidebar.header("📋 Enter Current Survey Data")
    survey_lead = st.sidebar.number_input(f"Survey Votes for {const_data['Leading Candidate']}", 0, 1000, 58)
    survey_trail = st.sidebar.number_input(f"Survey Votes for {const_data['Trailing Candidate']}", 0, 1000, 42)
    n_simulations = st.sidebar.slider("🎲 Number of Simulations", 1000, 50000, 10000, step=1000)

    # Bayesian prior using dummy historical vote assumption
    past_votes_lead = 6000
    past_votes_trail = 4000

    alpha_prior = past_votes_lead + 1
    beta_prior = past_votes_trail + 1

    # Bayesian update with survey
    alpha_post = alpha_prior + survey_lead
    beta_post = beta_prior + survey_trail

    samples = beta.rvs(alpha_post, beta_post, size=n_simulations)
    prob_lead = np.mean(samples > 0.5)
    prob_trail = 1 - prob_lead

    # Prediction output
    st.markdown("<h2 style='font-size: 28px;'>📈 Predicted Win Probability</h2>", unsafe_allow_html=True)
    pie_fig = px.pie(
        names=[const_data['Leading Candidate'], const_data['Trailing Candidate']],
        values=[prob_lead, prob_trail],
        title="Winning Probability Forecast",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"]
    )
    st.plotly_chart(pie_fig, use_container_width=True)

    # Survey bar chart
    st.markdown("<h2 style='font-size: 28px;'>📊 Survey Vote Comparison</h2>", unsafe_allow_html=True)
    bar_fig = px.bar(
        x=[const_data['Leading Candidate'], const_data['Trailing Candidate']],
        y=[survey_lead, survey_trail],
        labels={'x': 'Candidate', 'y': 'Survey Votes'},
        color=[const_data['Leading Candidate'], const_data['Trailing Candidate']],
        title="Entered Survey Votes"
    )
    st.plotly_chart(bar_fig, use_container_width=True)

    # Posterior plot using matplotlib
    st.markdown("<h2 style='font-size: 28px;'>🔵 Bayesian Posterior Distribution</h2>", unsafe_allow_html=True)
    x_vals = np.linspace(0, 1, 1000)
    y_vals = beta.pdf(x_vals, alpha_post, beta_post)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x_vals, y_vals, color='green', label='Posterior')
    ax.axvline(0.5, color='red', linestyle='--', label='50% Threshold')
    ax.set_title("Posterior Probability of Winning (Leading Candidate)")
    ax.set_xlabel("Winning Probability")
    ax.set_ylabel("Density")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.success("✅ Forecast Completed Successfully!")
else:
    st.info("⬅️ Please upload a valid election CSV file to begin.")
