# 04b — Data Cleaning Steps

## Purpose
The raw file contained injected data-quality issues (duplicates, missing values, spelling variants). Power Query Editor was used to clean the data and produce a reporting-ready file.

## Tools Used
- Power Query Editor (Excel)

## Cleaning Steps

| Step | Action | Result |
|---|---|---|
| 1 | Removed duplicate rows on `order_id` | 8,080 → 8,000 rows |
| 2 | Standardized `payment_mode` values | cod, Cod, C.O.D → COD; prepaid, PREPAID → Prepaid |
| 3 | Filled missing `pincode_tier` values | null → Unknown (160 rows) |
| 4 | Rounded `product_cost` to 2 decimals | 189.3660598 → 189.37 |
| 5 | Removed `rto_prob` column | Intermediate calculation, not observed data |

## Why Power Query (Not Python)
- Power Query is repeatable — the same steps run every time.
- Every step is recorded in the Applied Steps pane (visual proof).
- No code to maintain.
- Industry standard for Excel and Power BI workflows.

## Why rto_prob Was Dropped
- It was an intermediate calculation in the generation script.
- It represents a design assumption, not observed data.
- The final dataset should only contain fields that would exist in a real system.

## Final Clean File
- **Rows:** 8,000
- **Columns:** 17
- **File:** `orders_clean.csv`

## Note on Scope
The cleaning covers three common issues in Indian D2C order data: duplicates, missing `pincode_tier`, and `payment_mode` spelling variants. Corporate datasets typically have additional complexity such as multiple source systems, encoding issues, and free-text fields. These were not included to keep the project focused on the business decision rather than data engineering.
