from web3 import Web3
import time
import json
import hidden_details
import contracts.doe_token_abi as doe_token_abi
import contracts.eth_usdc_abi as eth_usdc_abi
import contracts.eth_usdc as eth_usdc

def handle_event(event):
    event_dict = json.loads(Web3.toJSON(event))
    print(json.dumps(event_dict, indent=3))
    print(f'Tx: {event_dict["transactionHash"]}')
    Web3.fromWei(event.args.amount0In, 'ether')
    print(f'In {eth_usdc.token0["tracker"]}  : {Web3.fromWei(event.args.amount0In,  eth_usdc.token0["unit"])}')
    print(f'In {eth_usdc.token1["tracker"]} : {Web3.fromWei(event.args.amount1In,  eth_usdc.token1["unit"])}')
    print(f'Out {eth_usdc.token0["tracker"]} : {Web3.fromWei(event.args.amount0Out,  eth_usdc.token0["unit"])}')
    print(f'Out {eth_usdc.token1["tracker"]}: {Web3.fromWei(event.args.amount1Out, eth_usdc.token1["unit"])}')
    # exit()

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)

def main():
    w3_eth = Web3(Web3.HTTPProvider(hidden_details.eth_mainnet))
    block_filter = w3_eth.eth.filter('latest')
    contract_address = eth_usdc.address
    contract = w3_eth.eth.contract(address=eth_usdc.address, abi=eth_usdc_abi.get_abi())
    events_filter = contract.events.Swap.createFilter(fromBlock='latest') # 14787280
    log_loop(events_filter, 2)

if __name__ == '__main__':
    main()
