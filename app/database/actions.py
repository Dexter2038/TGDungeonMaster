import json
from os import environ
from typing import List
from psycopg import connect
import psycopg2


def get_creatures_by_location_of_user(chat_id: int | str, user_id: int | str) -> str:
    with psycopg2.connect(
        # database=environ["POSTGRES_DB"],
        user=environ["POSTGRES_USER"],
        password=environ["POSTGRES_PASSWORD"],
        host=environ["POSTGRES_HOST"],
        port=environ["POSTGRES_PORT"],
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
SELECT 
p.location_id
FROM players p
JOIN games g ON p.game_id = g.id
WHERE p.user_id = %s AND g.chat_id = %s;
            """,
                (user_id, chat_id),
            )
            location_id = cur.fetchone()[0]
            cur.execute(
                """
WITH PlayerLocation AS (
  SELECT 
    p.location_id,
    p.user_id
  FROM players p
  JOIN games g ON p.game_id = g.id
  WHERE p.location_id = %s AND g.chat_id = %s
),
NPCsInLocation AS (
  SELECT
    n.id AS id,
    n.name AS name,
    n.health AS health,
    n.stamina AS stamina,
    n.role AS role,
    n.status AS status
  FROM npc n
  JOIN PlayerLocation pl ON n.location_id = pl.location_id
  WHERE n.name IS NOT NULL
),
PlayersInLocation AS (
  SELECT
    p.user_id AS id,
    u.nickname AS name,
    p.health AS health,
    p.stamina AS stamina,
    p.role AS role,
    p.status AS status
  FROM players p
  JOIN PlayerLocation pl ON p.location_id = pl.location_id
  JOIN users u ON p.user_id = u.id
  WHERE u.nickname IS NOT NULL
)
SELECT 
  'NPC' AS type,
  id, 
  name, health, stamina, role, status
FROM NPCsInLocation
UNION ALL
SELECT 
  'Player' AS type,
  id, 
  name, health, stamina, role, status
FROM PlayersInLocation;

            """,
                (location_id, chat_id),
            )
            res = cur.fetchall()

            json_data = json.dumps(
                [
                    dict(
                        zip(
                            ["type", "id", "name", "hp", "stamina", "role", "status"],
                            row,
                        )
                    )
                    for row in res
                ],
                indent=1,
            )

            return json_data


def get_locations_by_chat(chat_id: int | str) -> str:
    with psycopg2.connect(
        # database=environ["POSTGRES_DB"],
        user=environ["POSTGRES_USER"],
        password=environ["POSTGRES_PASSWORD"],
        host=environ["POSTGRES_HOST"],
        port=environ["POSTGRES_PORT"],
    ) as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
SELECT l.id, l.name, l.description, l.connections
FROM locations l
JOIN games g ON l.game_id = g.id
WHERE g.chat_id = %s
                """,
                (chat_id,),
            )
            res = cur.fetchone()

            json_data = json.dumps(
                [dict(zip(["id", "name", "description"], res))], indent=1
            )

            return json_data


res = get_creatures_by_location_of_user(1151523, 515152)

print(res)

print(get_locations_by_chat(1151523))
