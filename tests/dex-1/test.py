from brownie import accounts, Chocolate, Wei, Contract, interface
import pytest


@pytest.fixture(scope="module", autouse=False)
def setup():

    WETH_ADDRESS = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
    RICH_SIGNER = "0x8eb8a3b98659cce290402893d0123abb75e3ab28"
    ETH_BALANCE = Wei('300 ether'); 
    INITIAL_MINT = Wei('1000000 ether'); 

    deployer = accounts[0]

    richSigner = accounts.at(RICH_SIGNER, force=True)
    richSigner.transfer(deployer, ETH_BALANCE).wait(1)

    weth = Contract(WETH_ADDRESS)

    return  weth, INITIAL_MINT, deployer, richSigner

global NONCE
NONCE = 0
@pytest.fixture(scope="function", autouse=False)
def test_dep_choco(setup):
    [weth, INITIAL_MINT, deployer] = setup[:3]

    choco = Chocolate.deploy(INITIAL_MINT,{'from': deployer})
    pair = interface.IUniswapV2Pair(choco.uniswapV2Pair())

    global NONCE
    if NONCE == 0:
        print("\r\n\x1b[0;31mPair address at: \x1b[0;34m",pair)
        NONCE =NONCE +1
    else:
        pass
    return choco, pair, NONCE

global NONCE1
NONCE1 = 0
def test_deployer_liquidity(setup, test_dep_choco):
    INITIAL_LIQUIDITY = Wei('100000 ether');
    ETH_IN_LIQUIDITY = Wei('100 ether');

    deployer = setup[2]

    choco, pair = test_dep_choco[:2]

    choco.approve(choco.address, INITIAL_LIQUIDITY).wait(1)
    choco.addChocolateLiquidity(INITIAL_LIQUIDITY, {'value': ETH_IN_LIQUIDITY}).wait(1);

    global NONCE1
    if NONCE1 == 0:
        print("\r\n\x1b[0;31mLP Tokens deployer balance: \x1b[0;34m", pair.balanceOf(deployer.address), "\r\n");
        NONCE1 =NONCE1 +1
    else:
        pass
    return NONCE
#global NONCE
def test_user_swap(setup, test_dep_choco):
    user = accounts[4]
    choco = test_dep_choco[0]
    weth = setup[0]
    
    #Add liquidity
    test_deployer_liquidity(setup, test_dep_choco)

    HUNDRED_CHOCOLATES = Wei("100 ether")
    TEN_ETH = Wei('10 ether');

    userChocolateBalance = choco.balanceOf(user)
    userWETHBalance = weth.balanceOf(user)

    choco.swapChocolates(weth.address, TEN_ETH, {'value': '10 ether','from': user})
    assert(userChocolateBalance < choco.balanceOf(user))

    choco.swapChocolates(choco.address, HUNDRED_CHOCOLATES, {'from': user})
    assert(userWETHBalance < weth.balanceOf(user))


    print("\r\n\x1b[0;31mFinal userChocolateBalance: \x1b[0;34m", choco.balanceOf(user))
    print("\r\n\x1b[0;31mFinal userWETHBalance: \x1b[0;34m", weth.balanceOf(user), "\r\n")


def test_remove_liquidity(setup, test_dep_choco):
    deployer =setup[2]
    choco, pair = test_dep_choco[:2]

    test_deployer_liquidity(setup, test_dep_choco)
    LP_TOKENS_LIQUIDITY = pair.balanceOf(deployer.address)

    pair.approve(choco.address, LP_TOKENS_LIQUIDITY//2, {'from': deployer});
    choco.removeChocolateLiquidity(LP_TOKENS_LIQUIDITY //2).wait(1);
    assert(LP_TOKENS_LIQUIDITY > pair.balanceOf(deployer.address))
