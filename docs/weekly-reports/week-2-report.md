# Week 2 Report (18 to 28 Nov 2026)

## Completed
- Kafka load test: 100,000 records sent, producer speed 5,392 records per second, consumer read all records, lag 0 on all 3 partitions (docs/load-test-results.md).
- Snowflake: raw table ATMOSYNC.RAW.RAW_EVENTS and roles ATMOSYNC_LOADER and ATMOSYNC_BI_READONLY exist (Prakash). Kafka to Snowflake insert test on 25 Nov: 49 messages received, 49 inserted.
- kafka_to_snowflake.py now checks that all required Snowflake settings exist before it connects (commit b19cba1, Prakash). No passwords are stored in GitHub.
- dbt (Prakash): staging models for IoT and commodity prices (commit 6a06a4a). dbt compile found 4 models, 4 data tests and 2 sources, exit code 0. dbt test: 9 of 9 passed (screenshot received 28 Nov).
- Apache Superset runs in Docker, connected to Snowflake with the read-only role. SQL Lab read 10 rows from RAW_EVENTS (docs/superset-snowflake-proof.png).
- Superset dashboard "Container overview": 4 charts (raw events row count, temperature over time, humidity over time, container locations map) and a Container filter (docs/superset-dashboard-with-map.png).
- Data quality check: 1 row in RAW_EVENTS has no container_id (docs/data-quality-notes.md).
- GitHub Issues #5 and #8 closed with proof. Issue #4 assigned to Prakash.

## Not completed
- Full pipeline run end to end (simulator, Kafka, Snowflake, dbt, Superset).
- Consumer batch size tuning.
- Merge of branch prakash and branch shreya into main.
- Snowflake insert speed under load, and the join of IoT and pricing data in the dbt staging model.
- Confirmation that the dbt staging model filters out the NULL container_id row.
- Mid Review dry run.

## Team status
- Amarnath left the internship (written message). Aditya Kumar replied No on 17 Nov.
- Mentor said in the session to continue with the responsive members.
- Prakash works on simulator, Kafka, Snowflake and dbt. Shreya works on Superset, GitHub, documentation and integration.

## Risks
- The dbt spoilage_arbitrage model is needed before the arbitrage dashboard can be built (planned for 1 Dec).
- Two members now cover the work of four, so the schedule is tight until 4 Dec.