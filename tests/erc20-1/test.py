from brownie import accounts, Wei, HackersToken
from brownie.convert import to_uint
from web3.constants import MAX_INT, ADDRESS_ZERO
import pytest

@pytest.fixture
def setup():
    # ACCT SETUP 
    [deployer, user1, user2, user3]= accounts[:4]

    #Assigning intital suuply
    DEPLOYER_MINT = Wei("100000 ether")
    USERS_MINT = Wei("5000 ether")
    FIRST_TRANSFER = Wei("100 ether")
    SECOND_TRANSFER = Wei("1000 ether")
    #Deploying target
    token = HackersToken.deploy({'from': deployer})
    # Minting tokens for deployer and users
    token.mint(deployer, DEPLOYER_MINT, {'from': deployer})
    token.mint(user1, USERS_MINT, {'from': deployer})
    token.mint(user2, USERS_MINT, {'from': deployer})
    token.mint(user3, USERS_MINT, {'from': deployer})
    # Asserting mint
    assert(token.balanceOf(deployer) == DEPLOYER_MINT)
    assert(token.balanceOf(user2) == USERS_MINT)

    return token, deployer, user1, user2, user3, FIRST_TRANSFER, SECOND_TRANSFER, USERS_MINT

def test_transfer(setup):
    token, deployer, user1, user2, user3, FIRST_TRANSFER, SECOND_TRANSFER, USERS_MINT = setup
    # First transfer
    token.transfer(user3, FIRST_TRANSFER, {'from': user2})
    # Approval & Allowance test
    token.approve(user1, SECOND_TRANSFER, {'from': user3})
    assert(token.allowance(user3, user1) == SECOND_TRANSFER)

    # Second transfer
    token.transferFrom(user3, user1, SECOND_TRANSFER, {'from': user1})

    # Checking balances after transfer
    assert(token.balanceOf(user1) == USERS_MINT + SECOND_TRANSFER)
    assert(token.balanceOf(user2) == USERS_MINT - FIRST_TRANSFER)
    assert(token.balanceOf(user3) == USERS_MINT + FIRST_TRANSFER - SECOND_TRANSFER)
