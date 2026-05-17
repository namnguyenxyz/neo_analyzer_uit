CREATE OR REPLACE TABLE neo_typed_staging AS
WITH raw_source AS (
    SELECT *
    FROM read_parquet('__RAW_GLOB__', union_by_name = true)
),
typed AS (
    SELECT
        CAST(object_id AS VARCHAR) AS object_id,
        CAST(object_name AS VARCHAR) AS object_name,
        TRY_CAST(close_approach_date AS DATE) AS close_approach_date,
        TRY_CAST(close_approach_date AS TIMESTAMP) AS close_approach_ts,
        TRY_CAST(relative_velocity_km_s AS DOUBLE) AS relative_velocity_km_s,
        TRY_CAST(miss_distance_au AS DOUBLE) AS miss_distance_au,
        TRY_CAST(estimated_diameter_m AS DOUBLE) AS estimated_diameter_m,
        CAST(source_payload AS VARCHAR) AS source_payload,
        CAST(fetched_at_utc AS VARCHAR) AS fetched_at_utc,
        TRY_CAST(fetched_at_utc AS TIMESTAMP) AS fetched_at_ts,
        CAST(event_id AS VARCHAR) AS event_id
    FROM raw_source
),
ranked AS (
    SELECT
        object_id,
        object_name,
        close_approach_date,
        close_approach_ts,
        relative_velocity_km_s,
        miss_distance_au,
        estimated_diameter_m,
        source_payload,
        fetched_at_utc,
        fetched_at_ts,
        event_id,
        ROW_NUMBER() OVER (
            PARTITION BY COALESCE(event_id, object_id || ':' || CAST(close_approach_date AS VARCHAR) || ':' || COALESCE(fetched_at_utc, ''))
            ORDER BY fetched_at_ts DESC NULLS LAST, event_id DESC NULLS LAST
        ) AS dedupe_rank
    FROM typed
)
SELECT
    object_id,
    object_name,
    close_approach_date,
    close_approach_ts,
    relative_velocity_km_s,
    miss_distance_au,
    estimated_diameter_m,
    source_payload,
    fetched_at_utc,
    fetched_at_ts,
    event_id
FROM ranked
WHERE dedupe_rank = 1;
