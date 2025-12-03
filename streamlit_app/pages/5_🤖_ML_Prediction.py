import streamlit as st
import pandas as pd
import joblib
import numpy as np

st.title("🤖 PM2.5 Level Prediction (Random Forest)")

df = pd.read_csv("../cleaned_data/analysis_ready.csv")

# FEATURES
features = [c for c in df.columns if c not in ["mean_value_PM25", "country"]]

# Load your RF model (save using joblib)
# joblib.dump(model, "rf_model.pkl")
model_path = "rf_model.pkl"

try:
    import joblib
    model = joblib.load(model_path)
    st.success("Model Loaded Successfully!")
except:
    st.error("Model file not found. Train & save the model using joblib.")
    st.stop()

# Inputs
inputs = {}
for col in features:
    if df[col].dtype == "float64" or df[col].dtype == "int64":
        inputs[col] = st.number_input(col, float(df[col].median()))
    else:
        inputs[col] = st.selectbox(col, sorted(df[col].unique()))

# Convert to DataFrame
input_df = pd.DataFrame([inputs])

# Predict
if st.button("Predict PM2.5 Level"):
    pred = model.predict(input_df)[0]
    st.metric("Predicted PM2.5 (µg/m³)", f"{pred:.2f}")
