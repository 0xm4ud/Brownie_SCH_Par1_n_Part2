from scripts.erc20_2_helper import *

#@pytest.fixture
def test_deposit():
    #Assigning variables
    #Setting amount variables

    # Approve allowance
    contractAave.approve(depository.address, amount1, {'from': aaveHolder})
    contractUni.approve(depository.address, amount2, {'from': uniHolder})
    contractWeth.approve(depository.address, amount3, {'from': wethHolder})
    #Check Allowance to be sure
    assert(contractAave.allowance(aaveHolder, depository.address) == amount1)
    assert(contractUni.allowance(uniHolder, depository.address) == amount2)
    assert(contractWeth.allowance(wethHolder, depository.address) == amount3)
    # DEPOSIT
    depository.deposit(AAVE_ADDRESS, amount1, {'from': aaveHolder})
    depository.deposit(UNI_ADDRESS, amount2, {'from': uniHolder})
    depository.deposit(WETH_ADDRESS, amount3, {'from': wethHolder})
    #Check balance
    assert(contractAave.balanceOf(depository.address) == amount1)
    assert(contractUni.balanceOf(depository.address) == amount2)
    assert(contractWeth.balanceOf(depository.address) == amount3)

    # CHeck RECEIPT token balance of the holders
    assert(rtoken_aave.balanceOf(aaveHolder) == amount1)
    assert(rtoken_uni.balanceOf(uniHolder) == amount2)
    assert(rtoken_weth.balanceOf(wethHolder) == amount3)

    ####### WITHDRAW
def test_withdraw():

    depository.withdraw(AAVE_ADDRESS, amount1, {'from': aaveHolder})
    depository.withdraw(UNI_ADDRESS, amount2, {'from': uniHolder})
    depository.withdraw(WETH_ADDRESS, amount3, {'from': wethHolder})

    # Checking balances
    assert(contractAave.balanceOf(aaveHolder) == initialAAVEBalance)
    assert(contractUni.balanceOf(uniHolder) == initialUNIBalance)
    assert(contractWeth.balanceOf(wethHolder) == initialWETHBalance)

    # Check if depository burned the RECEIPT tokens
    assert(rtoken_aave.balanceOf(depository.address) == 0)
    assert(rtoken_uni.balanceOf(depository.address) == 0)
    assert(rtoken_weth.balanceOf(depository.address) == 0)