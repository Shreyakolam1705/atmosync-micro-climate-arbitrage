
import os
import json
import logging

import snowflake.connector
from dotenv import load_dotenv
from kafka import KafkaConsumer

# Load environment variables from the project root .env file
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

TOPIC = "container-telemetry"
BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092"
)

consumer = None
connection = None
cursor = None

try:
    # Connect to Snowflake
    logging.info("Connecting to Snowflake...")

    connection = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )

    cursor = connection.cursor()
    logging.info("Connected to Snowflake successfully.")

    # Connect to Kafka
    logging.info("Connecting to Kafka...")

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id="atmosync-snowflake-loader",
        enable_auto_commit=False,
        auto_offset_reset="earliest",
        value_deserializer=lambda message: json.loads(
            message.decode("utf-8")
        )
    )

    logging.info("Connected to Kafka.")
    logging.info("Listening for messages from topic: %s", TOPIC)
    logging.info("Press Ctrl+C to stop.")

    while True:
        records = consumer.poll(timeout_ms=1000, max_records=100)

        for partition_records in records.values():
            for message in partition_records:
                payload = json.dumps(message.value)

                cursor.execute(
                    """
                    INSERT INTO RAW_EVENTS (RAW_PAYLOAD)
                    SELECT PARSE_JSON(%s)
                    """,
                    (payload,)
                )

        # Commit Snowflake first, then Kafka offsets.
        if records:
            connection.commit()
            consumer.commit()

            message_count = sum(
                len(partition_records)
                for partition_records in records.values()
            )

            logging.info(
                "Successfully inserted %d messages into Snowflake.",
                message_count
            )

except KeyboardInterrupt:
    logging.info("Loader stopped by user.")

except Exception:
    if connection:
        connection.rollback()

    logging.exception("Kafka-to-Snowflake loader failed.")

finally:
    if consumer:
        consumer.close()

    if cursor:
        cursor.close()

    if connection:
        connection.close()

    logging.info("Loader shut down.")
