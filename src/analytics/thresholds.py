PHA_MISS_DISTANCE_AU_MAX = 0.05
PHA_DIAMETER_M_MIN = 140.0


def describe_hazard_rule() -> str:
    return (
        "is_potentially_hazardous = "
        f"(miss_distance_au < {PHA_MISS_DISTANCE_AU_MAX} "
        f"AND estimated_diameter_m > {PHA_DIAMETER_M_MIN})"
    )
