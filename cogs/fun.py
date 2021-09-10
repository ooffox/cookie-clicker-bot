import discord

from asyncio import sleep as asleep
import asyncio.exceptions

from discord.ext import commands

from random import uniform, randint, choice

from time import time

# Import various objects from discord-interactions.
# https://github.com/goverfl0w/discord-interactions/
# https://discord-interactions.readthedocs.io/en/latest/
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow, wait_for_component, create_button
from discord_slash.utils.manage_commands import create_option, create_choice, get_all_commands, remove_slash_command, remove_all_commands
from discord_slash.cog_ext import cog_slash

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(
        name = 'duel1',
        aliases = ['challenge1'],
        help = 'Challenge someone to a duel.',
        description = 'Challenge to someone to a duel. The duel consists in the bot sending a message and then adding a button after a couple seconds where the first person to press it wins.'
    )
    async def duel1(self, ctx, user: discord.User):
        actionrow = [
                create_actionrow(
                    create_button(
                        style = ButtonStyle.green, label = 'Click!'
                    )
                )]
        msg = await ctx.send('Get ready in 3...')
        await asleep(uniform(1.0, 3.0))
        await msg.edit(content = f'{msg.content} 2...')
        await asleep(uniform(0.7, 2.0))
        await msg.edit(content = f'{msg.content} 1...')
        await asleep(uniform(0.2, 1.0))
        await msg.edit(
            content = f'{msg.content} Go!',
            components = actionrow)
        def check(m):
            return m.author == ctx.author or  m.author == user
        try:
            seconds = time()
            button_ctx: ComponentContext = await wait_for_component(self. client, components = actionrow, timeout = 10, check = check)
        except asyncio.exceptions.TimeoutError:
            await msg.edit(
                components = [
                create_actionrow(
                    create_button(
                        style = ButtonStyle.red, label = 'Too late!'
                    )
                )]
            )
        await button_ctx.edit_origin(content = f'{msg.content}\n\n {button_ctx.author} answered first in {round(abs(seconds - time()), 2)} seconds!')
        


    @commands.command(
        name = 'duel2',
        aliases = ['challenge2'],
        help = 'Challenge someone to a duel.',
        description = 'Challenge to someone to a duel. The duel consists in the bot sending a message with a letter and then adding a bunch of buttons with individual letters on them, and then the first person to press the correct button wins.'
    )
    async def duel2(self, ctx, user: discord.User):
        letters = ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'J', 'K', 'M', 'N', 'L', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = [str(num) for num in range(1, 100)]
        chosen_labels = [(choice(letters) + choice(numbers)) for i in range(9)]
        good_label = choice(chosen_labels)
        actionrow = [
                create_actionrow(
                    create_button(
                        style = ButtonStyle.green, label = chosen_labels[0]),
                    create_button(
                        style = ButtonStyle.blurple, label = chosen_labels[1]),
                    create_button(
                        style = ButtonStyle.green, label = chosen_labels[2]),
                ),
                create_actionrow(
                    create_button(
                        style = ButtonStyle.blurple, label = chosen_labels[3]),
                    create_button(
                        style = ButtonStyle.gray, label = chosen_labels[4]),
                    create_button(
                        style = ButtonStyle.blurple, label = chosen_labels[5])
                ),
                create_actionrow(
                    create_button(
                        style = ButtonStyle.red, label = chosen_labels[6]),
                    create_button(
                        style = ButtonStyle.blurple, label = chosen_labels[7]),
                    create_button(
                        style = ButtonStyle.red, label = chosen_labels[8])
                    )
                ]
        msg = await ctx.send('Get ready in 3...')
        await asleep(uniform(1.0, 3.0))
        await msg.edit(content = f'{msg.content} 2...')
        await asleep(uniform(0.7, 2.0))
        await msg.edit(content = f'{msg.content} 1...')
        await asleep(uniform(0.2, 1.0))
        await msg.edit(
            content = f'{msg.content} Go! **__{good_label}__**',
            components = actionrow)
        def check(m):
            return m.author == ctx.author or  m.author == user
        try:
            seconds = time()
            button_ctx: ComponentContext = await wait_for_component(self. client, components = actionrow, timeout = 10, check = check)
        except asyncio.exceptions.TimeoutError:
            await msg.edit(
                components = [
                create_actionrow(
                    create_button(
                        style = ButtonStyle.red, label = 'Too late!'
                    )
                )]
            )
        
        if button_ctx.component['label'] == good_label:
            await button_ctx.edit_origin(content = f'{msg.content}\n\n {button_ctx.author} answered first in {round(abs(seconds - time()), 2)} seconds!', components = [])
        else:
            user_lost = ctx.author if button_ctx.author == ctx.author else user
            user_won = ctx.author if button_ctx.author != ctx.author else user
            await button_ctx.edit_origin(content = f'{msg.content}\n\n {user_lost} answered wrong and handed the victory to {user_won}!', components = [])
        

        
        
def setup(client):
    client.add_cog(Fun(client))