from brownie import network, chain, Wei, accounts, GoldExchange, GoldOracle, GoldToken
from brownie.utils import color
from web3 import Web3

sources = [ '0x4aC89064Fa0d03De57f802feC722925b4502572A',
        '0x96574c0392112CbEe134eb77e76A183d54A7c18f',
        '0xA7804BB057EBB7D0c0a3C7F4B8710AE854525fd4'
        ]

EXCHANGE_INITIAL_BALANCE = Wei('1800 ether'); 
INITIAL_GOLD_PRICE = Wei('1.5 ether');


#whaleSigner = accounts.at(WHALE, force=False)
# some colors
yellow = color("yellow")
red =color("red")
normal = color("none")
# Checking if connected to network, if not we connect
if not network.is_connected():
    network.connect('mainnet-fork')
    print(yellow,"\r\nTesting at block number:",red,chain[-1].number, "\r\n")
    if not network.is_connected():
        print(yellow,"\r\nSomething wrong:",red,chain[-1].number, "\r\n")
# yield deployments instantiation
def main():

    [deployer, attacker] = accounts[:2]
    for _ in range(0, 2):
        yield [deployer, attacker][_]

    #yield, user1, user2, user3, attacker
    w3 = Web3(Web3.HTTPProvider())
    w3.provider.make_request("evm_setAccountBalance", [deployer.address, "0x65A4DA25D3016C00000"])
    w3.provider.make_request("evm_setAccountBalance", [attacker.address, "0x1043561A8829300000"])

    for i in range(0, len(sources)):
        w3.provider.make_request("evm_setAccountBalance", [sources[i], "0x8AC7230489E80000"])
        print("source", i, "balance", w3.eth.getBalance(sources[i]))
        assert(w3.eth.getBalance(sources[i]) == 10*10**18)
        
    
    # Deploying the contract
    token = GoldToken.deploy({'from': deployer, 'gas_price': '19 gwei'})
    yield token

    oracle = GoldOracle.deploy(sources, [INITIAL_GOLD_PRICE, INITIAL_GOLD_PRICE, INITIAL_GOLD_PRICE],{'from': deployer, 'gas_price': '19 gwei'})
    yield oracle

    exchange = GoldExchange.deploy(token.address, oracle.address,{'from': deployer, 'gas_price': '19 gwei', 'value': EXCHANGE_INITIAL_BALANCE})
    yield exchange

    initialAttackerBalance = attacker.balance()
    yield initialAttackerBalance


deployer, attacker, token, oracle, exchange, initialAttackerBalance = main()