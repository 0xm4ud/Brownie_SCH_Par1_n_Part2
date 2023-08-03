from brownie import AdvancedVault, VaultAttack, accounts, Wei
#from brownie.utils import console

def test_flash_attack_2():

    [deployer, attacker] = accounts[:2]
    ETH_IN_VAULT = Wei('1000')

    adv_vault = AdvancedVault.deploy({'from': deployer})

    adv_vault.depositETH({'from': deployer, 'value':ETH_IN_VAULT})

    attackerInitialBalance = attacker.balance()
    vaultInitialBalance = adv_vault.balance()

    flash_attack = VaultAttack.deploy(adv_vault.address,{'from': attacker})

#    console.log(20, 15)
    flash_attack.attack()
    print("attacker initial balance ", attackerInitialBalance)
    assert(attackerInitialBalance + vaultInitialBalance == attacker.balance())
    print("attacker final balance ", attacker.balance())
    assert(adv_vault.balance() == 0)
