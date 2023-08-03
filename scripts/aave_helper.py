from brownie import network, chain, AaveUser, Wei, Contract, accounts
from brownie.utils import color
from time import sleep

AAVE_POOL = "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2";
USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48";
DAI = "0x6B175474E89094C44Da98b954EedeAC495271d0F";
WHALE = "0xf977814e90da44bfa03b6295a0616a897441acec";

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
    network.connect('mainnet-fork-3')
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
        yield Contract(A_USDC)
    except ValueError:
        yield Contract.from_explorer(A_USDC)

    try: 
        yield Contract(VARIABLE_DEBT_DAI)
    except ValueError:
        yield Contract.from_explorer(VARIABLE_DEBT_DAI)

    yield user.deploy(AaveUser,AAVE_POOL, USDC, DAI)

    yield accounts.at(WHALE, force=True)


usdc, dai, aUSDC, debtDAI, aaveUser, whaleSigner = main()
