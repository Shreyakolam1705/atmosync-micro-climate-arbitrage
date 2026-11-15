# AtmoSync Architecture

## 1. Pipeline flow

Python IoT simulator -> Kafka (topic: container-telemetry) -> Snowflake RAW table -> dbt (staging, spoilage and arbitrage models) -> Apache Superset dashboards and Slack/email alerts

## 2. Who owns each part

| Stage | Tool | Owner | Branch |
|---|---|---|---|
| IoT simulator | Python | Prakash Naik | prakash |
| Streaming | Apache Kafka | Prakash Naik | prakash |
| Raw storage | Snowflake | Amarnath | amar |
| Transformation | dbt Core (SQL) | Amarnath | amar |
| Dashboards and alerts | Apache Superset | Aditya Kumar | Aditya |
| Integration, docs, PR merges | GitHub | Shreya Kolam (Team Lead) | shreya |

## 3. Shared schema

Kafka topic: `container-telemetry`
Containers: CNT-001 to CNT-010
Timestamps: UTC

| Field | Meaning | Unit / format |
|---|---|---|
| container_id | Container name | CNT-001 to CNT-010 |
| commodity | What is inside (Week 1: avocado only) | lowercase name |
| timestamp | Time of the reading | ISO 8601, UTC |
| temperature | Temperature inside the container | degrees Celsius |
| humidity | Humidity inside the container | percent (0 to 100) |
| vibration | Vibration reading | g-force |
| lat | Latitude of the container | decimal degrees |
| lon | Longitude of the container | decimal degrees |

Missing sensor values must be sent as null, never as 0 (not implemented yet, planned for Week 2).

## 4. Snowflake

- Database: ATMOSYNC
- Schema: RAW
- Raw table: one row per Kafka message, with the full JSON stored in a VARIANT column, plus a load timestamp.
- Two roles: a loader role (writes raw data) and a read-only BI role (used by Superset).
- Later layers (dbt staging, spoilage and arbitrage models) are added in Weeks 2 and 3.