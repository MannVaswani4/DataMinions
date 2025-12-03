import streamlit as st

st.set_page_config(
    page_title="Global Air Quality Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Air Quality Dashboard")
st.markdown("""
Welcome to Phase 3 of the **Air Quality Data Mining Project**.  
Use the sidebar to navigate across different analyses:
- Pollutant trends  
- Country comparisons  
- Correlation studies  
- Seasonal variations  
- ML predictions
""")
