---
phase: 04-hardening-and-delivery
subsystem: release-hardening
tags: [requirements, docs, smoke-test]
key-files:
  - requirements.txt
  - README.md
  - src/analytics/build_analytics_db.py
  - src/dashboard/app.py
metrics:
  expected_release_checks: 3
  dependency_pins: 7
---

# Phase 04 Research

Phase 4 is a hardening pass rather than a feature build. The current repository already contains exact dependency pins, smoke commands, analytics validation, and dashboard launch instructions, so the main work is to confirm the delivery surface is consistent and complete.

Primary concerns:
- Ensure `requirements.txt` remains fully pinned and aligned with the workspace environment.
- Ensure `README.md` includes start order, phase-specific smoke checks, and the dashboard launch path.
- Ensure a clean release smoke path still works end-to-end with the local sample data and local DuckDB file.

Recommended execution shape:
- Wave 1: dependency manifest audit and version consistency checks.
- Wave 2: documentation hardening and troubleshooting review.
- Wave 3: end-to-end release smoke validation and delivery sign-off.
