from brownie import accounts, interface, Wei, TwoStepExchange, network, chain
from brownie.utils import color
from web3 import Web3


USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
WETH = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
BUY_WETH_SWAP_PATH = [USDC, WETH]
ORDER_USDC_AMOUNT = Wei('100 mwei') # 0.1 USDC
ORDER_CREATION_PRICE = Wei("5000 ether") # 5,000 USDC per ETH


def getKeeperPriceParams(price, block_number):
    return (price, block_number)

# some colors
green ='\x1b[0;32m'
yellow = color("yellow")
red =color("red")
normal = color("none")
# Checking if connected to network, if not we connect
if not network.is_connected():
    network.connect('mainnet-fork')
    print(yellow,"\r\nTesting at block number:",red,chain[-1].number, "\r\n")
    if not network.is_connected():
        print(yellow,"\r\nSomething wrong:",red,chain[-1].number, "\r\n")

def main():
    # setting up accounts
    [keeper, attacker] = accounts[:2]
    for _ in range(0, 2):
        yield [keeper, attacker][_]

    # Deployment
    weth = interface.IWETH9(WETH)
    yield weth
    usdc = interface.IERC20(USDC)
    yield usdc
    exchange = TwoStepExchange.deploy({'from': keeper})
    yield exchange
    # getting w3 instance
    # what is 6 eth in hex? 0x16345785D8A0000
    w3 = Web3(Web3.HTTPProvider())
    #w3.provider.make_request( "evm_setAccountBalance" , [keeper.address, "0x21e19e0c9bab2400000"]) #  0.1 ETH
    yield w3


keeper, attacker, weth, usdc, exchange, w3 = main()