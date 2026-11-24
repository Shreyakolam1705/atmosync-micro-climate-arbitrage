
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

BATCH_SIZE = 100

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
    logging.info("Batch size: %d", BATCH_SIZE)
    logging.info("Press Ctrl+C to stop.")

    while True:
        records = consumer.poll(
            timeout_ms=1000,
            max_records=BATCH_SIZE
        )

        # Collect messages from all Kafka partitions
        messages = [
            message
            for partition_records in records.values()
            for message in partition_records
        ]

        if not messages:
            continue

        logging.info(
            "Received %d messages from Kafka. Inserting into Snowflake...",
            len(messages)
        )

        # Convert messages into JSON strings
        payloads = [
            json.dumps(message.value)
            for message in messages
        ]

        # Build one INSERT statement for the entire batch
        placeholders = ", ".join(
            ["(%s)"] * len(payloads)
        )

        insert_query = f"""
            INSERT INTO RAW_EVENTS (RAW_PAYLOAD)
            SELECT PARSE_JSON(column1)
            FROM VALUES {placeholders}
        """

        # Insert the complete batch using one SQL request
        cursor.execute(insert_query, tuple(payloads))

        # Commit Snowflake first, then Kafka offsets
        connection.commit()
        consumer.commit()

        logging.info(
            "Successfully inserted %d messages into Snowflake.",
            len(messages)
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
