FROM apache/superset:latest
USER root
RUN pip install --target /app/.venv/lib/python3.10/site-packages snowflake-sqlalchemy
USER superset