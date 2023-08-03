from brownie import  accounts, Sniper, interface, Contract, DummyERC20, Wei, network, chain
from brownie.utils import color
import json

# setting accounts
deployer, liquidityAdder, user, attacker = [accounts.add() for _ in range(4)]

# Adresses and ABI
WETH_ADDRESS = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
UNISWAPV2_FACTORY_ADDRESS = "0x5c69bee701ef814a2b6a3edd4b1652cb9cc5aa6f"
UNISWAPV2_ROUTER_ADDRESS = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
UNISWAPV2_ROUTER_ABI = json.loads(open('/Users/m4ud/Desktop/SCH-2/sch-exercises-part-2/test/dex-2/router.json').read())

# Balance variables
INITIAL_BALANCE = hex(Wei("300 ether"))
INITIAL_MINT = Wei('80000 ether'); 
INITIAL_LIQUIDITY = Wei('10000 ether'); 
ETH_IN_LIQUIDITY = Wei('50 ether');

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
    yield Contract.from_abi(name="uniswapRouter", address=UNISWAPV2_ROUTER_ADDRESS, abi=UNISWAPV2_ROUTER_ABI)
    yield liquidityAdder.deploy(DummyERC20, "PreciousToken", "PRECIOUS", INITIAL_MINT)
    yield interface.IWETH9(WETH_ADDRESS)
    yield user.deploy(Sniper)

uniswapRouter, preciousToken, weth, sniper = main()


