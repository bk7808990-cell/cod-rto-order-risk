# 05 — Analysis

## Overview
This page covers the SQL analysis, Excel cross-check, and sensitivity analysis. All numbers were validated against the design rules and confirmed in three tools — SQL, Excel, and Python.

## SQL Findings
All queries were run on the clean table `orders_clean` in MySQL (8,000 rows, 17 columns). Cancelled orders were excluded from RTO calculations.

### Query 1 — RTO by Payment Mode

| Payment Mode | Total Orders | RTO Orders | RTO % |
|---|---|---|---|
| COD | 4613 | 1044 | 22.63% |
| Prepaid | 2987 | 157 | 5.26% |

**Insight:** COD orders return at 4x the rate of prepaid orders. This is the core problem — COD is where the risk sits.

### Query 2 — RTO by Order Value Bands

| Value Band | Orders | RTO | RTO % |
|---|---|---|---|
| A: 300-749 | 2264 | 334 | 14.75% |
| B: 750-1499 | 2658 | 386 | 14.52% |
| C: 1500-2999 | 1912 | 346 | 18.10% |
| D: 3000-5000 | 746 | 134 | 17.96% |
| E: Bulk (10k+) | 20 | 1 | 5.00% |

**Insight:** Orders above Rs 1,500 show roughly 3.5 percentage points higher RTO than orders below. This matches the design rule where high-value COD orders get +5 points. Band E has only 20 orders, so the rate is not statistically meaningful.

### Query 3 — RTO by Customer Type

| Customer Type | Payment Mode | Orders | RTO | RTO % |
|---|---|---|---|---|
| New | COD | 3058 | 731 | 23.90% |
| Repeat | COD | 1555 | 313 | 20.13% |
| New | Prepaid | 1958 | 101 | 5.16% |
| Repeat | Prepaid | 1029 | 56 | 5.44% |

**Insight:** New COD customers show about 3.8 points higher RTO than repeat COD customers. Prepaid shows no difference between new and repeat — which is expected because the new-customer rule only applies to COD.

### Query 4 — RTO Loss by Pincode Tier

| Pincode Tier | Orders | RTO | RTO % | Total Loss (Rs) |
|---|---|---|---|---|
| Tier-3 | 1826 | 324 | 17.74% | 69,660 |
| Remote | 1138 | 242 | 21.27% | 66,550 |
| Tier-2 | 2250 | 317 | 14.09% | 55,475 |
| Metro | 2233 | 301 | 13.48% | 40,635 |
| Unknown | 153 | 17 | 11.11% | 3,095 |

**Insight:** Tier-3 and Remote together account for 58% of total RTO loss, even though they are only 39% of orders. This is a Pareto pattern — the loss is concentrated in a few segments.

### Query 5 — Monthly RTO Trend

| Month | Orders | RTO | RTO % |
|---|---|---|---|
| 01-2026 | 1286 | 203 | 15.79% |
| 02-2026 | 1149 | 181 | 15.75% |
| 03-2026 | 1289 | 203 | 15.75% |
| 04-2026 | 1250 | 201 | 16.08% |
| 05-2026 | 1337 | 222 | 16.60% |
| 06-2026 | 1289 | 191 | 14.82% |

**Insight:** The RTO rate is stable across all six months, ranging from 14.82% to 16.60%. The problem is not seasonal — it is structural.

### Query 6 — A/B Test Result (Core Finding)

| Group | Orders | RTO | RTO % |
|---|---|---|---|
| Control (no call) | 228 | 77 | 33.77% |
| Treatment (call made) | 228 | 58 | 25.44% |
| Difference | — | — | 8.33 points |

**Insight:** The confirmation call reduced RTO by 8.33 percentage points. This is the main finding of the project.

### Query 7 — Average Loss per RTO

| Metric | Value |
|---|---|
| Avg loss per RTO | Rs 196.02 |
| Total RTO loss | Rs 2,35,415 |
| Total RTO orders | 1201 |

### Query 8 — Average Margin per Delivered Order

| Metric | Value |
|---|---|
| Avg margin per delivered | Rs 670.70 |
| Total delivered orders | 6399 |

## Excel Cross-Check
I built a pivot table in Excel to verify the SQL output. This was a consistency check — if Excel and SQL disagree, something is wrong.

| Payment Mode | Cancelled | Delivered | RTO | Total |
|---|---|---|---|---|
| COD | 235 | 3569 | 1044 | 4848 |
| Prepaid | 165 | 2830 | 157 | 3152 |
| Total | 400 | 6399 | 1201 | 8000 |

Both tools returned the same numbers. The analysis is validated.

## Sensitivity Analysis
I ran four scenarios to check how much RTO reduction the call needs to be profitable.

**Setup:**
- Control group RTO: 33.77%
- Orders per group: 228
- Loss per RTO: Rs 196
- Call cost: Rs 10

| Reduction | Prevented RTOs | Saving (Rs) | Cost (Rs) | Net (Rs) |
|---|---|---|---|---|
| 3 points | 6.84 | 1,341 | 2,280 | -939 |
| 5 points | 11.4 | 2,234 | 2,280 | -46 |
| 8 points | 18.24 | 3,575 | 2,280 | 1,295 |
| 10 points | 22.8 | 4,469 | 2,280 | 2,189 |

**Insight:** Break-even is at 5.1 points. Below that, the call loses money. Above that, it saves money. My actual A/B test showed 8.33 points, so the call was profitable — but not by a huge margin.

## Key Insights
- COD RTO (22.63%) is 4x higher than Prepaid RTO (5.26%). This is where the problem lives.
- High-value orders (Rs 1,500+) carry about 3.5 points more risk than low-value orders.
- New customers add about 3.8 points of risk in COD, but no difference in Prepaid.
- Tier-3 and Remote pincodes account for 58% of total RTO loss.
- The monthly trend is stable — no seasonality. Structural problem.
- The confirmation call reduced RTO by 8.33 points in the A/B test.
- Break-even is at 5.1 points. The actual reduction was above break-even.
- Average loss per RTO is Rs 196; average margin per delivered order is Rs 671.

## Recommended Next Step
Pilot the confirmation call on 500 high-risk orders. Measure the actual RTO reduction. Compare with the 8.33 points from the A/B test. If the reduction holds above 5 points, scale it.
