# Superset Setup (AtmoSync)

Apache Superset runs in Docker so the setup is the same on every laptop.

## Files
- Dockerfile: builds our Superset image and installs the Snowflake driver (snowflake-sqlalchemy) inside Superset's own Python folder (/app/.venv).
- docker-compose.yml: starts the Superset container on port 8088.

## Steps
1. Build the image: docker build -t atmosync-superset superset
2. Start Superset: docker compose -f superset/docker-compose.yml up -d
3. Set up the database: docker exec -it atmosync-superset superset db upgrade
4. Create an admin user: docker exec -it atmosync-superset superset fab create-admin (use your own username and password)
5. Create default roles: docker exec -it atmosync-superset superset init
6. Open http://localhost:8088 and log in.

Docker Desktop must be running before step 2.

## Driver note
Superset runs in /app/.venv, not in the system Python. A plain pip install put the driver in the wrong place, so Superset could not see it. The Dockerfile now installs it with:
pip install --target /app/.venv/lib/python3.10/site-packages snowflake-sqlalchemy

## Snowflake connection (read-only)
- Database name in Superset: AtmoSync Snowflake
- Connection type: Snowflake
- User: ATMOSYNC_BI_USER, Role: ATMOSYNC_BI_READONLY
- Warehouse: ATMOSYNC_WH, Database: ATMOSYNC, Schema: RAW
- Account: use the Snowflake account identifier shared by the team.
- The password is shared privately and is never stored in GitHub.
- Settings used: DML off, SQL Lab on.

## Datasets
- raw_events: the table ATMOSYNC.RAW.RAW_EVENTS (columns RAW_PAYLOAD and INGESTED_AT).
- iot_readings: a virtual dataset made in SQL Lab. It reads the JSON in RAW_PAYLOAD and gives normal columns. Nothing is changed in Snowflake.

```
SELECT
  RAW_PAYLOAD:container_id::STRING AS container_id,
  RAW_PAYLOAD:commodity::STRING AS commodity,
  RAW_PAYLOAD:temperature::FLOAT AS temperature,
  RAW_PAYLOAD:humidity::FLOAT AS humidity,
  RAW_PAYLOAD:vibration::FLOAT AS vibration,
  RAW_PAYLOAD:lat::FLOAT AS lat,
  RAW_PAYLOAD:lon::FLOAT AS lon,
  TO_TIMESTAMP_NTZ(RAW_PAYLOAD:timestamp::STRING) AS reading_time
FROM ATMOSYNC.RAW.RAW_EVENTS
```

## Dashboard: Container overview
- Raw events row count (Big Number)
- Temperature over time (Line Chart, average temperature)
- Humidity over time (Line Chart, average humidity)
- Container locations map (deck.gl Scatterplot, LON and LAT)
- Filter: Container (CONTAINER_ID)

## Screenshots
- docs/superset-snowflake-proof.png: Superset reads 10 rows from Snowflake.
- docs/superset-container-overview.png: dashboard with a container filter.
- docs/superset-dashboard-with-map.png: dashboard with the locations map.

## Known data issue
1 row in RAW_EVENTS has no container_id. See docs/data-quality-notes.md.

## Status (28 Nov 2026)
- Superset runs in Docker and is connected to Snowflake (read-only).
- Dashboard Container overview has 4 charts and a container filter.
- Next: arbitrage dashboard (after the dbt spoilage_arbitrage model), alerts.