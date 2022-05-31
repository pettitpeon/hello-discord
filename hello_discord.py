from asyncio.windows_events import NULL
import discord
import hidden_details
from web3 import Web3
import asyncio
import json
import time
import contracts.doe_token_abi as doe_token_abi
import contracts.eth_usdc_abi as eth_usdc_abi
import contracts.eth_usdc as eth_usdc

intents = discord.Intents.default()
client = discord.Client()

address = eth_usdc.address
token0 = eth_usdc.token0
token1 = eth_usdc.token1
channel = NULL
channel_name = "test-bot"

def get_channel(channels, name):
    for c in channels:
        if c.name == name:
            return c
    return NULL

@client.event
async def on_ready():
    global channel
    print(f'We have logged in as {client.user}')
    channel = get_channel(client.get_all_channels(), channel_name)
    w3_eth = Web3(Web3.HTTPProvider(hidden_details.eth_mainnet))
    contract = w3_eth.eth.contract(address=address, abi=eth_usdc_abi.get_abi())
    event_filter = contract.events.Swap.createFilter(fromBlock='latest')
    asyncio.create_task(log_loop(event_filter, 2))
    print(f'Swap event loop started')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        msg = await message.channel.send('Hello!')
        await msg.delete()

def to_string(amount, token):
    value = Web3.fromWei(amount, token['unit'])
    return f'{value:,.4f} {token["tracker"]}'

async def handle_event(event):
    event_dict = json.loads(Web3.toJSON(event))
    amountIn = event.args.amount0In
    tokenIn = token0
    amountOut = event.args.amount1Out
    tokenOut = token1
    if amountIn == 0:
        amountIn = event.args.amount1In
        tokenIn = token1
        amountOut = event.args.amount0Out
        tokenOut = token0
    
    message = f'Tx: [{event_dict["transactionHash"][0:8]}](https://etherscan.io/tx/{event_dict["transactionHash"]})\n'
    message = message + f'In:  {to_string(amountIn, tokenIn)}\n'
    message = message + f'Out: {to_string(amountOut, tokenOut)}\n'
    print(message)
    # embed = discord.Embed()
    # embed.description = message
    # msg = await channel.send(embed=embed, delete_after=1)

async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            await handle_event(event)
        time.sleep(poll_interval)


client.run(hidden_details.TOKEN)
