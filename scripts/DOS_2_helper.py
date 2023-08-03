from brownie import network, chain, Auction, Wei, accounts
from brownie.utils import color
from time import sleep

USER1_FIRST_BID = Wei('5 ether'); 
USER2_FIRST_BID = Wei('6.5 ether');

#AAVE USDC Receipt Token
A_USDC = "0x98C23E9d8f34FEFb1B7BD6a91B7FF122F4e16F5c";
#AAVE DAI Variable Debt Token
VARIABLE_DEBT_DAI = "0xcF8d0c70c850859266f5C338b38F9D663181C314";

USER_USDC_BALANCE = 100000000000
AMOUNT_TO_DEPOSIT = 1000000000
AMOUNT_TO_BORROW = Wei("100 ether");

user = accounts.add()
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
    [deployer, user1, user2, attacker] = accounts[:4]
    for _ in range(0, 4):
        yield [deployer, user1, user2, attacker][_]
    #yield, user1, user2, user3, attacker

    yield Auction.deploy({'from': deployer})


deployer, user1, user2, attacker, auction = main()