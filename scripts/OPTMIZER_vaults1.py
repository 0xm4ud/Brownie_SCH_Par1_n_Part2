from brownie import Wei, network, chain, accounts, interface, YieldContract, OptimizerStrategy, OptimizerVault
from web3 import Web3


ATTACKER_USDC_BALANCE = Wei('100000 mwei') + 1 # Attacker has 100,000 + 1 wei USDC
BOB_USDC_BALANCE = Wei('200000 mwei') # Bob has 200,000 USDC

USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
WHALE = "0xf977814e90da44bfa03b6295a0616a897441acec"

# some colors
green ='\x1b[0;32m'
yellow = '\x1b[0;33m'
red ='\x1b[0;31m'
normal = '\x1b[0m'

# Checking if connected to network, if not we connect
if not network.is_connected():
    network.connect('mainnet-fork-3')
    print(yellow,"\r\nTesting at block number:",red,chain[-1].number, "\r\n")
    if not network.is_connected():
        print(yellow,"\r\nSomething wrong:",red,chain[-1].number, "\r\n")

def main():
    # setting up accounts
    [deployer, attacker, bob] = accounts[:3]
    for _ in range(0, 3):
        yield [deployer, attacker, bob][_]

    # getting w3 instance
    w3 = Web3(Web3.HTTPProvider())
    yield w3

    # setting up USDC
    usdc = interface.IERC20(USDC)
    yield usdc

    # setting up whale
    whaleSigner = accounts.at(WHALE, force=True)
    yield whaleSigner

    #Set attacker, bob, & whale balance to 2 ETH
    w3.provider.make_request( "evm_setAccountBalance" , [attacker.address, "0x1BC16D674EC80000"]) #  2 ETH
    w3.provider.make_request( "evm_setAccountBalance" , [bob.address, "0x1BC16D674EC80000"]) #  2 ETH
    w3.provider.make_request( "evm_setAccountBalance" , [whaleSigner.address, "0x1BC16D674EC80000"]) #  2 ETH

    # Transfer USDC to the attacker & bob
    usdc.transfer(attacker.address, ATTACKER_USDC_BALANCE, {'from': whaleSigner})
    usdc.transfer(bob.address, BOB_USDC_BALANCE, {'from': whaleSigner})

    # Deploying the contract
    yieldContract = YieldContract.deploy(USDC,{'from': deployer, 'gas_price': '19 gwei'})
    yield yieldContract

    strategy = OptimizerStrategy.deploy(yieldContract,{'from': deployer, 'gas_price': '19 gwei'})
    yield strategy

    vault = OptimizerVault.deploy( strategy, "VAULT", "VLT", {'from': deployer, 'gas_price': '19 gwei'})
    yield vault

    #  Assign the vault to the strategy
    strategy.setVault(vault, {'from': deployer, 'gas_price': '19 gwei'})


deployer, attacker, bob, w3, usdc, whaleSigner, \
    yieldContract, strategy, vault = main()