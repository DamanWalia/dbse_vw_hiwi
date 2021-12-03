-- create database
CREATE DATABASE [dbname];
\c [dbname]

-- create timescaledb extension in database
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- create metadata table
DROP TABLE IF EXISTS "device_info";
CREATE TABLE "device_info"(
    timeid   TEXT,
    signalid   TEXT,
    time_factor  TEXT,
    time_offset DOUBLE PRECISION,
    signal_factor TEXT,
	signal_offset DOUBLE PRECISION,
	unit TEXT
);

-- create normalised signal table, it's index and make it hypertable to use timescaledb features
DROP TABLE IF EXISTS "readings";
CREATE TABLE "readings"(
    time TIMESTAMP NOT NULL,
    signal  DOUBLE PRECISION,
    timeid  TEXT,
    signalid  TEXT
);
CREATE INDEX ON "readings"(time DESC);
--CREATE INDEX ON "readings"(date, time DESC);
-- 86400000000 is in usecs and is equal to 1 day
SELECT create_hypertable('readings', 'time', chunk_time_interval => 86400000000);

-- for creating user to connect through python or client-side
CREATE USER [username] WITH PASSWORD [passwd];
-- grant privileges to the user
GRANT [privileges] TO [username]; -- ex: GRANT admins TO joe; 

-- ingestion using Copy functionality (recommended)
\copy [tablename] from '[filepath]' Delimiter '' CSV HEADER;