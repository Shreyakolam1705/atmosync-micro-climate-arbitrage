from datetime import datetime
import json
import random
import time

# Starting temperature of each container (Added quotes around string keys)
containers = {
    "CONT-001": 6.0,
    "CONT-002": 7.0,
    "CONT-003": 6.5,
    "CONT-004": 5.5,
}

faulty_container = "CONT-002"

# Added the missing try block for the KeyboardInterrupt handling
try:
    while True:
        for container_id in containers:
            if container_id == faulty_container:
                containers[container_id] += 0.15  # steady rise
            else:
                containers[container_id] += random.uniform(
                    -0.2, 0.2
                )  # small normal wobble

            # Added quotes around keys and fixed formatting
            reading = {
                "container_id": container_id,
                "timestamp": str(datetime.now()),
                "temperature_c": round(containers[container_id], 2),
                "humidity_pct": round(random.uniform(80, 95), 2),
                "vibration": round(random.uniform(0.1, 2.0), 2),
            }

            print(reading)

            # Part 2: save each reading to a file (Added quotes to filename)
            with open("readings.jsonl", "a") as f:
                f.write(json.dumps(reading) + "\n")

        time.sleep(2)

except KeyboardInterrupt:
    print("\nAtmoSync simulator stopped.")
