from brownie import network, chain, TheGridDAO, TheGridTreasury, Wei, accounts
from brownie.utils import color
from web3 import Web3

#Governance Tokens
DEPLOYER_TOKENS = Wei('1500 ether')
DAO_MEMBER_TOKENS = Wei('1000 ether')
ATTACKER_TOKENS = Wei('10 ether')

#ETH Balances
ETH_IN_TREASURY = Wei('1000 ether')

#Proposals
FIRST_PROPOSAL_AMOUNT = Wei('0.1 ether')
SECOND_PROPOSAL_AMOUNT = Wei('1 ether')

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
    [deployer, daoMember1, daoMember2, attacker, user] = accounts[:5]
    for _ in range(0, 5):
        yield [deployer, daoMember1, daoMember2, attacker, user][_]
    #yield, user1, user2, user3, attacker
    w3 = Web3(Web3.HTTPProvider())
    yield w3
    w3.provider.make_request( "evm_setAccountBalance" , [deployer.address, "0x90e40fbeea1d3a4abc8955e946fe31cdcf66f634e1000000000000000000"])
    #The evm_setAccountBalance rpc-json call equivalent in hardhat is hardhat_setBalance
    #Deploy and Setup Contracts
    dao= TheGridDAO.deploy({'from': deployer, 'gas_price': 0x4133110a0})
    yield dao

    treasury= TheGridTreasury.deploy(dao.address, {'from': deployer, 'gas_price': 0x4133110a0})
    yield treasury
    dao.setTreasury(treasury, {'from': deployer, 'gas_price': 0x4133110a0})

    #ETH to Treasury
    deployer.transfer(treasury, ETH_IN_TREASURY)

    assert(treasury.balance() == ETH_IN_TREASURY)

    # Mint tokens
    dao.mint(deployer, DEPLOYER_TOKENS, {'from': deployer, 'gas_price': 0x4133110a0})
    dao.mint(daoMember1, DAO_MEMBER_TOKENS, {'from': deployer, 'gas_price': 0x4133110a0})
    dao.mint(daoMember2, DAO_MEMBER_TOKENS, {'from': deployer, 'gas_price': 0x4133110a0})
    dao.mint(attacker, ATTACKER_TOKENS, {'from': deployer, 'gas_price': 0x4133110a0})

    attackerInitialETHBalance = attacker.balance()
    yield attackerInitialETHBalance


deployer, daoMember1, daoMember2, attacker, user, w3, dao, treasury, attackerInitialETHBalance = main()