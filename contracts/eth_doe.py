from web3 import Web3
import contracts.eth_doe_abi as abi

address = "0x9d9681d71142049594020bD863D34D9F48d9DF58"
token0 = "eth"
token1 = "doe"

def get_main_balance(w3, wallet):
    contract = w3.eth.contract(address=address, abi=abi.get_abi())
    balanceOf = contract.functions.balanceOf(wallet).call()
    return Web3.fromWei(balanceOf, 'ether')
    
