import discord
from discord.ext import commands
from config import settings, color_pick


class NewHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx, command: str = "all"):
        desc = ("All commands must begin with an !\n\n"
                "References to a clan can be in the form of the clan name of the clan tag.\n\n"
                "You can type !help <command> to display only the help for that command.")

        command_list = ["all", "player"]

        if command not in command_list:
            await ctx.send(":x: You have provided a command that does not exist. "
                           "Perhaps try !help to see all commands.")
            self.bot.logger.warning(f"{ctx.author} requested {command} on {ctx.guild}")


def setup(bot):
    bot.add_cog(NewHelp(bot))