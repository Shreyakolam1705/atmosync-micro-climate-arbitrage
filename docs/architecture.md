# AtmoSync – System Architecture

## 1. Project Overview

AtmoSync (Micro-Climate Arbitrage Analytics) is a data analytics project designed to collect container-level environmental telemetry and store it for further analysis.

The system simulates environmental readings from containers transporting commodities. These readings are streamed through Apache Kafka and ingested into Snowflake for data storage and downstream analytics.

## 2. System Data Flow

The current data pipeline follows this flow:

Python IoT Simulator → Apache Kafka → Kafka-to-Snowflake Loader → Snowflake → dbt

## 3. Components

### 3.1 Python IoT Simulator

The simulator generates sample telemetry readings for 10 containers (CNT-001 to CNT-010).

The readings include:
- Container ID
- Commodity
- Timestamp
- Temperature
- Humidity
- Vibration
- Latitude
- Longitude

The current Week 1 configuration uses avocado as the commodity for all containers.

### 3.2 Apache Kafka

Apache Kafka is used as the messaging system between the simulator and the data ingestion layer.

Topic:
- container-telemetry

The Python producer publishes telemetry messages to this topic. Kafka allows the ingestion service to consume messages independently of the simulator.

### 3.3 Kafka-to-Snowflake Loader

The Python loader consumes telemetry messages from Kafka and writes the received data into Snowflake.

Responsibilities:
- Connect to Kafka
- Subscribe to the telemetry topic
- Consume messages
- Insert telemetry into Snowflake
- Commit Kafka offsets after successful processing

The loader uses environment-based configuration for connection credentials.

### 3.4 Snowflake

Snowflake is used as the cloud data warehouse for storing telemetry.

Current database objects:
- Database: ATMOSYNC
- Warehouse: ATMOSYNC_WH
- Schema: RAW
- Table: RAW_EVENTS

The RAW_EVENTS table stores the original telemetry payload in a VARIANT column and records the ingestion timestamp.

### 3.5 dbt

dbt Core with the Snowflake adapter is configured for the AtmoSync project.

Current dbt work includes:
- Project initialization
- Snowflake connection configuration
- Source definition for RAW_EVENTS
- Source freshness monitoring

The local profiles.yml contains connection credentials and must never be committed to GitHub. The repository contains profiles.yml.example as a credential-free template.

## 4. Data Storage

The RAW_EVENTS table contains:

| Column | Description |
|---|---|
| RAW_PAYLOAD | Raw telemetry JSON stored as VARIANT |
| INGESTED_AT | Timestamp indicating when the record was ingested |

The telemetry payload contains container environmental readings.

## 5. Security

- Credentials are stored locally in environment variables or local configuration.
- The .env file is excluded from Git.
- Real dbt profiles.yml files are not committed.
- ATMOSYNC_LOADER is intended for data ingestion.
- ATMOSYNC_BI_READONLY is intended for read-only analytics access.

## 6. Current Project Status

Implemented:
- Python telemetry simulator
- Kafka producer and consumer
- Kafka telemetry topic
- Snowflake database and RAW_EVENTS table
- Kafka-to-Snowflake ingestion script
- Snowflake loader and BI read-only roles
- dbt Core project setup
- dbt source configuration
- Source freshness checks

Further analytics transformations and dashboard development can be extended in subsequent project phases.

## 7. End-to-End Workflow

1. The simulator generates telemetry readings.
2. The Kafka producer sends readings to container-telemetry.
3. The Kafka-to-Snowflake loader consumes the messages.
4. The loader inserts raw telemetry into ATMOSYNC.RAW.RAW_EVENTS.
5. dbt checks source availability and freshness.
6. The stored telemetry can be used for downstream analytics and visualization.
