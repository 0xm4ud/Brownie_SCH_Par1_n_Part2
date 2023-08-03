from web3 import Web3
from brownie import DonationMaster, MultiSigSafe,accounts, chain, Wei, reverts


#@pytest.fixture
def test_successfull_minting_tests():
    green ='\x1b[0;32m'
    red='\x1b[0;31m'
    nocolor='\x1b[0;m'
    print(chain[-1].number)

    ONE_ETH = Wei('1 ether'); # 100 ETH
    HUNDRED_ETH = Wei('100 ether'); # 100 ETH
    THOUSAND_ETH = Wei('1000 ether'); # 100 ETH


    [deployer, user1, user2, user3] = accounts[1:5]
    w3 = Web3(Web3.HTTPProvider())
    #2.5 ETH (ETH -> WEI -> Hexdecimal)
    w3.provider.make_request("evm_setAccountBalance", [deployer.address, "0x90e40fbeea1d3a4abc8955e946fe31cdcf66f634e1000000000000000000"])

    donationMaster = DonationMaster.deploy({'from': deployer})
    multiSig = MultiSigSafe.deploy([user1.address, user2.address, user3.address], 2,{'from': deployer})

    # New donation works
    donationMaster.newDonation(multiSig.address, HUNDRED_ETH)
    donationId = donationMaster.donationsNo() - 1
    # Donating to multisig wallet works
    donationMaster.donate(donationId, {'value': ONE_ETH})

    #Validate donation details
    donationInfo = donationMaster.donations(donationId)
    assert(donationInfo['id'] == donationId)
    assert(donationInfo['to'] == multiSig.address)
    assert(donationInfo['goal'] == HUNDRED_ETH)
    assert(donationInfo['donated'] == ONE_ETH)

    with reverts("Goal reached, donation is closed"):
        donationMaster.donate(donationId, {'from': deployer, 'value': THOUSAND_ETH, 'gas_price': '1 ether'})

    #checking balance of multisig wallet
    assert(multiSig.balance() == '1 ether')
