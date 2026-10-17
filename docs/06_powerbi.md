# 06 — Power BI Dashboard

This page documents the 5-page Power BI dashboard I built for the COD/RTO analysis.

## Data & Design Setup
- **Data Source:** `orders_clean.csv` (8,000 rows, 17 columns)
- **Theme:** I used a light grey canvas background (`#F5F5F5`) with pure white cards (`#FFFFFF`) so the data stands out clearly.
- **Font:** Segoe UI.

## The Logic Behind the Numbers
I created all my measures in a dedicated `_Measures` table to keep the data model clean. Instead of pasting the raw DAX code here, I have documented the business logic, as that is what matters most for decision-making:

- **RTO %:** I divided the count of RTO orders by the total dispatched orders (excluding cancellations). The result is 15.80%.
- **A/B Test (Control vs Treatment):** I used the same RTO % logic but applied a filter for the 'Control' group and then the 'Treatment' group. This showed that the Control group had a 33.77% RTO, while the Treatment group dropped to 25.44%.
- **A/B Reduction:** This is a simple subtraction (Control RTO % minus Treatment RTO %). The result is an 8.33 percentage point reduction.
- **Simulator (What-If):** The logic for the sliders on Page 5 is: (Total High-Risk Orders × Reduction % × Loss per RTO) - (Total High-Risk Orders × Call Cost). This calculates the live net benefit to see if the call strategy is profitable.

## Page by Page Breakdown
- **Page 1 (Overview):** 6 KPI cards, RTO % by Payment Mode (Bar chart), Delivery Status (Donut chart), and a Key Finding text box.
- **Page 2 (Risk Segments):** 3 KPI cards (High-Risk Count, Control, Treatment), RTO % by Value Band, RTO % by Pincode, and a table showing top loss pincodes. I also added a Pincode Tier slicer for interactivity.
- **Page 3 (A/B Result):** 3 KPI cards (I highlighted the Reduction card in green), a Control vs Treatment bar chart, and a Key Insight text box.
- **Page 4 (Loss & Unit Economics):** 3 KPI cards (Avg Loss, Total Loss, Avg Margin), Loss by Pincode (Bar chart), Monthly Trend (Line chart), and a Pareto table.
- **Page 5 (Recommendations & Simulator):** A pilot plan text box, 2 sliders (Call cost, Reduction %), and 2 cards showing the live net benefit and break-even point.

## Things I Got Stuck On (And How I Fixed Them)
While building this, I ran into a few technical hurdles in Power BI. I am noting them here as a troubleshooting log:

1. **Cards showing "8K" instead of "8000":** I went to Format visual > Callout values > selected the measure under "Apply settings to" > and changed Display units to None.
2. **Date column showing empty:** The date was in DD-MM-YYYY format, so I changed the `order_date` data type to Text in Power Query.
3. **Missing labels on the Donut chart:** The Cancelled slice (400 orders) was too small, so I turned on "Overflow" in the Detail labels settings.
4. **A/B chart showing "Not Eligible":** I applied a visual-level filter to the bar chart to only show "Control" and "Treatment" groups.
5. **Table name confusion:** Power BI auto-named my table "orders_raw (2)". I renamed it to `orders_clean` before writing any DAX measures.

## A Note on AI Use
I designed the business rules, logic, and dashboard layout myself. I used AI to help write the DAX syntax, but I reviewed every line and validated the output against my SQL and Excel analysis. All the numbers in the dashboard exactly match the validated analysis phase.
