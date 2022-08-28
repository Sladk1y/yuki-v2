import random
import pymongo

from utils.helper import *


async def get_default(ctx: commands.Context, member: disnake.Member):
    c = ctx.g["currency"]
    u = await users.find_one({"user_id": member.id, "guild_id": ctx.guild.id})
    return c, u


def pint(number):
    number = str(number)[::-1]
    result = ''
    for i, num in enumerate(number):
        if i % 3 == 0:
            result += '.'
        result += num
    return result[::-1][:-1]


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="profile", aliases=["balance", "bal", "$", "баланс", "бал", "профиль", "p", "п"],
        usage="profile [member]"
    )
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def profile(self, ctx: commands.Context, member: disnake.Member = None):
        if not member:
            member = ctx.author
        else:
            ctx.message.author = member
        c, u = await get_default(ctx, member)
        emb = disnake.Embed(
            title=f"Профиль {member}",
            colour=0x00FF00
        )
        emb.description = f"""
        💵 **На руках:** {pint(u['balance'])}{c}
        🏦 **В банке:** {pint(u['bank'])}{c}
        📊 **Общий баланс:** {pint(u['bank'] + u['balance'])}{c}
        """
        emb.set_thumbnail(url=member.avatar.url)
        ex = ""
        ex += f"{ctx.prefix + 'bonus' if not self.bonus.is_on_cooldown(ctx) else '~~' + ctx.prefix + 'bonus' + '~~'} "
        ex += f"{ctx.prefix + 'work' if not self.work.is_on_cooldown(ctx) else '~~' + ctx.prefix + 'work' + '~~'} "
        emb.add_field(name="🤑 Доступный заработок", value=ex, inline=True)
        await ctx.send(embed=emb)

    @commands.command(name="bonus", aliases=["бонус"], usage="bonus")
    #                    24 hours                    #
    @commands.cooldown(1, 86400, commands.BucketType.member)
    async def bonus(self, ctx: commands.Context):
        c, u = await get_default(ctx, ctx.author)
        emb = disnake.Embed(
            title="Ежедневный бонус",
            colour=0x00FF00
        )
        n = random.randint(1000, 5000)
        await users.update_one(
            {"user_id": ctx.author.id, "guild_id": ctx.guild.id}, {"$inc": {"balance": n}}
        )
        emb.description = f"**{ctx.author}** выиграл в бесплатной лоттерее **{pint(n)}**{c}"
        emb.add_field(name="Следующий бонус можно будет забрать", value="через 24 часа.")
        emb.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=emb)

    @commands.command(name="work", aliases=["работать"], usage="work")
    #                    2 hours                    #
    @commands.cooldown(1, 7200, commands.BucketType.member)
    async def work(self, ctx: commands.Context):
        c, u = await get_default(ctx, ctx.author)
        emb = disnake.Embed(
            title="Работа",
            colour=0x00FF00
        )
        n = random.randint(100, 1000)
        await users.update_one(
            {"user_id": ctx.author.id, "guild_id": ctx.guild.id},
            {"$inc": {"balance": n}}
        )
        work = random.choice(['грузчиком', 'кассиром', 'менеджером', 'трубочистом'])
        emb.description = f"**{ctx.author}** заработал **{pint(n)}**{c}, работая {work}"
        emb.add_field(name="Вы устали, снова можно будет пойти на работу", value="через 2 часа.")
        emb.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=emb)

    @commands.command(aliases=['dep', 'деп', 'вложить'], usage="dep <money>")
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def deposit(self, ctx: commands.Context, money):
        c, u = await get_default(ctx, ctx.author)
        if money == "all":
            money = u['balance']
        money = int(money)
        if u['balance'] < money:
            return
        await users.update_one(
            {"user_id": ctx.author.id, "guild_id": ctx.guild.id},
            {"$set": {"balance": u['balance'] - money, "bank": u['bank'] + round(money * (97 / 100), 0)}}
        )
        emb = disnake.Embed(
            title="Внесение наличных",
            colour=0x00FF00
        )
        emb.description = f"**{ctx.author}** положил **{pint(money)}**{c} в банк\n\nКомиссия составила **3%**"
        emb.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=emb)

    @commands.command(name="with", aliases=['вывести'], usage="with <money>")
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def _with(self, ctx: commands.Context, money):
        c, u = await get_default(ctx, ctx.author)
        if money == "all":
            money = u['bank']
        money = int(money)
        if u['bank'] < money:
            return
        await users.update_one(
            {"user_id": ctx.author.id, "guild_id": ctx.guild.id},
            {"$set": {"balance": u['balance'] + round(money * (90 / 100), 0), "bank": u['bank'] - money}}
        )
        emb = disnake.Embed(
            title="Снятие денег",
            colour=0x00FF00
        )
        emb.description = f"**{ctx.author}** снял **{pint(money)}**{c} из банка\n\nКомиссия составила **10%**"
        emb.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=emb)

    @commands.command(name="pay", aliases=["передать", "перевести"], usage="pay <member> <money>")
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def pay(self, ctx: commands.Context, member: disnake.Member, money):
        c, u = await get_default(ctx, ctx.author)
        if money == "all":
            money = u['balance']
        money = int(money)
        if u['balance'] < money:
            return
        await users.update_one(
            {"guild_id": ctx.guild.id, "user_id": member.id},
            {"$inc": {"balance": money}}
        )
        await users.update_one(
            {"guild_id": ctx.guild.id, "user_id": ctx.author.id},
            {"$set": {"balance": u["balance"] - money}}
        )
        emb = disnake.Embed(
            title="Передача денег",
            colour=0x00FF00
        )
        emb.description = f"**{ctx.author}** передал **{member}** **{pint(money)}**{c}"
        emb.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=emb)

    @commands.command(name="casino", aliases=["казино"], usage="casino <bet>")
    @commands.cooldown(1, 1.5, commands.BucketType.member)
    async def casino(self, ctx: commands.Context, bet):
        c, u = await get_default(ctx, ctx.author)
        if bet == "all":
            bet = u['balance']
        bet = int(bet)
        if u['balance'] < bet:
            return
        z = random.randint(0, 100)
        kof = 0
        if z <= 32:
            kof = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 10, 2, 2, 2, 2, 2, 2, 3])
        bet = bet * kof
        emb = disnake.Embed(
            title="Казино",
            colour=0x00FF00 if bet != 0 else disnake.Colour.red()
        )
        emb.description = f"""
        **{ctx.author}** сделал ставку в казино и **{'выиграл' if bet != 0 else 'проиграл'}**
        
        🎟️ Ставка: **{pint(bet / kof)}**{c}
        💸 Баланс: **{pint(u['balance'] + bet)}**{c}
        {('📈 Коэффициент: **X' + str(kof) + '**') if bet != 0 else ''}
        """
        emb.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=emb)

    @commands.command(aliases=["ограбить"], usage="rob <member>")
    @commands.cooldown(1, 86400, commands.BucketType.member)
    async def rob(self, ctx: commands.Context, member: disnake.Member):
        c, u = await get_default(ctx, member)
        if u['balance'] < 1000:
            return await ctx.message.add_reaction("❌")
        money = random.randint(100, round(u['balance'] * (70 / 100), 0))
        await users.update_one(
            {"guild_id": ctx.guild.id, "user_id": member.id},
            {"$set": {"balance": u["balance"] - money}}
        )
        await users.update_one(
            {"guild_id": ctx.guild.id, "user_id": ctx.author.id},
            {"$inc": {"balance": money}}
        )
        emb = disnake.Embed(
            title="Ограбление",
            colour=0x00FF00
        )
        emb.description = f"**{ctx.author}** ограбил **{member}** на **{pint(money)}**{c}"
        emb.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=emb)

    @commands.command(name="top|btop", aliases=["топ", "btop", "бтоп", "top"])
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def _top(self, ctx: commands.Context):
        if 'btop' not in ctx.message.content.lower() and 'бтоп' not in ctx.message.content.lower():
            title = '`👑` Таблица лидеров'
            param = 'balance'
        else:
            title = '`👑` таблица лидеров по банкам'
            param = 'bank'
        user_list = []
        async for _ in users.find({'guild_id': ctx.guild.id}) \
                .sort([(param, pymongo.DESCENDING)]).limit(10):
            user_list.append(_)
        description = ''
        currency, _ = await get_default(ctx, ctx.author)
        for num, user in enumerate(user_list):
            i = user['user_id']
            rew_list = ['🥇', '🥈', '🥉']
            if num < 3:
                description += f'\n`{rew_list[num]}` **<@{i}>** — **{pint(user[param])}** {currency}\n'
            else:
                description += f'\n**#{num+1} <@{i}>** — **{pint(user[param])}** {currency}\n'
        await ctx.send(embed=disnake.Embed(description=description, colour=0x00FF00, title=title))


def setup(bot):
    bot.add_cog(Economy(bot))
