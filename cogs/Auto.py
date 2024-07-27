import discord
from discord import app_commands
from discord.ext import commands
from Core.classes import Cog_Extension
import json

with open("settings.json", "r", encoding="utf8") as f:
    settings = json.load(f)


class auto(Cog_Extension):

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(settings["announce_channel"])
        print(f'{member} has joined the server.')
        await channel.send(settings["Welcome_Message"].format(member))
        role = discord.utils.get(member.guild.roles, name="Member")
        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(settings["announce_channel"])
        print(f'{member} has left the server.')
        await channel.send(settings["Leave_Message"].format(member))

    # 言論審查系統
    @commands.Cog.listener()
    async def on_message(self, msg):
        channel = self.bot.get_channel(settings["command_testing_channel"])
        for i in settings["Bad_Words"]:
            if i in msg.content.lower() and msg.author != self.bot.user and not str(msg.author.id) in settings["Bot_OwnerID"]:
                await msg.delete()
                await msg.channel.send(f"{msg.author.mention} 言论审查系统已将您的讯息删除。")
                await channel.send(f'{msg.author} said {msg.content} in {msg.channel}.')


async def setup(bot):
    await bot.add_cog(auto(bot))
