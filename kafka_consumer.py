
import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "sensor-readings",
    bootstrap_servers="127.0.0.1:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="atmosync-test-consumer"
)

print("AtmoSync Kafka Consumer started!")
print("Waiting for sensor readings...\n")

try:
    for message in consumer:
        print("Received:", message.value)

except KeyboardInterrupt:
    print("\nConsumer stopped.")

finally:
    consumer.close()
