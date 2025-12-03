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

st.markdown("""
### Key Findings:
1. **PM2.5 ↔ PM10: r = 0.901** (Strong Positive)
   - Same sources (combustion, dust)
   - PM2.5 is subset of PM10
2. **PM2.5 ↔ NO2: r = -0.295** (Weak Negative)
   - Different source profiles
   - NO2 = urban/traffic; PM2.5 = biomass/household
3. **PM10 ↔ O3: r = -0.616** (Moderate Negative)
   - Inverse relationship in country-level data

### Real Correlation Matrix:
|           | PM2.5 | PM10  | NO2   | O3    |
|-----------|-------|-------|-------|-------|
| **PM2.5** | 1.000 | **0.901** | -0.295 | -0.412 |
| **PM10**  | 0.901 | 1.000 | -0.293 | **-0.616** |
| **NO2**   | -0.295 | -0.293 | 1.000 | 0.040 |
| **O3**    | -0.412 | -0.616 | 0.040 | 1.000 |
""")
