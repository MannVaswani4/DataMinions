import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

st.title("🤖 PM2.5 Level Prediction (Random Forest)")

# Use absolute path or relative path from project root
data_path = os.path.join(os.path.dirname(__file__), "../../cleaned_data/analysis_ready.csv")
df = pd.read_csv(data_path)

# FEATURES
features = [c for c in df.columns if c not in ["mean_value_PM25", "country"]]

# Load your RF model (save using joblib)
# joblib.dump(model, "rf_model.pkl")
model_path = os.path.join(os.path.dirname(__file__), "../../models/rf_model.pkl")

try:
    import joblib
    model = joblib.load(model_path)
    st.success("Model Loaded Successfully!")
except:
    st.error(f"Model file not found at {model_path}. Train & save the model using joblib.")
    st.stop()

# Inputs
inputs = {}
for col in features:
    if df[col].dtype == "float64" or df[col].dtype == "int64":
        inputs[col] = st.number_input(col, float(df[col].median()))
    else:
        # Convert to string to handle mixed types (e.g. NaN and str) and ensure sortability
        unique_vals = df[col].astype(str).unique()
        inputs[col] = st.selectbox(col, sorted(unique_vals))

# Load Encoders
encoders_path = os.path.join(os.path.dirname(__file__), "../../models/encoders.pkl")
encoders = {}
if os.path.exists(encoders_path):
    encoders = joblib.load(encoders_path)

# Convert to DataFrame
input_df = pd.DataFrame([inputs])

# Encode categorical columns
for col, le in encoders.items():
    if col in input_df.columns:
        # Handle unseen labels by assigning a default or raising an error
        # Here we use a safe approach: map to known labels or use a default
        # For simplicity in this context, we'll try to transform, and if it fails (unseen label), 
        # we might need a fallback. However, since we populate selectbox from unique values,
        # it should be fine unless the model was trained on a different dataset version.
        # But wait, we populate selectbox from `df` which is loaded from CSV.
        # The model was trained on the same CSV.
        # So the labels should be consistent.
        # We need to ensure the input is string because we converted to string for selectbox.
        input_df[col] = input_df[col].astype(str)
        input_df[col] = le.transform(input_df[col])

# Ensure input_df has the same columns as the model expects
if hasattr(model, "feature_names_in_"):
    # Reorder and filter columns to match model's expected input
    input_df = input_df[model.feature_names_in_]
else:
    st.warning("Model does not have feature_names_in_ attribute. Prediction might fail if feature order is incorrect.")

# Predict
if st.button("Predict PM2.5 Level"):
    pred = model.predict(input_df)[0]
    st.metric("Predicted PM2.5 (µg/m³)", f"{pred:.2f}")
