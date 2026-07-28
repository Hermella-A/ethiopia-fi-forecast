# Forecasting Financial Inclusion in Ethiopia: A Data-Driven Approach

## Introduction

Ethiopia is undergoing a rapid digital financial transformation. Telebirr has grown to over 54 million users since launching in 2021, and M-Pesa entered the market in 2023 with over 10 million users. Yet according to the 2024 Global Findex survey, only 49% of Ethiopian adults have a financial account—just 3 percentage points higher than in 2021.

**The question:** Why did growth slow despite massive mobile money expansion?

## The Data Challenge

The Global Findex survey provides the gold standard for financial inclusion data, but it's only conducted every three years. This leaves significant gaps between survey rounds. To forecast 2025-2027, we needed to:

1. Enrich the dataset with additional indicators
2. Model event impacts (Telebirr launch, M-Pesa entry, policy changes)
3. Build a forecasting system with quantified uncertainty

## Our Approach

### 1. Data Enrichment

We added 10 new indicators from IMF FAS, GSMA, ITU, and NBE:

| Indicator              | Source  |
| ---------------------- | ------- |
| Agent Density          | IMF FAS |
| POS Terminals          | NBE     |
| Smartphone Penetration | GSMA    |
| 4G Coverage            | ITU     |

### 2. Event Impact Modeling

We quantified impacts of key events:

| Event           | Indicator             | Impact  |
| --------------- | --------------------- | ------- |
| Telebirr Launch | Mobile Money Accounts | +4.75pp |
| M-Pesa Entry    | P2P Transfers         | +8%     |
| Agent Expansion | Mobile Money Accounts | +8%     |

### 3. Forecasting (2025-2027)

| Scenario    | Access 2027 | Usage 2027 |
| ----------- | ----------- | ---------- |
| Optimistic  | 60%         | 48%        |
| Base        | 56%         | 42%        |
| Pessimistic | 51%         | 37%        |

## Key Insights

1. **Account ownership growth slowed because mobile money accounts are not translating to active usage.** Only ~0.5% of adults are mobile money-only users.

2. **Telebirr was validated as a significant positive event**, contributing +4.75pp to mobile money accounts.

3. **Infrastructure investments (4G coverage, agent density) are key drivers.** Strong correlations suggest continued investment will drive future progress.

4. **The 60% NFIS-II target is achievable under the Optimistic scenario** but requires continued policy support and investment.

## The Dashboard

We built an interactive Streamlit dashboard that allows stakeholders to:

- Explore historical trends
- Compare scenarios
- Track progress toward targets
- Download data

## Engineering Excellence

To make this project production-ready, we implemented:

| Improvement             | Description                                   |
| ----------------------- | --------------------------------------------- |
| **Type Hints**          | Added type annotations to all functions       |
| **Unit Tests**          | 7+ tests using pytest                         |
| **CI/CD**               | GitHub Actions for automated testing          |
| **SHAP Explainability** | 4 visualizations explaining model predictions |

## Lessons Learned

1. **Start with the data:** Enriching the dataset with supplementary sources was critical for accurate forecasting.

2. **Validate against history:** The Telebirr validation confirmed our approach was robust.

3. **Communicate uncertainty:** Scenarios and confidence intervals build trust.

4. **Build for stakeholders:** The dashboard made the results accessible to non-technical users.

## Conclusion

Financial inclusion in Ethiopia is progressing, but the pace has slowed. To reach the 60% target by 2027, continued investment in infrastructure, digital ID, and agent networks is critical. Mobile money is a powerful tool, but it must be paired with use cases that drive active adoption.

---

_This project was completed as part of the 10 Academy Week 12 challenge._
