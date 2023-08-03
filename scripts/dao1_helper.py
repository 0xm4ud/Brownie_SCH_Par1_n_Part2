from brownie import network, chain, RainbowAllianceToken, Wei, accounts
from brownie.utils import color
from web3 import Web3

DEPLOYER_MINT = Wei('1000 ether');
USERS_MINT = Wei('100 ether');
USER2_BURN = Wei('30 ether');


#whaleSigner = accounts.at(WHALE, force=False)
# some colors
green ='\x1b[0;32m'
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
    [deployer, user1, user2, user3] = accounts[:4]
    for _ in range(0, 4):
        yield [deployer, user1, user2, user3][_]
    #yield, user1, user2, user3, attacker
    w3 = Web3(Web3.HTTPProvider())
    w3.provider.make_request( "evm_setAccountBalance" , [deployer.address, "0x90e40fbeea1d3a4abc8955e946fe31cdcf66f634e1000000000000000000"])
    #The evm_setAccountBalance rpc-json call equivalent in hardhat is hardhat_setBalance
    rainbowAlliance= RainbowAllianceToken.deploy({'from': deployer, 'gas_price': 0x4133110a0})
    yield rainbowAlliance


deployer, user1, user2, user3, rainbowAlliance = main()