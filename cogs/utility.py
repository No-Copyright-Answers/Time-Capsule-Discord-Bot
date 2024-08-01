import discord
from discord import app_commands
from discord.ext import commands
from Core.classes import Cog_Extension
import json

with open("settings.json", "r", encoding="utf8") as f:
    settings = json.load(f)


class utility(Cog_Extension):

    @app_commands.command(name="ping", description="Return the bot's latency.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Response time: {round(self.bot.latency * 1000)}ms', ephemeral=True)


async def setup(bot):
    await bot.add_cog(utility(bot))
