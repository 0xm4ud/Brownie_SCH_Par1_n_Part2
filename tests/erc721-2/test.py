from brownie import accounts, OpenOcean, DummyERC721, Wei, reverts
import pytest

@pytest.fixture
def setup_erc721_2():
    #setting accounts
    [deployer, user1, user2, user3] = accounts[:4]
    #User1 creates his own NFT collection
    CUTE_NFT_PRICE = Wei('5 ether');
    BOOBLES_NFT_PRICE = Wei('7 ether');

    cuteNFT = DummyERC721.deploy("Crypto Cuties", "CTC", 1000,{'from': user1})
    # MINT crypto cuties]
    cuteNFT.mintBulk(30, {'from': user1})
    assert(cuteNFT.balanceOf(user1) == 30)
    # User3 creates his own NFT collection
    booblesNFT = DummyERC721.deploy("Rare Boobles", "RBS", 10000,{'from': user3})
    # MINT rare boobles
    booblesNFT.mintBulk(120, {'from': user3})
    assert(booblesNFT.balanceOf(user3) == 120)

    #Store user initial balance
    user1InitialBal = user1.balance()
    user2InitialBal = user2.balance()
    user3InitialBal = user3.balance()

    marketplace = OpenOcean.deploy({'from': deployer})

    return [deployer, user1, user2, user3, cuteNFT, booblesNFT, CUTE_NFT_PRICE, BOOBLES_NFT_PRICE, user1InitialBal, user2InitialBal, user3InitialBal, marketplace]


def test_listing_n_purchase(setup_erc721_2):
    [deployer, user1, user2, user3, cuteNFT, booblesNFT, CUTE_NFT_PRICE, BOOBLES_NFT_PRICE, user1InitialBal, user2InitialBal, user3InitialBal, marketplace] = setup_erc721_2

    #User1 lists 1-10 crypto cuties for sale for 5 ether each
    for _ in range(0, 10):
        cuteNFT.approve(marketplace.address, (_+1), {'from': user1})
        marketplace.listItem(cuteNFT.address, (_+1), CUTE_NFT_PRICE, {'from': user1})
        
    for i in range(0, 9):
        assert(marketplace.listedItems(i+1) == (i+1, cuteNFT.address, i+1, CUTE_NFT_PRICE, user1.address, False))

    # assert that MarketPlace owns all listed items
    assert(cuteNFT.balanceOf(marketplace.address) == 10)

    # Checks that the marketplace mapping is correct (All data is correct), check the 10th item.
    lastItem = marketplace.listedItems(10)
    assert(lastItem['itemId'] == 10)
    assert(lastItem['collection'] == cuteNFT.address)
    assert(lastItem['tokenId'] == 10)
    assert(lastItem['price'] == CUTE_NFT_PRICE)
    assert(lastItem['seller'] == user1.address)
    assert(lastItem['isSold'] == False)

    # User2 lists 1-5 rare boobles for sale for 7 ether each
    for _ in range(0, 5):
        booblesNFT.approve(marketplace.address, (_+1), {'from': user3})
        marketplace.listItem(booblesNFT.address, (_+1), BOOBLES_NFT_PRICE, {'from': user3})

    # Check that Marketplace owns 5 Booble NFTs
    assert(booblesNFT.balanceOf(marketplace.address) == 5)

    #Checks that the marketplace mapping is correct (All data is correct), check the 15th item.
    lastItem = marketplace.listedItems(15)
    assert(lastItem['itemId'] == 15)
    assert(lastItem['collection'] == booblesNFT.address)
    assert(lastItem['tokenId'] == 5)
    assert(lastItem['price'] == BOOBLES_NFT_PRICE)
    assert(lastItem['seller'] == user3.address)
    assert(lastItem['isSold'] == False)

    #Try to purchase itemId 100, should revert
    with reverts("incorrect _itemId"):
        marketplace.purchase(100, {'from': user2})

    #Try to purchase itemId 3, without ETH, should revert
    with reverts("wrong ETH was sent"):
        marketplace.purchase(3, {'from': user2})

    #Try to purchase itemId 3, with ETH, should work
    marketplace.purchase(3, {'from': user2, 'value': CUTE_NFT_PRICE})

    #Can't purchase sold item
    with reverts("item is already sold"):
        marketplace.purchase(3, {'from': user2, 'value': CUTE_NFT_PRICE})

    # User2 owns itemId 3 -> Cuties tokenId 3
    assert(cuteNFT.ownerOf(3) == user2.address)

    #User1 got the right amount of ETH for the sale
    user1Balance = user1.balance()
    assert(user1Balance > user1InitialBal + CUTE_NFT_PRICE - Wei('0.2 ether'))

    #Purchase itemId 11
    marketplace.purchase(11, {'from': user2, 'value': BOOBLES_NFT_PRICE})

    # User2 owns itemId 11 -> Boobles tokenId 1
    assert(booblesNFT.ownerOf(1) == user2.address)

    #User3 got the right amount of ETH for the sale
    user3Balance = user3.balance()
    assert(user3Balance > user3InitialBal + BOOBLES_NFT_PRICE - Wei('0.2 ether'))