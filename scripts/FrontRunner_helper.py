from brownie import network, chain, Chocolate, Wei, accounts, interface, Sandwich, Contract
from brownie.utils import color
from time import sleep

WETH_ADDRESS = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"

INITIAL_MINT = Wei('1000000 ether'); 
INITIAL_LIQUIDITY = Wei('100000 ether'); 
ETH_IN_LIQUIDITY = Wei('100 ether');
USER1_SWAP = Wei('120 ether');
USER2_SWAP = Wei('100 ether');


#whaleSigner = accounts.at(WHALE, force=False)
# some colors
yellow = color("yellow")
red =color("red")
normal = color("none")
# Checking if connected to network, if not we connect
if not network.is_connected():
    network.connect('mainnet-fork')
    print(yellow,"\r\nTesting at block number:",red,chain[-1].number, "\r\n")
    if not network.is_connected():
        print(yellow,"\r\nSomething wrong:",red,chain[-1].number, "\r\n")
# yield deployments instantiation
def main():

    [deployer, user1, user2, attacker] = accounts[:4]
    for _ in range(0, 4):
        yield [deployer, user1, user2,  attacker][_]
    #yield, user1, user2, user3, attacker
    # Deploying the contract
    weth = interface.IWETH9(WETH_ADDRESS)

    yield weth
    # Deploying the contract
    chocolate = Chocolate.deploy(INITIAL_MINT,{'from': deployer, 'gas_price': '19 gwei'})
    yield chocolate

    pairAddress = chocolate.uniswapV2Pair()
    pair = interface.IUniswapV2Pair(pairAddress)

    yield pair

    # Deploy attacker contract
    sandwichContract = Sandwich.deploy(weth.address, chocolate.address, {'from': attacker, 'gas_price': '19 gwei'})
    yield sandwichContract

    chocolateInterface = interface.IChocolate(chocolate.address)
    yield chocolateInterface

deployer, user1, user2, attacker, weth, chocolate, pair, sandwichContract, chocolateInterface = main()