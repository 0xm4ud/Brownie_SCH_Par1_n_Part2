from brownie import network, chain, FlashLoanUser, ShibaPool, ShibaToken, Wei, accounts
from brownie.utils import color
from time import sleep

INITIAL_SUPPLY = Wei('1000000 ether'); 
TOKENS_IN_POOL = Wei('100000 ether'); 
ATTACKER_TOKENS = Wei('10 ether'); 

#whaleSigner = accounts.at(WHALE, force=False)
# some colors
yellow = color("yellow")
red =color("red")
normal = color("none")
# Checking if connected to network, if not we connect
if not network.is_connected():
    network.connect('development')
    print(yellow,"\r\nTesting at block number:",red,chain[-1].number, "\r\n")
    if not network.is_connected():
        print(yellow,"\r\nSomething wrong:",red,chain[-1].number, "\r\n")
# yield deployments instantiation
def main():
    [deployer, user, attacker] = accounts[:3]
    for _ in range(0, 3):
        yield [deployer, user, attacker][_]
    #yield, user1, user2, user3, attacker


    shiba_token = ShibaToken.deploy(INITIAL_SUPPLY,{'from': deployer})
    yield shiba_token

    shiba_pool = ShibaPool.deploy(shiba_token.address,{'from': deployer})
    yield shiba_pool

    yield FlashLoanUser.deploy(shiba_pool.address,{'from': user})


deployer, user, attacker, shiba_token, shiba_pool, flash_loan = main()