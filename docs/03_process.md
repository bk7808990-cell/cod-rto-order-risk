# 03 — Process (AS-IS, TO-BE)

## AS-IS Process (Current State)
- **Step 1:** Order received from customer (COD or Prepaid).
- **Step 2:** Order is dispatched without any risk check.
- **Step 3:** Delivery attempted at customer address.
  - *Decision Point:* Does customer accept the order?
  - *If Yes:* Order delivered, payment collected (COD) or already paid (Prepaid).
  - *If No:* Product returns to origin (RTO).
- **Step 4:** RTO causes shipping and packaging loss to seller.

### Current Process Gaps
- No risk check before dispatch.
- No confirmation call for high-risk orders.
- RTO loss is not tracked by segment.
- No data on which orders are risky.

## TO-BE Process (Future State — Proposed)
- **Step 1:** Order received from customer (COD or Prepaid).
- **Step 2:** Risk check runs automatically.
  - *Decision Point:* Is the order high-risk COD?
  - *If No:* Dispatch immediately (same as AS-IS).
  - *If Yes:* Proceed to confirmation call.
- **Step 3:** Confirmation call made to customer.
  - *Decision Point:* Does customer confirm the order?
  - *If Yes:* Dispatch order.
  - *If No:* Cancel before dispatch (saves shipping and packaging).
- **Step 4:** RTO loss tracked by segment in dashboard.

### Expected Benefits (from A/B simulation)
- High-risk orders identified before dispatch.
- RTO reduction simulated at 5 points (Control vs Treatment).
- Break-even analysis shows call cost vs loss saved.
