# 🗳️ Election Result Forecasting using Bayesian Statistics

This is a **mini-project for the Artificial Intelligence & Machine Learning (AIML)** subject.

It predicts the probability of candidates winning an election using **Bayesian Statistics** and **Monte Carlo Simulation**, based on real constituency-wise data from the **2019 Indian General Election** and live user-provided survey data.

---

## 📌 Features

- 🧑‍💼 **CSV File Upload** to analyze real constituency-wise data
- 📊 **Past result visualization** (candidates, parties, and vote margins)
- 🎯 **Bayesian forecasting** using prior + survey votes
- 🔁 **10,000+ Monte Carlo simulations** for probability prediction
- 🧠 Uses **Beta distribution** for Bayesian updating
- 📈 **Pie charts, bar charts, and density plots** to visualize predictions
- 🖥️ Clean and modern **Streamlit-based web UI**

---

## 🚀 How It Works

1. Loads real past election data from a CSV file.
2. Allows the user to input **live survey votes**.
3. Applies **Bayesian updating** using:
   - Prior = past vote counts  
   - Likelihood = survey results
4. Samples from the **posterior distribution** using `scipy.stats.beta`.
5. Computes winning probability using **Monte Carlo simulations**.
6. Displays results using **interactive graphs** with Plotly and Matplotlib.

---

## 🧾 Dataset Format

The uploaded `.csv` file must include the following columns:


We use:
- `Leading Candidate`, `Leading Party`, `Trailing Candidate`, `Trailing Party`
- `Margin, Status` (be careful of the comma in this column name)
- `Constituency` for dropdown selection

Example dataset: [2019 Indian General Election – Constituency-wise](https://www.kaggle.com/datasets/vignesh9147/2019-indian-general-election-constituencywise)

---

## 📦 Libraries Used

- `numpy`
- `pandas`
- `scipy`
- `matplotlib`
- `plotly`
- `streamlit`

### 📥 Install all required packages:

```bash
pip install streamlit numpy pandas scipy matplotlib plotly
streamlit run election_forecast_app.py
💡 Sample Use Case
Predict the winning chances for a candidate from Mumbai South based on past results and a new survey of 100 people.

![image](https://github.com/user-attachments/assets/1819825e-5c94-4d8f-b2b0-898853c1b42f)
![image](https://github.com/user-attachments/assets/63c2fc4c-f42d-4030-bba5-c7bb7ec62d25)

