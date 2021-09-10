# Import discord.py and its extensions.
# https://github.com/Rapptz/discord.py
# https://discordpy.readthedocs.io/en/stable/
import discord
from discord.ext import commands
from discord.ext import tasks




# Used as a trick to keep the bot running on https://replit.com/
import keep_alive




# Import Discord-interactions and its extensions.
# https://github.com/goverfl0w/discord-interactions/
# https://discord-interactions.readthedocs.io/en/latest/
from discord_slash import SlashCommand
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_components import create_actionrow, wait_for_component, create_button
from discord_slash.utils.manage_commands import create_option



# Miscellaneous libraries.
import json
import os
import random
import sys


# Done in order to import currency functions and the currency cog
from currency.currencyFunctions import *



# Bot token.
token = os.environ['DISCORD_BOT_SECRET']



prefixes = ['cookie ', 'ck ', 'Cookie ', 'Ck ', 'CK ']
intent = discord.Intents.all()
client = commands.Bot(command_prefix=prefixes,
                      case_insensitive=True,
                      intents=intent)


slash = SlashCommand(client, sync_commands = True)



# EVENTS

@client.event
async def on_ready():
    print('ready lol')



# COMMANDS

from discord_slash.context import MenuContext
from discord_slash.model import ContextMenuType
@slash.context_menu(target=ContextMenuType.MESSAGE,
                    name="Balance",
                    guild_ids=[856870048807518218])
async def test(ctx: MenuContext):
    await ctx.send(
        content=f"test {ctx.target_message.content}",
        hidden=True
    )




for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')




keep_alive.keep_alive()

client.run(token)