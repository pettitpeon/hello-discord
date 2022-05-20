from web3 import Web3
import contracts.usdc_doe_abi as abi

address = "0xa626EB9cC7Dec00703586414d0811E1ba2021443"
token0 = "usdc"
token1 = "doe"

def get_main_balance(w3, wallet):
    contract = w3.eth.contract(address=address, abi=abi.get_abi())
    balanceOf = contract.functions.balanceOf(wallet).call()
    return Web3.fromWei(balanceOf, 'ether')
    
