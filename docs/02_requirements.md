# 02 — Requirements (BRD-lite)

## Purpose
To analyse RTO risk for COD orders, calculate unit economics, and simulate the impact of a confirmation call strategy.

## Scope
**In Scope:**
- Analysis of COD and prepaid orders
- RTO risk identification by segment
- Unit economics (margin, loss)
- A/B test simulation (call vs no call)
- Power BI dashboard with what-if parameters

**Out of Scope:**
- Real customer data
- Marketing cost, gateway fees
- Lost sales revenue
- Real-world implementation

## Business Rules
- **RTO %:** RTO orders / dispatched orders (cancelled excluded).
- **Loss per RTO:** Shipping + return shipping + packaging.
- **Margin per delivered order:** Order value - product cost - shipping - packaging.
- **High-risk:** COD + New customer + Order value >= Rs 1,500 + Tier-3/Remote.
- **Call cost:** Rs 10 per call (assumption).

## Success Criteria
- High-risk COD segment identified (456 orders, 5.7% of total).
- Control group RTO: 33.77%.
- Treatment group RTO: 25.44% (8.33 point reduction simulated).
- Break-even point calculated for call cost (5.1 points at Rs 10).
- Interactive dashboard with simulation sliders.
- Recommendation backed by sensitivity analysis.

## Stakeholders
- **Primary:** D2C Head of Operations (decision maker).
- **Secondary:** Finance Manager, Logistics Manager.

## Assumptions
- Product returns safely (product cost is not a loss).
- Call effect is uncertain (no guarantee).
- All costs are design assumptions (synthetic data).
- High-risk flag focuses on customer-side risk only (Courier B is not included in the flag).
