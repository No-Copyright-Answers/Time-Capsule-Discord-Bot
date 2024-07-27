import discord
from discord import app_commands
from discord.ext import commands
from Core.classes import Cog_Extension
from gtts import gTTS
import os
import json
import asyncio

with open("settings.json", "r", encoding="utf8") as f:
    settings = json.load(f)


class tts(Cog_Extension):

    @commands.command()
    async def ts(self, ctx, uinput=None):
        if not ctx.author.voice:
            await ctx.send("請先進入語音頻道。")
        else:
            if not ctx.guild.voice_client:
                await ctx.author.voice.channel.connect()
            if uinput != None:
                tts = gTTS(text=uinput, lang='zh-CN')
                tts.save("tts.mp3")
                # play mp3
                voice = ctx.guild.voice_client
                source = discord.FFmpegPCMAudio("tts.mp3")
                player = voice.play(source)
                while voice.is_playing():
                    await asyncio.sleep(1)
                os.remove("tts.mp3")
            else:
                await ctx.send("請輸入你要轉換成文字的訊息.")

    @app_commands.command(name="tts", description="文字轉語音")
    @app_commands.describe(message="輸入文字")
    async def tts(self, interaction: discord.Interaction, message: str):
        try:
            voicechannel = interaction.user.voice.channel.id
            try:
                botvoicechannel = interaction.guild.voice_client.channel.id
                if botvoicechannel != voicechannel:
                    await interaction.guild.voice_client.disconnect()
                    await interaction.user.voice.channel.connect(timeout=10)
            except:
                await interaction.user.voice.channel.connect(timeout=10)
            tts = gTTS(text=message, lang='zh-CN')
            tts.save("tts.mp3")
            # play mp3
            voice = interaction.guild.voice_client
            source = discord.FFmpegPCMAudio("tts.mp3")
            player = voice.play(source)
            while voice.is_playing():
                await asyncio.sleep(1)
            os.remove("tts.mp3")
            await interaction.response.send_message(f"**{str(interaction.user)[:-5]}: {message}**")
        except:
            await interaction.response.send_message("請先進入語音頻道。")


async def setup(bot):
    await bot.add_cog(tts(bot))
