from os import environ
import psycopg2


def create_tables(conn: psycopg2.extensions.connection) -> None:
    with conn.cursor() as cur:
        game_status_type = """
        CREATE TYPE GAME_STATUS AS ENUM (
            'start',
            'progress',
            'ended'
        )
        """

        users_query = """
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT PRIMARY KEY,
            nickname VARCHAR(255) NOT NULL,
            madness_scores INTEGER NOT NULL
        )
        """

        players_query = """
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            game_id BIGINT NOT NULL UNiQUE,
            user_id BIGINT NOT NULL,
            status VARCHAR(255),
            role VARCHAR(255),
            location_id INTEGER,
            inventory VARCHAR(255),
            equipment VARCHAR(255),
            health INTEGER,
            stamina INTEGER,

            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (location_id) REFERENCES locations (id) ON DELETE CASCADE,
            FOREIGN KEY (game_id) REFERENCES games (id) ON DELETE CASCADE
        )
        """

        npc_query = """
        CREATE TABLE IF NOT EXISTS npc (
            id SERIAL PRIMARY KEY,
            game_id BIGINT NOT NULL,
            location_id INTEGER NOT NULL,
            name VARCHAR(255),
            health INTEGER,
            stamina INTEGER,
            role VARCHAR(255),
            status VARCHAR(255),
            description VARCHAR(255),

            FOREIGN KEY (game_id) REFERENCES games (id) ON DELETE CASCADE,
            FOREIGN KEY (location_id) REFERENCES locations (id) ON DELETE CASCADE
        )
        """

        locations_query = """
        CREATE TABLE IF NOT EXISTS locations (
            id SERIAL PRIMARY KEY,
            game_id BIGINT NOT NULL,
            name VARCHAR(255),
            description VARCHAR(255),
            connections INTEGER[],

            FOREIGN KEY (game_id) REFERENCES games (id) ON DELETE CASCADE
        )
        """

        games_query = """
        CREATE TABLE IF NOT EXISTS games (
            id SERIAL PRIMARY KEY,
            chat_id BIGINT NOT NULL,
            status GAME_STATUS
        )
        """

        cur.execute(game_status_type)
        cur.execute(users_query)
        cur.execute(players_query)
        cur.execute(npc_query)
        cur.execute(locations_query)
        cur.execute(games_query)

        conn.commit()


conn = psycopg2.connect(
    database=environ["POSTGRES_DB"],
    user=environ["POSTGRES_USER"],
    password=environ["POSTGRES_PASSWORD"],
    host=environ["POSTGRES_HOST"],
    port=environ["POSTGRES_PORT"],
)
create_tables(conn)
