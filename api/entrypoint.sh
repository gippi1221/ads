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

gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app -b 0.0.0.0:8000
