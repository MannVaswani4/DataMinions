import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 Pollutant Correlation Analysis")

df = pd.read_csv("../cleaned_data/analysis_ready.csv")
pollutants = ["mean_value_PM25", "mean_value_PM10", "mean_value_NO2", "mean_value_O3"]

corr = df[pollutants].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, square=True, ax=ax)
ax.set_title("Correlation Heatmap")

st.pyplot(fig)
