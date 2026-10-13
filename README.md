# COD/RTO Order Risk and Unit Economics

I built this project to understand a problem that Indian D2C sellers face every day — Cash on Delivery orders that come back. It started as a simple question: can we predict which COD orders will return, and does calling the customer actually help?

This is my Business + Data Analyst portfolio project. It covers the full flow — designing the data rules, generating a synthetic dataset, cleaning it, and then running an A/B test to see if a confirmation call makes a difference.

---

## The Problem

An online store takes both prepaid and COD orders. Prepaid is safe — the customer already paid. COD is risky — the customer can refuse at the door, and the product comes back. Every RTO (Return to Origin) costs the seller shipping both ways plus packaging.

The real question management asked was simple: **should we call high-risk COD customers before dispatching?**

---

## About the Data

I could not find a public dataset with actual COD/RTO outcomes for Indian e-commerce, so I built one myself. It is **synthetic** — meaning I designed the rules and generated the data using Python.

I used a fixed seed (42) so anyone can reproduce the same numbers.

- Raw file: 8,080 rows, 18 columns
- Clean file: 8,000 rows, 17 columns
- Time period: Jan 2026 to June 2026

I deliberately injected some messy data — missing values, duplicates, and spelling variations — so the cleaning step would be realistic. Real company data is never clean.

---

## How I Built It

1. **Wrote the rules first** — a table listing every RTO rule (COD 15%, Prepaid 2%, and the risk factors on top)
2. **Generated the data** — Python + pandas, following those rules
3. **Cleaned it** — used Power Query Editor in Excel (removed duplicates, fixed spelling, filled missing values)
4. **Analysed it** — SQL for the heavy lifting, Excel to cross-check the KPIs
5. **Built a dashboard** — Power BI with simulation sliders (still working on this)

---

## What I Found

Some findings surprised me:

- **COD orders return at 22.63%** — that is more than 4x the prepaid rate of 5.26%
- **The overall RTO rate is 15.8%** across all dispatched orders
- **Only 456 orders** qualify as truly "high-risk" (5.7% of all orders) — COD + new customer + order value above Rs 1,500 + in a Tier-3 or Remote pincode
- **In the A/B test, the treatment group had 25.44% RTO vs 33.77% in control** — the confirmation call did make a difference
- **Every RTO costs about Rs 196** on average, and my average margin on delivered orders was Rs 671

---

## The A/B Test

I structured the data so that high-risk orders were split 50/50 between a control group (no call) and a treatment group (called).

| Group | RTO Rate |
|---|---|
| Control (no call) | 33.77% |
| Treatment (call made) | 25.44% |
| Difference | ~8 percentage points |

The important part was not just the reduction — it was whether the reduction covers the cost of the call.

**Break-even math:**
- If a call costs Rs 10: the reduction needs to be more than 5.1 percentage points
- If a call costs Rs 20: it needs to be more than 10.2 percentage points

That is the whole decision in one line.

---

## My Recommendation

Do not call every COD customer. Call only the high-risk segment — COD + new customer + order value ≥ Rs 1,500 + Tier-3 or Remote pincode.

But — and this is important — the numbers are close to break-even. So I would recommend a pilot on 500 orders first, measure the actual reduction, and then decide whether to scale.

If I had said "this saves money, let's do it" without checking the break-even, I would have been wrong.

---

## Impact

Since this is synthetic data, I label everything as **expected impact**, not actual:

- **Per RTO prevented:** Rs 196 loss avoided, minus the Rs 10 call cost
- **For the segment:** Results look positive but the sample is small (228 per group)
- **For the whole business:** Total RTO loss is Rs 3.38 lakh; potential saving is Rs 74,860 against a call cost of Rs 76,000 — essentially a wash

The whole point of this analysis was to show that the decision is **sensitive** — it depends on how much you spend on the call and how much you actually reduce RTO.

---

## Tools I Used

- **Python (pandas)** — data generation
- **Power Query Editor** — data cleaning
- **SQL** — analysis (currently working on this)
- **Excel** — KPI cross-check
- **Power BI** — dashboard (in progress)
- **Jira** — project tracking
- **Confluence** — all the documentation

---

## Folder Structure
cod-rto-order-risk/
├── README.md
├── data/
│ ├── raw/ (raw data with injected issues)
│ └── clean/ (cleaned data)
├── scripts/
│ └── generate_data.py
├── sql/ (SQL analysis)
├── excel/ (KPI cross-check)
├── powerbi/ (dashboard)
└── docs/ (detailed documentation)

## Documentation

All the detailed work — business context, requirements, process maps, data design — is on Confluence:

- **Confluence:** [BA + DA Portfolio — COD/RTO](https://bk7808990.atlassian.net/wiki/spaces/BDPC/pages/13303809/00+Project+Home)
- **Jira:** [CODRTO Project](https://bk7808990.atlassian.net/jira/software/projects/CODRTO/list?jql=project%20%3D%20CODRTO%20ORDER%20BY%20cf%5B10019%5D%20ASC)

---

## What This Project Does Not Do

I want to be honest about the limits:

- All patterns come from my design rules, not real observations
- These findings cannot be generalised to a real business
- Direct loss does not include lost sales, marketing, or payment gateway fees
- "New customer" only means the first order in the 6-month window
- The high-risk count (456) came out lower than I first expected, because all four conditions must be true at the same time

---

## A Note on AI

I designed the business rules and the data structure myself. I used AI (Claude) to help write the Python generation script and to draft some documentation. I reviewed every line, validated the output against expected RTO rates, and made all the analytical decisions myself. The business context and rules are my own work.

---

## Where I Am Now

- Phase 1: Setup — done
- Phase 2: Business Analysis — done
- Phase 3: Data Design — done
- Phase 4: Analysis — in progress
- Phase 5: Power BI Dashboard — pending
- Phase 6: Recommendations and Impact — pending
- Phase 7: Final Delivery — pending

