import discord
from discord import app_commands
from discord.ext import commands
from Core.classes import Cog_Extension
import json

with open("settings.json", "r", encoding="utf8") as f:
    settings = json.load(f)


class voice(Cog_Extension):

    @commands.command()
    async def joinvc(self, ctx):
        bot_voice = ctx.guild.voice_client
        author_voice = ctx.author.voice

        if bot_voice and bot_voice.is_connected():
            await bot_voice.move_to(author_voice.channel)
            await ctx.send("Moved to the voice channel")

        elif author_voice and not bot_voice:  # Author connected but bot not connected
            voice = await author_voice.channel.connect()
            await ctx.send("Connected to the voice channel")

        elif not author_voice:  # Author not connected
            await ctx.send("**You need to get in to a voice channel**")

        elif ctx.bot.user in author_voice.channel.members:  # Bot and Author both connected
            await ctx.send("**Already in the channel**")

    @commands.command()
    async def leavevc(self, ctx):
        try:
            voice = ctx.guild.voice_client.channel.id
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected from the voice channel")
        except:
            await ctx.send("Not in a voice channel")

    @app_commands.command(name="join", description="Join the voice channel")
    async def join(self, interaction: discord.Interaction):
        bot_voice = interaction.guild.voice_client
        author_voice = interaction.user.voice
        try:
            bot_cid = bot_voice.channel.id
            author_cid = author_voice.channel.id
            if bot_cid != author_cid:
                await interaction.guild.voice_client.disconnect()
                await interaction.user.voice.channel.connect()
                await interaction.response.send_message("Moved to the voice channel")
            else:
                await interaction.response.send_message("Already in the channel")
        except:
            try:
                author_cid = author_voice.channel.id
                await interaction.user.voice.channel.connect()
                await interaction.response.send_message("Connected to the voice channel")
            except:
                await interaction.response.send_message("You need to get in to a voice channel first")

    @app_commands.command(name="leave", description="Leave the voice channel")
    async def leave(self, interaction: discord.Interaction):
        try:
            bot_cid = interaction.guild.voice_client.channel.id
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("Disconnected from the voice channel")
        except:
            await interaction.response.send_message("Not in a voice channel")


async def setup(bot):
    await bot.add_cog(voice(bot))
