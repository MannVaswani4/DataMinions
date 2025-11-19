# Hypothesis Testing Guide

## Overview

This folder contains 5 Jupyter notebooks for comprehensive hypothesis testing on air quality data. Each notebook tests a specific hypothesis with appropriate statistical methods and visualizations.

---

## 📊 Notebooks Summary

### **HY1: Urbanization Effect**
**File:** `HY1_Urbanization_Effect.ipynb`

**Hypothesis:**
- H1a: Urbanization ↑ → PM₂.₅ ↑ (positive correlation)
- H1b: Urbanization ↑ → O₃ ↓ (negative correlation)

**Methods:**
- Pearson correlation coefficient
- PCA (Principal Component Analysis)
- K-Means clustering (k=3)
- Statistical significance testing

**Visualizations:**
- Correlation heatmap
- Scatter plots with regression lines
- PCA biplot
- 3D cluster plot
- K-Means cluster visualization

**Key Metrics:**
- Pearson r and p-values
- PCA loadings and explained variance
- Cluster centroids

---

### **HY2: Environmental Kuznets Curve**
**File:** `HY2_Environmental_Kuznets_Curve.ipynb`

**Hypothesis:**
Economic development follows an inverted-U relationship with pollution:
- Early stage: GDP ↑ → Pollution ↑
- Later stage: GDP ↑ → Pollution ↓

**Methods:**
- Polynomial (quadratic) regression
- Linear vs quadratic model comparison
- ANOVA F-test for model significance
- K-Means clustering (k=4)
- Income category analysis

**Visualizations:**
- Scatter plot with linear and quadratic fits
- GDP bins boxplot
- Income category boxplot
- Clustered scatter plot with EKC curve

**Key Metrics:**
- R² (linear vs quadratic)
- F-statistic and p-value
- Turning point (peak pollution GDP level)
- Quadratic coefficients

---

### **HY3: Policy Impact (Post-2015)**
**File:** `HY3_Policy_Impact_Post2015.ipynb`

**Hypothesis:**
Developed nations show improved air quality after 2015 due to stricter environmental regulations.

**Methods:**
- Independent t-test (pre vs post 2015)
- Paired t-test (country-level)
- Linear trend analysis (slope calculation)
- CAGR (Compound Annual Growth Rate)
- Moving average trend

**Visualizations:**
- Time series with trend lines
- Pre vs post bar comparison
- Moving average plot
- Country-level change bars

**Key Metrics:**
- t-statistics and p-values
- Mean PM₂.₅ (pre vs post)
- Percentage change
- Trend slopes
- CAGR

---

### **HY4: Pollutant Correlation**
**File:** `HY4_Pollutant_Correlation.ipynb`

**Hypothesis:**
PM₂.₅, PM₁₀, and NO₂ are strongly correlated due to shared emission sources.

**Methods:**
- Pearson correlation matrix
- Statistical significance testing
- PCA analysis
- Pairwise relationships

**Visualizations:**
- Correlation heatmap
- Pairplot (scatter matrix)
- PCA variance plot

**Key Metrics:**
- Pearson correlation coefficients
- P-values for all pairs
- Expected correlations:
  - PM₂.₅-PM₁₀: r ≈ 0.8-0.9
  - PM₂.₅-NO₂: r ≈ 0.6-0.8

---

### **HY5: Seasonal Hemispheric Variation**
**File:** `HY5_Seasonal_Hemispheric_Variation.ipynb`

**Hypothesis:**
- NH (Northern Hemisphere): Winter pollution peak
- SH (Southern Hemisphere): Summer ozone peak / lower winter PM₂.₅

**Methods:**
- Monthly aggregation by hemisphere
- Seasonal comparison t-tests
- Peak month detection
- Cross-hemisphere comparison

**Visualizations:**
- Monthly line charts (NH vs SH)
- Seasonality heatmaps
- Hemisphere comparison plots

**Key Metrics:**
- Monthly mean pollutant levels
- Seasonal amplitude
- Peak months (winter: 12,1,2; summer: 6,7,8)
- T-test for seasonal differences

---

## 🚀 How to Run

### 1. Prerequisites

```bash
# Install required packages
pip install pandas numpy matplotlib seaborn scipy scikit-learn jupyter

# Or use requirements.txt
pip install -r requirements.txt
```

### 2. Prepare Data

```bash
# From project root, run data pipeline
python fetch_data.py
python clean_data.py
```

This creates: `cleaned_data/analysis_ready.csv` and `cleaned_data/openaq_cleaned.csv`

### 3. Launch Jupyter

```bash
# From project root
jupyter notebook

# Navigate to notebooks/ folder
# Open any HY*.ipynb file
```

### 4. Run Notebooks

- Open a notebook
- Click **Cell → Run All** (or run cells individually)
- Visualizations will be saved to `visualizations/` folder

---

## 📁 Data Files Used

| Notebook | Data File | Key Columns |
|----------|-----------|-------------|
| HY1 | analysis_ready.csv | urban_population_pct, mean_value_PM25, mean_value_O3 |
| HY2 | analysis_ready.csv | gdp_per_capita, mean_value_PM25, income_category |
| HY3 | analysis_ready.csv | year, mean_value_PM25, income_category |
| HY4 | analysis_ready.csv | All mean_value_* columns |
| HY5 | openaq_cleaned.csv | latitude, measurement_month, parameter, value |

---

## 📈 Expected Output

Each notebook generates:

1. **Statistical Results**
   - Test statistics (t, F, r, p-values)
   - Effect sizes
   - Confidence intervals

2. **Visualizations**
   - Saved to `visualizations/` folder
   - High-resolution PNG files (300 dpi)
   - Publication-ready plots

3. **Summary Conclusions**
   - Hypothesis supported/not supported
   - Key insights
   - Interpretation guidance

---

## 🎯 Hypothesis Testing Workflow

```
1. HY1: Urbanization Effect
   ↓
2. HY2: Environmental Kuznets Curve
   ↓
3. HY3: Policy Impact
   ↓
4. HY4: Pollutant Correlation
   ↓
5. HY5: Seasonal Patterns
```

**Recommended order:** Run in sequence (HY1 → HY5) for logical flow.

---

## ⚠️ Common Issues

### Issue: "File not found: analysis_ready.csv"
**Solution:** Run `python clean_data.py` first

### Issue: "Module not found"
**Solution:** Install missing packages: `pip install <package>`

### Issue: "Empty DataFrame"
**Solution:** Check data filtering criteria, some countries/years may have missing data

### Issue: "Kernel died"
**Solution:** Restart kernel and run cells one by one to identify problematic cell

---

## 📊 Statistical Significance Criteria

Throughout all notebooks:
- **α = 0.05** (significance level)
- **p < 0.05** → Statistically significant
- **Correlation strength:**
  - |r| > 0.7: Strong
  - |r| > 0.4: Moderate
  - |r| < 0.4: Weak

---

## 🔬 Validation & Reproducibility

All analyses are:
- ✓ **Reproducible** (fixed random seeds where applicable)
- ✓ **Documented** (code comments + markdown explanations)
- ✓ **Validated** (statistical assumptions checked)
- ✓ **Transparent** (all code visible)

---

## 📚 References

Statistical methods based on:
- Pearson, K. (1895). Correlation coefficient
- Student (1908). t-test
- Fisher, R.A. (1925). ANOVA
- Kuznets, S. (1955). Economic growth and income inequality

---

## 💡 Tips

1. **Run cells in order** - Each cell may depend on previous ones
2. **Check visualizations** - Saved in `visualizations/` folder
3. **Read interpretations** - Each notebook has detailed conclusions
4. **Modify parameters** - Feel free to adjust thresholds, bins, etc.
5. **Export results** - Use File → Download as PDF/HTML

---

## 🤝 Contributing

To add new hypotheses:
1. Create new notebook: `HY6_YourHypothesis.ipynb`
2. Follow existing structure
3. Use same style guidelines
4. Update this README

---

## 📞 Support

For issues or questions:
- Check notebook comments
- Review [CODE_STRUCTURE.md](../CODE_STRUCTURE.md)
- Check data dictionary: `cleaned_data/data_dictionary.json`

---

**Happy Hypothesis Testing! 🎉**
