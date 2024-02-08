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
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMMDD(event_date)
    ORDER BY (id)
    TTL event_date + INTERVAL 30 DAY;

    CREATE TABLE sample.events_queue (
        id Int64,
        event_date String,
        attribute1 Nullable(Int64),
        attribute2 Nullable(Int64),
        attribute3 Nullable(Int64),
        attribute4 Nullable(String),
        attribute5 Nullable(String),
        attribute6 Nullable(Bool),
        metric1 Int64,
        metric2 Float64
    ) ENGINE = Kafka('kafka:9092', 'samples', 'chcg','JSONEachRow')
    settings kafka_thread_per_consumer = 0, kafka_num_consumers = 1;

    CREATE MATERIALIZED VIEW sample.events_mv TO sample.events AS
    SELECT id
        , parseDateTimeBestEffortOrNull(event_date) as event_date
        , attribute1
        , attribute2
        , attribute3
        , attribute4
        , attribute5
        , attribute6
        , metric1
        , metric2
    FROM sample.events_queue;

EOSQL
