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

check_clickhouse

exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
