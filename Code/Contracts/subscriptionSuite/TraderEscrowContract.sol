pragma solidity 0.8.0;

// This is the model contract to hold the tokens paid by subscribers
// for subscriptions to a Trader.

// It will contain a deployer that deploys a new contract for each new
// Trader License.

contract logger {
    address payable trader;
    address payable server;
    uint256 TraderId;
    uint tradeNum;