import json
from typing import List

import aiomysql

from telathbot.config import get_settings
from telathbot.schemas.reaction import PostReaction


async def get_post_reactions(
    start_post_id: int, reaction_id: int
) -> List[PostReaction]:
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
            await cur.execute(
                f"""
                SELECT
                    post_id, 
                    thread_id, 
                    username, 
                    reactions, 
                    reaction_users,
                    position
                FROM xf_post 
                WHERE 
                    post_id > {start_post_id} AND 
                    reaction_users like '%reaction_id\":{reaction_id}%';
            """
            )
            query_results = await cur.fetchall()

    pool.close()
    await pool.wait_closed()

    raw_results = []
    for result in query_results:
        raw_results.append(
            PostReaction(
                post_id=result[0],
                thread_id=result[1],
                username=result[2],
                reactions=json.loads(result[3]),
                reaction_users=json.loads(result[4]),
                position=result[5],
            )
        )

    return raw_results
