import discord
from discord.ext import commands, bridge
from discord.commands import slash_command, Option

import aiohttp
import aiosqlite
import logging
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("discord")
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)


async def get_prefix(client, message):
    db = await aiosqlite.connect('database/prefixes.db')
    async with db.execute("SELECT * FROM prefixes") as cursor:
        async for row in cursor:
            if row[0] == message.guild.id:
                return commands.when_mentioned_or(row[1])(client, message)
        return commands.when_mentioned_or("x!")(client, message)


class Xout(bridge.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session: aiohttp.ClientSession = None
        self.help_command = None
        self.case_insensitive = True
        self.command_prefix = get_prefix

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


client = Xout(intents=discord.Intents.all())


async def get_extensions(ctx: discord.AutocompleteContext):
    cog_directories = ['./commands', './events']
    extensions = []
    for cog_directory in cog_directories:
        for filename in os.listdir(cog_directory):
            if filename.endswith(".py"):
                extensions.append(f"{cog_directory[2:]}.{filename[:-3]}")
    if extensions:
        return [cog for cog in extensions if cog.startswith(ctx.value.lower())]

    return ["None"]


@client.slash_command(name="load", description="loads a cog")
@discord.option("cog", description="choose a cog to load", autocomplete=get_extensions)
async def _load(ctx: discord.ApplicationContext, cog: str):
    if cog == "None":
        await ctx.respond(embed=discord.Embed(color=discord.Color.brand_red(),
                                              description="There were no cogs to load in."), ephemeral=True)
        return

    client.load_extension(cog)
    await client.sync_commands(force=True)
    await ctx.respond(embed=discord.Embed(color=discord.Color.brand_green(),
                                          description=f"`{cog}` was successfully loaded in."), ephemeral=True)


@client.slash_command(name="unload", description="unloads a cog")
@discord.option("cog", description="choose a cog to unload", autocomplete=get_extensions)
async def _unload(ctx: discord.ApplicationContext, cog: str):
    if cog == "None":
        await ctx.respond(embed=discord.Embed(color=discord.Color.brand_red(),
                                              description="There were no cogs to unload."), ephemeral=True)
        return

    client.unload_extension(cog)
    await client.sync_commands(force=True)
    await ctx.respond(embed=discord.Embed(color=discord.Color.brand_green(),
                                          description=f"`{cog}` was successfully unloaded."), ephemeral=True)


@client.slash_command(name="reload", description="reloads a cog")
@discord.option("cog", description="choose a cog to reload", autocomplete=get_extensions)
async def _reload(ctx: discord.ApplicationContext, cog: str):
    if cog == "None":
        await ctx.respond(embed=discord.Embed(color=discord.Color.brand_red(),
                                              description="There were no cogs to reload."), ephemeral=True)
        return

    client.unload_extension(cog)
    client.load_extension(cog)
    await client.sync_commands(force=True)
    await ctx.respond(embed=discord.Embed(color=discord.Color.brand_green(),
                                          description=f"`{cog}` was successfully reloaded."), ephemeral=True)


@client.bridge_command(name="revive", description="revive server!", guild_ids=[965061411430600824, 981880587994419250])
async def _revive(ctx):
    async with client.session.get("https://api.waifu.pics/sfw/smile") as resp:
        data = await resp.json()
        image = data["url"]
    role = ctx.guild.get_role(984247539215765525)
    embed = discord.Embed(
        color=discord.Color.nitro_pink(),
        description="[**Revived Server!**](https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley)"
    )
    embed.set_image(url=image)

    await ctx.respond(
        f"{role.mention} {ctx.author.mention} has revived the server!",
        embed=embed
    )

client.run(os.environ["DISCORD_TOKEN"])

