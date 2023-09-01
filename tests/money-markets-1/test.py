from web3 import Web3
from scripts.aave_helper import *

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


def test_deposit_USDC():

    usdc.approve(aaveUser, AMOUNT_TO_DEPOSIT, {'from': user})
    aaveUser.depositUSDC(AMOUNT_TO_DEPOSIT, {'from': user})

    aUSDC.balanceOf(aaveUser)

    assert(aaveUser.depositedAmount() == AMOUNT_TO_DEPOSIT)
    assert(aUSDC.balanceOf(aaveUser.address) == AMOUNT_TO_DEPOSIT)

def test_borrow_DAI():

    aaveUser.borrowDAI(AMOUNT_TO_BORROW, {'from': user})
    assert(aaveUser.borrowedAmount() == AMOUNT_TO_BORROW)
    assert(dai.balanceOf(user) == AMOUNT_TO_BORROW)
    assert(debtDAI.balanceOf(aaveUser) == AMOUNT_TO_BORROW)


def test_repay_DAI():

    dai.approve(aaveUser, AMOUNT_TO_BORROW, {'from': user})
    aaveUser.repayDAI(AMOUNT_TO_BORROW, {'from': user})
    assert(aaveUser.borrowedAmount() == 0)
    assert(dai.balanceOf(user) == 0)
    assert(debtDAI.balanceOf(aaveUser) < AMOUNT_TO_BORROW*1//1000)
    print("Not yet")

def test_withdraw_DAI():

    aaveUser.withdrawUSDC(AMOUNT_TO_DEPOSIT, {'from': user})
    assert(aaveUser.depositedAmount() == 0)
    assert(usdc.balanceOf(user) == USER_USDC_BALANCE)
    assert(aUSDC.balanceOf(aaveUser) < AMOUNT_TO_DEPOSIT*1//1000)
