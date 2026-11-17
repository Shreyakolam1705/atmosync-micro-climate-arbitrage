
# Import Kafka admin tools
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

# Kafka topic settings
BOOTSTRAP_SERVERS = "127.0.0.1:9092"
TOPIC_NAME = "container-telemetry"

# Create Kafka admin client
admin = KafkaAdminClient(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    client_id="atmosync-topic-creator"
)

try:
    # Define the topic
    topic = NewTopic(
        name=TOPIC_NAME,
        num_partitions=3,
        replication_factor=1
    )

    # Create the topic
    try:
        admin.create_topics(new_topics=[topic])
        print(f"Topic '{TOPIC_NAME}' created successfully!")

    except TopicAlreadyExistsError:
        print(f"Topic '{TOPIC_NAME}' already exists.")

    # Confirm that the topic exists
    topics = admin.list_topics()

    if TOPIC_NAME in topics:
        print(f"Verified: '{TOPIC_NAME}' exists in Kafka.")
    else:
        raise RuntimeError("Topic creation could not be verified.")

finally:
    # Close Kafka admin connection
    admin.close()
