# 07 — Recommendations & Impact

## Executive Summary
Based on the A/B test simulation and unit economics, I recommend implementing a targeted confirmation call strategy specifically for high-risk COD orders. This is a decision tool, not just a dashboard.

## The Pilot Plan
- **Target:** Call the 500 highest-risk COD orders first.
- **Action:** Call before dispatch to confirm the order.
- **Cost:** Rs 10 per call (Total pilot cost: Rs 5,000).
- **Expected Outcome:** If the RTO drops by 8.33 points (as seen in our A/B test), we prevent about 41.65 RTOs. At a loss of Rs 196.02 per RTO, we save approximately Rs 8,163 in shipping and packaging costs. The net benefit for this pilot will be **+Rs 3,163**.

## Unit Economics (The "Why")
- **Loss per RTO:** Rs 196.02.
- **Margin per Delivered Order:** Rs 670.70.
- **Break-even:** If a call costs Rs 10, the RTO needs to drop by at least 5.1 points just to break even.
- **Decision:** If the call reduces RTO by more than 5.1 points, it is profitable.

## Impact (3 Levels)
I calculated the expected impact at three different levels to show the scale of the solution:

1. **Unit Level:** Rs 196 loss avoided minus Rs 10 call cost = Rs 186 net benefit per prevented RTO.
2. **Segment Level:** For all 456 high-risk orders, a 5-point reduction saves Rs 4,469, but the calls cost Rs 4,560. This means we are at break-even, and we need a reduction greater than 5 points to make a real profit here.
3. **Portfolio Level:** The total RTO loss across all dispatched orders is Rs 2,35,415. If we apply this strategy to all 7,600 dispatched orders and reduce RTO by 5 points, we can potentially save around Rs 74,480 against a call cost of Rs 76,000 (essentially breaking even).

## Limitations & Next Steps
- **Data Note:** This project uses synthetic data, so all findings are design assumptions, not real-world discoveries.
- **Next Step:** Do not scale this to all 8,000 orders immediately. Execute the 500-order pilot first to validate the actual RTO reduction in the real world.
