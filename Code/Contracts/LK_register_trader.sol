pragma solidity ^0.5.0;

// Goal is to assign a unique log identifier to each registered trader

// This is the "Art Registry" contract from class but I don't think we need
// a full minting process just to assign a unique log ID to each trader.

import "https://github.com/OpenZeppeLin/openzeppelin-contracts/blob/release-v2.3.0/contracts/token/ERC721/ERC721Full.sol";
contract TraderID is ERC721Full {
    constructor () public ERC721Full ("TraderID", "TraderLog") {}

    function registerTrader(address Trader, string memory TraderURI) public returns (uint256){
        uint256 TraderId = totalSupply();
        _mint(Trader, TraderID);
        _setTokenURI (TraderId, TraderURI);

        return TraderId;
    }
}