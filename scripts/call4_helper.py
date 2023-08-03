from brownie import network, chain, DummyERC20, BlockSafe, BlockSafeFactory, BlockSafeDestructor, Wei, accounts
from brownie.utils import color
from web3 import Web3


# Variables
CALL_OPERATION = 1
DELEGATECALL_OPERATION = 2


#whaleSigner = accounts.at(WHALE, force=False)
# some colors
green ='\x1b[032m'
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
    [deployer, user1, user2, user3, attacker] = accounts[:5]
    for _ in range(0, 5):
        yield [deployer, user1, user2, user3, attacker][_]
    #yield, user1, user2, user3, attacker
    w3 = Web3(Web3.HTTPProvider())
    yield w3
    w3.provider.make_request( "evm_setAccountBalance" , [deployer.address, "0x90e40fbeea1d3a4abc8955e946fe31cdcf66f634e1000000000000000000"])
    #The evm_setAccountBalance rpc-json call equivalent in hardhat is hardhat_setBalance
    #Deploy and Setup Contracts
    token= DummyERC20.deploy("Dummy ERC20", "DToken", Wei('1000 ether'), {'from': deployer, 'gas_price': 0x4133110a0})
    yield token

    blockSafeTemplate = BlockSafe.deploy({'from': deployer, 'gas_price': 0x4133110a0})
    yield blockSafeTemplate

    blockSafeFactory= BlockSafeFactory.deploy(deployer, blockSafeTemplate, {'from': deployer, 'gas_price': 0x4133110a0})
    yield blockSafeFactory

    #  User1 creating CryptoKeepers
    User1Salt = w3.keccak(text=user1.address)
    blockSafe1Address = blockSafeFactory.predictBlockSafeAddress(User1Salt)
    blockSafeFactory.createBlockSafe(User1Salt, [user1], {'from': user1, 'gas_price': 0x4133110a0})
    blockSafe1 = BlockSafe.at(blockSafe1Address)
    yield blockSafe1

    #  User2 creating CryptoKeepers
    User2Salt = w3.keccak(text=user2.address)
    blockSafe2Address = blockSafeFactory.predictBlockSafeAddress(User2Salt)
    blockSafeFactory.createBlockSafe(User2Salt, [user2], {'from': user2, 'gas_price': 0x4133110a0})
    blockSafe2 = BlockSafe.at(blockSafe2Address)
    yield blockSafe2

    #  User3 creating CryptoKeepers
    User3Salt = w3.keccak(text=user3.address)
    blockSafe3Address = blockSafeFactory.predictBlockSafeAddress(User3Salt)
    blockSafeFactory.createBlockSafe(User3Salt, [user3], {'from': user3, 'gas_price': 0x4133110a0})
    blockSafe3 = BlockSafe.at(blockSafe3Address)
    yield blockSafe3

    # Users load their Block Safe with some ETH
    user1.transfer(blockSafe1, Wei('10 ether'))
    user2.transfer(blockSafe2, Wei('10 ether'))
    user3.transfer(blockSafe3, Wei('10 ether'))


deployer, user1, user2, user3, attacker, w3, token, blockSafeTemplate, \
blockSafeFactory, blockSafe1, blockSafe2, blockSafe3  = main()