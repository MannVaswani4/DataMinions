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

st.markdown("""
### Key Observations:
- **PM2.5 & PM10:** Relatively stable (slight increase)
- **NO2:** No significant change
- **O3:** Slight upward trend (+3.4%)

### Real Data Results (2010-2023):
| Pollutant | 2010 Value | 2023 Value | Change |
|-----------|------------|------------|--------|
| **PM2.5** | 26.94 µg/m³ | 27.20 µg/m³ | +1.0% |
| **PM10** | 30.67 µg/m³ | 30.70 µg/m³ | +0.1% |
| **NO2** | 2.39 ppm | 2.39 ppm | +0.0% |
| **O3** | 0.02 ppm | 0.02 ppm | +3.4% |
""")
