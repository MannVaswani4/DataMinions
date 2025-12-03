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

st.markdown("""
### Key Insight:
- **PM2.5/PM10:** Low-income countries dominate (Afghanistan, India)
- **Different pollutants = Different top countries**

### Top 5 Countries by Pollutant:

**PM2.5 (µg/m³):**
| Rank | Country | Value |
|------|---------|-------|
| 1 | Afghanistan | 136.00 |
| 2 | Mongolia | 118.00 |
| 3 | India | 100.70 |
| 4 | Bosnia and Herzegovina | 85.00 |
| 5 | Bangladesh | 84.00 |

**PM10 (µg/m³):**
| Rank | Country | Value |
|------|---------|-------|
| 1 | India | 187.55 |
| 2 | Mongolia | 171.39 |
| 3 | Mexico | 65.14 |
| 4 | Bosnia and Herzegovina | 64.90 |
| 5 | Peru | 63.35 |

**NO2 (ppm):**
| Rank | Country | Value |
|------|---------|-------|
| 1 | Ecuador | 37.67 |
| 2 | Australia | 0.36 |
| 3 | Mexico | 0.02 |

**O3 (ppm):**
| Rank | Country | Value |
|------|---------|-------|
| 1 | Republic of Korea | 0.05 |
| 2 | South Africa | 0.03 |
| 3 | United States | 0.03 |
""")
