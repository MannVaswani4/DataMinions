import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("❄️ Seasonal Variation (OpenAQ Raw Data)")

df = pd.read_csv("../cleaned_data/openaq_cleaned.csv")
poll = st.selectbox("Select Pollutant", ["PM25", "PM10", "NO2", "O3"])

df_p = df[df["parameter"] == poll]

monthly = df_p.groupby("measurement_month")["value"].mean()

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly.index, monthly.values, marker="o")
ax.set_title(f"Seasonal Pattern — {poll}")
ax.set_xlabel("Month")
ax.set_ylabel("Concentration")
ax.grid(alpha=0.3)

st.pyplot(fig)
