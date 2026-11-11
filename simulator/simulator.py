
from datetime import datetime, timezone
import json
import random
import time
from pathlib import Path

# Save generated readings outside the sample-data folder
OUTPUT_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "generated"
    / "readings.jsonl"
)

# Create the output folder automatically if it doesn't exist
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Generate 10 containers with starting temperatures
containers = {
    f"CNT-{i:03d}": random.uniform(5.0, 7.0)
    for i in range(1, 11)
}

# Starting simulated GPS coordinates
START_LATITUDE = 12.9716
START_LONGITUDE = 77.5946

# Each container gets a slightly different starting position
container_positions = {
    container_id: {
        "lat": START_LATITUDE + index * 0.0005,
        "lon": START_LONGITUDE + index * 0.0005
    }
    for index, container_id in enumerate(containers)
}

# One container simulates a temperature problem
faulty_container = "CNT-002"

# Eastward movement per simulation cycle
MOVEMENT_STEP = 0.0001

print("AtmoSync simulator started!")
print("Tracking 10 moving avocado containers...")
print(f"Saving readings to: {OUTPUT_FILE}\n")

try:
    while True:
        for container_id in containers:

            # Simulate temperature changes
            if container_id == faulty_container:
                containers[container_id] += 0.15
            else:
                containers[container_id] += random.uniform(-0.2, 0.2)

            position = container_positions[container_id]

            # UTC timestamp
            timestamp = (
                datetime.now(timezone.utc)
                .isoformat(timespec="seconds")
                .replace("+00:00", "Z")
            )

            # Generate sensor reading using the official schema
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

            print(reading)

            # Save reading to generated JSON Lines file
            with OUTPUT_FILE.open("a", encoding="utf-8") as f:
                f.write(json.dumps(reading) + "\n")

            # Move container slightly east for next cycle
            position["lon"] += MOVEMENT_STEP

        time.sleep(2)

except KeyboardInterrupt:
    print("\nAtmoSync simulator stopped.")
