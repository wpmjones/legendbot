import asyncpg
from config import settings


class LegendDB:
    def __init__(self, bot):
        self.bot = bot

    async def create_pool(self):
        pool = await asyncpg.create_pool(settings['pg']['uri'], max_size=15)
        return pool