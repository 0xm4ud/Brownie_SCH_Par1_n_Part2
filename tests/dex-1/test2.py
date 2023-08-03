from brownie import accounts, Chocolate, Wei, Contract, interface
import pytest


class Test_Chocolate_Swap:
    INITIAL_MINT = Wei('1000000 ether'); 

    deployer = accounts.add()
    accounts.add()
    accounts.add()
    user = accounts[1]
    user2 = accounts[2]

    @pytest.fixture(scope="module", autouse=False)
    def setup(self):

        WETH_ADDRESS = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
        RICH_SIGNER = "0x8eb8a3b98659cce290402893d0123abb75e3ab28"
        ETH_BALANCE = Wei('300 ether'); 

        richSigner = accounts.at(RICH_SIGNER, force=True)
        richSigner.transfer(self.deployer, ETH_BALANCE)

        weth = Contract(WETH_ADDRESS)

        return weth


    @pytest.fixture(scope="module", autouse=False)
    def test_dep_choco(self, setup):

        choco = Chocolate.deploy(self.INITIAL_MINT,{'from': self.deployer})
        pair = interface.IUniswapV2Pair(choco.uniswapV2Pair())

        print("\r\n\x1b[0;31mPair address at: \x1b[0;34m",pair)

        return choco, pair

    global NONCE
    NONCE = 0
    def test_deployer_add_liquidity(self, test_dep_choco):
        INITIAL_LIQUIDITY = Wei('100000 ether');
        ETH_IN_LIQUIDITY = Wei('100 ether');

        choco, pair = test_dep_choco[:2]

        choco.approve(choco.address, INITIAL_LIQUIDITY)
        choco.addChocolateLiquidity(INITIAL_LIQUIDITY, {'value': ETH_IN_LIQUIDITY});
        global NONCE
        if NONCE == 0:
            print("\r\n\x1b[0;31mLP Tokens deployer balance: \x1b[0;34m", pair.balanceOf(self.deployer.address));
            NONCE =NONCE +1
        else:
            pass

    def test_user_swap(self, setup, test_dep_choco):
        choco = test_dep_choco[0]
        weth = setup
        user= accounts[0]

        HUNDRED_CHOCOLATES = Wei("100 ether")
        TEN_ETH = Wei('10 ether');

        userChocolateBalance = choco.balanceOf(user)
        userWETHBalance = weth.balanceOf(user)

        choco.swapChocolates(weth.address, TEN_ETH, {'value': '10 ether','from': user})
        assert(userChocolateBalance < choco.balanceOf(user))

        choco.swapChocolates(choco.address, HUNDRED_CHOCOLATES, {'from': user})
        assert(userWETHBalance < weth.balanceOf(user))

    def test_remove_liquidity(self, test_dep_choco):
        deployer = self.deployer
        choco, pair = test_dep_choco[:2]

        self.test_deployer_add_liquidity(test_dep_choco)
        LP_TOKENS_LIQUIDITY = pair.balanceOf(deployer.address)

        pair.approve(choco.address, LP_TOKENS_LIQUIDITY //2, {'from': deployer});
        choco.removeChocolateLiquidity(pair.balanceOf(deployer.address) //2).wait(1);

        assert(LP_TOKENS_LIQUIDITY > pair.balanceOf(deployer.address))
