#!/bin/bash
set -e

clickhouse client -n <<-EOSQL
    CREATE DATABASE sample;
    
    CREATE TABLE sample.events (
        id Int64,
        event_date DateTime,
        attribute1 Nullable(Int64),
        attribute2 Nullable(Int64),
        attribute3 Nullable(Int64),
        attribute4 Nullable(String),
        attribute5 Nullable(String),
        attribute6 Nullable(Bool),
        metric1 Int64,
        metric2 Float64
    ) ENGINE = ReplacingMergeTree
    PARTITION BY toYYYYMMDD(event_date)
    ORDER BY (id)
    TTL event_date + INTERVAL 30 DAY;

EOSQL
