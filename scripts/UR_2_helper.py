import brownie
from brownie import network, chain, Escrow, EscrowNFT, Wei, accounts
from brownie.utils import color
from web3 import Web3


ONE_MONTH = 30 * 24 * 60 * 60;

USER1_ESCROW_AMOUNT = Wei('10 ether'); # 10 ETH
USER2_ESCROW_AMOUNT = Wei('54 ether'); # 54 ETH
USER3_ESCROW_AMOUNT = Wei('72 ether'); # 72 ETH



#whaleSigner = accounts.at(WHALE, force=False)
# some colors
yellow = color("yellow")
red =color("red")
normal = color("none")
# Checking if connected to network, if not we connect
if not network.is_connected():
    network.connect('development')
    print(yellow,"\r\nTesting at block number:",red,chain[-1].number, "\r\n")
    if not network.is_connected():
        print(yellow,"\r\nSomething wrong:",red,chain[-1].number, "\r\n")
# yield deployments instantiation
def main():
    [deployer, user1, user2, user3, attacker] = accounts[:5]
    for _ in range(0, 5):
        yield [deployer, user1, user2, user3, attacker][_]


    w3 = Web3(Web3.HTTPProvider())
    w3.provider.make_request( "evm_setAccountBalance" , [deployer.address, "0x1BC16D674EC80000"])
    yield w3
    #The evm_setAccountBalance rpc-json call equivalent in hardhat is hardhat_setBalance

    # Deploy NFT
    escrowNFT = EscrowNFT.deploy({'from': deployer})
    yield escrowNFT
    # Deploy Escrow
    escrow = Escrow.deploy(escrowNFT.address,{'from': deployer})
    yield escrow

    # Transfer ownership of NFT contrct to Escrow contract
    escrowNFT.transferOwnership(escrow.address,{'from': deployer})

    attackerInitialBalance = attacker.balance()
    yield attackerInitialBalance



deployer, user1, user2, user3, attacker, w3, \
escrowNFT, escrow, attackerInitialBalance = main()