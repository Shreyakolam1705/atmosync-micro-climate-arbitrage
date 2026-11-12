
from datetime import datetime, timezone
import json
import random
import time
from pathlib import Path

# Save generated readings
OUTPUT_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "generated"
    / "readings.jsonl"
)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Initialize 10 containers
containers = {
    f"CNT-{i:03d}": {
        "temperature": random.uniform(5.0, 7.0),
        "humidity": random.uniform(85.0, 90.0)
    }
    for i in range(1, 11)
}

# Starting GPS coordinates
START_LATITUDE = 12.9716
START_LONGITUDE = 77.5946

container_positions = {
    container_id: {
        "lat": START_LATITUDE + index * 0.0005,
        "lon": START_LONGITUDE + index * 0.0005
    }
    for index, container_id in enumerate(containers)
}

# Simulate a temperature fault
FAULTY_CONTAINER = "CNT-002"
MOVEMENT_STEP = 0.0001


def generate_readings():
    """Generate one reading for each container."""

    readings = []

    timestamp = (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )

    for container_id, sensor in containers.items():

        if container_id == FAULTY_CONTAINER:
            # Gradual temperature increase
            sensor["temperature"] += 0.15

            # Simplified relative humidity decrease
            sensor["humidity"] *= 0.9895

        else:
            # Normal random-walk changes
            sensor["temperature"] += random.uniform(-0.1, 0.1)
            sensor["humidity"] += random.uniform(-0.5, 0.5)

        # Keep values within simulation limits
        sensor["temperature"] = max(
            4.0, min(12.0, sensor["temperature"])
        )

        sensor["humidity"] = max(
            70.0, min(95.0, sensor["humidity"])
        )

        position = container_positions[container_id]

        reading = {
            "container_id": container_id,
            "commodity": "avocado",
            "timestamp": timestamp,
            "temperature": round(sensor["temperature"], 2),
            "humidity": round(sensor["humidity"], 2),
            "vibration": round(random.uniform(0.1, 0.3), 2),
            "lat": round(position["lat"], 6),
            "lon": round(position["lon"], 6)
        }

        readings.append(reading)

        # Simulate eastward movement
        position["lon"] += MOVEMENT_STEP

    # Save readings to JSON Lines file
    with OUTPUT_FILE.open("a", encoding="utf-8") as file:
        for reading in readings:
            file.write(json.dumps(reading) + "\n")

    return readings


if __name__ == "__main__":
    print("AtmoSync simulator started!")
    print("Tracking 10 avocado containers...")
    print("Generating 10 readings every second.")
    print(f"Saving readings to: {OUTPUT_FILE}\n")

    try:
        while True:
            for reading in generate_readings():
                print(json.dumps(reading))

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nAtmoSync simulator stopped.")
