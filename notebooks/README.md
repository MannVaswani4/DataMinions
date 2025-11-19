# Hypothesis Testing Notebooks

This folder contains 5 Jupyter notebooks for hypothesis testing on air quality data.

## Notebooks

1. **HY1_Urbanization_Effect.ipynb** - Tests if urbanization increases PM₂.₅ and decreases O₃
2. **HY2_Environmental_Kuznets_Curve.ipynb** - Tests for inverted-U relationship between GDP and pollution
3. **HY3_Policy_Impact_Post2015.ipynb** - Tests if air quality improved after 2015 policies
4. **HY4_Pollutant_Correlation.ipynb** - Tests correlation between different pollutants
5. **HY5_Seasonal_Hemispheric_Variation.ipynb** - Tests seasonal patterns by hemisphere

## Requirements

```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn
```

## Usage

```bash
jupyter notebook
# Then open any .ipynb file
```

## Data

All notebooks use: `../cleaned_data/analysis_ready.csv`

Make sure to run `python clean_data.py` first to generate the cleaned dataset.
