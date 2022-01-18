import json
from typing import List

import aiomysql

from telathbot.config import get_settings


async def _run_query(query: str):
    config = get_settings()

    pool = await aiomysql.create_pool(
        host=config.xenforo_db_host,
        port=config.xenforo_db_port,
        user=config.xenforo_db_user,
        password=config.xenforo_db_password,
        db=config.xenforo_db_name,
    )

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query)
            query_results = await cur.fetchall()

    pool.close()
    await pool.wait_closed()

    return query_results


async def get_post_reactions(reaction_id: int) -> List:
    query = f"""
        SELECT
            post_id, 
            thread_id, 
            username, 
            reactions, 
            reaction_users,
            position
        FROM xf_post 
        WHERE 
            reaction_users like '%reaction_id\":{reaction_id}%';
    """
    return await _run_query(query)
