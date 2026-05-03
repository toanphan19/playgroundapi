import os

import psycopg
from cachetools import TTLCache, cached


@cached(cache=TTLCache(maxsize=32, ttl=600))
def get_top_stories(conn_str: str, nr_days: int, limit: int = 20):
    limit = min(50, limit)
    sql = """
select
    id,
    time,
    title,
    url,
    score,
    comments
from hn_stories
where time > now() - make_interval(days => %s)
order by score desc
limit %s;
"""
    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (nr_days, limit))
            rows = cur.fetchall()

    return rows
