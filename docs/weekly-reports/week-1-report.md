# Week 1 Report (10 to 17 Nov 2026)

Prepared by: Shreya Kolam (Team Lead)
Project: AtmoSync: Micro-Climate Arbitrage Analytics

## Completed
- GitHub repository created with folder structure, README, .gitignore and .env.example.
- Branches created for each team member.
- Shared data schema written (docs/data-schema.md): topic container-telemetry, containers CNT-001 to CNT-010, fields container_id, commodity, timestamp (UTC), temperature, humidity, vibration, lat, lon.
- Work Distribution Document written (docs/work-distribution.md) with a change log.
- Architecture document written (docs/architecture.md).
- 4 milestones and 4 Week 1 Issues (#3 to #6) created with owners and "Done when" criteria.
- Project report outline and daily reports (10 to 16 Nov) written.
- Python IoT simulator for 10 avocado containers, Kafka topic creation script, producer, consumer and docker-compose.yml built by Prakash Naik. Reviewed on GitHub and merged to main through PR #7 on 17 Nov 2026 (merge commit f56832c). The consumer test showed readings from all 10 containers.

## Not completed
- Snowflake setup (Issue #4): account, database, RAW schema, raw table and roles.
- Apache Superset in Docker (Issue #5).
- Integration test simulator -> Kafka -> Snowflake RAW (Issue #6). It is blocked until the Snowflake raw table exists. Issue #3 stays open until this test passes.

## Team status
- Amarnath informed the group in writing on 16 Nov that he cannot continue the internship (screenshot saved). Mentor informed on 17 Nov.
- Aditya Kumar has not confirmed whether he will continue and has not given a start date (screenshots saved). He can rejoin if he confirms in writing with a start date.
- Mentor said in the session to continue with the responsive members.
- Roles updated on 17 Nov: Prakash takes Snowflake setup and dbt in addition to the simulator and Kafka. Shreya takes Apache Superset in addition to Team Lead work.

## Plan for Week 2 (17 to 24 Nov)
- Load test and consumer lag measurement.
- Mock commodity pricing generator.
- Snowflake setup and dbt installation.
- Superset in Docker and baseline dashboard.
- Mid Review preparation.

## Risks
- Shreya has semester exams from 19 Nov to 6 Dec 2026. Mentor informed.
- Prakash now owns four areas of work.