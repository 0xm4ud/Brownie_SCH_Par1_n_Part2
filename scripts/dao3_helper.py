from brownie import network, chain, DAOToken, Governance, LendingPool, Treasury, Wei, accounts
from brownie.utils import color
from web3 import Web3

# DAO Tokens
DEPLOYER_TOKENS = Wei('2500000 ether'); # 2.5M Tokens
MEMBER_1_TOKENS = Wei('500000 ether'); # 500K Tokens
MEMBER_2_TOKENS = Wei('1000000 ether'); # 1M Tokens
TOKENS_IN_POOL = Wei('2000000 ether'); # 2M tokens

# Treasury ETH
ETH_IN_TREASURY = Wei('1500'); # 1500 ETH


#whaleSigner = accounts.at(WHALE, force=False)
# some colors
green ='\x1b[0;32m'
yellow = color("yellow")
red =color("red")
normal = color("none")
# Checking if connected to network, if not we connect
if not network.is_connected():
    network.connect('development')
    print(yellow,"\r\nTesting at block number:",red,chain[-1].number, "\r\n")
    if not network.is_connected():
        print(yellow,"\r\nSomething wrong:",red,chain[-1].number, "\r\n")
# yield deployments instantiation
def main():
    [deployer, member1, member2, attacker] = accounts[:4]
    for _ in range(0, 4):
        yield [deployer, member1, member2, attacker][_]
    #yield, user1, user2, user3, attacker
    w3 = Web3(Web3.HTTPProvider())
    yield w3
    w3.provider.make_request( "evm_setAccountBalance" , [deployer.address, "0x90e40fbeea1d3a4abc8955e946fe31cdcf66f634e1000000000000000000"])
    #The evm_setAccountBalance rpc-json call equivalent in hardhat is hardhat_setBalance
    #Deploy and Setup Contracts
    token= DAOToken.deploy({'from': deployer, 'gas_price': 0x4133110a0})
    yield token

    pool= LendingPool.deploy(token.address, {'from': deployer, 'gas_price': 0x4133110a0})
    yield pool

    treasury= Treasury.deploy({'from': deployer, 'gas_price': 0x4133110a0})
    yield treasury

    governance = Governance.deploy(token.address, treasury.address, {'from': deployer, 'gas_price': 0x4133110a0})
    yield governance

    treasury.setGovernance(governance, {'from': deployer, 'gas_price': 0x4133110a0})

    # Send ETH to Treasury
    deployer.transfer(treasury, ETH_IN_TREASURY)

    assert(treasury.balance() == ETH_IN_TREASURY)

    # Mint tokens
    token.mint(deployer, DEPLOYER_TOKENS, {'from': deployer, 'gas_price': 0x4133110a0})
    token.mint(member1, MEMBER_1_TOKENS, {'from': deployer, 'gas_price': 0x4133110a0})
    token.mint(member1, MEMBER_2_TOKENS, {'from': deployer, 'gas_price': 0x4133110a0})
    token.mint(pool, TOKENS_IN_POOL, {'from': deployer, 'gas_price': 0x4133110a0})



deployer, member1, member2, attacker, w3, token, pool, treasury, governance = main()