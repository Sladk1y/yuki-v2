from utils.helper import *


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        emb = disnake.Embed(title="Ошибка", colour=disnake.Colour.red())
        if isinstance(error, (commands.errors.MissingRequiredArgument, commands.errors.BadArgument)):
            emb.description = "Вы неправильно использовали команду\n\n**Правильное использование:**\n"\
                              f"{ctx.prefix}" \
                              f"{ctx.command.usage}"
        elif isinstance(error, commands.errors.CommandNotFound):
            return
        elif isinstance(error, commands.errors.MissingPermissions):
            ex = ""
            for i in error.missing_permissions:
                ex += f"{objects['errors'][i]}, "
            emb.description = f"Вы не можете `{ex[:-2]}` для использования этой команды"
        else:
            emb.description = str(error)
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Errors(bot))
