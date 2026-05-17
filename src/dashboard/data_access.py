from pathlib import Path

import duckdb


def _db_path() -> str:
    # file layout: <repo>/src/dashboard/data_access.py -> parents[2] is repo root
    repo_root = Path(__file__).resolve().parents[2]
    db_file = repo_root / "neo_analytics.db"
    if db_file.exists():
        return str(db_file.resolve())
    # fallback to working dir path
    return str(Path("neo_analytics.db").resolve())


def connect(read_only: bool = True):
    path = _db_path()
    try:
        con = duckdb.connect(path, read_only=read_only)
        return con
    except Exception:
        return None


def get_totals():
    con = connect()
    if not con:
        return {"total_neos": None, "total_phas": None}
    try:
        total_neos = con.execute("select count(*) from v_neo_latest").fetchone()[0]
    except Exception:
        total_neos = None
    try:
        total_phas = con.execute("select sum(total_phas) from v_pha_counts").fetchone()[0]
    except Exception:
        # fallback to counting flagged rows
        try:
            total_phas = con.execute("select count(*) from neo_hazard_classified where is_potentially_hazardous").fetchone()[0]
        except Exception:
            total_phas = None
    return {"total_neos": total_neos, "total_phas": total_phas}


def get_closest_approach_today():
    con = connect()
    if not con:
        return None
    try:
        row = con.execute("select * from v_closest_approach_today limit 1").fetchone()
        return row
    except Exception:
        return None


def fetch_latest(limit: int = 50, offset: int = 0):
    con = connect()
    if not con:
        return []
    try:
        rows = con.execute(
            "select * from v_neo_latest limit ? offset ?",
            [limit, offset],
        ).fetchall()
        return rows
    except Exception:
        return []


def fetch_latest_filtered(
    limit: int = 50,
    offset: int = 0,
    search_text: str = "",
    hazard_only: bool = False,
    sort_desc: bool = False,
):
    con = connect()
    if not con:
        return []

    where_clauses = []
    params: list[object] = []

    if search_text:
        where_clauses.append("lower(object_name) like ?")
        params.append(f"%{search_text.lower()}%")

    if hazard_only:
        where_clauses.append("coalesce(is_potentially_hazardous, false) = true")

    where_sql = f" where {' and '.join(where_clauses)}" if where_clauses else ""
    order_sql = " order by miss_distance_au desc" if sort_desc else " order by miss_distance_au asc"
    sql = f"select * from v_neo_latest{where_sql}{order_sql} limit ? offset ?"
    params.extend([limit, offset])

    try:
        return con.execute(sql, params).fetchall()
    except Exception:
        return []


def fetch_visualization_frame(limit: int = 1000):
    con = connect()
    if not con:
        return []
    try:
        return con.execute(
            "select estimated_diameter_m, miss_distance_au, relative_velocity_km_s, is_potentially_hazardous from neo_hazard_classified limit ?",
            [limit],
        ).fetchdf()
    except Exception:
        return []
