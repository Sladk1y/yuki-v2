from utils.helper import *


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban", aliases=["бан"], usage="ban <member> [reason]")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: disnake.Member, *, reason: str = None):
        try:
            await member.ban(delete_message_days=0, reason=reason)
        except (Exception,):
            return await ctx.message.add_reaction("❌")
        await ctx.message.add_reaction("✅")

    @commands.command(name="mute", aliases=["мут", "timeout", "мьют"], usage="mute <member> [duration] [reason]")
    @commands.has_permissions(manage_guild=True)
    async def mute(self, ctx: commands.Context, member: disnake.Member, timeout: int = 60, *, reason: str = None):
        try:
            await member.timeout(duration=timeout * 60, reason=reason)
        except (Exception,):
            return await ctx.message.add_reaction("❌")
        await ctx.message.add_reaction("✅")

    @commands.command(name="unmute", aliases=["размут", "анмут"], usage="unmute <member>")
    @commands.has_permissions(manage_guild=True)
    async def unmute(self, ctx: commands.Context, member: disnake.Member):
        try:
            await member.timeout(duration=None)
        except (Exception,):
            return await ctx.message.add_reaction("❌")
        await ctx.message.add_reaction("✅")

    @commands.command(name="kick", aliases=["кик"], usage="kick <member> [reason]")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: disnake.Member, *, reason: str = None):
        try:
            await member.kick(reason=reason)
        except (Exception,):
            return await ctx.message.add_reaction("❌")
        await ctx.message.add_reaction("✅")


def setup(bot):
    bot.add_cog(Moderation(bot))
