from brownie import network, chain, FlashLoan, Wei, Contract, accounts
from brownie.utils import color
from time import sleep

AAVE_POOL = "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9";
USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48";
WHALE = "0x8e5dedeaeb2ec54d0508973a0fccd1754586974a";

BORROW_AMOUNT = 100000000000000
FEE_AMOUNT = 90000000000

user = accounts.add()
#whaleSigner = accounts.at(WHALE, force=False)
# some colors
yellow = color("yellow")
red =color("red")
normal = color("none")
# Checking if connected to network, if not we connect
if not network.is_connected():
    network.connect('mainnet-fork-2')
    print(yellow,"\r\nTesting at block number:",red,chain[-1].number, "\r\n")
    if not network.is_connected():
        print(yellow,"\r\nSomething wrong:",red,chain[-1].number, "\r\n")
# yield deployments instantiation
def main():
    try: 
        yield Contract(USDC)
    except:
        yield Contract.from_explorer(USDC)

    try: 
        yield Contract(AAVE_POOL)
    except:
        yield Contract.from_explorer(AAVE_POOL)
    user = accounts[0]
    print("user bal=",user.balance())

    yield FlashLoan.deploy(AAVE_POOL, {'from': user, "gas_price": '20 gwei'})

    yield accounts.at(WHALE, force=True)


usdc, pool, flash_loan, whaleSigner = main()
