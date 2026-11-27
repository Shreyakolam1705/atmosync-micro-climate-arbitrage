# Kafka load test results (27 Nov 2026)

Tester: Shreya Kolam. Local Kafka in Docker (apache/kafka:4.4.0), one broker, on a laptop.
Test topic: loadtest-telemetry (3 partitions, replication factor 1). It is separate from the real topic container-telemetry.

## What this is for
Mid Review proof: Kafka handles a high-frequency event stream without lag.

## Producer test
Tool: kafka-producer-perf-test.sh, 100,000 records, 200 bytes each, no speed limit.
- 100,000 records sent
- 5,392 records/sec (1.03 MB/sec)
- Average latency 5,475 ms, max 6,625 ms, 99th percentile 6,311 ms

## Consumer test
Tool: kafka-consumer-perf-test.sh.
- First try read 0 messages (timeout). The new group started at the end of the topic.
- Second try with auto.offset.reset=earliest read all 100,000 messages.
- 10,082 messages/sec (1.92 MB/sec) overall, 17,211 messages/sec while fetching

## Lag check
Tool: kafka-consumer-groups.sh --describe, group loadtest-group2.

| Partition | Messages stored | Lag |
|---|---|---|
| 0 | 33,431 | 0 |
| 1 | 33,850 | 0 |
| 2 | 32,719 | 0 |

Total 100,000 messages, lag 0 on every partition.

## Limits
- Plain Kafka test tools were used, not the Kafka to Snowflake consumer.
- One broker on a laptop. Latency was high because the producer sent as fast as it could.
- The simulator sends about 10 readings per second, so this test was far heavier than real use.
- Snowflake insert speed was not tested.