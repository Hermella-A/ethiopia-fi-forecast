# Ethiopia Financial Inclusion Forecasting System

[![CI/CD Pipeline](https://github.com/Hermella-A/ethiopia-fi-forecast/actions/workflows/ci.yml/badge.svg)](https://github.com/Hermella-A/ethiopia-fi-forecast/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.17+-blueviolet.svg)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

# 📋 Table of Contents

- [Project Overview](#project-overview)
- [Key Findings](#key-findings)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Data Enrichment](#data-enrichment)
- [Analysis Workflow](#analysis-workflow)
- [Forecast Results](#forecast-results)
- [Interactive Dashboard](#interactive-dashboard)
- [Model Explainability](#model-explainability)
- [Technical Details](#technical-details)
- [Future Improvements](#future-improvements)
- [Technology Stack](#technology-stack)
- [Author](#author)

---

# Project Overview

This project develops a **financial inclusion forecasting system** for Ethiopia, predicting progress on two core dimensions of financial inclusion as defined by the World Bank's Global Findex.

### Financial Inclusion Metrics

- **Access (Account Ownership Rate):** The share of adults (15+) who own an account at a financial institution or use a mobile money account.
- **Usage (Digital Payment Adoption Rate):** The share of adults who use mobile money, debit/credit cards, or mobile phones to make digital payments.

## Business Context

Selam Analytics, a financial technology consulting firm, was engaged by a consortium of development finance institutions, mobile money operators, and the National Bank of Ethiopia to answer the following questions:

- What drives financial inclusion in Ethiopia?
- How do policy changes, product launches, and infrastructure investments affect financial inclusion?
- How will financial inclusion change in 2025–2027?

### Project Statistics

| Metric          |          Value |
| --------------- | -------------: |
| Total Records   | 43+ (Enriched) |
| Observations    |             40 |
| Events          |             15 |
| Impact Links    |             19 |
| Forecast Period |      2025–2027 |

---

# Key Findings

| Finding                       | Result                                    |
| ----------------------------- | ----------------------------------------- |
| Account Ownership (2024)      | **49%** (up from 14% in 2011)             |
| Mobile Money Accounts (2024)  | **9.45%** (up from 4.7% in 2021)          |
| 2021–2024 Trend               | Growth slowed despite 54M+ Telebirr users |
| Mobile Money-Only Users       | Approximately **0.5%**                    |
| Forecast (2027 Base Scenario) | Account Ownership **54–56%**              |
| Forecast (2027 Usage)         | Digital Payments **40–42%**               |
| Largest Positive Event        | Telebirr Launch (+4–5 percentage points)  |
| Largest Negative Event        | None identified                           |

---

## Project Structure

```text
ethiopia-fi-forecast/
├── .github/
│   └── workflows/
│       ├── unittests.yml
│       └── ci.yml                # CI/CD pipeline
├── data/
│   ├── raw/
│   │   ├── ethiopia_fi_unified_data.xlsx
│   │   └── reference_codes.xlsx
│   └── processed/
│       ├── ethiopia_fi_enriched.csv
│       ├── event_impact_matrix.csv
│       └── forecasts_2025_2027.csv
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_exploratory_data_analysis.ipynb
│   ├── 03_event_impact_modeling.ipynb
│   ├── 04_forecasting.ipynb
│   └── 06_shap_explainability.ipynb    # SHAP explainability
├── src/
│   ├── __init__.py
│   ├── data_loader.py                   # Type hints, dataclasses
│   └── model.py                         # Model training with type hints
├── dashboard/
│   ├── app.py
│   └── requirements.txt
├── reports/
│   └── figures/
│       ├── shap_summary.png             # SHAP plots
│       ├── shap_bar.png
│       ├── shap_waterfall.png
│       └── shap_dependence.png
├── tests/
│   ├── __init__.py
│   └── test_data_loader.py              # Unit tests
├── models/
│   └── best_model.pkl
├── docs/
│   └── week12_task1_plan.md
├── data_enrichment_log.md
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Setup and Installation

### Prerequisites

- Python 3.10+
- Git
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/YourUsername/ethiopia-fi-forecast.git
cd ethiopia-fi-forecast
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

#### Activate the Environment

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 3. Install Project Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Dashboard Dependencies

```bash
cd dashboard
pip install -r requirements.txt
cd ..
```

---

## Data Enrichment

The original dataset was enriched with:

- **10 new observations**
- **5 new events**
- **5 new event-impact links**

### New Observations

| Indicator                       | Source     | Value  |
| ------------------------------- | ---------- | ------ |
| Agent Density (per 100k adults) | IMF FAS    | 45     |
| POS Terminals                   | NBE        | 12,000 |
| Mobile Internet Penetration     | ITU        | 38%    |
| Digital ID Coverage             | NBE        | 25%    |
| Bank Branches (per 100k adults) | IMF FAS    | 4.5    |
| Smartphone Penetration          | GSMA       | 42%    |
| Data Affordability              | GSMA       | 3.5%   |
| 4G Coverage                     | ITU        | 65%    |
| Literacy Rate                   | World Bank | 52%    |
| Urbanization Rate               | World Bank | 23%    |

### New Events

| Date       | Event                             | Category       |
| ---------- | --------------------------------- | -------------- |
| 2020-01-01 | EthSwitch Launch                  | Infrastructure |
| 2022-06-01 | Agent Network Expansion           | Infrastructure |
| 2023-01-15 | Fayda Digital ID Rollout          | Product Launch |
| 2024-03-15 | M-Pesa–MTN Interoperability       | Infrastructure |
| 2024-06-01 | Mobile Money Regulatory Framework | Policy         |

### New Impact Links

| Event                       | Indicator             | Direction | Magnitude | Lag       |
| --------------------------- | --------------------- | --------- | --------- | --------- |
| Fayda Digital ID            | Account Ownership     | Positive  | +5%       | 18 Months |
| EthSwitch Launch            | P2P Count             | Positive  | +10%      | 12 Months |
| M-Pesa–MTN Interoperability | Telebirr Users        | Positive  | +8%       | 6 Months  |
| Agent Expansion             | Mobile Money Accounts | Positive  | +8%       | 24 Months |
| Regulatory Framework        | Active Rate           | Positive  | +5%       | 12 Months |

**Documentation:** `data_enrichment_log.md`

---

## Analysis Workflow

### Task 1 — Data Exploration & Enrichment

**Notebook:** `notebooks/01_eda.ipynb`

- Explored the unified dataset.
- Identified missing observations and events.
- Added new observations, events, and impact links.

---

### Task 2 — Exploratory Data Analysis

**Notebook:** `notebooks/02_exploratory_data_analysis.ipynb`

- Analyzed account ownership trends (2011–2024).
- Investigated the slowdown after 2021.
- Examined digital payment adoption.
- Built correlation analysis.
- Generated key insights and hypotheses.

---

### Task 3 — Event Impact Modeling

**Notebook:** `notebooks/03_event_impact_modeling.ipynb`

- Built the event-impact matrix.
- Validated impacts using historical events.
- Refined impact estimates.
- Documented confidence levels.

---

### Task 4 — Forecasting

**Notebook:** `notebooks/04_forecasting.ipynb`

- Developed baseline trend models.
- Created event-augmented forecasts.
- Generated Optimistic, Base, and Pessimistic scenarios.
- Produced forecasts for 2025–2027.

---

### Task 5 — Dashboard Development

**File:** `dashboard/app.py`

- Built a multi-page interactive Streamlit dashboard.
- Created 4+ interactive visualizations.
- Added CSV download functionality.
- Implemented forecast scenario selector.
- Displayed confidence intervals for predictions.
- Designed a responsive layout for desktop and mobile devices.

---

### Task 6 — Engineering Excellence (Week 12)

**Files:** `src/data_loader.py`, `src/model.py`, `tests/test_data_loader.py`, `.github/workflows/ci.yml`, `notebooks/05_shap_explainability.ipynb`

- **Code Refactoring:** Added type hints to all functions, used dataclasses for configuration objects, replaced magic numbers with named constants.
- **Testing:** Wrote 7+ unit tests using pytest, all passing.
- **CI/CD:** Configured GitHub Actions for automated testing and linting on push. Added CI badge to README.
- **Model Explainability:** Added SHAP visualizations including Summary Plot, Bar Plot, Waterfall Plot, and Dependence Plot.
- **Documentation:** Updated README with comprehensive project documentation and blog post.

---

## Forecast Results

| Target | Scenario    | 2025 | 2026 | 2027 |
| ------ | ----------- | ---: | ---: | ---: |
| Access | Optimistic  |  55% |  57% |  60% |
| Access | Base        |  52% |  54% |  56% |
| Access | Pessimistic |  48% |  49% |  51% |
| Usage  | Optimistic  |  42% |  45% |  48% |
| Usage  | Base        |  38% |  40% |  42% |
| Usage  | Pessimistic |  34% |  35% |  37% |

---

## Interactive Dashboard

The project includes an interactive **Streamlit dashboard** for exploring historical trends and forecast scenarios.

### Dashboard Features

| Feature                       | Description                                                     |
| ----------------------------- | --------------------------------------------------------------- |
| 4+ Interactive Visualizations | Time-series plots, forecast charts, and scenario comparisons    |
| Key Metrics Cards             | Account ownership, mobile money, and digital payment indicators |
| Date Range Selector           | Filter trends using custom date ranges                          |
| Event Overlay                 | Display historical events on charts                             |
| Scenario Selector             | Compare Optimistic, Base, and Pessimistic forecasts             |
| Confidence Intervals          | Visual uncertainty bands around forecasts                       |
| Data Download                 | Export filtered datasets as CSV                                 |
| Progress Tracking             | Monitor progress toward the 60% NFIS-II target                  |

### Dashboard Pages

| Page        | Features                                                       |
| ----------- | -------------------------------------------------------------- |
| Overview    | Summary metrics, data quality overview, events, key insights   |
| Trends      | Interactive charts, event overlays, date filters, CSV download |
| Forecasts   | Scenario comparison, confidence intervals, forecast tables     |
| Projections | Progress tracking, gap analysis, policy recommendations        |

---

## Running the Dashboard

### Option 1 — From the Dashboard Folder

```bash
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```

### Option 2 — From the Project Root

```bash
streamlit run dashboard/app.py
```

The dashboard will be available at:

```text
http://localhost:8501
```

---

## Dashboard Screenshots

| Screenshot                                  | Description                                  |
| ------------------------------------------- | -------------------------------------------- |
| `reports/figures/dashboard_overview.png`    | Dashboard overview with summary metrics      |
| `reports/figures/dashboard_trends.png`      | Interactive trend analysis                   |
| `reports/figures/dashboard_forecasts.png`   | Forecast scenarios with confidence intervals |
| `reports/figures/dashboard_projections.png` | Progress projections toward the 60% target   |

---

## Model Explainability

SHAP (SHapley Additive exPlanations) was used to explain the model's predictions and build trust with stakeholders.

### SHAP Visualizations

| Plot                | Description                                         |
| ------------------- | --------------------------------------------------- |
| **Summary Plot**    | Global feature importance showing impact direction  |
| **Bar Plot**        | Mean absolute SHAP values per feature               |
| **Waterfall Plot**  | Explanation of a single prediction                  |
| **Dependence Plot** | Relationship between top feature and its SHAP value |

### Top Features Driving Financial Inclusion

1. **Mobile Phone Penetration** – Strong positive correlation with account ownership
2. **4G Coverage** – Enables mobile money access
3. **Agent Density** – Improves access to financial services
4. **Literacy Rate** – Enables understanding of financial products
5. **Urbanization** – Better access in urban areas

---

## Technical Details

### Data Sources

| Source                      | Data Collected                              |
| --------------------------- | ------------------------------------------- |
| Global Findex Database      | Account ownership, digital payments         |
| IMF Financial Access Survey | Agent density, bank branches, POS terminals |
| GSMA Mobile Economy Report  | Smartphone penetration, data affordability  |
| ITU ICT Statistics          | Mobile internet, 4G coverage                |
| National Bank of Ethiopia   | Digital ID, regulatory frameworks           |

### Model Architecture

- **Model Type:** Event-augmented linear regression with scenario analysis
- **Features:** 10+ enriched indicators
- **Target Variables:** Account Ownership (Access), Digital Payment Adoption (Usage)

### Evaluation Metrics

| Metric           | Access Model             | Usage Model              |
| ---------------- | ------------------------ | ------------------------ |
| R²               | 0.95                     | 0.89                     |
| RMSE             | 2.3 pp                   | 3.1 pp                   |
| Cross-Validation | 5-fold Stratified K-Fold | 5-fold Stratified K-Fold |

---

## Future Improvements

- Add Bayesian Structural Time Series for causal impact analysis
- Incorporate machine learning models (XGBoost, LightGBM)
- Add more granular demographic data (age, gender, region)
- Deploy dashboard to Streamlit Cloud
- Add automated retraining pipeline
- Integrate additional data sources (satellite imagery, mobile usage data)

---

## Technology Stack

| Category        | Technologies                               |
| --------------- | ------------------------------------------ |
| Data Analysis   | Python, Pandas, NumPy, Matplotlib, Seaborn |
| Modeling        | Scikit-learn, SciPy, Statsmodels           |
| Visualization   | Plotly, Matplotlib, Seaborn, SHAP          |
| Dashboard       | Streamlit                                  |
| Testing         | Pytest, Pytest-cov                         |
| CI/CD           | GitHub Actions                             |
| Version Control | Git                                        |
| Environment     | Python 3.10+, Virtual Environment          |

---

## Author

**Hermella Amha**  
[GitHub](https://github.com/Hermella-A/ethiopia-fi-forecast)

---
