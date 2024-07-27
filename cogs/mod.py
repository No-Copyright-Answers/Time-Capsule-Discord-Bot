import discord
from discord import app_commands
from discord.ext import commands
from Core.classes import Cog_Extension
import json

with open("settings.json", "r", encoding="utf8") as f:
    settings = json.load(f)


class mod(Cog_Extension):

    @commands.command()
    async def add_badword(self, ctx, word):
        if str(ctx.author.id) in settings["admin_ids"]:
            settings["Bad_Words"].append(word)
            with open("settings.json", "w", encoding="utf8") as f:
                json.dump(settings, f, indent=4)
            await ctx.send(f"Added {word} to bad words list.")
        else:
            await ctx.send("You are not allowed to use this command.")

    @commands.command()
    async def remove_badword(self, ctx, word):
        if str(ctx.author.id) in settings["admin_ids"]:
            settings["Bad_Words"].remove(word)
            with open("settings.json", "w", encoding="utf8") as f:
                json.dump(settings, f, indent=4)
            await ctx.send(f"Removed {word} from bad words list.")
        else:
            await ctx.send("You are not allowed to use this command.")

    @commands.command()
    async def add_admin(self, ctx, user: int):
        if str(ctx.author.id) in settings["admin_ids"]:
            if len(str(user)) == 18:
                if str(user) in settings["admin_ids"]:
                    await ctx.send(f"{user} is already an admin.")
                else:
                    settings["admin_ids"].append(str(user))
                    with open("settings.json", "w", encoding="utf8") as f:
                        json.dump(settings, f, indent=4)
                    await ctx.send(f"Added {user} to admin list.")
            else:
                await ctx.send(f"Member id {user} not found")
        else:
            await ctx.send("You are not allowed to use this command.")

    @commands.command()
    async def remove_admin(self, ctx, user: int):
        if str(ctx.author.id) in settings["Bot_OwnerID"]:
            if len(str(user)) == 18:
                if str(user) in settings["admin_ids"]:
                    settings["admin_ids"].remove(str(user))
                    with open("settings.json", "w", encoding="utf8") as f:
                        json.dump(settings, f, indent=4)
                    await ctx.send(f"Removed {user} from admin list.")
                else:
                    await ctx.send(f"{user} is not an admin.")
            else:
                await ctx.send(f"Member id {user} not found")
        else:
            await ctx.send("You are not allowed to use this command.")


async def setup(bot):
    await bot.add_cog(mod(bot))
