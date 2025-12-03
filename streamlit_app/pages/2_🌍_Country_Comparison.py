import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🌍 Country Comparison")

df = pd.read_csv("../cleaned_data/analysis_ready.csv")
pollutant = st.selectbox(
    "Select Pollutant",
    ["mean_value_PM25", "mean_value_PM10", "mean_value_NO2", "mean_value_O3"]
)

top_n = st.slider("Number of Countries", 5, 20, 10)

country_avg = df.groupby("country")[pollutant].mean().sort_values(ascending=False).head(top_n)

fig, ax = plt.subplots(figsize=(10, 5))
country_avg.plot(kind="bar", ax=ax)
ax.set_title(f"Top {top_n} Countries by {pollutant}")
ax.set_ylabel(pollutant)
ax.set_xticklabels(country_avg.index, rotation=45)

st.pyplot(fig)
