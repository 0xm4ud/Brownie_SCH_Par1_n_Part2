from brownie import Pool2, Receiver, GreedyReceiver, accounts, Wei, web3
from web3 import Web3
import brownie

def test_deploy_n_greedyReceiver():
    #Set accounts
    deployer, user = accounts[:2]
    POOL_BALANCE = Wei('1000 ether')

    w3 = Web3(Web3.HTTPProvider())
    # Set deployer balance to 1,000 ETH
    w3.provider.make_request("evm_setAccountBalance", [deployer.address, hex(POOL_BALANCE)])

    #Deploy Pool.sol contract with 1,000 ETH
    pool = Pool2.deploy({'from': deployer, 'value': POOL_BALANCE})
    #Deploy Receiver.sol contract
    receiver = Receiver.deploy(pool.address, {'from': user})

    #Successfuly execute a Flash Loan of all the balance using Receiver.sol contract
    receiver.flashLoan(POOL_BALANCE, {'from': user})

    #Deploy GreedyReceiver.sol contract
    greedyReceiver = GreedyReceiver.deploy(pool.address, {'from': user})

    #Fails to execute a flash loan with GreedyReceiver.sol contract
    with brownie.reverts("ETH wasn't paid back"):
        greedyReceiver.flashLoan(POOL_BALANCE, {'from': user})
