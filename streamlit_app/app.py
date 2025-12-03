import streamlit as st

st.set_page_config(
    page_title="Global Air Quality Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Air Quality Intelligence Dashboard")

st.markdown("""
Welcome to the **Global Air Quality Intelligence Dashboard**, an interactive platform built using  
**OpenAQ real-time pollution data** and **World Bank socio-economic indicators**.

### 📌 Overview  
This project integrates environmental and economic data from over **100+ countries**, processes it through a  
robust data-cleaning pipeline, and visualizes key insights on global pollution trends.

The dashboard helps users understand:

- 🏭 **Pollutant levels** such as PM2.5, PM10, NO2, and O3  
- 📈 **Long-term trends** across countries and income groups  
- 🌍 **Comparisons between nations**  
- 🔗 **Correlations** between pollution, GDP, and urbanization  
- ❄️ **Seasonal patterns** (winter vs summer pollution)  
- 🤖 **Machine learning predictions** for PM2.5 based on economic and environmental factors  

---

### 🎯 Purpose of the Project  
The goal of this system is to:

- Provide **researchers** with accurate, cleaned multi-source environmental data  
- Help **students and analysts** understand pollution dynamics through visual exploration  
- Enable **policy-makers** to identify high-pollution regions  
- Showcase how **data engineering + visualization + ML** can be combined to extract actionable insights  

---

### 🧠 How It Works  
This dashboard is powered by:

- **OpenAQ API v3** – Live air quality measurements  
- **World Bank Indicators** – GDP per capita, urbanization, PM2.5 exposure  
- **Custom ETL Pipeline** – Cleaning, validation, merging, aggregation  
- **Feature Engineering** – AQI category, composite pollution index, completeness scoring  
- **Machine Learning Model** – Random Forest to predict PM2.5 levels  

---

Use the sidebar on the left to navigate across:

✔ Pollutant Trends  
✔ Country Comparisons  
✔ Correlation Explorer  
✔ Seasonal Variations  
✔ ML Predictions  

Enjoy exploring the global air quality landscape! 🌱
""")
