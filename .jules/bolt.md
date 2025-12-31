## 2025-12-31 - [Excessive Rounding in Frame Loop]
**Learning:** In a physics simulation loop running at 250 FPS (attempted), iterating over all bodies and calling `round()` on their properties multiple times per frame resulted in over 3 million calls to `round()` in a 15-second run. This creates significant overhead.
**Action:** When collecting data for later use (like keyframes), consider if rounding is strictly necessary per frame or if it can be done at export time. Also, optimize repeated calculations involving constants.
