from typing import Dict, List, Any
from datetime import datetime
from hosts.host_model import HostResponse
from storage.postgres_db import get_connection


class CountriesRepository:
    def ensure_exists(self, country_place_id: str) -> None:
        conn = get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    now = datetime.utcnow()
                    cur.execute(
                        """
                        INSERT INTO countries (country_place_id, created_at, updated_at)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (country_place_id) DO NOTHING
                        """,
                        (country_place_id, now, now),
                    )
        finally:
            conn.close()

    def get_all(self) -> list[Any] | None:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT country_place_id, display_name, created_at, updated_at FROM countries ORDER BY country_place_id ASC"
                )
                rows = cur.fetchall()
                cols = [d[0] for d in cur.description]
                out = []
                for r in rows:
                    d = dict(zip(cols, r))
                    if d.get("created_at"):
                        d["created_at"] = d["created_at"].isoformat()
                    if d.get("updated_at"):
                        d["updated_at"] = d["updated_at"].isoformat()
                    out.append(d)
                    return out
        finally:
            conn.close()



    def get_top5_hosts_per_country(self) -> Dict[str, List[HostResponse]]:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    WITH ranked AS (
                    SELECT
                        c.country_place_id AS c_country_place_id,
                        h.*,
                        ROW_NUMBER() OVER (
                        PARTITION BY c.country_place_id
                        ORDER BY h.created_at DESC NULLS LAST
                        ) AS rn
                    FROM countries c
                    LEFT JOIN hosts h
                        ON h.country_place_id = c.country_place_id
                    )
                    SELECT *
                    FROM ranked
                    WHERE rn <= 5 AND id IS NOT NULL
                    ORDER BY c_country_place_id, created_at DESC;
                """)
                rows = cur.fetchall()
                cols = [d[0] for d in cur.description]

            result: Dict[str, List[HostResponse]] = {}
            for r in rows:
                d = dict(zip(cols, r))
                if d.get("created_at"):
                    d["created_at"] = d["created_at"].isoformat()
                if d.get("updated_at"):
                    d["updated_at"] = d["updated_at"].isoformat()
                country = d.pop("c_country_place_id")
                d.pop("rn", None)
                host = HostResponse(**d)
                result.setdefault(country, []).append(host)
            return result
        finally:
            conn.close()
