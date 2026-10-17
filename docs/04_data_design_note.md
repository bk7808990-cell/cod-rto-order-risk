# 04 — Data Design

## Data Rules Table

| Rule | Value | Why | Source Type |
|---|---|---|---|
| Base RTO rate for COD | 15% | No payment made yet, so refusal is easy | Domain logic |
| Base RTO rate for Prepaid | 2% | Payment already made | Domain logic |
| New customer (COD only) | +5 points | Less trust in the brand | My assumption |
| Order value >= Rs 1,500 (COD only) | +5 points | Bigger cash decision at door | My assumption |
| Tier-3 pincode | +4 points | Higher delivery failure rate | Published range |
| Remote pincode | +8 points | Highest delivery failure rate | Published range |
| Metro and Tier-2 pincode | +0 points | Control group | Reference |
| Courier B | +3 points | Performance difference between couriers | Domain logic |
| Weekday | No effect | Control factor | My assumption |
| Product category | No effect | Control factor | My assumption |
| RTO probability cap | 1% to 50% | Realistic range | My assumption |

## Data Generation Rules

| Rule | Value | Why | Source Type |
|---|---|---|---|
| Total orders | 8,000 | Portfolio-scale dataset | My assumption |
| Date range | 1 Jan to 30 Jun 2026 | 6-month window | My assumption |
| Customer pool | 9,000 unique IDs | To allow repeat orders | My assumption |
| COD share | 60% | Typical for Indian D2C | Published range |
| Prepaid share | 40% | Remaining share | Domain logic |
| Cancelled orders | 400 (exact) | Before dispatch cancellations | My assumption |

## Data Dictionary

| Column Name | Data Type | Description | Source |
|---|---|---|---|
| order_id | Integer | Unique order identifier | Synthetic |
| order_date | Date | Date when order was placed | Synthetic |
| customer_id | Integer | Unique customer identifier | Synthetic |
| customer_type | Text | New or Repeat (first order in window = New) | Derived |
| payment_mode | Text | COD or Prepaid | Synthetic |
| order_value | Decimal | Order amount in INR | Synthetic |
| product_category | Text | Product category (5 types, no effect) | Synthetic |
| pincode_tier | Text | Metro / Tier-2 / Tier-3 / Remote | Synthetic |
| courier | Text | Courier partner (A, B, C) | Synthetic |
| delivery_status | Text | Delivered / RTO / Cancelled Before Dispatch | Synthetic |
| shipping_cost | Decimal | Forward shipping cost in INR | Derived from tier |
| return_shipping_cost | Decimal | Return shipping cost (equals forward if RTO) | Derived |
| packaging_cost | Decimal | Packaging cost in INR (Rs 15 if dispatched) | Fixed |
| product_cost | Decimal | Product cost (40-60% of order value) | Derived |
| is_high_risk | Boolean | TRUE if COD + New + >=1500 + Tier-3/Remote | Derived |
| group | Text | Control / Treatment / Not eligible (for A/B test) | Assigned |
| call_cost | Decimal | Cost of confirmation call (Rs 10 if Treatment, else 0) | Assigned |

## Data Design Note

### Purpose
This project uses synthetic order-level data because no suitable public dataset with COD/RTO outcomes was found. The data is designed to reflect realistic Indian D2C patterns, not real customer data.

### Tables and Columns
One table: `orders`. 17 columns. 8,000 rows (raw file: 8,080 with duplicates). Columns include order details, customer type, payment mode, pincode tier, courier, delivery status, and cost fields.

### Key Rules (Summary)
- Base RTO: COD 15%, Prepaid 2%
- Risk factors (COD only): New customer +5, order value >= Rs 1,500 +5
- Risk factors (all orders): Tier-3 +4, Remote +8, Courier B +3
- No-effect factors: weekday, product category
- Cap: RTO probability capped at 1% to 50%

### Injected Data-Quality Issues
- 160 rows with missing `pincode_tier` (simulates a skipped form field)
- 80 rows with `payment_mode` spelling variants (simulates manual entry)
- 80 exact duplicate rows (simulates a system retry)
- Raw file: 8,080 rows; clean file: 8,000 rows

## Validation Checklist
The following checks were run on the generated dataset:

- **Row Counts — Passed:** Clean file: 8,000 rows / Raw file: 8,080 rows (80 duplicates injected).
- **RTO Rate for COD — Passed:** Computed 22.63% (within expected design range).
- **High-Risk Segment — Passed:** 456 orders identified (5.7% of total).
- **A/B Group Balance — Passed:** Control: 228 orders / Treatment: 228 orders.
- **Cost Fields — Passed:** No negative values. No missing values in cost columns.
- **Injected Data-Quality Issues — Passed:** 160 missing pincode, 80 variants, 80 duplicates.
- **No-Effect Factors — Passed:** Weekday and product category show no impact (as designed).

## Factors With No Effect
Weekday and product category were deliberately included with no effect, so the analysis can honestly report "no effect" instead of assuming every factor matters.

## Limitations
- All patterns are design assumptions, not discoveries.
- Findings cannot be generalised to real businesses.
- Direct loss excludes lost sales, marketing, and gateway fees.
- "New customer" means first order in the 6-month window.
