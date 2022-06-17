import discord

import logging
import os

from utils.bot import MyClient


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("discord")
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)


client = MyClient()


cog_directories = ['./commands', './events']

for directory in [cog_directories[0][2:]]:
    for file in os.listdir(directory):
        if file.endswith(".py"):
            client.load_extension(f"{directory}.{file[:-3]}")


async def get_extensions(ctx: discord.AutocompleteContext):
    extensions = []
    for cog_directory in cog_directories:
        for filename in os.listdir(cog_directory):
            if filename.endswith(".py"):
                extensions.append(f"{cog_directory[2:]}.{filename[:-3]}")
    if extensions:
        return [cog for cog in extensions if cog.startswith(ctx.value.lower())]

    return ["None"]


@client.slash_command(name="load", description="loads a cog")
@discord.option("extension", description="choose a cog to load", autocomplete=get_extensions)
async def load(ctx: discord.ApplicationContext, extension: str):
    await ctx.defer()
    if extension == "None":
        await ctx.respond(embed=discord.Embed(color=discord.Color.brand_red(),
                                              description="There were no cogs to load in."), ephemeral=True)
        return

    client.load_extension(extension)
    try:
        await client.sync_commands()
    except discord.HTTPException:
        pass
    await ctx.respond(embed=discord.Embed(color=discord.Color.brand_green(),
                                          description=f"`{extension}` was successfully loaded in."), ephemeral=True)


@client.slash_command(name="unload", description="unloads a cog")
@discord.option("extension", description="choose a cog to unload", autocomplete=get_extensions)
async def unload(ctx: discord.ApplicationContext, extension: str):
    await ctx.defer()
    if extension == "None":
        await ctx.respond(embed=discord.Embed(color=discord.Color.brand_red(),
                                              description="There were no cogs to unload."), ephemeral=True)
        return

    client.unload_extension(extension)
    try:
        await client.sync_commands(force=True)
    except discord.HTTPException:
        pass
    await ctx.respond(embed=discord.Embed(color=discord.Color.brand_green(),
                                          description=f"`{extension}` was successfully unloaded."), ephemeral=True)


@client.slash_command(name="reload", description="reloads a cog")
@discord.option("extension", description="choose a cog to reload", autocomplete=get_extensions)
async def reload(ctx: discord.ApplicationContext, extension: str):
    await ctx.defer()
    if extension == "None":
        await ctx.respond(embed=discord.Embed(color=discord.Color.brand_red(),
                                              description="There were no cogs to reload."), ephemeral=True)
        return

    client.unload_extension(extension)
    client.load_extension(extension)
    try:
        await client.sync_commands(force=True)
    except discord.HTTPException:
        pass
    await ctx.respond(embed=discord.Embed(color=discord.Color.brand_green(),
                                          description=f"`{extension}` was successfully reloaded."), ephemeral=True)


if __name__ == "__main__":
    client.run(os.environ["DISCORD_TOKEN"])

