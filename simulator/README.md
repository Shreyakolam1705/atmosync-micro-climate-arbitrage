
# AtmoSync Simulator and Kafka

Owner: Prakash

This folder contains the Python IoT simulator and Kafka producer/consumer scripts.

## Requirements

- Python 3
- Docker Desktop
- Kafka running in Docker

## Installation

From the project root folder, activate the virtual environment and install dependencies:

```powershell
python -m pip install -r .\simulator\requirements.txt
```

## 1. Run the IoT Simulator

```powershell
python .\simulator\simulator.py
```

The simulator generates readings for 10 avocado containers (`CNT-001` to `CNT-010`).

It simulates temperature, humidity, vibration, UTC timestamps and GPS movement.

Generated readings are saved to:

`data/generated/readings.jsonl`

Press `Ctrl + C` to stop the simulator.

## 2. Run the Kafka Consumer

Make sure the Kafka Docker container is running.

```powershell
python .\simulator\kafka_consumer.py
```

## 3. Run the Kafka Producer

Open another PowerShell terminal:

```powershell
python .\simulator\kafka_producer.py
```

The producer sends sensor readings to the Kafka topic:

`container-telemetry`

The consumer listens to this topic and displays received messages.

## Data Format

All Kafka messages follow the shared schema in `docs/data-schema.md`.

Fields include:

- `container_id`
- `commodity`
- `timestamp`
- `temperature`
- `humidity`
- `vibration`
- `lat`
- `lon`

All timestamps use UTC.

Note: GPS coordinates are simulated values, not live GPS tracking.
