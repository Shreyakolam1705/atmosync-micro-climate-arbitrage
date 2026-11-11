# AtmoSync: Micro-Climate Arbitrage Analytics

AtmoSync watches the conditions inside shipping containers (temperature, humidity and vibration) and estimates how long perishable goods will stay sellable. When a container is at risk, it points the trader to a closer market so the cargo can be sold before it spoils.

This repository is the Infotact Solutions internship project for the Data Analytics domain.

## How data flows
Simulator -> Kafka -> Snowflake -> dbt -> Superset

## Team
| Member | Role |
|---|---|
| Shreya Kolam | Team Lead, coordination, documentation, integration |
| Prakash Naik | Python IoT simulator and Kafka streaming |
| Amarnath | Snowflake, dbt and SQL models |
| Aditya | Superset dashboards and alerts |

## Folders
- simulator/ : sensor data generator and Kafka producer/consumer
- snowflake/ : warehouse, schema and table setup
- dbt/ : staging and analytics models
- superset/ : dashboard and alert configuration
- data/sample/ : small sample files for testing
- docs/ : work distribution, daily and weekly reports

## Working rules
- Every member commits only to their own branch.
- The Team Lead merges branches into main through pull requests.
- No passwords or real .env files are committed.
