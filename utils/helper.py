from motor.motor_asyncio import AsyncIOMotorClient
import json
import disnake
from disnake.ext import commands


with open("utils/objects.json", "r", encoding="utf-8") as f:
    objects = json.load(f)

db = AsyncIOMotorClient("mongodb+srv://admin:yuki77784564810@yukicluster.afvzitv.mongodb.net/?retryWrites=true&w"
                        "=majority").test
users = db.users
guilds = db.guilds


# class Languages:
#     @staticmethod
#     async def get_language(guild_id: int, _type: Literal["general", "lang", "commands"], value: str):
#         g = await guilds.find_one({"guild_id": guild_id})
#         try:
#             return _all[_type][g["lang"]][value]
#         except KeyError:
#             await guilds.update_one({"guild_id": guild_id}, {"$set": {"lang": "ru"}})
#         return _all[_type]["ru"][value]
#
#     @staticmethod
#     async def get_language_command(guild_id: int, command: str, value: str):
#         g = await guilds.find_one({"guild_id": guild_id})
#         try:
#             return _all["commands"][command][g["lang"]][value]
#         except KeyError:
#             await guilds.update_one({"guild_id": guild_id}, {"$set": {"lang": "ru"}})
#         return _all["commands"][command]["ru"][value]
#
#     @staticmethod
#     async def set_language(guild_id: int, language: str = "en"):
#         await guilds.update_one({"guild_id": guild_id}, {"$set": {"lang": language}})


async def get_prefix(_, message: disnake.Message):
    g = await guilds.find_one({"guild_id": message.guild.id})
    if not g:
        g = objects["guild"]
        g["guild_id"] = message.guild.id
        await guilds.insert_one(g)
    message.reference = g
    return g["prefix"]


async def get_user(context: commands.Context | disnake.Message):
    u = await users.find_one({"user_id": context.author.id, "guild_id": context.guild.id})
    if not u:
        u = objects["user"]
        u["guild_id"] = context.guild.id
        u["user_id"] = context.author.id
        await users.insert_one(u)
    return u
