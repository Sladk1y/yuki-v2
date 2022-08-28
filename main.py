import random

from utils.helper import *
import art
from os import listdir
import colorama
colorama.init()


class Intents(disnake.Intents):
    def __init__(self):
        super(Intents, self).__init__()

    def __call__(self):
        x = self.all()
        x.presences = False
        return x


class Bot(commands.AutoShardedBot):
    def __init__(self):
        super(Bot, self).__init__(
            command_prefix=get_prefix,
            intents=Intents()(),
            help_command=None,  # type: ignore
            strip_after_prefix=True
        )

    async def on_ready(self):
        print(f"Ready with {len(self.commands)} commands!")

    async def on_connect(self):
        _art = art.text2art("Yuki   V2")
        _art_ = ""
        for sym in _art:
            color = random.choice([colorama.Fore.GREEN, colorama.Fore.BLUE, colorama.Fore.CYAN])
            _art_ += f"{color}{sym}{colorama.Fore.RESET}"
        print(_art_)
        for file in listdir("cogs"):
            if file.endswith(".py"):
                try:
                    self.load_extension("cogs." + file[:-3])
                    print("Loaded extension: " + file)
                except Exception as e:
                    print(f"Not loaded extension: {file} with error: {str(e)}")

    async def on_message(self, message: disnake.Message):
        if message.author.bot:
            return
        if not message.guild:
            return
        ctx = await self.get_context(message)
        ctx.g = message.reference
        await self.invoke(ctx)
        if message.content == "?prefix":
            return await message.channel.send(message.g["prefix"])
        await get_user(message)


Bot().run("DISCORD-TOKEN")
