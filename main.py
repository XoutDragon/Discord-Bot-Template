import discord
from discord.ext import commands, bridge
from discord.commands import slash_command, Option

import aiohttp
import logging
import os

"""   Logging   """
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("discord")
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)


class Xout(bridge.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session: aiohttp.ClientSession = None
        self.help_command = None
        self.case_insensitive = True

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_connect(self):
        self.session: aiohttp.ClientSession = aiohttp.ClientSession()

    async def on_ready(self):
        logging.info("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        logging.info(f'Connected to bot: {self.user.name}'.center(55))
        logging.info(f'Bot ID: {self.user.id}'.center(55))
        logging.info("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")


async def get_prefix(bot, message):
    return commands.when_mentioned_or('!')

client = Xout(
    command_prefix="!"
)


client.run(os.environ["DISCORD_TOKEN"])

