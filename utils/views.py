import discord


class HelpSelectMenu(discord.ui.View):
    options = []

    def __init__(self, client, prefix):
        super().__init__()
        self.client = client
        self.prefix = prefix

        if not self.options:
            for cog in self.client.cogs:
                if self.client.get_cog(cog).walk_commands() is not None:
                    self.options.append(discord.SelectOption(label=cog, emoji="🔧"))

    @discord.ui.select(
        placeholder="Choose a module to view commands",
        options=options,
    )
    async def select_callback(self, select, interaction):
        description = ""

        for command in self.client.get_cog(select.values[0]).walk_commands():
            if command.full_parent_name:
                if f"{command.full_parent_name} {command.name}" not in description:
                    description += f"**{self.prefix}{command.full_parent_name} {command.name}**\n"\
                                   f"```{command.description}```\n"
            else:
                if f"{command.name}" not in description:
                    description += f"**{self.prefix}{command.name}**\n"\
                                   f"```{command.description}```\n"

        await interaction.response.send_message(
            embed=discord.Embed(
                color=discord.Color.brand_green(),
                description=f"{description}",
            ), ephemeral=True
        )
