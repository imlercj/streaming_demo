-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Create stations table to store wind measurement locations
CREATE TABLE stations (
    station_id TEXT PRIMARY KEY,
    station_name TEXT NOT NULL
);

-- Create wind_measurements table
CREATE TABLE wind_measurements (
    --timestamp TIMESTAMPTZ NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    station_id TEXT REFERENCES stations(station_id),
    wind_speed DOUBLE PRECISION NOT NULL,
    wind_direction INTEGER NOT NULL,
    CONSTRAINT wind_direction_range CHECK (wind_direction >= 0 AND wind_direction <= 360)
);

-- Create hypertable for wind measurements
SELECT create_hypertable('wind_measurements', 'timestamp');

-- Create index for faster querying
CREATE INDEX ON wind_measurements (station_id, timestamp DESC);

-- Insert Norwegian port stations
INSERT INTO stations (station_id, station_name) 
VALUES 
    ('VS1721', 'Stavanger (SW) - Risavika'),
    ('VS1596', 'Stavanger (S) - DSD'),
    ('VS1595', 'Stavanger (N) - Tjuvholmen'),
    ('VS1722', 'Stavanger (NW) - Mekjarvik')
ON CONFLICT (station_id) DO NOTHING;

-- Create continuous aggregates for wind data

-- 15-minute aggregates
CREATE MATERIALIZED VIEW wind_measurements_15min
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('15 minutes', timestamp) AS bucket,
    station_id,
    avg(wind_speed) as avg_speed,
    max(wind_speed) as max_speed,
    min(wind_speed) as min_speed,
    -- Calculate the average direction using vector components
    degrees(point(avg(cos(radians(wind_direction))), avg(sin(radians(wind_direction)))) <-> point(0,0)) as avg_direction,
    count(*) as sample_count
FROM wind_measurements
GROUP BY bucket, station_id
WITH NO DATA;

-- Hourly aggregates
CREATE MATERIALIZED VIEW wind_measurements_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', timestamp) AS bucket,
    station_id,
    avg(wind_speed) as avg_speed,
    max(wind_speed) as max_speed,
    min(wind_speed) as min_speed,
    -- Calculate the average direction using vector components
    degrees(point(avg(cos(radians(wind_direction))), avg(sin(radians(wind_direction)))) <-> point(0,0)) as avg_direction,
    count(*) as sample_count
FROM wind_measurements
GROUP BY bucket, station_id
WITH NO DATA;

-- Add retention policy: keep raw data for 30 days, and aggregated data for 1 year
SELECT add_retention_policy('wind_measurements', INTERVAL '30 days');
SELECT add_retention_policy('wind_measurements_15min', INTERVAL '1 year');
SELECT add_retention_policy('wind_measurements_hourly', INTERVAL '1 year');

-- Add refresh policies
SELECT add_continuous_aggregate_policy('wind_measurements_15min',
    start_offset => INTERVAL '3 hours',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '15 minutes');

SELECT add_continuous_aggregate_policy('wind_measurements_hourly',
    start_offset => INTERVAL '12 hours',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour');

