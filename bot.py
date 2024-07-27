import discord
from discord import app_commands
from discord.ext import commands
import os
import json

with open("settings.json", "r", encoding="utf8") as f:
    settings = json.load(f)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=settings["Bot_Prefix"], intents=intents)

# Bot events


@bot.event
async def on_ready():
    print('NCA Bot is online.\n')
    print("Loading Extensions...")
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Extension {filename[:-3]} has been loaded.')
            except Exception as e:
                print(f'Extension {filename[:-3]} failed to load: {e}')
    print("Extensions loaded.\n")
    print("Syncing slash commands...")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Failed to sync command(s): {e}")

# Bot commands

# Load Extension


@bot.command()
async def load(ctx, extension):
    if str(ctx.author.id) in settings["admin_ids"]:
        try:
            await bot.load_extension(f'cogs.{extension}')
            await ctx.send(f'Loaded {extension} done.')
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f'{extension} has already been loaded.')
        except:
            await ctx.send(f'Failed to load {extension}.')
    else:
        await ctx.send("You are not allowed to use this command.")

# Unload Extension


@bot.command()
async def unload(ctx, extension):
    if str(ctx.author.id) in settings["admin_ids"]:
        try:
            await bot.unload_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} has been unloaded.')
        except commands.ExtensionNotLoaded:
            await ctx.send(f'{extension} has not been loaded.')
        except:
            await ctx.send(f'Failed to unload {extension}.')
    else:
        await ctx.send("You are not allowed to use this command.")

# Reload Extension


@bot.command()
async def reload(ctx, extension):
    if str(ctx.author.id) in settings["admin_ids"]:
        try:
            await bot.reload_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} has been reloaded.')
        except commands.ExtensionNotLoaded:
            await bot.load_extension(f'cogs.{extension}')
            await ctx.send(f'Loaded {extension} done.')
        except:
            await ctx.send(f'Failed to reload {extension}.')
    else:
        await ctx.send("You are not allowed to use this command.")


# sync commands


@bot.command()
async def sync(ctx) -> None:
    if str(ctx.author.id) in settings["admin_ids"]:
        try:
            synced = await bot.tree.sync()
            await ctx.send(f"Synced {len(synced)} command(s).")
        except Exception as e:
            await ctx.send(f"Failed to sync command(s): {e}")
    else:
        await ctx.send("You are not allowed to use this command.")


# Shutdown the bot


@bot.command()
async def shutdown(ctx):
    if str(ctx.author.id) == settings["Bot_OwnerID"]:
        await ctx.send("Closing the bot...")
        await bot.close()
    else:
        await ctx.send("You are not allowed to use this command.")

# Run the bot
if __name__ == "__main__":
    bot.run(settings["Bot_Token"])
