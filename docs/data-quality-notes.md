# Data quality notes

## 28 Nov 2026 - NULL container_id in RAW_EVENTS

- Found in Superset: the Container filter showed 11 options (CNT-001 to CNT-010 and NULL).
- Checked in SQL Lab on ATMOSYNC.RAW.RAW_EVENTS (read-only, nothing changed in Snowflake).
- Result: each of the 10 containers has about 1,884 to 1,900 rows. 1 row has no container_id.
- Action: the dbt staging model should filter out rows with a NULL container_id.