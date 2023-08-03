from brownie import accounts, RedHawksVIP, network, chain
from eth_account.messages import *
from web3 import Web3


def test_replay_3():
    web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))

    dep = accounts.add()
    attacker = accounts.add()
    vouchersSigner = accounts.add()


    test = RedHawksVIP.deploy(vouchersSigner.address, {'from': dep})

    domain = {
        'chainId': chain.id,
        'verifyingContract': web3.toChecksumAddress(test.address),
    }
    types = {
        'VoucherData': [
            {'name': 'amountOfTickets', 'type': 'uint256'},
            {'name': 'password', 'type': 'string'},
        ],
    }
    data_to_sign = {
        'amountOfTickets': 2,
        'password': "RedHawksRulzzz133",
    }

    typed_data = {
        'types': {
            'EIP712Domain': [
                {'name': 'chainId', 'type': 'uint256'},
                {'name': 'verifyingContract', 'type': 'address'},
            ],
            **types
        },
        'domain': domain,
        'primaryType': 'VoucherData',
        'message': data_to_sign,
    }


    encoded_data = encode_structured_data(typed_data)

    sigx1 = web3.eth.account.sign_message(encoded_data, vouchersSigner.private_key)

    test.mint(2, "RedHawksRulzzz133", sigx1.signature.hex(), {'from': attacker.address})



    hey = SignableMessage(version=b'E', header='thereum Signed Message:\n', body=encoded_data.body)
