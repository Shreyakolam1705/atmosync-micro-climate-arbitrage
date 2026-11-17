import json
import time

from kafka import KafkaProducer
from simulator import generate_readings, INTERVAL_SECONDS

TOPIC = "container-telemetry"

producer = KafkaProducer(
    bootstrap_servers="127.0.0.1:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

print("AtmoSync Kafka Producer started!")
print(f"Sending 10 avocado container readings to topic: {TOPIC}")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        readings = generate_readings()

        for reading in readings:
            future = producer.send(TOPIC, value=reading)
            future.get(timeout=10)
            print("Sent to Kafka:", json.dumps(reading))

        producer.flush()
        print("-" * 60)
        time.sleep(INTERVAL_SECONDS)

except KeyboardInterrupt:
    print("\nKafka Producer stopped.")

finally:
    producer.close()
