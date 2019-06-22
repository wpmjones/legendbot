import traceback
from discord.ext import commands


class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="load", hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        """Command which loads a module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            print(f"ERROR: {type(e).__name__} - {e}")
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            print(f"{cog} successfully loaded")
            await ctx.send("**`SUCCESS`**")

    @commands.command(name="unload", hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        """Command which unloads a module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            print(f"ERROR: {type(e).__name__} - {e}")
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            print(f"{cog} successfully unloaded")
            await ctx.send("**`SUCCESS`**")

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        """Command which reloads a module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            print(f"ERROR: {type(e).__name__} - {e}")
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            print(f"{cog} reloaded successfully")
            await ctx.send("**`SUCCESS`**")

    @commands.command(name="pull", hidden=True)
    @commands.is_owner()
    async def git_pull(self, ctx):
        """Command to pull latest updates from master branch on GitHub"""
        origin = self.bot.repo.remotes.origin
        try:
            origin.pull()
            print("Code successfully pulled from GitHub")
            await ctx.send("Code successfully pulled from GitHub")
        except Exception as e:
            print(f"ERROR: {type(e).__name__} - {e}")
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")

    @commands.command(name="close_db", aliases=["cdb", "cbd"], hidden=True)
    @commands.is_owner()
    async def close_db(self, ctx):
        """Command to close db connection before shutting down bot"""
        if self.bot.db.pool is not None:
            await self.bot.db.pool.close()
            await ctx.send("Database connection closed.")

    @commands.command()
    @commands.is_owner()
    async def log(self, ctx, num_lines: int = 10):
        with open(f"oakbot.log", "r") as f:
            list_start = -1 * num_lines
            await self.send_text(ctx.channel, "\n".join([line for line in f.read().splitlines()[list_start:]]))

    @log.error
    async def log_handler(self, ctx, error):
        """Listens for errors in log command"""
        tb_lines = traceback.format_exception(error.__class__, error, error.__traceback__)
        tb_text = "".join(tb_lines)
        await self.bot.test_channel.send(f"Exception found in {ctx.command}:\n"
                                         f"{tb_text}")


def setup(bot):
    bot.add_cog(OwnerCog(bot))