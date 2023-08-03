from web3 import Web3
from scripts.flashL_helper import *
from time import sleep

def test_setup():
    # providers instance
    w3 = Web3(Web3.HTTPProvider())
    # setting balances for test
    w3.provider.make_request("evm_setAccountBalance", [user.address, "0x1BC16D674EC80000" ])
    w3.provider.make_request("evm_setAccountBalance", [whaleSigner.address, "0x1BC16D674EC80000" ])
    #Transfer USDC to the user
    usdc.transfer(flash_loan.address, FEE_AMOUNT, {'from': whaleSigner, "gas_price": '30 gwei'})

    #assert(usdc.balanceOf(user) == BORROW_AMOUNT)

def test_deployment():
    assert(flash_loan != 0)

def test_flashL():
    flash_loan.getFlashLoan(USDC,BORROW_AMOUNT, {"gas_price": '30 gwei'})
    sleep(2)
    

