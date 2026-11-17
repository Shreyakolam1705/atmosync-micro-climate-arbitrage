
import argparse
import json
import logging

from kafka import KafkaConsumer
from kafka.errors import KafkaError


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def parse_arguments():
    """Read command-line options."""
    parser = argparse.ArgumentParser(
        description="AtmoSync Kafka Consumer"
    )

    parser.add_argument(
        "--topic",
        default="container-telemetry",
        help="Kafka topic name (default: container-telemetry)"
    )

    parser.add_argument(
        "--bootstrap-servers",
        default="127.0.0.1:9092",
        help="Kafka server address (default: 127.0.0.1:9092)"
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    consumer = None

    logger.info("Starting AtmoSync Kafka Consumer")
    logger.info("Kafka server: %s", args.bootstrap_servers)
    logger.info("Kafka topic: %s", args.topic)

    try:
        # Connect to Kafka
        consumer = KafkaConsumer(
            bootstrap_servers=args.bootstrap_servers,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="atmosync-test-consumer",
            request_timeout_ms=10000,
        )

        # Check whether the topic exists
        partitions = consumer.partitions_for_topic(args.topic)

        if not partitions:
            logger.error(
                "Topic '%s' does not exist or has no partitions. "
                "Please create the topic first.",
                args.topic
            )
            return

        # Subscribe to the topic
        consumer.subscribe([args.topic])

        logger.info(
            "Connected successfully. Waiting for messages..."
        )

        # Receive messages in batches
        while True:
            batches = consumer.poll(timeout_ms=1000)

            for topic_partition, messages in batches.items():
                logger.info(
                    "Received batch of %d messages from topic '%s'",
                    len(messages),
                    topic_partition.topic
                )

                for message in messages:
                    try:
                        reading = json.loads(
                            message.value.decode("utf-8")
                        )

                        logger.info("Received reading: %s", reading)

                    except (json.JSONDecodeError, UnicodeDecodeError) as error:
                        logger.error(
                            "Invalid message received: %s",
                            error
                        )

    except KafkaError as error:
        logger.error(
            "Kafka connection or operation failed at %s: %s",
            args.bootstrap_servers,
            error
        )

    except OSError as error:
        logger.error("Connection error: %s", error)

    except KeyboardInterrupt:
        logger.info("Consumer stopped by user.")

    finally:
        if consumer is not None:
            try:
                consumer.close()
                logger.info("Kafka consumer connection closed.")
            except Exception as error:
                logger.error("Error while closing consumer: %s", error)


if __name__ == "__main__":
    main()
