
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

# One container only
container_id = "CNT-001"
commodity = "avocado"

# Initial sensor values
temperature = random.uniform(5.0, 7.0)
humidity = random.uniform(85.0, 90.0)

# Initial GPS coordinates
latitude = 12.9716
longitude = 77.5946

# Simulated movement per reading
MOVEMENT_STEP = 0.0001


def generate_reading():
    """Generate one random-walk reading for CNT-001."""

    global temperature, humidity, latitude, longitude

    # Random-walk temperature and humidity
    temperature += random.uniform(-0.01, 0.1)
    humidity += random.uniform(-0.5, 0.5)

    # Keep sensor values within simulation limits
    temperature = max(4.0, min(12.0, temperature))
    humidity = max(70.0, min(95.0, humidity))

    # Generate UTC timestamp
    timestamp = (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )

    # Create reading matching docs/data-schema.md
    reading = {
        "container_id": container_id,
        "commodity": commodity,
        "timestamp": timestamp,
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2),
        "vibration": round(random.uniform(0.1, 0.3), 2),
        "lat": round(latitude, 6),
        "lon": round(longitude, 6)
    }

    # Simulate container movement
    latitude += MOVEMENT_STEP
    longitude += MOVEMENT_STEP

    # Save reading in JSON Lines format
    with OUTPUT_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(reading) + "\n")

    return reading


if __name__ == "__main__":
    print("AtmoSync simulator started!")
    print("Tracking container: CNT-001")
    print("Temperature and humidity: Random walk")
    print("GPS: Simulated movement")
    print("Generating one reading every second.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            reading = generate_reading()
            print(json.dumps(reading))
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nAtmoSync simulator stopped.")
