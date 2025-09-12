from asyncpg import Connection


class BotActions:
    def __init__(self, conn: Connection):
        self._conn = conn

    async def add_bot(
        self,
        bot_name: str,
        bot_username: str,
        bot_status: str = "True"
    ):
        query = """
            INSERT INTO bots (bot_name, bot_username, bot_status) VALUES($1, $2, $3)      
        """
        await self._conn.execute(query, bot_name, bot_username, bot_status)

    async def get_bot(self, bot_username: str):
        query = """
            SELECT * FROM bots WHERE bot_username = $1
        """
        return await self._conn.fetchrow(query, bot_username)

    async def get_all_bots(self):
        query = """
            SELECT * FROM bots
        """
        return await self._conn.fetch(query)

    async def update_bot_status(self, new_bot_status: str, bot_username: str):
        query = """
            UPDATE bots SET bot_status = $1 WHERE bot_username = $2
        """
        await self._conn.execute(query, new_bot_status, bot_username)

    async def delete_bot(self, bot_username: str):
        query = """
            DELETE FROM bots WHERE bot_username = $1 
        """
        await self._conn.execute(query, bot_username)