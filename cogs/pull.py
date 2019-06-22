import asyncio
import time
from discord.ext import commands


class Pull(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.flag = 1
        self.bg_task = self.bot.loop.create_task(self.main())

    async def main(self):
        await asyncio.sleep(5)
        while self.flag == 1:
            start = time.perf_counter()
            conn = self.bot.db.pool
            self.bot.logger.debug("Postgresql connection established.")
            sql = "SELECT clan_tag FROM legend_clans"
            rows = await conn.fetch(sql)
            clans = []
            for row in rows:
                clans.append(f"#{row['clan_tag']}")
            sql = ("INSERT INTO legend_members (player_tag, player_name, trophies, attack_wins, "
                   "defense_wins, league, clan_tag) "
                   "VALUES ('$1', '$2', $3, $4, $5, '$6', '$7')")
            async for clan in self.bot.coc_client.get_clans(clans):
                print(f"Running {clan.name}")
                for member in clan.members:
                    if member.trophies >= 5000:
                        try:
                            print(f" - {member.name}")
                            await conn.execute(sql,
                                               member.tag[1:], member.name, member.trophies, member.attack_wins,
                                               member.defense_wins, member.league.name, member.clan.tag[1:])
                        except:
                            self.bot.logger.exception("INSERT")
                self.bot.logger.debug(f"Added member data for {clan.name}")
            await conn.close()
            elapsed = time.perf_counter() - start
            self.bot.logger.info(f"All legend members recorded in {elapsed} seconds.")
            await asyncio.sleep(60)

    @commands.command(name="flip_pull")
    @commands.is_owner()
    async def flip(self, ctx):
        if self.flag == 1:
            self.flag = 0
            await ctx.send("Flag changed to 0")


def setup(bot):
    bot.add_cog(Pull(bot))