from web3 import Web3
from scripts.flash3_helper import *
from time import sleep
from brownie.network.rpc import hardhat
from brownie.network.rpc import ganache
import subprocess
import threading

def test_setup():
    # providers instance
    print("network at",network.show_active())

    ##getConsoleLog()
    w3 = Web3(Web3.HTTPProvider())
    # setting balances for test
    w3.provider.make_request("evm_setAccountBalance", [user.address, "0x1BC16D674EC80000" ])
    w3.provider.make_request("evm_setAccountBalance", [whaleSigner.address, "0x1BC16D674EC80000" ])
    #Transfer USDC to the user
    usdc.transfer(flash_swap.address, FEE_AMOUNT, {'from': whaleSigner, "gas_price": '30 gwei'})
    #usdc.transfer(user.address, usdc.balanceOf(whaleSigner), {'from': whaleSigner, "gas_price": '30 gwei'})
    #assert(usdc.balanceOf(user) == BORROW_AMOUNT)

def test_deployment():
    assert(flash_swap != 0)

def test_flash_swap():
    from brownie.utils import console
    # Create a thread for the logger and start it"""
    ##logger_thread = threading.Thread(target=console.getConsoleLog, args=[102],daemon=True)
    #newnew.getConsoleLog()
    ####logger_thread.start()
    #haha.logger()
    console.log(15, duration=30)
    usdc.approve(flash_swap.address,BORROW_AMOUNT, {'from': whaleSigner,"gas_price": '25 gwei'})
    flash_swap.executeFlashSwap(USDC,BORROW_AMOUNT, {'from': whaleSigner,"gas_price": '30 gwei'})
    #logger_thread.join()
    print("HERE BE DRAGONS!!!")
    
