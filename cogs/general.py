from utils.helper import *


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["хелп", "помощь"])
    async def _help(self, ctx: commands.Context):
        g = await guilds.find_one({"guild_id": ctx.guild.id})
        emb = disnake.Embed()
        emb.description = "Вы можете посмотреть все команды на нашем [сайте](https://yukibot.ml/pages/commands.html)."
        emb.colour = 0x00FF00
        _fields = {
            "⚙ Главное": "`?prefix` ",
            "💰 Экономика": "",
            "🛡 Модерация": ""
        }
        for cmd in self.bot.commands:
            if cmd.module == "cogs.general":
                _fields["⚙ Главное"] += f"`{g['prefix']}{cmd.name}` "
            elif cmd.module == "cogs.economy":
                _fields["💰 Экономика"] += f"`{g['prefix']}{cmd.name}` "
            elif cmd.module == "cogs.moderation":
                _fields["🛡 Модерация"] += f"`{g['prefix']}{cmd.name}` "
        for key in _fields.keys():
            emb.add_field(name=key, value=_fields[key], inline=False)
        emb.set_footer(text=f"Всего команд: {len(self.bot.commands)}", icon_url=ctx.author.avatar.url)
        emb.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.send(embed=emb)

    @commands.command(name="avatar", aliases=["аватар"])
    async def avatar(self, ctx: commands.Context, member: disnake.Member = None):
        if not member:
            member = ctx.author
        emb = disnake.Embed()
        emb.title = f"Аватар {member.name}"
        emb.description = f"[Скачать]({member.avatar.url})"
        emb.colour = 0x0FF00
        emb.set_image(url=member.avatar.url)
        emb.set_footer(icon_url=ctx.author.avatar.url)
        await ctx.send(embed=emb)

    @commands.command(name="say", aliases=["сказать"], usage="say <text>")
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx: commands.Context, *, text: str):
        await ctx.send(text)

    @commands.command(name="server", aliases=["сервер"])
    async def server(self, ctx: commands.Context):
        emb = disnake.Embed()
        emb.title = ctx.guild.name
        emb.colour = 0x00FF00
        emb.set_thumbnail(url=ctx.guild.icon.url)
        ver_lvl = {
            "none": "отсутствует",
            "low": "низкий",
            "medium": "средний",
            "high": "высокий",
            "highest": "самый высокий"
        }
        emb.description = f"""
        <:settings:998148541904080946> **Уровень верификации:** {ver_lvl[str(ctx.guild.verification_level)]}
        <:owner:998149232269733888> **Владелец:** {ctx.guild.owner.mention}
        """
        emb.add_field(name=f"Каналы [{len(ctx.guild.channels) - len(ctx.guild.categories)}]", value=f"""
        <:text:998149819212251207> Текстовых: {len(ctx.guild.text_channels)}
        <:voice:998149839772721253> Голосовых: {len(ctx.guild.voice_channels)}
        """)
        emb.add_field(name=f"Статистика", value=f"""
        <:users:998149460062371840> Участников: {ctx.guild.member_count}
        <:roles:998148133676646441> Ролей: {len(ctx.guild.roles)}
        <:emojis:998148479761272934> Эмодзи: {len(ctx.guild.emojis)}
        """)
        emb.set_footer(text=f"ID: {ctx.guild.id}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=emb)

    @commands.command(name="set-prefix")
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx: commands.Context, prefix: str = "!"):
        await guilds.update_one({"guild_id": ctx.guild.id}, {"$set": {"prefix": prefix}})
        emb = disnake.Embed()
        emb.description = f"Установлен новый префикс: `{prefix}`"
        emb.colour = 0x00FF00
        await ctx.send(embed=emb)

    @commands.command(name="set-currency")
    @commands.has_permissions(administrator=True)
    async def set_currency(self, ctx: commands.Context, currency: str = "<a:money:998158048952586280>"):
        await guilds.update_one({"guild_id": ctx.guild.id}, {"$set": {"currency": currency}})
        emb = disnake.Embed()
        emb.description = f"Установлен новый значок валюты: {currency}"
        emb.colour = 0x00FF00
        await ctx.send(embed=emb)

    @commands.command()
    async def bot(self, ctx: commands.Context):
        emb = disnake.Embed(
            title="Информация",
            colour=0x00FF00
        )
        emb.description = f"""
        ping: {round(self.bot.latency*1000, 2)}ms
        db ping: {await db.command('ping')}
        """
        await ctx.send(embed=emb)

    # @commands.command()
    # async def addmoney(self, ctx, guildid: int):
    #     a = await users.update_one({"gid": guildid, "uid": ctx.author.id}, {"$set": {"balance": 9223372036854775807}})


def setup(bot):
    bot.add_cog(General(bot))
