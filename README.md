# 🗳️ Election Result Forecasting using Bayesian Statistics

This is a mini-project for the Artificial Intelligence & Machine Learning (AIML) subject.  
It predicts the probability of candidates winning an election using **Bayesian Statistics** and **Monte Carlo Simulation** based on past voter data and survey results.

---

## 📌 Features

- User-friendly interface using **Streamlit**
- Bayesian inference with **Beta distribution**
- Real-time prediction using **survey data**
- Probability simulation with **10,000+ Monte Carlo runs**
- Graphical visualization of the winning probability

---

## 🚀 How it works

1. Uses **past election vote counts** as prior knowledge.
2. Updates the prior using **new survey data** (Bayesian Updating).
3. Uses the **Beta distribution** to model uncertainty.
4. Runs thousands of simulations to estimate each candidate's chance of winning.

---

## 📦 Libraries Used

- `numpy`
- `scipy`
- `matplotlib`
- `streamlit`

Install all required packages:

```bash
pip install numpy scipy matplotlib streamlit
