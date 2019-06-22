import os
import traceback
import git
import asyncio
import coc
from loguru import logger
from discord.ext import commands
from config import settings
from legenddb import LegendDB

enviro = "dev"

if enviro == "LIVE":
    token = settings['discord']['legendToken']
    prefix = "!"
    log_level = "INFO"
    coc_names = "vps"
else:
    token = settings['discord']['testToken']
    prefix = ">"
    log_level = "DEBUG"
    coc_names = "dev"

logger.add("legendbot.log", rotation="25MB", level=log_level)

description = """Welcome to Legend Bot - by TubaKid

All commands must begin with an exclamation point"""

bot = commands.Bot(command_prefix=prefix,
                   description=description,
                   case_insensitive=True)


@bot.event
async def on_ready():
    logger.info("-------")
    logger.info(f"Logged in as {bot.user}")
    logger.info("-------")
    bot.test_channel = bot.get_channel(settings['oakChannels']['testChat'])
    await bot.test_channel.send("Legend Bot has restarted")


@bot.event
async def on_resumed():
    logger.info("Bot has been resumed.")

initial_extensions = ["cogs.newhelp",
                      "cogs.owner",
                      "cogs.pull",
                      ]

if __name__ == "__main__":
    bot.remove_command("help")
    bot.repo = git.Repo(os.getcwd())
    bot.db = LegendDB(bot)
    loop = asyncio.get_event_loop()
    pool = loop.run_until_complete(bot.db.create_pool())
    bot.loop = loop
    bot.db.pool = pool
    bot.logger = logger
    bot.coc_client = coc.login(settings['supercell']['user'],
                               settings['supercell']['pass'],
                               key_names=coc_names)

    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            logger.debug(f"{extension} loaded successfully")
        except Exception as e:
            logger.info(f"Failed to load extension {extension}")
            traceback.print_exc()

    bot.run(token)
