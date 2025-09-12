from asyncpg import Connection


class RefferralActions:

    def __init__(self, conn: Connection):
        self._conn = conn

    async def add_referral(self, referral_id: str, referral_name: str, referral_member_count: int = 0):
        query = """
            INSERT INTO referrals (referral_id, referral_name, referral_members_count) VALUES ($1, $2, $3);
        """
        return await self._conn.execute(query, referral_id, referral_name, referral_member_count)

    async def get_referral(self, referral_id: str):
        query = """
            SELECT *
            FROM referrals
            WHERE referral_id = $1
        """
        return await self._conn.fetchrow(query, referral_id)

    async def get_all_referrals(self):
        query = """
            SELECT * FROM referrals
        """
        return await self._conn.fetch(query)

    async def increment_referal_members_count(self, referral_id: str):
        query = """
            UPDATE referrals 
            SET referral_members_count = referral_members_count + 1
            WHERE referral_id = $1
        """
        return await self._conn.execute(query, referral_id)

    async def delite_referral(self, referral_id: str):
        query = """
            DELETE FROM referrals WHERE referral_id = $1
        """
        await self._conn.execute(query, referral_id)


