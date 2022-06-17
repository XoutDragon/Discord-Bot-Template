import discord
from discord.ext import commands, bridge

import aiohttp
import aiosqlite
import logging
import yaml


async def get_config():
    with open('./config.yaml') as f:
        return yaml.safe_load(f)


async def get_prefix(client, message):
    db = await aiosqlite.connect('database/prefixes.db')
    async with db.execute("SELECT * FROM prefixes") as cursor:
        async for row in cursor:
            if row[0] == message.guild.id:
                return commands.when_mentioned_or(row[1])(client, message)

        prefix = await get_config()
        return commands.when_mentioned_or(prefix["BotConfiguration"]["Default_Prefix"])(client, message)


class MyClient(bridge.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(
            intents=discord.Intents.all(),
            command_prefix=get_prefix,
            case_insensitive=True,
            strip_after_prefix=True,
            activity=discord.Activity(
                type=discord.ActivityType.listening, name=f"/help"
            ),
            help_command=None,
        )

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
        await self.sync_commands()
