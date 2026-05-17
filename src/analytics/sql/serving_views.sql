CREATE OR REPLACE VIEW v_neo_latest AS
WITH ranked AS (
    SELECT
        object_id,
        object_name,
        close_approach_date,
        close_approach_ts,
        relative_velocity_km_s,
        miss_distance_au,
        estimated_diameter_m,
        is_potentially_hazardous,
        fetched_at_ts,
        event_id,
        ROW_NUMBER() OVER (
            PARTITION BY object_id
            ORDER BY close_approach_ts DESC NULLS LAST, fetched_at_ts DESC NULLS LAST, event_id DESC NULLS LAST
        ) AS row_num
    FROM neo_hazard_classified
)
SELECT
    object_id,
    object_name,
    close_approach_date,
    close_approach_ts,
    relative_velocity_km_s,
    miss_distance_au,
    estimated_diameter_m,
    is_potentially_hazardous,
    fetched_at_ts,
    event_id
FROM ranked
WHERE row_num = 1;

CREATE OR REPLACE VIEW v_pha_counts AS
SELECT
    COUNT(*) AS total_neos,
    SUM(CASE WHEN is_potentially_hazardous THEN 1 ELSE 0 END) AS total_phas
FROM neo_hazard_classified;

CREATE OR REPLACE VIEW v_closest_approach_today AS
SELECT
    object_id,
    object_name,
    close_approach_date,
    miss_distance_au,
    relative_velocity_km_s,
    estimated_diameter_m,
    is_potentially_hazardous
FROM neo_hazard_classified
WHERE close_approach_date = CURRENT_DATE
ORDER BY miss_distance_au ASC NULLS LAST, close_approach_ts ASC NULLS LAST, object_id ASC
LIMIT 1;
