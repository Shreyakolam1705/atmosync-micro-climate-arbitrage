
# Import required libraries
from datetime import datetime, timezone
import json
import random
import time
from pathlib import Path

# Get the folder where this Python file is located
BASE_DIR = Path(__file__).resolve().parent

# Configuration file path
CONFIG_FILE = BASE_DIR / "config.json"

# Output file path
OUTPUT_FILE = BASE_DIR.parent / "data" / "generated" / "readings.jsonl"

# Create output folder if it does not exist
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_config():
    """Load container details from config.json."""

    with CONFIG_FILE.open("r", encoding="utf-8-sig") as file:
        config = json.load(file)

    return config


# Load the configuration
CONFIG = load_config()

# Get interval and container information
INTERVAL_SECONDS = CONFIG["interval_seconds"]
CONTAINERS = CONFIG["containers"]


def validate_config():
    """Check whether the configuration is correct."""

    # Check that exactly 10 containers are configured
    if len(CONTAINERS) != 10:
        raise ValueError("Config must contain exactly 10 containers.")

    # Expected container IDs
    expected_ids = [
        f"CNT-{number:03d}"
        for number in range(1, 11)
    ]

    # Actual container IDs
    actual_ids = [
        container["container_id"]
        for container in CONTAINERS
    ]

    # Check container IDs and their order
    if actual_ids != expected_ids:
        raise ValueError("Container IDs must be CNT-001 to CNT-010 in order.")

    # Check that all containers carry avocado
    for container in CONTAINERS:
        if container["commodity"] != "avocado":
            raise ValueError("All containers must carry avocado.")

        # Convert sensor values into numbers
        container["temperature"] = float(container["temperature"])
        container["humidity"] = float(container["humidity"])

        # Check required location fields
        if "lat" not in container or "lon" not in container:
            raise ValueError("Every container must have lat and lon.")

    # Check reading interval
    if INTERVAL_SECONDS <= 0:
        raise ValueError("interval_seconds must be greater than zero.")


# Validate configuration before starting
validate_config()


def generate_reading(container, timestamp):
    """Generate a new reading for one container."""

    # Randomly change temperature slightly
    container["temperature"] += random.uniform(-0.1, 0.1)

    # Randomly change humidity slightly
    container["humidity"] += random.uniform(-0.5, 0.5)

    # Keep temperature within simulation limits
    container["temperature"] = max(
        4.0, min(12.0, container["temperature"])
    )

    # Keep humidity within simulation limits
    container["humidity"] = max(
        70.0, min(95.0, container["humidity"])
    )

    # Create reading using the shared data schema
    reading = {
        "container_id": container["container_id"],
        "commodity": container["commodity"],
        "timestamp": timestamp,
        "temperature": round(container["temperature"], 2),
        "humidity": round(container["humidity"], 2),
        "vibration": round(random.uniform(0.1, 0.3), 2),
        "lat": round(container["lat"], 6),
        "lon": round(container["lon"], 6)
    }

    # Simulate small location movement
    container["lat"] += 0.0001
    container["lon"] += 0.0001

    return reading


def generate_readings():
    """Generate one reading for every container."""

    readings = []

    # Create one UTC timestamp for this batch
    timestamp = (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )

    # Generate a reading for each container
    for container in CONTAINERS:
        reading = generate_reading(container, timestamp)
        readings.append(reading)

    return readings

def save_readings(readings):
    """Append readings to readings.jsonl."""
    with OUTPUT_FILE.open("a", encoding="utf-8") as file:
        # Save each reading as a separate JSON line
        for reading in readings:
            file.write(json.dumps(reading) + "\n")


def print_readings(readings):
    """Print all container readings."""

    for reading in readings:
        print(json.dumps(reading))

    print("-" * 60)


def main():
    """Run the simulator continuously."""

    print("AtmoSync simulator started!")
    print("Tracking 10 avocado containers: CNT-001 to CNT-010")
    print(f"Generating readings every {INTERVAL_SECONDS} second(s).")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            # Generate readings for all containers
            readings = generate_readings()

            # Save readings to the output file
            save_readings(readings)

            # Print readings in the terminal
            print_readings(readings)

            # Wait before generating the next batch
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nAtmoSync simulator stopped.")


if __name__ == "__main__":
    main()
