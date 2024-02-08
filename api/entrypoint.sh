#!/bin/sh

check_clickhouse() {
    python3 - <<END
import socket
import time

def is_clickhouse_available():
    try:
        socket.create_connection(("clickhouse", 9000), timeout=5)
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False

print("Waiting for ClickHouse to start...")
while not is_clickhouse_available():
    time.sleep(1)
print("ClickHouse is ready!")
END
}

check_kafka() {
    python3 - <<END
import socket
import time

def is_kafka_available():
    try:
        socket.create_connection(("kafka", 9092), timeout=5)
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False

print("Waiting for Kafka to start...")
while not is_kafka_available():
    time.sleep(1)
print("Kafka is ready!")
END
}

check_clickhouse
check_kafka

gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app -b 0.0.0.0:8000
