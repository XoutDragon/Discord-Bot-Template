import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

import aiosqlite


class Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    config = SlashCommandGroup(
        "config", description="configuration commands",
        default_member_permissions=discord.Permissions(permissions=32)
    )

    @config.command(name="prefix", description="sets the prefix for the bot")
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def _prefix(self, ctx, prefix: str):
        await ctx.defer()
        if len(prefix) > 25:
            return await ctx.respond(
                embed=discord.Embed(
                    color=discord.Color.brand_red(),
                    description="Prefix must be less than 25 characters."
                )
            )
        db = await aiosqlite.connect('database/prefixes.db')
        async with db.execute("SELECT * FROM prefixes") as cursor:
            async for row in cursor:
                if row[0] == ctx.guild.id:
                    await db.execute("UPDATE prefixes SET prefix = ? WHERE guild_id = ?", (prefix, ctx.guild.id))
                    await db.commit()
                    await ctx.respond(
                        embed=discord.Embed(
                            color=discord.Color.brand_green(),
                            description=f"Prefix set to `{prefix}`"
                        )
                    )
                    await ctx.guild.me.edit(nick=f"❮{prefix}❯ {ctx.guild.me.name}")
                    return

            await db.execute("INSERT INTO prefixes (guild_id, prefix) VALUES (?, ?)", (ctx.guild.id, prefix))
            await db.commit()
            await ctx.respond(
                embed=discord.Embed(
                    color=discord.Color.brand_green(),
                    description=f"Prefix set to `{prefix}`"
                )
            )
            await ctx.guild.me.edit(nick=f"❮{prefix}❯ {ctx.guild.me.name}")


def setup(client):
    client.add_cog(Config(client))
