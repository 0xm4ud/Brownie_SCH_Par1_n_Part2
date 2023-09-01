from brownie import accounts, EtherBank, rAttack1

def test_reentrancy_1():
    #Setting accounts
    dep = accounts[0]
    user = accounts[1]
    attacker = accounts[3]
    #Deploying targey
    bank = EtherBank.deploy({'from': dep})
    # Initial deposit
    bank.depositETH({'from': dep, 'value': '10 ether'})

    #Assigning intial balance variable
    attackerInitialBal = attacker.balance()
    bankInitialBal = bank.balance()

    #deploying Attacker contract
    att = rAttack1.deploy(bank.address, {'from': attacker, 'value': '1 ether'})
    #asserting attacker contract balance
    assert(att.balance() == '1 ether')

    # Attacking
    att.attack()

    ## Asserting hack through balances of attacker, bank and attacker contract
    assert(bank.balance() == 0)
    assert(bank.balances(att.address) == 0)
    assert(attacker.balance() == attackerInitialBal + bankInitialBal)
