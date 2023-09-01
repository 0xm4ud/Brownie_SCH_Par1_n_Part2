from web3 import Web3
from scripts.compound_helper import *

def test_setup():
    # providers instance
    w3 = Web3(Web3.HTTPProvider())
    # setting balances for test
    w3.provider.make_request("evm_setAccountBalance", [user.address, "0x1BC16D674EC80000" ])
    w3.provider.make_request("evm_setAccountBalance", [whaleSigner.address, "0x1BC16D674EC80000" ])
    #Transfer USDC to the user
    usdc.transfer(user.address, USER_USDC_BALANCE, {'from': whaleSigner})
    #Burn DAI balance form the user (somehow this signer has DAI on mainnet lol)
    dai.transfer("0x000000000000000000000000000000000000dEaD", dai.balanceOf(user.address), {'from': user})

    assert(usdc.balanceOf(user) == USER_USDC_BALANCE)
    assert(dai.balanceOf(user) == 0)

def test_deployment():
    assert(compUser != 0)

def test_deposit():
    usdc.approve(compUser, AMOUNT_TO_DEPOSIT, {'from': user})
    compUser.deposit(AMOUNT_TO_DEPOSIT)
    assert(compUser.depositedAmount() != 0)
    cUSDCBalanceBefore = cUSDC.balanceOf(compUser)
    assert(cUSDCBalanceBefore > 0)

def test_borrow():
    compUser.allowUSDCAsCollateral()
    compUser.borrow(AMOUNT_TO_BORROW)
    assert(compUser.borrowedAmount() != 0)
    assert(dai.balanceOf(user) == AMOUNT_TO_BORROW)

def test_repay():
    dai.approve(compUser.address, AMOUNT_TO_BORROW, {'from': user})
    compUser.repay(AMOUNT_TO_BORROW)
    assert(compUser.borrowedAmount() == 0)
    assert(dai.balanceOf(user) == 0)

def test_withdraw():
    compUser.withdraw(AMOUNT_TO_DEPOSIT)
    assert(compUser.depositedAmount() == 0)
    assert(usdc.balanceOf(user) == USER_USDC_BALANCE)
    currentCusdcBalance = cUSDC.balanceOf(compUser.address)
    assert(currentCusdcBalance < AMOUNT_TO_DEPOSIT*1//1000)