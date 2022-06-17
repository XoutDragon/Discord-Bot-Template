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
                        ), delete_after=10
                    )
                case commands.errors.BotMissingPermissions:
                    return await ctx.send(
                        embed=discord.Embed(
                            color=discord.Color.brand_red(),
                            description="I do not have the required permissions to use this command."
                        ), delete_after=10
                    )
                case commands.errors.MissingRole:
                    return await ctx.send(
                        embed=discord.Embed(
                            color=discord.Color.brand_red(),
                            description="You do not have the required role to use this command."
                        ), delete_after=10
                    )
                case commands.errors.NotOwner:
                    return await ctx.send(
                        embed=discord.Embed(
                            color=discord.Color.brand_red(),
                            description="You do not have the required permissions to use this command."
                        ), delete_after=10
                    )
                case commands.errors.NoPrivateMessage:
                    return await ctx.send(
                        embed=discord.Embed(
                            color=discord.Color.brand_red(),
                            description="This command cannot be used in private messages."
                        ), delete_after=10
                    )
                case commands.errors.PrivateMessageOnly:
                    return await ctx.send(
                        embed=discord.Embed(
                            color=discord.Color.brand_red(),
                            description="This command can only be used in private messages."
                        ), delete_after=10
                    )
                case _:
                    print(f"Unhandled Error: {error}")

        except discord.DiscordException:
            return logging.error(f"DiscordException: {error}")

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.ApplicationCommandError):
        try:
            match isinstance(error):
                case self.ignored_errors:
                    return
                case commands.errors.CommandOnCooldown:
                    return await ctx.respond(
                        embed=discord.Embed(
                            color=discord.Color.brand_red(),
                            description=f"This command is on cooldown. Try again in {error.retry_after:.2f} seconds."
                        ), ephemeral=True
                    )
                case commands.errors.MissingPermissions:
                    return await ctx.respond(
                        embed=discord.Embed(
                            color=discord.Color.brand_red(),
                            description="You do not have the required permissions to use this command."
                        ), ephemeral=True
                    )
                case commands.errors.BotMissingPermissions:
                    return await ctx.respond(
                        embed=discord.Embed(
                            color=discord.Color.brand_red(),
                            description="I do not have the required permissions to use this command."
                        ), ephemeral=True
                    )
                case commands.errors.MissingRole:
                    return await ctx.respond(
                        embed=discord.Embed(
                            color=discord.Color.brand_red(),
                            description="You do not have the required role to use this command."
                        ), ephemeral=True
                    )
                case commands.errors.NotOwner:
                    return await ctx.respond(
                        embed=discord.Embed(
                            color=discord.Color.brand_red(),
                            description="You do not have the required permissions to use this command."
                        ), ephemeral=True
                    )
                case commands.errors.NoPrivateMessage:
                    return await ctx.send(
                        embed=discord.respond(
                            color=discord.Color.brand_red(),
                            description="This command cannot be used in private messages."
                        ), ephemeral=True
                    )
                case commands.errors.PrivateMessageOnly:
                    return await ctx.respond(
                        embed=discord.Embed(
                            color=discord.Color.brand_red(),
                            description="This command can only be used in private messages."
                        ), ephemeral=True
                    )
                case _:
                    print(f"Unhandled Error: {error}")

        except discord.HTTPException:
            logging.info("Unable to send application error message")


def setup(client):
    client.add_cog(ErrorHandler(client))