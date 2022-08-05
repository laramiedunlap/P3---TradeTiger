pragma solidity 0.8.0;

// This is the model contract to hold the tokens paid by subscribers
// for subscriptions to a Trader.

// It will contain a deployer that deploys a new contract for each new
// Trader License.

contract TraderEscrow {
    address payable trader;
    address payable server;
    uint256 TraderLicenseId;
    uint tradeNum;

contract paymentSplitter {
    address payable [] public recipients;

    constructor(address payable [] memory _addrs) {
        for (uint i=0; i<_addrs.length; i++){
            recipients.push(_addrs[i]);
        }
    }

    receive() payable external {}
}