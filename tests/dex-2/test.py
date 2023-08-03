from web3 import Web3
from scripts.dex2_helper import *

def test_setup():
    # providers instance
    w3 = Web3(Web3.HTTPProvider())
    # Set the liquidity add operation deadline
    deadline = w3.eth.get_block(w3.eth.block_number)['timestamp'] + 10000
    # setting some richy balances for users
    w3.provider.make_request("evm_setAccountBalance", [liquidityAdder.address, INITIAL_BALANCE ])
    w3.provider.make_request("evm_setAccountBalance", [user.address, INITIAL_BALANCE ])
    #Asserting new balances
    assert(liquidityAdder.balance() == INITIAL_BALANCE)
    assert(user.balance() == INITIAL_BALANCE)

    # Deposit to WETH & approve router to spend tokens
    weth.deposit({'from':liquidityAdder, 'value': ETH_IN_LIQUIDITY})
    weth.approve(UNISWAPV2_ROUTER_ADDRESS, ETH_IN_LIQUIDITY, {'from':liquidityAdder})

    preciousToken.approve(UNISWAPV2_ROUTER_ADDRESS, INITIAL_LIQUIDITY, {'from':liquidityAdder})
    uniswapRouter.addLiquidity(
        preciousToken.address,
        weth.address,
        INITIAL_LIQUIDITY,
        ETH_IN_LIQUIDITY,
        INITIAL_LIQUIDITY,
        ETH_IN_LIQUIDITY,
        liquidityAdder.address,
        deadline,
        {
        'from': liquidityAdder
        }
    )

def test_sniper():
    assert(sniper.address != 0)

    ethToInvest = Wei('35 ether')
    minAbsoluteAmoutOut = Wei('1750 ether')
    assert(user.balance() == INITIAL_BALANCE)

    weth.deposit({'from': user,'value': ethToInvest})
    weth.transfer(sniper.address, ethToInvest, {'from': user})

    sniper.snipe(
        weth.address, 
        preciousToken.address,
        ethToInvest,
        minAbsoluteAmoutOut,
        3
    )

def test_outcome():
    preciousBalance = preciousToken.balanceOf(user.address)
    print(yellow,"\rPrecious balance:",red,preciousBalance,normal)
    assert(preciousBalance > Wei('4000 ether'))
