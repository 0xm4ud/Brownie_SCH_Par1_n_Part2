from brownie import accounts, Wei, Contract, TokensDepository, rToken, chain, network
from brownie.utils import color

AAVE_ADDRESS = "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9"
UNI_ADDRESS = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"
WETH_ADDRESS = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
#HOLDERS
AAVE_HOLDER = "0x2efb50e952580f4ff32d8d2122853432bbf2e204"
UNI_HOLDER = "0x193ced5710223558cd37100165fae3fa4dfcdc14"
WETH_HOLDER = "0x741aa7cfb2c7bf2a1e7d4da2e3df6a56ca4131f3"

amount1 = 15e18
amount2 = 5231e18
amount3 = 33e18

#@pytest.fixture
# some colors
yellow = color("yellow")
red =color("red")
normal = color("none")
# Checking if connected to network, if not we connect
if not network.is_connected():
    network.connect('mainnet-fork')
    print(yellow,"\r\nTesting at block number:",red,chain[-1].number, "\r\n")
    if not network.is_connected():
        print(yellow,"\r\nSomething went wrong:",red,chain[-1].number, "\r\n")
# yield deployments instantiation
def main():
    deployer = accounts[0]
    yield deployer

    try:
        contractAave = Contract(AAVE_ADDRESS)
        yield contractAave
    except ValueError:
        contractAave = Contract.from_explorer(AAVE_ADDRESS)
        yield contractAave

    try:
        contractUni = Contract(UNI_ADDRESS)
        yield contractUni
    except ValueError:
        contractUni = Contract.from_explorer(UNI_ADDRESS)
        yield contractUni

    try:
        contractWeth = Contract(WETH_ADDRESS)
        yield contractWeth
    except ValueError:
        contractWeth = Contract.from_explorer(WETH_ADDRESS)
        yield contractWeth

    # 3 -NOT NEEDED if you did any of the two above, WHen you have the abi you can get from one of the the two above methods
    #contractAave = Contract.from_abi("AAVE", AAVE_ADDRESS, contractAave.abi)
    #yield contractAave
    #contractUni = Contract.from_abi("UNI", UNI_ADDRESS, contractWeth.abi)
    #yield contractUni
    #contractWeth = Contract.from_abi("WETH", WETH_ADDRESS, contractUni.abi)
    #yield contractWeth
    depository = deployer.deploy(TokensDepository, AAVE_ADDRESS, UNI_ADDRESS, WETH_ADDRESS)
    yield depository

    ## LOAD RECEIPT TOKENS deployed with rTokens.sol
    rtoken_aave = rToken.at(depository.receiptTokens(AAVE_ADDRESS))
    yield rtoken_aave
    rtoken_uni = rToken.at(depository.receiptTokens(UNI_ADDRESS))
    yield rtoken_uni
    rtoken_weth = rToken.at(depository.receiptTokens(WETH_ADDRESS))
    yield rtoken_weth

    ## LOAD VARIABLE DEBT TOKENS deployed with vTokens.sol
    initialAAVEBalance = contractAave.balanceOf(AAVE_HOLDER)
    yield initialAAVEBalance
    initialUNIBalance = contractUni.balanceOf(UNI_HOLDER)
    yield initialUNIBalance 
    initialWETHBalance = contractWeth.balanceOf(WETH_HOLDER)
    yield initialWETHBalance

    #Create alias for HOLDERs accounts
    aaveHolder = accounts.at(AAVE_HOLDER, force=True)
    yield aaveHolder
    uniHolder = accounts.at(UNI_HOLDER, force=True)
    yield uniHolder
    wethHolder = accounts.at(WETH_HOLDER, force=True)
    yield wethHolder


deployer, contractAave, contractUni, contractWeth, depository, rtoken_aave, rtoken_uni, rtoken_weth, initialAAVEBalance, initialUNIBalance, initialWETHBalance, aaveHolder, uniHolder, wethHolder  = main()
