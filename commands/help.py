import discord
from discord.ext import commands, bridge


class HelpCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @bridge.bridge_command(name="help", description="shows explanations of commands")
    async def _help(self, ctx):
        pass


def setup(client):
    client.add_cog(HelpCommand(client))
