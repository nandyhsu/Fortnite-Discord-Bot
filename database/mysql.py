import os

import aiomysql


class MySQL:
    """ Super barebone MySQL class """
    @classmethod
    async def create(cls):
        self = MySQL()
        self._conn = await self._instantiate_connection()
        return self

    async def _instantiate_connection(self):
        """ Instantiate MySQL connection """
        params = {
            "host": os.getenv("DATABASE_HOST"),
            "port": int(os.getenv("DATABASE_PORT")),
            "user": os.getenv("DATABASE_USERNAME"),
            "password": os.getenv("DATABASE_PASSWORD"),
            "db": os.getenv("DATABASE_NAME"),
            "charset": "utf8mb4",
            "cursorclass": aiomysql.cursors.DictCursor
        }
        return await aiomysql.connect(**params)

    async def insert_player(self, params):
        """ Insert player into the table """
        query = """INSERT INTO players (`username`, `season`, `mode`, `kd`, `games`,
                                        `wins`, `win_rate`, `trn`, `date_added`)
                   VALUES (%(username)s, %(season)s, %(mode)s, %(kd)s, %(games)s, %(wins)s,
                           %(win_rate)s, %(trn)s, %(date_added)s);
                """
        await self._executemany(query, params)

    async def fetch_players_today(self):
        """ Fetch all players from the current playing session.
        A playing session is defined as from 3 am of the current
        day to now.
        """
        query = ("SELECT * "
                 "FROM players "
                 "WHERE date_inserted >= %()s;")
        params = None  # TODO: Starting from 3 am of the current day in PT
        return await self._fetch_all(query, params)

    async def _executemany(self, query, params=None):
        """ Execute SQL query """
        async with self._conn.cursor() as cursor:
            await cursor.executemany(query, params)
            await self._conn.commit()

    async def _fetch_all(self, query, params=None):
        """ Fetch rows from MySQL """
        async with self._sql_connection.cursor() as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchall()
