# Import discord.py and its extensions.
# https://github.com/Rapptz/discord.py
# https://discordpy.readthedocs.io/en/stable/
import discord
from discord.ext import commands
from discord.ext import tasks



# Import various objects from discord-interactions.
# https://github.com/goverfl0w/discord-interactions/
# https://discord-interactions.readthedocs.io/en/latest/
from discord_slash import SlashCommand
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow, wait_for_component, create_button
from discord_slash.utils.manage_commands import create_option, create_choice, get_all_commands, remove_slash_command, remove_all_commands


# Used as a trick to keep the bot running on https://replit.com/
import keep_alive


# Miscellaneous libraries.
import json
import os
import random



# Bot token.
token = os.environ['DISCORD_BOT_SECRET']



prefixes = ['cookie ', 'ck ', 'Cookie ', 'Ck ', 'CK ']
intent = discord.Intents.all()
client = commands.Bot(command_prefix=prefixes,
                      case_insensitive=True,
                      intents=intent)


slash = SlashCommand(client, sync_commands=True)



# EVENTS

@client.event
async def on_ready():
    print('ready lol')
    commands = await get_all_commands(bot_id = 882373466618212514, bot_token = token, guild_id = None)


# FUNCTIONS

async def fetch_wallet(user_id = ''):
    user_id = str(user_id)
    with open('currency/wallet.json', 'r') as file:
        wallet = json.load(file)
    
    if not user_id:
        return wallet
    else:
        return wallet[user_id]

async def fetch_networth(user_id = ''):
    user_id = str(user_id)
    with open('currency/networth.json', 'r') as file:
        networth = json.load(file)
    
    if not user_id:
        return networth
    else:
        return networth[user_id]

async def fetch_multiplier(user_id = ''):
    user_id = str(user_id)
    with open('currency/multiplier.json', 'r') as file:
        multiplier = json.load(file)
    
    if not user_id:
        return multiplier
    else:
        return multiplier[user_id]

async def change_wallet(user_id, amount: int):
    user_id = str(user_id)
    wallet = await fetch_wallet()
    wallet[user_id] = amount
    with open('currency/wallet.json', 'w') as file:
        json.dump(wallet, file)
    return amount

async def change_networth(user_id, amount: int):
    user_id = str(user_id)
    networth = await fetch_networth()
    networth[user_id] = amount
    with open('currency/networth.json', 'w') as file:
        json.dump(networth, file)
    return amount

async def change_multiplier(user_id, amount: int):
    user_id = str(user_id)
    multiplier = await fetch_multiplier()
    multiplier[user_id] = amount
    with open('currency/multiplier.json', 'w') as file:
        json.dump(multiplier, file)
    return amount

async def add_money(user_id, amount: int):
    wallet = await fetch_wallet(user_id)
    networth = await fetch_networth(user_id)
    await change_wallet(user_id, wallet + amount)
    if amount > 0:
        await change_networth(user_id, wallet + amount)
    return wallet + amount

async def create_user(user_id: str):
    user_id = str(user_id)
    wallet = await fetch_wallet()
    networth = await fetch_networth()
    multiplier = await fetch_multiplier()

    wallet[user_id] = 0 if user_id not in wallet.keys() else wallet[user_id]
    networth[user_id] = 0 if user_id not in networth.keys() else networth[user_id]
    multiplier[user_id] = 1 if user_id not in multiplier.keys() else multiplier[user_id]

    json.dump(wallet, open('currency/wallet.json', 'w'))
    json.dump(networth, open('currency/networth.json', 'w'))
    json.dump(multiplier, open('currency/multiplier.json', 'w'))



# COMMANDS

@slash.slash(
    name = 'ping',
    description = 'Sends current bot latency in milliseconds.'
)
async def bot_latency(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms.")



@slash.subcommand(
    base = 'cookie',
    name = 'balance', 
    description = 'Sends current balance and net worth.',
    options = [
        create_option(
            name = "target",
            description = "User of which to fetch the balance. Author by default.",
            option_type = 6,
            required = False
            ),
        create_option(
            name = "hide",
            description = "Whether or not to hide the message from others. Disabled by default.",
            option_type = 5,
            required = False
            )]
        )
async def balance(ctx, target = None, hide = False):
    if not target:
        target = ctx.author
    await create_user(target.id)

    wallet = await fetch_wallet(target.id)
    networth = await fetch_networth(target.id)

    em = discord.Embed(title = f"{target.name}'s balance", colour = discord.Colour.blurple())
    em.add_field(name = 'Wallet', value = f'{wallet}$', inline = False)
    em.add_field(name = 'Net Worth', value = f'{networth}$', inline = False)
    await ctx.send(embed = em, hidden = hide)
    
@slash.subcommand(
    base = 'cookie',
    name = 'clicker', 
    description = 'Actual cookie clicker.',
    options = [
        create_option(
            name = "hide",
            description = "Whether to hide the message or not. True by default. Dont change it if unsure.",
            option_type = 5,
            required = False)
    ])
async def CookieClicker(ctx, hide = True):
    user_id = ctx.author.id
    await create_user(user_id)
    wallet = await fetch_wallet(user_id)
    networth = await fetch_networth(user_id)
    multiplier = await fetch_multiplier(user_id)
    action_row = [
        create_actionrow(
            create_button(style = ButtonStyle.green, label = f'{multiplier}$', custom_id = 'ClickerButton'))
            ]
    
    em = discord.Embed(title = f'CURRENT MONEY IN WALLET: {wallet}$', color = discord.Colour.green())
    em.set_footer(text = '*After 10 minutes of not clicking the button will stop working.')

    await ctx.send(embed = em, components = action_row, hidden = hide)
    def check(m):
            return m.author == ctx.author
    while True:
        button_ctx: ComponentContext = await wait_for_component(client, components = action_row, timeout = 600, check = check)
        wallet = await add_money(user_id = user_id, amount = 1)
        em.title = f'CURRENT MONEY IN WALLET: {wallet}$'
        await button_ctx.edit_origin(embed = em)

@slash.subcommand(
    base = 'cookie',
    name = 'gamble', 
    description = 'Gamble a certain amount of money.',
    options = [
        create_option(
            name = "amount",
            description = "Amount to gamble.",
            option_type = 4,
            required = True)]
        )
async def CookieGamble(ctx, amount):
    userId = ctx.author.id
    await create_user(userId)
    wallet = await fetch_wallet(userId)

    if amount > wallet:
        await ctx.send('Amount gambled is more than current amount in wallet.', hidden = True)
        return
    elif amount <= 4:
        await ctx.send('You must gamble 5$ or more.', hidden = True)
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
        em.add_field(name = "Amount won:", value = f'{abs(amount_won)}$')

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
        em.add_field(name = "Amount lost:", value = f'{abs(amount_won)}$')
    
    await ctx.send(embed = em)
    await add_money(user_id = userId, amount = amount_won)

@slash.subcommand(
    base = 'cookie',
    name = 'slots',
    description = 'Gamble a certain amount of money in slots.',
    options = [
        create_option(
            name = "amount",
            description = "Amount to gamble.",
            option_type = 4,
            required = True)]
)
async def CookieSlots(ctx, amount):
    userId = ctx.author.id
    await create_user(userId)
    wallet = await fetch_wallet(userId)

    if amount > wallet:
        await ctx.send('Amount gambled is more than current amount in wallet.', hidden = True)
        return
    elif amount <= 4:
        await ctx.send('You must gamble 5$ or more.', hidden = True)
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
        em.add_field(name = 'Amount won:', value = f'{amount_won}$')
        em.color = discord.Colour.green()
    else:
        amount_won = -(amount)
        em.title = f'{ctx.author.name} lost bet!'
        em.add_field(name = 'Amount lost:', value = f'{amount}$')
        em.color = discord.Colour.red()

    em.description = str(slots)[1:-1]
    await ctx.send(embed = em)
    await add_money(userId, amount_won)




@client.command(
    name = 'balance',
    aliases = ['bal'],
    help = 'Sends current balance and net worth.'
)
async def _balance(ctx, target = None):
    if not target:
        target = ctx.author
    await create_user(target.id)

    wallet = await fetch_wallet(target.id)
    networth = await fetch_networth(target.id)

    em = discord.Embed(title = f"{target.name}'s balance", colour = discord.Colour.blurple())
    em.add_field(name = 'Wallet', value = f'{wallet}$', inline = False)
    em.add_field(name = 'Net Worth', value = f'{networth}$', inline = False)
    await ctx.send(embed = em)




@client.command(
    name = 'clicker',
    aliases = ['click'],
    help = 'Actual cookie clicker.'
)
async def _CookieClicker(ctx):
    user_id = ctx.author.id
    await create_user(user_id)
    wallet = await fetch_wallet(user_id)
    multiplier = await fetch_multiplier(user_id)
    action_row = [
        create_actionrow(
            create_button(style = ButtonStyle.green, label = f'{multiplier}$', custom_id = 'ClickerButton'))
            ]
    
    em = discord.Embed(title = f'CURRENT MONEY IN WALLET: {wallet}$', color = discord.Colour.green())
    em.set_footer(text = '*After 10 minutes of not clicking the button will stop working.')

    await ctx.send(embed = em, components = action_row)
    def check(m):
            return m.author == ctx.author
    while True:
        button_ctx: ComponentContext = await wait_for_component(client, components = action_row, timeout = 600, check = check)
        wallet = await add_money(user_id = user_id, amount = 1)
        em.title = f'CURRENT MONEY IN WALLET: {wallet}$'
        await button_ctx.edit_origin(embed = em)




@client.command(
    name = 'gamble',
    aliases = ['bet'],
    help = 'Gamble a certain amount of money in slots.'
)
async def _CookieGamble(ctx, amount):
    userId = ctx.author.id
    await create_user(userId)
    wallet = await fetch_wallet(userId)

    if amount > wallet:
        await ctx.send('Amount gambled is more than current amount in wallet.', hidden = True)
        return
    elif amount <= 4:
        await ctx.send('You must gamble 5$ or more.', hidden = True)
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
        em.add_field(name = "Amount won:", value = f'{abs(amount_won)}$')

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
        em.add_field(name = "Amount lost:", value = f'{abs(amount_won)}$')
    
    await ctx.send(embed = em)
    await add_money(user_id = userId, amount = amount_won)




@client.command(
    name = 'slots',
    help = 'Gamble a certain amount of money in slots.'
)
async def _CookieSlots(ctx, amount):
    userId = ctx.author.id
    await create_user(userId)
    wallet = await fetch_wallet(userId)

    if amount > wallet:
        await ctx.send('Amount gambled is more than current amount in wallet.', hidden = True)
        return
    elif amount <= 4:
        await ctx.send('You must gamble 5$ or more.', hidden = True)
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
        em.add_field(name = 'Amount won:', value = f'{amount_won}$')
        em.color = discord.Colour.green()
    else:
        amount_won = -(amount)
        em.title = f'{ctx.author.name} lost bet!'
        em.add_field(name = 'Amount lost:', value = f'{amount}$')
        em.color = discord.Colour.red()

    em.description = str(slots)[1:-1]
    await ctx.send(embed = em)
    await add_money(userId, amount_won)

keep_alive.keep_alive()

client.run(token)