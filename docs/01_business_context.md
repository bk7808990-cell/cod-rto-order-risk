# 01 — Business Context

## Domain Overview
- **COD (Cash on Delivery):** Customer pays after delivery.
- **RTO (Return to Origin):** Customer refuses or returns, product goes back.
- **RTO Loss:** Shipping (both sides) + packaging cost.
- **Assumption:** Product returns safely (product cost is not a loss).

## Stakeholders
- **Primary:** D2C Head of Operations (decision maker).
- **Secondary:** Finance Manager, Logistics Manager.

## Decision to be Made
> "Should we call high-risk COD orders before dispatch?"

## Why This Matters
- **Benefit:** RTO % can reduce.
- **Risk:** Call effect is uncertain — no guarantee.
- **Solution:** A/B test (Control vs Treatment groups).

## Business Problem Statement
> "Our online store sells on both prepaid and Cash on Delivery (COD). Some dispatched orders return to origin (RTO), causing shipping and packaging losses. Management does not know which COD orders carry the most RTO risk, or whether a confirmation call reduces it. Decision: Should we call high-risk COD orders before dispatch?"

## Assumptions
- Product returns safely (product cost is not a loss).
- Call cost is Rs 10 per call.
- Call effect is uncertain — no guarantee.

## Limitations
- Synthetic data (no real order-level dataset available).
- All costs and effect sizes are assumptions. 
