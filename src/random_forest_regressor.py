import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import joblib
import os

# ----------------------------------------
# 1. Load Data
# ----------------------------------------
# Use absolute path or relative path from project root
data_path = os.path.join(os.path.dirname(__file__), "../cleaned_data/analysis_ready.csv")
df = pd.read_csv(data_path)
print("Initial Shape:", df.shape)

# ----------------------------------------
# 2. REMOVE EXACT DUPLICATES
# ----------------------------------------
df = df.drop_duplicates()
df = df.drop_duplicates(subset=["country", "year"], keep="first")  
print("After Removing Duplicates:", df.shape)

# ----------------------------------------
# 3. DROP CONSTANT / NON-VARYING COLUMNS
# ----------------------------------------
constant_cols = [
    'mean_value_CO','mean_value_NO2','mean_value_O3',
    'mean_value_PM10',
    'median_value_CO','median_value_NO2','median_value_O3',
    'median_value_PM10','median_value_PM25',
    'measurement_count_CO','measurement_count_NO2',
    'measurement_count_O3','measurement_count_PM10','measurement_count_PM25',
    'num_locations_CO','num_locations_NO2','num_locations_O3',
    'num_locations_PM10','num_locations_PM25',
    'urban_pollution_index',
    'urbanization_level',
    'aqi_category_pm25',
    'country'
]

print(df.columns)

df = df.drop(columns=[c for c in constant_cols if c in df.columns], errors='ignore')
print("After Removing Constant Columns:", df.shape)

# ----------------------------------------
# 4. REMOVE HIGH-LEAKAGE COLUMNS
# ----------------------------------------
leakage_cols = [
    "pm25_exposure",
    "pm25_per_gdp",
    "composite_pollution_index"
]

df = df.drop(columns=[c for c in leakage_cols if c in df.columns], errors='ignore')
print("After Removing Leakage Columns:", df.shape)

# ----------------------------------------
# 5. DROP METADATA COLUMNS
# ----------------------------------------
meta_drop = ["country_code"]
df = df.drop(columns=[c for c in meta_drop if c in df.columns], errors='ignore')
print("After Dropping Metadata:", df.shape)

# ----------------------------------------
# 6. Remove zero-variance columns
# ----------------------------------------
zero_var_cols = df.columns[df.nunique() <= 1].tolist()
df = df.drop(columns=zero_var_cols, errors='ignore')
print("After Zero Variance Removal:", df.shape)
print(df.columns);
# ----------------------------------------
# 7. Ensure Target Exists
# ----------------------------------------
if "mean_value_PM25" not in df.columns:
    raise ValueError("Target column mean_value_PM25 is missing!")

df = df.dropna(subset=["mean_value_PM25"])

# ----------------------------------------
# 8. TYPE-SAFE IMPUTATION (IMPORTANT)
# ----------------------------------------

# 8A. Numeric columns → convert to numeric + median fill
numeric_cols = df.select_dtypes(include=[np.number]).columns

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df[col] = df[col].fillna(df[col].median())

# 8B. Categorical columns → convert to string + mode fill
categorical_cols = df.select_dtypes(include=["object"]).columns

for col in categorical_cols:
    df[col] = df[col].astype(str)
    df[col] = df[col].fillna(df[col].mode()[0])

# ----------------------------------------
# 9. Label Encode Categorical Features
# ----------------------------------------
model_dir = os.path.join(os.path.dirname(__file__), "../models")
os.makedirs(model_dir, exist_ok=True)

encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# Save Encoders
encoders_path = os.path.join(model_dir, "encoders.pkl")
joblib.dump(encoders, encoders_path)
print(f"Encoders saved to {encoders_path}")

# ----------------------------------------
# 10. Define Feature Set
# ----------------------------------------
feature_cols = [c for c in df.columns if c != "mean_value_PM25"]
X = df[feature_cols]
y = df["mean_value_PM25"]

print("Final Feature Count:", len(feature_cols))
print("Final X Shape:", X.shape)

# ----------------------------------------
# 11. Train-Test Split
# ----------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ----------------------------------------
# 12. Train Random Forest
# ----------------------------------------
model = RandomForestRegressor(
    n_estimators=400,
    max_depth=None,
    random_state=42
)

model.fit(X_train, y_train)

# ----------------------------------------
# 13. Evaluate Model
# ----------------------------------------
y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)

print("\nMODEL PERFORMANCE:")
print(f"R² Score: {r2:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"MAE: {mae:.4f}")

# ----------------------------------------
# 14. Save Model
# ----------------------------------------
model_dir = os.path.join(os.path.dirname(__file__), "../models")
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "rf_model.pkl")
joblib.dump(model, model_path)
print(f"Model saved to {model_path}")

# ----------------------------------------
# 15. Feature Importance Plot
# ----------------------------------------
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 6))
plt.title("Feature Importance", fontsize=15)
plt.bar(range(len(importances)), importances[indices])
plt.xticks(range(len(importances)), X.columns[indices], rotation=90)
plt.tight_layout()
# plt.show() # Commented out to avoid blocking execution in non-interactive environments
