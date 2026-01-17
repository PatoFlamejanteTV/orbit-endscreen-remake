## 2024-05-22 - Broken Optimization Caused Crash
**Learning:** Always verify that optimization placeholders (like comments describing code) are actually implemented. The `orbit remake.py` contained a cache block `if not hasattr(body, 'bolt_cached_data'):` that relied on variables (`dropped`, `size_val`, `is_poly`) that were never defined, causing a guaranteed runtime crash.
**Action:** When seeing incomplete code or "optimization" comments, treat them as potential bugs. Verify correctness before attempting further optimization.
