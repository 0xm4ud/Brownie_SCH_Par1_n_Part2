from brownie import reverts
from scripts.dao1_helper import *

#@pytest.fixture
def test_dao_setup():

    print(red,"\r[ * ] \x1b[0;43m0xm4ud DAO Attacker 3000\x1b[0;m")

    #Mint 1000 RainbowAllianceToken to deployer
    rainbowAlliance.mint(deployer, DEPLOYER_MINT, {'from': deployer, 'gas_price': 0x4133110a0})
    #Mint 100 RainbowAllianceToken to user1 and user2
    rainbowAlliance.mint(user1, USERS_MINT, {'from': deployer, 'gas_price': 0x4133110a0})
    rainbowAlliance.mint(user2, USERS_MINT, {'from': deployer, 'gas_price': 0x4133110a0})

    #Burn 30 RainbowAllianceToken from user2
    print(green,"\r[ + ]\x1b[0;m Burning 30 RainbowAllianceToken from user2",normal)
    rainbowAlliance.burn(user2.address, USER2_BURN, {'from': deployer, 'gas_price': 0x4133110a0})


def test_governance():
    #Test Governance Token
    #Can't create proposals, if there is no voting power
    print(green,"\r[ + ]\x1b[0;m Creating proposal without voting power",normal)
    with reverts("no voting rights"):
        assert(rainbowAlliance.createProposal("Donate 1000$ to charities", {'from': user3, 'gas_price': 0x4133110a0}))

    #Should be able to create proposals if you have voting power
    assert(rainbowAlliance.createProposal("Pay 100$ to george for a new Logo", {'from': deployer, 'gas_price': 0x4133110a0}))

    #Can't vote twice
    with reverts("already voted"):
        assert(rainbowAlliance.vote(1, True, {'from': deployer, 'gas_price': 0x4133110a0}))
    #Shouldn't be able to vote without voting rights
    with reverts("no voting rights"):
        assert(rainbowAlliance.vote(1, True, {'from': user3, 'gas_price': 0x4133110a0}))
    #Non existing proposal, reverts
    with reverts("proposal doesn't exist"):
        assert(rainbowAlliance.vote(123, False))

    #Users votes
    rainbowAlliance.vote(1, True, {'from': user1, 'gas_price': 0x4133110a0})
    rainbowAlliance.vote(1, False, {'from': user2, 'gas_price': 0x4133110a0})

    #Check accounting is correct
    proposal = rainbowAlliance.getProposal(1)
    print(green,"\r[ + ]\x1b[0;m Proposal 1: ", proposal, normal)
    # Supposed to be 1,100 (User1 - 100, deployer - 1,000)
    assert(proposal['yes'] == DEPLOYER_MINT + USERS_MINT)
    #Supposed to be 70 (100 - 30, becuase we burned 30 tokens of user2)
    assert(proposal['no'] == USERS_MINT - USER2_BURN)

def test_poc_should_FAIL_to_catch_bug():
    user1Balance = rainbowAlliance.balanceOf(user1.address)
    rainbowAlliance.transfer(user3.address, user1Balance, {'from': user1, 'gas_price': 0x4133110a0})
    with reverts("no voting rights"):
        assert(rainbowAlliance.createProposal("DUMMY PROPOSAL", {'from': user1, 'gas_price': 0x4133110a0}))