from currency.currencyFunctions import *

import discord

import asyncio.exceptions

from discord.ext import commands

# Import various objects from discord-interactions.
# https://github.com/goverfl0w/discord-interactions/
# https://discord-interactions.readthedocs.io/en/latest/
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow, wait_for_component, create_button
from discord_slash.utils.manage_commands import create_option, create_choice, get_all_commands, remove_slash_command, remove_all_commands
from discord_slash.cog_ext import cog_slash

class Currency(commands.Cog):

    def __init__(self, client):
        self.client = client
    @commands.command(
        name = 'shop',
        help = 'Shop where you can buy things.'
    )
    async def shop(self, ctx, page = 1, item = ''):
        userId = ctx.message.author.id
        await create_user(userId)
        shop = await fetch_shop(page = page, item = item)
        em = discord.Embed(title = 'Cookie Clicker Shop', color = discord.Colour.blue())
        em.set_footer(text = f'page {page} of {len(list((await fetch_shop())[0].keys()))}')

        for name, data in shop.items():
            price = data['price']
            description = data['description']
            em.add_field(name = f'{name}: ${price}', value = description)
        await ctx.send(embed = em)


    @commands.command(
        name = 'balance',
        aliases = ['bal'],
        help = 'Sends current balance and net worth.'
    )
    async def balance(self, ctx, target = None):
        if not target:
            target = ctx.author
        else:
            target = await self.client.fetch_user(int(''.join([letter for letter in target if letter.isdigit()])))
        await create_user(target.id)

        wallet = await fetch_wallet(target.id)
        networth = await fetch_networth(target.id)

        em = discord.Embed(title = f"{target.name}'s balance", colour = discord.Colour.gold())
        em.add_field(name = 'Wallet', value = f'${wallet}', inline = False)
        em.add_field(name = 'Net Worth', value = f'${networth}', inline = False)
        await ctx.send(embed = em)












    @commands.command(
        name = 'clicker',
        aliases = ['click'],
        help = 'Actual cookie clicker.'
    )
    async def clicker(self, ctx):
        user_id = ctx.author.id
        await create_user(user_id)
        wallet = await fetch_wallet(user_id)
        multiplier = await fetch_multiplier(user_id)
        action_row = [
            create_actionrow(
                create_button(style = ButtonStyle.green, label = f'${multiplier}', custom_id = 'ClickerButton'))
                ]
        
        em = discord.Embed(title = f'CURRENT MONEY IN WALLET: ${wallet}', color = discord.Colour.green())
        em.set_footer(text = '*After 10 minutes of not clicking the button will stop working.')

        await ctx.send(embed = em, components = action_row)
        while True:
            button_ctx: ComponentContext = await wait_for_component(self.client, components = action_row, check = check, timeout = 600)
            wallet = await add_money(user_id = user_id, amount = 1)
            em.title = f'CURRENT MONEY IN WALLET: ${wallet}'
            await button_ctx.edit_origin(embed = em)












    @commands.command(
        name = 'gamble',
        aliases = ['bet'],
        help = 'Gamble a certain amount of money.'
    )
    async def gamble(self, ctx, amount):
        userId = ctx.author.id
        await create_user(userId)
        wallet = await fetch_wallet(userId)

        if amount > wallet:
            await ctx.send('Amount gambled is more than current amount in wallet.')
            return
        elif amount <= 4:
            await ctx.send('You must gamble $5 or more.')
            return
        
        user_dice = random.randint(1, 6)
        bot_dice = random.randint(1, 6)
        em = discord.Embed()
        if user_dice > bot_dice:
            em.title = f'{ctx.author.name} won bet!'
            em.add_field(name = 'Your dice:', value = user_dice)
            em.add_field(name = "Bot's dice:", value = bot_dice)
            em.color = discord.Colour.green()
            amount_won = amount
            em.add_field(name = "Amount won:", value = f'${abs(amount_won)}')

        elif user_dice == bot_dice:
            em.title = f'{ctx.author.name} tied bet!'
            em.add_field(name = 'Your dice:', value = user_dice)
            em.add_field(name = "Bot's dice:", value = bot_dice)
            em.color = discord.Colour.gold()
            amount_won = 0
        
        elif user_dice < bot_dice:
            em.title = f'{ctx.author.name} lost bet!'
            em.add_field(name = 'Your dice:', value = user_dice)
            em.add_field(name = "Bot's dice:", value = bot_dice)
            em.color = discord.Colour.red()
            amount_won = -amount
            em.add_field(name = "Amount lost:", value = f'${abs(amount_won)}')
        
        await ctx.send(embed = em)
        await add_money(user_id = userId, amount = amount_won)












    @commands.command(
        name = 'slots',
        help = 'Gamble a certain amount of money in slots.'
    )
    async def slots(self, ctx, amount):
        userId = ctx.author.id
        await create_user(userId)
        wallet = await fetch_wallet(userId)

        if amount > wallet:
            await ctx.send('Amount gambled is more than current amount in wallet.')
            return
        elif amount <= 4:
            await ctx.send('You must gamble $5 or more.')
            return
        

        options = {
            ':fortune_cookie:': 10,
            ':cookie:': 8, 
            ':peach:': 6,
            ':blueberries:': 4,
            ':cherries:': 2,
            ':strawberry:': 1.5
            }
        slots = [random.choice(list(options.keys())) for iterator in range(3)]
        emoji = slots[0]
        mult = options[emoji]
        em = discord.Embed()
        
        if (emoji == slots[1] and emoji == slots[2]):
            amount_won = round(amount * mult)
            em.title = f'{ctx.author.name} won bet!'
            em.add_field(name = 'Amount won:', value = f'${amount_won}')
            em.color = discord.Colour.green()
        else:
            amount_won = -(amount)
            em.title = f'{ctx.author.name} lost bet!'
            em.add_field(name = 'Amount lost:', value = f'${amount}')
            em.color = discord.Colour.red()

        em.description = str(slots)[1:-1]
        await ctx.send(embed = em)
        await add_money(userId, amount_won)
    
    @commands.command(
        name = 'give',
        help = 'Give money to someone else'
    )
    async def give(self, ctx, user: str, amount: int):
        target = await self.client.fetch_user(int(''.join([letter for letter in user if letter.isdigit()])))
        userId = target.id
        authorId = ctx.author.id
        await create_user(userId)
        await create_user(authorId)
        wallet = await fetch_wallet(authorId)

        if amount > wallet:
            await ctx.send('Amount given is more than current amount in wallet.')
            return
        elif amount < 1:
            await ctx.send('You must give $1 or more.')
            return
        
        await add_money(authorId, -amount)
        await add_money(userId, amount)
        await ctx.send(f'{ctx.author.name} has succesfully given {target.name} {amount} money.')
    

    @cog_slash(
        name = 'clicker',
        description = 'Actual cookie clicker.',
        options = [
            create_option(
                name = 'hide',
                description = 'Whether to hide the message from other users or not.',
                option_type = 5,
                required = False
            )
        ]
    )
    async def _clicker(self, ctx, hide = True):
        user_id = ctx.author.id
        await create_user(user_id)
        wallet = await fetch_wallet(user_id)
        networth = await fetch_networth(user_id)
        multiplier = await fetch_multiplier(user_id)
        action_row = [
            create_actionrow(
                create_button(style = ButtonStyle.green, label = f'${multiplier}', custom_id = 'ClickerButton'))
                ]
        
        em = discord.Embed(title = f'CURRENT MONEY IN WALLET: ${wallet}', color = discord.Colour.green())
        em.set_footer(text = '*After 10 minutes of not clicking the button will stop working.')

        msg = await ctx.send(embed = em, components = action_row, hidden = hide)
        def check(m):
                return m.author == ctx.author
        while True:
            try:
                button_ctx: ComponentContext = await wait_for_component(self.client, components = action_row, timeout = 5, check = check)
            except asyncio.exceptions.TimeoutError:
                msg['components'] = []
                
                return
            wallet = await add_money(user_id = user_id, amount = 1)
            em.title = f'CURRENT MONEY IN WALLET: ${wallet}'
            await button_ctx.edit_origin(embed = em)
def setup(client):
    client.add_cog(Currency(client))