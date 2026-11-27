# Superset Setup (AtmoSync)

Apache Superset runs in Docker so the setup is the same on every laptop.

## Files
- Dockerfile: builds our Superset image with the Snowflake driver (snowflake-sqlalchemy).
- docker-compose.yml: starts the Superset container on port 8088.

## Steps
1. Build the image: docker build -t atmosync-superset superset
2. Start Superset: docker compose -f superset/docker-compose.yml up -d
3. Set up the database: docker exec -it atmosync-superset superset db upgrade
4. Create an admin user: docker exec -it atmosync-superset superset fab create-admin (use your own username and password)
5. Create default roles: docker exec -it atmosync-superset superset init
6. Open http://localhost:8088 and log in.

## Snowflake connection (read-only)
- Role: ATMOSYNC_BI_READONLY
- Warehouse: ATMOSYNC_WH, Database: ATMOSYNC, Schema: RAW
- The password is shared privately and is never stored in GitHub.

## Status (27 Nov 2026)
- Docker image built, Superset running, admin login works.
- Next: connect to Snowflake and create a dataset from RAW_EVENTS.