from web3 import Web3
import time
import json
import hidden_details
import contracts.doe_token_abi as doe_token_abi
import contracts.weth_abi as weth_abi
import contracts.weth_contract as weth_contract

def handle_event(event):
    event_dict = json.loads(Web3.toJSON(event))
    print(json.dumps(event_dict, indent=3))
    # exit()

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)

def main():
    w3_eth = Web3(Web3.HTTPProvider(hidden_details.eth_mainnet))
    block_filter = w3_eth.eth.filter('latest')
    contract_address = weth_contract.address
    contract = w3_eth.eth.contract(address=weth_contract.address, abi=weth_abi.get_abi())
    events_filter = contract.events.Swap.createFilter(fromBlock='latest') # 14787280
    log_loop(events_filter, 2)

if __name__ == '__main__':
    main()
