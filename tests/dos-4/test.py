from web3 import Web3
from scripts.DOS_4_helper import *
#from brownie.utils import console
from brownie import reverts



#@pytest.fixture
def test_successfull_minting_tests():

    w3 = Web3(Web3.HTTPProvider())
    #2.5 ETH (ETH -> WEI -> Hexdecimal)
    w3.provider.make_request("evm_setAccountBalance", [attacker.address, "0x22B1C8C1227A0000" ])


    deployerBalanceBefore = deployer.balance();
    nft.mint(2, {'from': user, 'value': MINT_PRICE*2})
    assert(nft.balanceOf(user.address)== 2)
    assert(nft.ownerOf(1)== user.address)
    assert(nft.ownerOf(2)== user.address)
    deployerBalanceAfter = deployer.balance();
    assert(deployerBalanceAfter == deployerBalanceBefore + MINT_PRICE * 2)

def test_failed_minting_tests():
    with reverts("wrong _mintAmount"):
        assert(nft.mint(20, {'from': user}))
    with reverts("not enough ETH"):
        assert(nft.mint(1, {'from': user}))
    with reverts("exceeded MAX_PER_WALLET"):
        print("mintCount", nft.mintCount(user.address))
        assert(nft.mint(4, {'from': user, 'value': MINT_PRICE * 4}))


def test_pause_tests():

    with reverts("Ownable: caller is not the owner"):
        assert(nft.pause(True, {'from': user}))
    with reverts("contract is paused"):
        nft.pause(True);
        assert(nft.mint(1, {'from': user, 'value': MINT_PRICE}))
    nft.pause(False);
    nft.mint(1, {'from': user, 'value': MINT_PRICE})
    assert(nft.balanceOf(user.address) == 3)



def test_exploit():
 #   console.log(20,duration=10)
    #time.sleep(2)
    assert(nft.ownerOf(1)== user.address)
    assert(nft.ownerOf(2)== user.address)
    assert(nft.ownerOf(3)== user.address)

    nft.mint(1, {'from': attacker, 'value': '1 ether'})
    nft.mint(1, {'from': attacker, 'value': '1 ether'})
    assert(nft.ownerOf(5)== attacker.address)
    assert(nft.ownerOf(4)== attacker.address)
    nft.burn(4, {'from': attacker})
    assert(nft.ownerOf(5)== attacker.address)
    #nft.burn(4, {'from': attacker})
    with reverts("ERC721: token already minted"):
        nft.mint(1, {'from': user, 'value': '1 ether'})
    
    #Fixing the issue (attacker is a good guy at the end)
    with reverts("wrong _tokenId"):
        nft.burn(5, {'from': attacker})
