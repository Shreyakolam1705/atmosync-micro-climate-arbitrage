
import json
import time
from kafka import KafkaProducer
from simulator import generate_readings

# Connect to local Kafka
producer = KafkaProducer(
    bootstrap_servers="127.0.0.1:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

TOPIC = "container-telemetry"

print("AtmoSync Kafka Producer started!")
print(f"Sending readings to Kafka topic: {TOPIC}")
print("Tracking 10 containers. Press Ctrl+C to stop.\n")

try:
    while True:
        # Generate readings using the shared simulator
        readings = generate_readings()

        # Send each reading to Kafka
        for reading in readings:
            future = producer.send(TOPIC, value=reading)

            # Wait for Kafka acknowledgement
            future.get(timeout=10)

            print("Sent to Kafka:", json.dumps(reading))

        producer.flush()

        print("Batch complete: 10 readings sent.\n")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nAtmoSync Kafka Producer stopped.")

finally:
    producer.close()
