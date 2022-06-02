from web3 import Web3
import asyncio
import hidden_details
import json
import contracts.doe_token_abi as doe_token_abi
import contracts.usdc_eth_abi as usdc_eth_abi
import contracts.usdc_eth as usdc_eth
import time

address = usdc_eth.address
token0 = usdc_eth.token0
token1 = usdc_eth.token1

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
    
    print(f'Tx: https://etherscan.io/tx/{event_dict["transactionHash"]}')
    print(f'In:  {to_string(amountIn, tokenIn)}')
    print(f'Out: {to_string(amountOut, tokenOut)}')
    exit()

async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            await handle_event(event)
        time.sleep(poll_interval)

def main():
    w3_eth = Web3(Web3.HTTPProvider(hidden_details.eth_mainnet))
    contract = w3_eth.eth.contract(address=address, abi=usdc_eth_abi.get_abi())
    event_filter = contract.events.Swap.createFilter(fromBlock='latest')

    asyncio.run(log_loop(event_filter, 2))
    print("running")
    time.sleep(100)

if __name__ == '__main__':
    main()
