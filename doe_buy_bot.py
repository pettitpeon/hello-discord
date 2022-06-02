import discord
from web3 import Web3
import asyncio
import json
import time
import contracts.usdc_doe as usdc_doe
import contracts.usdc_doe_abi as usdc_doe_abi
import contracts.eth_doe as eth_doe
import contracts.eth_doe_abi as eth_doe_abi

# For testing with other contracts
# Change the swap[] list with these
import contracts.usdc_eth as usdc_eth
import contracts.usdc_eth_abi as usdc_eth_abi
import contracts.eth_usdt as eth_usdt
import contracts.eth_usdt_abi as eth_usdt_abi

######## Details required from the user
import hidden_details
discord_token = hidden_details.TOKEN
eth_node_url = hidden_details.eth_mainnet # eg: https://mainnet.infura.io/v3/{infura_key}
discord_channel_id = 978368981951987797
######## Details required from the user

swap = [{}, {}]
swap[0]['abi'] = usdc_doe_abi.get_abi()
swap[0]['addr'] = usdc_doe.address
swap[0]['tokens'] = [usdc_doe.token0, usdc_doe.token1]
swap[0]['buyT'] = 0

swap[1]['abi'] = eth_doe_abi.get_abi()
swap[1]['addr'] = eth_doe.address
swap[1]['tokens'] = [eth_doe.token0, eth_doe.token1]
swap[1]['buyT'] = 1

channel = None
intents = discord.Intents.default()
client = discord.Client()

def get_swap_filters():
    w3_eth = Web3(Web3.HTTPProvider(eth_node_url))
    print(f'W3 connected: {w3_eth.isConnected()}')
    contract = w3_eth.eth.contract(address=swap[0]['addr'], abi=swap[0]['abi'])
    swap_filter0 = contract.events.Swap.createFilter(fromBlock='latest')
    contract = w3_eth.eth.contract(address=swap[1]['addr'], abi=swap[1]['abi'])
    swap_filter1 = contract.events.Swap.createFilter(fromBlock='latest')
    return [swap_filter0, swap_filter1]

@client.event
async def on_ready():
    global channel
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(discord_channel_id)
    print(f'Channel: {channel}')
    asyncio.create_task(event_loop(get_swap_filters(), 2))
    print(f'Swap event loop started')

def to_string(amount, token):
    value = Web3.fromWei(amount, token['unit'])
    return f'{value:,.4f} {token["tracker"]}'

async def handle_event(event, swap):
    # Check buy
    amnt_in = event.args.amount1In
    amnt_out = event.args.amount0Out
    tok_in = 1
    if swap['buyT'] == 0:
         if event.args.amount0Out == 0:
             return
    else:
        if event.args.amount1Out == 0:
             return
        amnt_in = event.args.amount0In
        amnt_out = event.args.amount1Out
        tok_in = 0
    
    event_dict = json.loads(Web3.toJSON(event))
    message = f'Tx: [{event_dict["transactionHash"][0:8]}](https://etherscan.io/tx/{event_dict["transactionHash"]})\n'
    message = message + f'In:  {to_string(amnt_in, swap["tokens"][tok_in])}\n'
    message = message + f'Out: {to_string(amnt_out, swap["tokens"][swap["buyT"]])}\n'
    print(message) # Debug message

    embed = discord.Embed()
    embed.description = message
    await channel.send(embed=embed)

async def event_loop(swap_filter, poll_interval):
    while True:
        for i in range(len(swap_filter)):
            for event in swap_filter[i].get_new_entries():
                await handle_event(event, swap[i])
        time.sleep(poll_interval)

client.run(discord_token)
