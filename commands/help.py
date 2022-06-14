import discord
from discord.ext import commands, bridge
from discord.ext.pages import PaginatorButton, Paginator

import aiosqlite


class HelpCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @staticmethod
    async def get_prefix(ctx):
        db = await aiosqlite.connect('database/prefixes.db')
        async with db.execute("SELECT * FROM prefixes") as cursor:
            async for row in cursor:
                if row[0] == ctx.guild.id:
                    return row[1]
            return "x!"

    @bridge.bridge_command(name="help", description="shows explanations of commands")
    async def _help(self, ctx):
        prefix = await self.get_prefix(ctx)
        cogs = [cog for cog in self.client.cogs if self.client.get_cog(cog).walk_commands() is not None]

        modules = ""

        for cog in cogs:
            modules += f"{cog}\n"

        embed = discord.Embed(
            color=discord.Color.blurple(),
            title="List of Modules: ",
            description=f"{modules}"
        )

        pages = [embed]

        commands_list = []

        for cog in cogs:
            cog_embed = discord.Embed(color=discord.Color.blurple(), description=f"**{cog}'s commands:**")
            cog_embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar.url)

            for command in self.client.get_cog(cog).walk_commands():
                if isinstance(command, discord.SlashCommandGroup):
                    continue
                if command.full_parent_name:
                    command_name = command.full_parent_name + " " + command.name
                else:
                    command_name = command.name

                if command_name in commands_list:
                    continue

                commands_list.append(command_name)

                cog_embed.add_field(
                    name=f"{prefix}{command_name}",
                    value=f"""```{command.description}```"""
                )

            pages.append(cog_embed)

        buttons = [
            PaginatorButton("first", label="<<", style=discord.ButtonStyle.blurple),
            PaginatorButton("prev", label="<-", style=discord.ButtonStyle.blurple),
            PaginatorButton("page_indicator", style=discord.ButtonStyle.blurple, disabled=True),
            PaginatorButton("next", label="->", style=discord.ButtonStyle.blurple),
            PaginatorButton("last", label=">>", style=discord.ButtonStyle.blurple)
        ]

        paginator = Paginator(
            pages=pages,
            show_disabled=True,
            show_indicator=True,
            use_default_buttons=False,
            custom_buttons=buttons,
            loop_pages=False,
            disable_on_timeout=True,
            timeout=30
        )

        if isinstance(ctx, commands.Context):
            await paginator.respond(ctx, ephemeral=True)
        else:
            await paginator.respond(ctx.interaction, ephemeral=True)


def setup(client):
    client.add_cog(HelpCommand(client))
