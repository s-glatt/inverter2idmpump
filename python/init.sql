CREATE TABLE watts ( "time" timestamptz NOT NULL, "key" varchar NOT NULL, "value" double precision );
SELECT create_hypertable('watts', 'time');
ALTER TABLE watts SET ( timescaledb.compress, timescaledb.compress_segmentby = 'time' );
SELECT add_compression_policy('watts', INTERVAL '1 days');
SELECT add_retention_policy('watts', INTERVAL '7 days');
CREATE TABLE voltages ( "time" timestamptz NOT NULL, "key" varchar NOT NULL, "value" double precision );
SELECT create_hypertable('voltages', 'time');
ALTER TABLE voltages SET ( timescaledb.compress, timescaledb.compress_segmentby = 'time' );
SELECT add_compression_policy('voltages', INTERVAL '1 days');
SELECT add_retention_policy('voltages', INTERVAL '7 days');
CREATE TABLE temps ( "time" timestamptz NOT NULL, "key" varchar NOT NULL, "value" double precision );
SELECT create_hypertable('temps', 'time');
ALTER TABLE temps SET ( timescaledb.compress, timescaledb.compress_segmentby = 'time' );
SELECT add_compression_policy('temps', INTERVAL '1 days');
SELECT add_retention_policy('temps', INTERVAL '7 days');
CREATE TABLE percentages ( "time" timestamptz NOT NULL, "key" varchar NOT NULL, "value" double precision );
SELECT create_hypertable('percentages', 'time');
ALTER TABLE percentages SET ( timescaledb.compress, timescaledb.compress_segmentby = 'time' );
SELECT add_compression_policy('percentages', INTERVAL '1 days');
SELECT add_retention_policy('percentages', INTERVAL '7 days');
CREATE TABLE kilowatthours ( "time" timestamptz NOT NULL, "key" varchar NOT NULL, "value" double precision );
SELECT create_hypertable('kilowatthours', 'time');
ALTER TABLE kilowatthours SET ( timescaledb.compress, timescaledb.compress_segmentby = 'time' );
SELECT add_compression_policy('kilowatthours', INTERVAL '1 days');
SELECT add_retention_policy('kilowatthours', INTERVAL '7 days');
