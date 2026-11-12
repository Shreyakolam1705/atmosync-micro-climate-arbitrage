# Work Distribution Document

- **Project:** AtmoSync: Micro-Climate Arbitrage Analytics
- **Team Lead:** Shreya Kolam
- **Project window:** 10 Nov 2026 to 10 Dec 2026
- **Mid Review:** 27 to 30 Nov 2026 (as informed by mentor, to be confirmed)
- **Final Review:** Date to be confirmed

## Team and roles
| Member | Role | Branch | Main ownership |
|---|---|---|---|
| Shreya Kolam | Team Lead, Project Coordinator, Documentation, Integration | shreya | GitHub, documentation, PR reviews, reports, mentor communication |
| Prakash Naik | Python IoT Simulator + Apache Kafka Developer | prakash | Simulator and Kafka streaming |
| Amarnath | Snowflake + dbt + SQL Data Engineer | amarnath | Snowflake, dbt, analytical models |
| Aditya | Apache Superset + BI Dashboard + Alerts Developer | Aditya | Dashboards, visualization, alerts |

## Week 1 (11 to 17 Nov): Foundation
| Member | Tasks |
|---|---|
| Shreya | Repo, branches, folder structure, README, data schema, architecture document, PR reviews, merge to main |
| Prakash | Python environment, telemetry schema, simulator for one then multiple containers, Kafka setup, topic, producer |
| Amarnath | Snowflake account, database ATMOSYNC, warehouse, RAW schema, raw readings table, roles, commodity prices table |
| Aditya | Docker, Superset running locally, connect to Snowflake, user roles |

## Week 2 (18 to 24 Nov): ELT and baseline dashboards
| Member | Tasks |
|---|---|
| Shreya | Weekly report, bug tracking, test plan, end-to-end test, mentor update, Mid Review preparation |
| Prakash | Kafka consumer into Snowflake RAW, commodity pricing generator, drift and spike scenarios, load test |
| Amarnath | dbt setup, sources, staging models for readings and prices, dbt tests |
| Aditya | Baseline charts (temperature, humidity, container routes), Container Overview dashboard |

## Weeks 3 and 4 (25 Nov to 8 Dec)
To be added after the Mid Review. Week 3: spoilage arbitrage models and at-risk dashboard. Week 4: automation, query optimisation and Slack/email alerts.

## Working rules
- Everyone commits only to their own branch, at least once a day.
- The Team Lead merges branches into main through pull requests.
- Messages are answered within 24 hours. A member silent for 48 hours is reported to the mentor.
- No passwords or real .env files in the repo.

## Change log
| Date | Change | Updated by |
|---|---|---|
| 11 Nov 2026 | First version: roles and Weeks 1 and 2 | Shreya |
| 11 Nov 2026 | Mid Review date updated to 27 to 30 Nov, Final Review date pending | Shreya |
| 12 Nov 2026 | Week dates corrected to 11 to 17 Nov, 18 to 24 Nov, 25 Nov to 8 Dec | Shreya |
| 12 Nov 2026 | Aditya is unwell and away for about a week; review on Mon 16 Nov, his Superset tasks may move to about 18 Nov | Shreya |
