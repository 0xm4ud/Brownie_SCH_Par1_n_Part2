from brownie import network, chain, UST, DAI,USDC, StableSwap, Wei, accounts
from brownie.utils import color
from web3 import Web3
from time import sleep

TOKENS_INITIAL_SUPPLY = 100000000000000 # $100M
TOKENS_IN_STABLESWAP = 1000000000000 # $1M
CHAIN_ID = 31337;


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
    [deployer, attacker] = accounts[:2]
    for _ in range(0, 2):
        yield [deployer, attacker][_]
    #yield, user1, user2, user3, attacker
    w3 = Web3(Web3.HTTPProvider())
    w3.provider.make_request( "evm_setAccountBalance" , [deployer.address, "0x90e40fbeea1d3a4abc8955e946fe31cdcf66f634e1000000000000000000"])
    #The evm_setAccountBalance rpc-json call equivalent in hardhat is hardhat_setBalance
    ust = UST.deploy(TOKENS_INITIAL_SUPPLY, "Terra USD", "UST", 6,{'from': deployer})
    yield ust

    dai = DAI.deploy(CHAIN_ID,{'from': deployer})
    yield dai

    usdc = USDC.deploy({'from': deployer})
    usdc.initialize(
        "Center Coin", "USDC", "USDC", 6, deployer.address,
            deployer.address, deployer.address, deployer.address,
            {'from': deployer, 'gas_price': '20 gwei'}
        )
    yield usdc

    stableSwap = StableSwap.deploy([ust.address, usdc.address, dai.address], {'from': deployer, 'gas_price': '20 gwei'})
    yield stableSwap


deployer, attacker, ust, dai, usdc, stableSwap = main()