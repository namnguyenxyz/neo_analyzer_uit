CREATE OR REPLACE TABLE neo_hazard_classified AS
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
    (
        miss_distance_au < 0.05
        AND estimated_diameter_m > 140.0
    ) AS is_potentially_hazardous
FROM neo_typed_staging;
