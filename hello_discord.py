import discord
import hidden_details
import web3 as Web3
import json
import contracts.doe_token_abi as doe_token_abi
import contracts.eth_usdc_abi as eth_usdc_abi
import contracts.eth_usdc as eth_usdc

intents = discord.Intents.default()

client = discord.Client()
address = eth_usdc.address
token0 = eth_usdc.token0
token1 = eth_usdc.token1

@client.event
async def on_ready():
    w3_eth = Web3(Web3.HTTPProvider(hidden_details.eth_mainnet))
    contract = w3_eth.eth.contract(address=address, abi=eth_usdc_abi.get_abi())
    events_filter = contract.events.Swap.createFilter(fromBlock='latest')

    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(hidden_details.TOKEN)
