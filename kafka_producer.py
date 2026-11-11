
import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

# Connect Python to our local Kafka server
producer = KafkaProducer(
    bootstrap_servers="127.0.0.1:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

containers = [
    "CONT-001",
    "CONT-002",
    "CONT-003",
    "CONT-004",
]

print("AtmoSync Kafka Producer started!")
print("Sending avocado sensor readings...\n")

try:
    while True:
        for container in containers:
            reading = {
                "container_id": container,
                "commodity": "Avocados",
                "timestamp": datetime.now().isoformat(),
                "temperature_c": round(random.uniform(4, 12), 2),
                "humidity_pct": round(random.uniform(80, 95), 2),
                "vibration": round(random.uniform(0.1, 2.0), 2)
            }

            producer.send("sensor-readings", value=reading)

            print("Sent:", reading)

        producer.flush()
        time.sleep(2)

except KeyboardInterrupt:
    print("\nAtmoSync producer stopped.")

finally:
    producer.close()
