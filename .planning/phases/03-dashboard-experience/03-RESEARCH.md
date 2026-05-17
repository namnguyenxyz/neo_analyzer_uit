---
phase: 03-dashboard-experience
subsystem: dashboard
tags: [streamlit, duckdb, plotly]
key-files:
  - src/dashboard/app.py
  - src/dashboard/ui.py
  - src/dashboard/data_access.py
metrics:
  expected_interactive_latency_ms: 500
  memory_budget_mb: 1024
---

# Phase 03 Research

Goal: Provide a low-memory Streamlit dashboard that reads `neo_analytics.db` in read-only mode and surfaces core KPIs and a fast explorer table.

Constraints:
- Target 4GB-8GB RAM machines; prefer DuckDB vectorized reads over in-memory materialization.
- Avoid heavy front-end frameworks; use Streamlit + Plotly Express.

Key UX elements:
- KPI cards: total NEOs, total PHAs, closest approach today.
- Explorer: searchable/filterable table with pagination and on-demand DuckDB queries.
- Visuals: size distribution histogram, approach velocity scatter.

Data access:
- Use DuckDB read-only connection to `neo_analytics.db` via `duckdb.connect(..., read_only=True)`.
- Support simple parameterized query helpers in `src/dashboard/data_access.py`.

Security & ops:
- Dashboard should run as a user process; document `streamlit run src/dashboard/app.py` usage.
