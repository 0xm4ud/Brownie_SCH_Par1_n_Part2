from scripts.ORACLE2_helper import *
from brownie import reverts
from brownie.convert import to_uint
import brownie


def test_oracle2_borrow():

        # DAI despoit succeded
    assert(dai.balanceOf(lendly.address) == DAI_LIQUIDITY)
    assert(lendly.deposited(dai, impersonatedSigner) == DAI_LIQUIDITY)
    #  Didn't deposit WETH so can't borrow DAI
    with reverts("Not enough collateral"):
        lendly.borrow(dai.address, DAI_LIQUIDITY, {'from': attacker, 'gas_price': '19 gwei'})
    
    # WETH depositor can borrow some DAI
    lendly.borrow(dai.address, Wei('100 ether'), {'from': deployer, 'gas_price': '19 gwei'})

def test_oracle2_exploit():
    attackerContract = AttackLendly.deploy(PAIR_ADDRESS ,lendly.address, {'from': attacker})
    attackerContract.attack({'from': attacker})

    # SUCCESS CONDITIONS 
    # Protocol Liquidity
    print("Lendly DAI balance: ", to_uint(w3.fromWei(dai.balanceOf(lendly.address), 'ether')))
    print("Lendly WETH balance: ", to_uint(w3.fromWei(weth.balanceOf(lendly.address), 'ether')))

    print("Attacker DAI balance: ", to_uint(w3.fromWei(dai.balanceOf(attacker), 'ether')))
    print("Attacker WETH balance: ", to_uint(w3.fromWei(weth.balanceOf(attacker), 'ether')))

    # Pool liquidity should be at least -95%
    assert(weth.balanceOf(lendly.address) < WETH_LIQUIDITY * 0.05) # 5% of WETH, 5 // 100 = 0.05
    assert(dai.balanceOf(lendly.address) < DAI_LIQUIDITY * 0.05) # 5% of DAI, 5 // 100 = 0.05

    #  Attacker stole the liquidity - at least +88%
    assert(weth.balanceOf(attacker) > WETH_LIQUIDITY * 0.88) # 88% of WETH, 88 // 100 = 0.88
    assert(dai.balanceOf(attacker) > DAI_LIQUIDITY * 0.88) # 88% of DAI, 88 // 100 = 0.88