from brownie import network, chain, GalacticGorillas, Wei, accounts
from brownie.utils import color
from time import sleep

MINT_PRICE = Wei('1 ether')

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


    nft = GalacticGorillas.deploy({'from': deployer})
    yield nft


deployer, user, attacker, nft = main()