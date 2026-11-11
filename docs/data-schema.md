# Shared Data Schema

This is the agreed format for container sensor readings. The simulator, Kafka, Snowflake and dbt all use these exact field names.

## Kafka message (JSON)
Topic: container-telemetry

| Field | Type | Unit / format | Example |
|---|---|---|---|
| container_id | string | CNT-001 to CNT-010 | CNT-003 |
| commodity | string | lowercase name | avocado |
| timestamp | string | ISO 8601, UTC | 2026-11-12T08:30:00Z |
| temperature | float | degrees Celsius | 6.4 |
| humidity | float | percent (0 to 100) | 87.5 |
| vibration | float | g-force | 0.12 |
| lat | float | decimal degrees | 12.9716 |
| lon | float | decimal degrees | 77.5946 |

## Example message
```json
{
  "container_id": "CNT-003",
  "commodity": "avocado",
  "timestamp": "2026-11-12T08:30:00Z",
  "temperature": 6.4,
  "humidity": 87.5,
  "vibration": 0.12,
  "lat": 12.9716,
  "lon": 77.5946
}
```

## Snowflake
- Database: ATMOSYNC
- Schema: RAW
- Raw table: one row per message, with the full JSON stored in a VARIANT column, plus a load timestamp.

## Rules
- Field names are lowercase and must not change without telling the Team Lead.
- Timestamps are always UTC.
- Missing sensor values are sent as null, never as 0.
- Any change to this file needs a pull request that Prakash and Amarnath both review.
