import disnake.ui

from utils.helper import *


class SetFlag(disnake.ui.View):
    def __init__(self, author):
        super().__init__(timeout=30)
        self.langs = Languages()
        self.author = author

    @disnake.ui.button(label="🇷🇺", custom_id="ru", style=disnake.ButtonStyle.gray)
    async def ru_callback(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author == self.author:
            await interaction.response.defer()
            await self.langs.set_language(interaction.guild.id, str(button.custom_id))
            await interaction.edit_original_message(
                embed=disnake.Embed(
                    title=await self.langs.get_language(interaction.guild.id, "general", "success"),
                    description=await self.langs.get_language(interaction.guild.id, "lang", "lang_changed") % button.
                    custom_id
                ),
                view=None
            )

    @disnake.ui.button(label="🇺🇦", custom_id="ua", style=disnake.ButtonStyle.gray)
    async def ua_callback(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author != self.author:
            await interaction.send(content="Вы не можете использовать эти кнопки!", ephemeral=True)
        else:
            await interaction.response.defer()
            await self.langs.set_language(interaction.guild.id, str(button.custom_id))
            await interaction.edit_original_message(
                embed=disnake.Embed(
                    title=await self.langs.get_language(interaction.guild.id, "general", "success"),
                    description=await self.langs.get_language(interaction.guild.id, "lang", "lang_changed") % button.
                    custom_id
                ),
                view=None
            )

    @disnake.ui.button(label="🇺🇸", custom_id="en", style=disnake.ButtonStyle.gray)
    async def en_callback(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.author == self.author:
            await interaction.response.defer()
            await self.langs.set_language(interaction.guild.id, str(button.custom_id))
            await interaction.edit_original_message(
                embed=disnake.Embed(
                    title=await self.langs.get_language(interaction.guild.id, "general", "success"),
                    description=await self.langs.get_language(interaction.guild.id, "lang", "lang_changed") % button.
                    custom_id
                ),
                view=None
            )


class Localization(commands.Cog):
    def __init__(self, bot):
        super(Localization, self).__init__()
        self.bot = bot
    #     self.languages = Languages()
    #
    # @commands.command(name="hello")
    # async def hello(self, ctx: commands.Context, test: str):
    #     l = await self.languages.get_language_command(guild_id=ctx.guild.id, command="hello", value="output")
    #     await ctx.send(content=l)
    #
    # @commands.command(name="change_local", description="Изменить локализацию")
    # @commands.has_permissions(administrator=True)
    # async def change_local(self, ctx: commands.Context):
    #     emb = disnake.Embed(
    #         title=await self.languages.get_language(guild_id=ctx.guild.id, _type="lang", value="select_lang"),
    #         colour=0x00FF00
    #     )
    #     await ctx.send(embed=emb, view=SetFlag(ctx.author))


def setup(bot) -> None:
    bot.add_cog(Localization(bot))
