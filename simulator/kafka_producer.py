
import json
import random
import time
from datetime import datetime, timezone
from kafka import KafkaProducer

# Connect Python to local Kafka
producer = KafkaProducer(
    bootstrap_servers="127.0.0.1:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

# Generate 10 container IDs
containers = {
    f"CNT-{i:03d}": random.uniform(5.0, 7.0)
    for i in range(1, 11)
}

# Starting GPS coordinates
START_LATITUDE = 12.9716
START_LONGITUDE = 77.5946

# Give each container a different starting position
container_positions = {
    container_id: {
        "lat": START_LATITUDE + index * 0.0005,
        "lon": START_LONGITUDE + index * 0.0005
    }
    for index, container_id in enumerate(containers)
}

# Simulate one faulty container
faulty_container = "CNT-002"

# Eastward movement per cycle
MOVEMENT_STEP = 0.0001

print("AtmoSync Kafka Producer started!")
print("Sending 10 avocado container readings...\n")

try:
    while True:

        for container_id in containers:

            # Simulate temperature changes
            if container_id == faulty_container:
                containers[container_id] += 0.15
            else:
                containers[container_id] += random.uniform(-0.2, 0.2)

            position = container_positions[container_id]

            # Generate UTC timestamp
            timestamp = (
                datetime.now(timezone.utc)
                .isoformat(timespec="seconds")
                .replace("+00:00", "Z")
            )

            # Create message according to official schema
            reading = {
                "container_id": container_id,
                "commodity": "avocado",
                "timestamp": timestamp,
                "temperature": round(containers[container_id], 2),
                "humidity": round(random.uniform(80, 95), 2),
                "vibration": round(random.uniform(0.1, 2.0), 2),
                "lat": round(position["lat"], 6),
                "lon": round(position["lon"], 6)
            }

            # Send reading to Kafka
            producer.send("container-telemetry", value=reading)

            print("Sent:", reading)

            # Move container eastward
            position["lon"] += MOVEMENT_STEP

        producer.flush()

        time.sleep(2)

except KeyboardInterrupt:
    print("\nAtmoSync Kafka Producer stopped.")

finally:
    producer.close()
