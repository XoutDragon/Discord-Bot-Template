import discord
from discord.ext import commands

import logging


class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ignored_errors = (
            commands.CheckFailure,
            commands.CommandNotFound,
            commands.DisabledCommand,
            commands.UserInputError,
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        try:
            match isinstance(error):
                case self.ignored_errors:
                    return
                case commands.errors.CommandOnCooldown:
                    return await ctx.send(
                        embed=discord.Embed(
                            color=discord.Color.brand_red(),
                            description=f"This command is on cooldown. Try again in {error.retry_after:.2f} seconds."
                        ), delete_after=10
                    )
                case commands.errors.MissingPermissions:
                    return await ctx.send(
                        embed=discord.Embed(
                            color=discord.Color.brand_red(),
                            description="You do not have the required permissions to use this command."
                        )
                    )

        except discord.DiscordException:
            return logging.error(f"DiscordException: {error}")

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.ApplicationCommandError):
        if isinstance(error, self.ignored_errors):
            return
        try:
            if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
                embed = discord.Embed(color=discord.Color.brand_red(),
                                      description=f"You are on cooldown for this command. Try again in \
                                                    {error.retry_after:.2f} seconds.")
                await ctx.respond(embed=embed, ephemeral=True)
                return

            elif isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(color=discord.Color.brand_red(),
                                      description=f"You need the {error.missing_permissions} to execute this command.")
                await ctx.respond(embed=embed, ephemeral=True)
                return

            elif isinstance(error, commands.MissingRole):
                embed = discord.Embed(color=discord.Color.brand_red(),
                                      description=f"You need the {error.missing_role} role to execute this command.")
                await ctx.respond(embed=embed, ephemeral=True)
                return

            elif isinstance(error, commands.NotOwner):
                embed = discord.Embed(color=discord.Color.brand_red(),
                                      description=f"You need to be the bot owner to execute this command.")
                await ctx.respond(embed=embed, ephemeral=True)
                return

            elif isinstance(error, commands.BotMissingPermissions):
                embed = discord.Embed(color=discord.Color.brand_red(),
                                      description=f"I need the {error.missing_permissions} to execute this command.")
                await ctx.respond(embed=embed, ephemeral=True)
                return

            elif isinstance(error, commands.NoPrivateMessage):
                embed = discord.Embed(color=discord.Color.brand_red(),
                                      description=f"This command cannot be used in private messages.")
                await ctx.respond(embed=embed, ephemeral=True)
                return

            elif isinstance(error, commands.PrivateMessageOnly):
                embed = discord.Embed(color=discord.Color.brand_red(),
                                      description=f"This command can only be used in private messages.")
                await ctx.respond(embed=embed, ephemeral=True)
                return
        except discord.HTTPException:
            logging.info("Unable to send application error message")


def setup(client):
    client.add_cog(ErrorHandler(client))