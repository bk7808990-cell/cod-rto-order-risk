# COD/RTO Order Risk and Unit Economics

## Overview
This is an end-to-end Business + Data Analyst portfolio project. It analyzes the risk of Return to Origin (RTO) for Cash on Delivery (COD) orders, builds a unit economics model, and simulates the impact of a confirmation call strategy using an A/B test approach. 

The core business question was: **Should we call high-risk COD customers before dispatching, and does the call cost justify the RTO reduction?**

## The Problem (Real-World Context)
In the Indian D2C e-commerce space, COD is highly preferred but carries a massive risk — customers can refuse delivery at the door. When this happens, the seller bears the cost of forward shipping, return shipping, and damaged packaging. 
The management needed a data-backed decision: Can we identify which orders are high-risk, and does a pre-dispatch confirmation call reduce the loss?

## Data Strategy & Disclosure
Since real order-level RTO datasets are proprietary to companies, I designed a synthetic dataset (8,000 rows, 17 columns) to simulate a realistic Indian D2C environment. 

The data generation rules are not random. They are based on published industry ranges and domain logic. For example:
- Base COD RTO is set at 15% (vs 2% for Prepaid), reflecting real-world refusal rates.
- Risk factors like Tier-3 (+4%) and Remote pincodes (+8%) are based on known logistics failure rates in India.
- No-effect factors (like Weekday or Product Category) were intentionally included as control variables to ensure the analysis is honest.
- The dataset uses a fixed seed (42) for reproducibility, and messy data (duplicates, missing values, spelling variants) was injected to simulate real-world cleaning challenges.

## Methodology & Tools
I followed a strict pipeline to ensure data integrity:
1. **Data Generation:** Python (pandas) based on the researched business rules.
2. **Data Cleaning:** Power Query Editor (Excel) to remove duplicates, fix payment mode variants, and handle missing pincodes (8,080 raw rows → 8,000 clean rows).
3. **Analysis:** SQL (MySQL) to aggregate the KPIs, cross-checked with Excel pivot tables for consistency.
4. **Visualization:** A 5-page interactive Power BI dashboard featuring dynamic What-If sliders.

## Key Findings (Business Impact)
- **The Core Issue:** COD orders return at **22.63%**, which is more than 4x the Prepaid rate of **5.26%**. 
- **The Segment:** Only **456 orders (5.7%)** qualified as "high-risk" (COD + New Customer + Order Value ≥ ₹1,500 + Tier-3/Remote pincode). 
- **The A/B Test:** High-risk orders were split 50/50. The Control group (no call) had a **33.77% RTO**, while the Treatment group (called) had a **25.44% RTO** — a **8.33 percentage point reduction**.
- **Unit Economics:** The average loss per RTO is **₹196.02**, while the average margin on a delivered order is **₹670.70**.

## The Financial Decision & Break-even
The key to this project is the break-even analysis. A call isn't always profitable.
- If a call costs **₹10**, the RTO reduction needs to be greater than **5.1 points** to break even.
- Since the A/B test showed an **8.33 point reduction**, the strategy is profitable. 
- **3-Level Impact:**
  1. **Unit Level:** ₹196.02 loss avoided - ₹10 call cost = ₹186.02 net benefit per prevented RTO.
  2. **Segment Level:** For all 456 high-risk orders, a 5-point reduction saves ₹4,469, against a call cost of ₹4,560 (Break-even).
  3. **Pilot Level:** On a 500-order pilot, an 8.33 point reduction saves ₹8,164 against a cost of ₹5,000 (Net Benefit: +₹3,164).

## My Recommendation
Do not scale immediately. The numbers are close to break-even at the broader level. 
**Action:** Pilot the confirmation call on 500 high-risk orders. Measure the actual reduction. If it holds above 5 points, scale it to the full portfolio.

## Project Structure & Links
- **Confluence Documentation:** [Project Documentation](https://bk7808990.atlassian.net/wiki/external/YTJjNDgzNzIzMzkwNDYzYzlkYTg0ZjYwNWZhYmU1ZGY)(Contains BRD, Process Maps, Data Design Note, and Analysis).
- **Jira Project Board:** [CODRTO Project](https://bk7808990.atlassian.net/jira/software/projects/CODRTO/list?jql=project%20%3D%20CODRTO%20ORDER%20BY%20cf%5B10019%5D%20ASC)*(Login required as per Atlassian policy)*
- **Jira Board Screenshot:** [View Screenshot](docs/jira_p1_board.png.png)




## Limitations & AI Disclosure
To be fully transparent about the boundaries of this analysis:

 Synthetic Data: All patterns are design assumptions based on industry logic, not real-world discoveries. The findings cannot be generalised to a real business without a pilot.

Scope Limitations: The direct loss calculation does not include lost sales, marketing spend, or payment gateway fees.

 AI Workflow: I designed the business logic, data structure, and analytical approach independently. I used AI purely as a coding assistant to accelerate the Python script and DAX formulas. However, I manually reviewed, tested, and validated every calculation against my SQL and Excel outputs to ensure 100% accuracy.

```text
cod-rto-order-risk/
├── README.md
├── data/
│   ├── raw/          (8,080 rows with injected issues)
│   └── clean/        (8,000 rows, 17 columns)
├── scripts/          (Python data generation)
├── sql/              (8 Analysis queries)
├── excel/            (KPI cross-check & Sensitivity)
├── powerbi/          (5-page interactive dashboard)
└── docs/             (Detailed markdown documentation)
