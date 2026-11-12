
import json
import time

from kafka import KafkaProducer
from simulator import generate_reading

TOPIC = "container-telemetry"

producer = KafkaProducer(
    bootstrap_servers="127.0.0.1:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

print("AtmoSync Kafka Producer started!")
print(f"Sending CNT-001 readings to topic: {TOPIC}")
print("Sending one reading every second. Press Ctrl+C to stop.\n")

try:
    while True:
        # Generate one reading from the shared simulator
        reading = generate_reading()

        # Send reading to Kafka
        future = producer.send(TOPIC, value=reading)

        # Wait for Kafka acknowledgement
        future.get(timeout=10)

        print("Sent to Kafka:", json.dumps(reading))

        producer.flush()
        time.sleep(1)

except KeyboardInterrupt:
    print("\nKafka Producer stopped.")

finally:
    producer.close()
