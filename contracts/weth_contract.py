from web3 import Web3
import contracts.doe_token_abi as doe_token_abi

address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'

def get_main_balance(w3, wallet):
    contract = w3.eth.contract(address=address, abi=doe_token_abi.get_abi())
    balanceOf = contract.functions.balanceOf(wallet).call()
    return Web3.fromWei(balanceOf, 'ether')
    
