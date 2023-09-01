from brownie import Wei, accounts, MyAwesomeArt


def test_minting_n_transfer():
    DEPLOYER_MINT = 5;
    USER1_MINT = 3;
    MINT_PRICE = Wei('0.1 ether');

    [deployer, user1, user2] = accounts[:3]

    nft = MyAwesomeArt.deploy({'from': deployer})
    # Deployer should own token ids 1-5
    for _ in range(0, DEPLOYER_MINT):
        nft.mint({'from': deployer, 'value': MINT_PRICE})

    # User1 should own token ids 6-8
    for _ in range(0, USER1_MINT):
        nft.mint({'from': user1, 'value': MINT_PRICE})

    # Check Minting
    assert(nft.balanceOf(deployer) == DEPLOYER_MINT)
    assert(nft.balanceOf(user1) == USER1_MINT)
    # Transfer tokenId 6 from user1 to user2
    nft.transferFrom(user1, user2, 6, {'from': user1})
    # Check user2 owns tokenId 6
    assert(nft.ownerOf(6) == user2)

    # Deployer approves user1 to transfer tokenId 3
    nft.approve(user1, 3, {'from': deployer})
    # Test that user1 has approval to spend tokenId 3
    assert(nft.getApproved(3) == user1.address)

    #Use approval and transfer tokenId 3 from deployer to User1
    nft.transferFrom(deployer, user1, 3, {'from': user1})
    # Check user1 owns tokenId 3
    assert(nft.ownerOf(3) == user1)

    #Checking balances after transfer
    #Deployer: 5 minted, 1 sent, 0 received
    assert(nft.balanceOf(deployer) == DEPLOYER_MINT - 1)
    #User1: 3 minted, 1 sent, 1 received
    assert(nft.balanceOf(user1) == USER1_MINT)
    #User2: 0 minted, 0 sent, 1 received
    assert(nft.balanceOf(user2) == 1)
