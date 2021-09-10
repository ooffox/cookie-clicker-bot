import json

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





async def fetch_shop(page = None, item = None, user_id = ''):
    user_id = str(user_id)
    with open('currency/shop.json', 'r') as file:
        shop = json.load(file)
    
    if (not page) and (not user_id):
        return shop
    
    elif (user_id):
        return shop[1][user_id]
    
    elif (page) and (not item):
        return shop[0][str(page)]
    
    elif (page) and (item):
        return shop[0][str(page)][item]





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





async def change_shop(user_id, amount: int):
    user_id = str(user_id)
    shop = await fetch_shop(user_id)
    shop[user_id] = amount
    with open('currency/multiplier.json', 'w') as file:
        json.dump(shop, file)
    return shop





async def add_money(user_id, amount: int):
    wallet = await fetch_wallet(user_id)
    await change_wallet(user_id, wallet + amount)
    if amount > 0:
        await change_networth(user_id, wallet + amount)
    return wallet + amount





async def create_user(user_id: str):
    user_id = str(user_id)
    wallet = await fetch_wallet()
    networth = await fetch_networth()
    multiplier = await fetch_multiplier()
    shop = await fetch_shop()

    wallet[user_id] = 0 if user_id not in wallet.keys() else wallet[user_id]
    networth[user_id] = 0 if user_id not in networth.keys() else networth[user_id]
    multiplier[user_id] = 1 if user_id not in multiplier.keys() else multiplier[user_id]
    shop[1][user_id] = {} if user_id not in shop[1].keys() else shop[1][user_id]

    json.dump(wallet, open('currency/wallet.json', 'w'))
    json.dump(networth, open('currency/networth.json', 'w'))
    json.dump(multiplier, open('currency/multiplier.json', 'w'))
    json.dump(shop, open('currency/shop.json', 'w'))