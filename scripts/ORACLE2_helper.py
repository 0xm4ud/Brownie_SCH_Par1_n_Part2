from web3 import Web3
from brownie import Lendly, interface, accounts, chain, Wei, network, AttackLendly
from brownie.utils import color
import pytest


#Addresses
PAIR_ADDRESS = "0xa478c2975ab1ea89e8196811f51a7b7ade33eb11" # DAI/WETH
DAI_ADDRESS = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
WETH_ADDRESS = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
IMPERSONATED_ACCOUNT_ADDRESS = "0xf977814e90da44bfa03b6295a0616a897441acec" # Binance Hot Wallet

# Amounts
WETH_LIQUIDITY = Wei('180 ether') # 180 ETH
DAI_LIQUIDITY = Wei('270000 ether') # 270K USD

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

    [deployer, attacker] = accounts[:2]
    for _ in range(0, 2):
        yield [deployer, attacker][_]

    # Attacker starts with 1 ETH
    w3 = Web3(Web3.HTTPProvider())
    w3.provider.make_request("evm_setAccountBalance", [attacker.address, "0xDE0B6B3A7640000"]) #  1 ETH
    yield w3
    assert(attacker.balance() == Wei('1 ether'))

    #  Deploy Lendly with DAI/WETH contract
    lendly = Lendly.deploy(PAIR_ADDRESS,{'from': deployer, 'gas_price': '19 gwei'})
    yield lendly

    # Deploy Lendly with DAI/WETH contract
    weth = interface.IWETH9(WETH_ADDRESS)
    yield weth

    dai = interface.IERC20(DAI_ADDRESS)
    yield dai

    # Convert ETH to WETH
    weth.deposit({'from': deployer, 'gas_price': '19 gwei', 'value': WETH_LIQUIDITY})
    assert(weth.balanceOf(deployer) == WETH_LIQUIDITY)

    #  Deposit WETH from Deployer to Lendly
    weth.approve(lendly.address, WETH_LIQUIDITY, {'from': deployer, 'gas_price': '19 gwei'})
    lendly.deposit(weth.address ,WETH_LIQUIDITY, {'from': deployer, 'gas_price': '19 gwei'})
    # WETH despoit succeded
    assert(weth.balanceOf(lendly.address) == WETH_LIQUIDITY)
    assert(lendly.deposited(weth, deployer) == WETH_LIQUIDITY)

    # Depsit DAI on Lendly (from Binance hot wallet)
    impersonatedSigner = accounts.at(IMPERSONATED_ACCOUNT_ADDRESS, force=True)
    yield impersonatedSigner
    dai.approve(lendly.address, DAI_LIQUIDITY, {'from': impersonatedSigner, 'gas_price': '19 gwei'})
    lendly.deposit(dai.address ,DAI_LIQUIDITY, {'from': impersonatedSigner, 'gas_price': '19 gwei'})



deployer, attacker, w3, lendly, weth, dai, impersonatedSigner = main()
