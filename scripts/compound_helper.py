from brownie import network, chain, CompoundUser, Wei, Contract, accounts
from brownie.utils import color
from time import sleep


COMPOUND_CONTROLLER= "0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B"

USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
DAI = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
WHALE = "0xf977814e90da44bfa03b6295a0616a897441acec"
#Compound USDC Receipt Token
cUSDC = "0x39AA39c021dfbaE8faC545936693aC917d5E7563"
#Compound DAI Receipt Token
cDAI = "0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643"

USER_USDC_BALANCE = 100000000000
AMOUNT_TO_DEPOSIT = 1000000000
AMOUNT_TO_BORROW = Wei("100 ether")

user = accounts.add()
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
    try: 
        yield Contract(USDC)
    except ValueError:
        yield Contract.from_explorer(USDC)

    try: 
        yield Contract(DAI)
    except ValueError:
        yield Contract.from_explorer(DAI)

    try: 
        yield Contract(cUSDC)
    except ValueError:
        yield Contract.from_explorer(cUSDC)

    try: 
        yield Contract(cDAI)
    except ValueError:
        yield Contract.from_explorer(cDAI)

    yield user.deploy(CompoundUser,COMPOUND_CONTROLLER, cUSDC, cDAI)

    yield accounts.at(WHALE, force=True)

usdc, dai, cUSDC, cDAI, compUser, whaleSigner = main()