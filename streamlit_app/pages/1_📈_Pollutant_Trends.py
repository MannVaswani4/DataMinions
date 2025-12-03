import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📈 Pollutant Trends Over Time")

df = pd.read_csv("../cleaned_data/analysis_ready.csv")

pollutant = st.selectbox(
    "Select Pollutant",
    ["mean_value_PM25", "mean_value_PM10", "mean_value_NO2", "mean_value_O3"]
)

df_p = df[["year", pollutant]].dropna()
yearly = df_p.groupby("year")[pollutant].mean()

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(yearly.index, yearly.values, marker="o")
ax.set_title(f"{pollutant} Trend Over Time")
ax.set_xlabel("Year")
ax.set_ylabel(pollutant)
ax.grid(alpha=0.3)

st.pyplot(fig)
