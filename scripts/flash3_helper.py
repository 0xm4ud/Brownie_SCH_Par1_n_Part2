from brownie import network, chain, FlashSwap, Wei, Contract, accounts
from brownie.utils import color
#from time import sleep
#from brownie.network.rpc import hardhat, ganache

USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48";
PAIR = "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc";
WHALE = "0x8e5dedeaeb2ec54d0508973a0fccd1754586974a";


BORROW_AMOUNT = 40000000000000
FEE_AMOUNT = BORROW_AMOUNT * 3 // 997 + 1;


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
        yield Contract(PAIR)
    except ValueError:
        yield Contract.from_explorer(PAIR)
    user = accounts[0]
    yield user 
    yield FlashSwap.deploy(PAIR, {'from': user, "gas_price": '20 gwei'})

    yield accounts.at(WHALE, force=True)


usdc, pair, user, flash_swap, whaleSigner = main()