# AtmoSync Simulator and Kafka

**Owner:** Prakash

This folder contains the Python IoT simulator and Kafka producer, consumer, and topic creation scripts.

The simulator generates sensor readings for 10 avocado containers (`CNT-001` to `CNT-010`) and sends them to the Kafka topic `container-telemetry`.

## Requirements

- Python 3
- Docker Desktop
- Docker Compose
- Kafka running in Docker

## 1. Project Setup

Open PowerShell in the project root folder.

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required Python dependencies:

```powershell
python -m pip install -r .\simulator\requirements.txt
```

## 2. Start Kafka

Make sure Docker Desktop is running.

Start the Kafka container:

```powershell
docker compose up -d
```

Check whether Kafka is running:

```powershell
docker compose ps
```

Kafka runs on:

`127.0.0.1:9092`

## 3. Create the Kafka Topic

Run the topic creation script:

```powershell
python .\simulator\create_topic.py
```

Topic details:

- **Topic name:** `container-telemetry`
- **Partitions:** 3
- **Replication factor:** 1

The script creates the topic if it does not exist and verifies that it exists.

If the topic already exists, the script displays an appropriate message.

## 4. Run the IoT Simulator

Run the simulator:

```powershell
python .\simulator\simulator.py
```

The simulator generates readings for all 10 avocado containers:

- CNT-001
- CNT-002
- CNT-003
- CNT-004
- CNT-005
- CNT-006
- CNT-007
- CNT-008
- CNT-009
- CNT-010

It simulates:

- Temperature
- Humidity
- Vibration
- UTC timestamps
- GPS coordinates

Generated readings are saved to:

`data/generated/readings.jsonl`

Press `Ctrl + C` to stop the simulator.

## 5. Run the Kafka Consumer

Open a new PowerShell terminal, navigate to the project root folder, and activate the virtual environment.

Run:

```powershell
python .\simulator\kafka_consumer.py
```

The consumer listens to the `container-telemetry` topic and displays received messages.

## 6. Run the Kafka Producer

Open another PowerShell terminal, navigate to the project root folder, and activate the virtual environment.

Run:

```powershell
python .\simulator\kafka_producer.py
```

The producer:

- Generates readings for all 10 containers.
- Sends readings to the `container-telemetry` Kafka topic.
- Prints successfully sent messages.
- Repeats according to the configured interval.

Check the consumer terminal to confirm that readings are received from all 10 containers.

Press `Ctrl + C` to stop the producer and consumer.

## 7. Data Format

All Kafka messages follow the shared data schema documented in:

`docs/data-schema.md`

Each reading contains the following fields:

| Field | Description |
|---|---|
| `container_id` | Container identifier (CNT-001 to CNT-010) |
| `commodity` | Commodity name (`avocado`) |
| `timestamp` | ISO 8601 UTC timestamp |
| `temperature` | Temperature in degrees Celsius |
| `humidity` | Humidity percentage |
| `vibration` | Vibration in g-force |
| `lat` | Latitude in decimal degrees |
| `lon` | Longitude in decimal degrees |

All timestamps use UTC.

**Note:** GPS coordinates are simulated values, not live GPS tracking.

## 8. Stop Kafka

After completing the tests, stop the Kafka Docker container:

```powershell
docker compose down
```

To stop Kafka and remove its stored volume data as well, use:

```powershell
docker compose down -v
```

**Warning:** The `-v` option deletes Kafka's stored data. Use it only when you intentionally want to reset Kafka.