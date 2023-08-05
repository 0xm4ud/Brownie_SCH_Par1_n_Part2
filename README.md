# Brownie-SCH-Part2
Note: few re-Naming conventions were applied here to avoid Brownie infamous NameSpace collision that should be addressed on v2.0.
```
Structure:
/hardhat - holds console.sol
/tests - Contain test files used to test n hack contracts
/script - Contains Helper scripts used by the test files 
/interfaces - Contains the interfaces used by the Contracts
/Contracts - Contains all the contracts for the course
```
Notes:
In the Second part, there are a few different forks we are going to be running tests on.


```
dex-1/dex-2
--------------------------------------------------------------------
NOTE: Let's add a network forked on 16776127, to make things easier

brownie networks add development mainnet-fork-1 cmd=ganache-cli host=http://127.0.0.1 fork=RPC_URL@15969633 accounts=10 mnemonic=brownie port=8545

brownie test tests/dex-1/test19.py -s --disable-warnings --network mainnet-fork-1
```


```
mm-1 /
NOTE: Let's add a network forked on 16776127, to make things easier

brownie networks add development mainnet-fork-2 cmd=ganache-cli host=http://127.0.0.1 fork=RPC_URL@16776127 accounts=10 mnemonic=brownie port=8545

run test:
brownie test tests/mm-1/test23.py -s --disable-warnings --network mainnet-fork-2

```
