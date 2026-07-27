# Week 12 Capstone: Project Selection & Gap Analysis

**Author:** Hermella Amha
**Date:** 27 July 2026  
**Project:** Ethiopia Financial Inclusion Forecasting System (Week 11)

---

## 1. Project Selection

### Chosen Project: Week 11 – Ethiopia Financial Inclusion Forecasting System

**Why this project?**

| Criteria                     | Justification                                                                                                        |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Finance Sector Relevance** | Directly addresses financial inclusion, banking, mobile money, and policy decisions at the National Bank of Ethiopia |
| **Business Impact**          | Quantifiable results: Account ownership 14%→49%, Telebirr impact +4.75pp, forecasts for 2025-2027                    |
| **Technical Complexity**     | Demonstrates forecasting, event impact modeling, scenario analysis, interactive dashboard                            |
| **Portfolio Strength**       | Complete project with data enrichment, modeling, forecasting, and dashboard                                          |
| **Gap Size**                 | Small manageable gaps (tests, type hints, CI/CD, SHAP) that can be completed within 1-2 days                         |

### Project Summary

- **Business Problem:** Ethiopia's financial inclusion growth slowed to +3pp (2021-2024) despite 54M+ Telebirr users. Stakeholders need to understand drivers and forecast future progress.
- **Solution:** Event-augmented forecasting system predicting Access (Account Ownership) and Usage (Digital Payments) for 2025-2027.
- **Key Results:** Base scenario predicts 56% Access and 42% Usage by 2027. Telebirr validated at +4.75pp impact.

---

## 2. Gap Analysis

| Category            | Question                                 | Status     | Evidence                                                     |
| ------------------- | ---------------------------------------- | ---------- | ------------------------------------------------------------ |
| **Code Quality**    | Is the code modular and well-organized?  | ✅ Yes     | `src/` folder with `eda.py`, `data_loader.py`                |
|                     | Are there type hints on functions?       | ❌ No      | Missing type annotations                                     |
|                     | Is there a clear project structure?      | ✅ Yes     | Standard structure with src/, notebooks/, dashboard/, tests/ |
| **Testing**         | Are there unit tests for core functions? | ❌ No      | No `tests/` folder with pytest tests                         |
|                     | Do tests run automatically on push?      | ❌ No      | No CI/CD pipeline configured                                 |
| **Documentation**   | Is the README comprehensive?             | ✅ Yes     | Complete with overview, setup, dashboard instructions        |
|                     | Are there docstrings on functions?       | ⚠️ Partial | Some functions have docstrings, others don't                 |
| **Reproducibility** | Can someone else run this project?       | ✅ Yes     | requirements.txt included, clear instructions                |
|                     | Are dependencies in requirements.txt?    | ✅ Yes     | Complete list of dependencies                                |
| **Visualization**   | Is there an interactive dashboard?       | ✅ Yes     | Streamlit dashboard with 4 pages                             |
| **Business Impact** | Is the problem clearly articulated?      | ✅ Yes     | Clear business context in README and notebooks               |
|                     | Are success metrics defined?             | ✅ Yes     | Account Ownership %, Digital Payment %, R², RMSE             |

---

## 3. Improvement Plan

### Priority 1: Add Unit Tests (pytest)

| Item              | Details                                            |
| ----------------- | -------------------------------------------------- |
| **Task**          | Write 5+ unit tests for core functions             |
| **Time Estimate** | 2 hours                                            |
| **Impact**        | High – proves reliability, reduces risk            |
| **Deliverable**   | `tests/test_data_loader.py`, `tests/test_model.py` |

### Priority 2: Add Type Hints and Docstrings

| Item              | Details                                              |
| ----------------- | ---------------------------------------------------- |
| **Task**          | Add type hints to all functions, complete docstrings |
| **Time Estimate** | 1.5 hours                                            |
| **Impact**        | Medium – improves code quality, maintainability      |
| **Deliverable**   | Updated `src/` files with type hints                 |

### Priority 3: Set Up GitHub Actions CI/CD

| Item              | Details                                                |
| ----------------- | ------------------------------------------------------ |
| **Task**          | Configure automated testing and linting on push        |
| **Time Estimate** | 1 hour                                                 |
| **Impact**        | High – automates quality checks, professional standard |
| **Deliverable**   | `.github/workflows/ci.yml`, CI badge in README         |

### Priority 4: Add SHAP Explainability

| Item              | Details                                                |
| ----------------- | ------------------------------------------------------ |
| **Task**          | Create SHAP notebook with visualizations               |
| **Time Estimate** | 1.5 hours                                              |
| **Impact**        | High – builds trust, transparency for finance audience |
| **Deliverable**   | `notebooks/06_shap_explainability.ipynb`, SHAP plots   |

### Priority 5: Write Blog Post / Technical Report

| Item              | Details                                  |
| ----------------- | ---------------------------------------- |
| **Task**          | Write a blog post explaining the project |
| **Time Estimate** | 2 hours                                  |
| **Impact**        | Medium – showcases communication skills  |
| **Deliverable**   | `reports/blog_post.md`                   |

---

## 4. Timeline

| Day                 | Tasks                                           |
| ------------------- | ----------------------------------------------- |
| **Day 1 (Monday)**  | Task 1: Gap analysis, Type hints, Unit tests    |
| **Day 2 (Monday)**  | GitHub Actions CI/CD, SHAP notebook             |
| **Day 3 (Tuesday)** | Blog post, Dashboard enhancements, Final review |

---

## 5. Success Metrics

| Metric     | Target                   |
| ---------- | ------------------------ |
| Unit Tests | 5+ passing tests         |
| Type Hints | 100% functions annotated |
| CI/CD      | Passing build on push    |
| SHAP       | 4+ visualizations        |
| Blog Post  | 500+ words with visuals  |
| README     | CI badge, comprehensive  |

---

## 6. Risk Assessment

| Risk                          | Likelihood | Mitigation                         |
| ----------------------------- | ---------- | ---------------------------------- |
| Tests fail due to data issues | Medium     | Use sample data for tests          |
| CI/CD pipeline fails          | Low        | Test locally first                 |
| SHAP installation issues      | Low        | Use `pip install shap`             |
| Running out of time           | Medium     | Prioritize high-impact items first |

---

## 7. Conclusion

Week 11 (Ethiopia Financial Inclusion Forecasting) is the optimal choice for this capstone. It has strong finance sector relevance, a complete foundation, and manageable gaps that can be addressed within the available timeframe.

The improvements will demonstrate:

- **Reliability** through testing and CI/CD
- **Transparency** through SHAP explainability
- **Professionalism** through code quality and documentation
- **Business Impact** through clear metrics and storytelling

---
