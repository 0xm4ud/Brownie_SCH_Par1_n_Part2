from scripts.UR_2_helper import *
from brownie import reverts, AttackEscrow


def test_escrow():

    # Escrow 10 ETH from user1 to user2, one month treshold
    escrow.escrowEth(user2, ONE_MONTH, {'from': user1, 'value': USER1_ESCROW_AMOUNT})


    tokenId = escrowNFT.tokenCounter()

    # User2 can't withdraw before matureTime
    escrowNFT.approve(escrow.address, tokenId, {'from': user2})
    with reverts("Escrow period not expired."):
        escrow.redeemEthFromEscrow(tokenId, {'from': user2})

    # Fast forward to mature time
    chain.sleep(ONE_MONTH)
    chain.mine()

    #  Another user can't withdraw if he doesn't own this NFT
    with reverts("Must own token to claim underlying ETH"):
        escrow.redeemEthFromEscrow(tokenId, {'from': user3})

    # Recipient can withdraw after matureTime
    escrowNFT.approve(escrow.address, tokenId, {'from': user2})
    balanceBefore = user2.balance()
    escrow.redeemEthFromEscrow(tokenId, {'from': user2})
    balanceAfter = user2.balance()
    #dotOne = Wei('0.1 ether') # gas, if not using gas during tests, just comment it out
    assert(balanceAfter == balanceBefore + USER1_ESCROW_AMOUNT)

def test_Some_users_escrow_more_ETH():
    escrow.escrowEth(user2, ONE_MONTH, {'from': user1, 'value': USER1_ESCROW_AMOUNT})
    escrow.escrowEth(user1, ONE_MONTH, {'from': user2, 'value': USER2_ESCROW_AMOUNT})
    escrow.escrowEth(user1, ONE_MONTH, {'from': user3, 'value': USER3_ESCROW_AMOUNT})

def test_exploit():
    attackerContract = AttackEscrow.deploy(escrowNFT, escrow, {'from': attacker})

    attackerContract.attack({'from': attacker, 'value': Wei('1 ether')})

    # Attacker should drain the escrow contract
    assert(escrow.balance() == 0)
    assert(attacker.balance() > attackerInitialBalance + USER1_ESCROW_AMOUNT + USER2_ESCROW_AMOUNT + USER3_ESCROW_AMOUNT - Wei('1 ether'))