pragma solidity ^0.8.0;

import "https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/KeeperCompatible.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol";


// The Registration Manager takes in a user's address and uses 
// Chainlink code to check the Account Data CSV to verify that 
// the user has paid the correct subscription fees.

// If the fees are verified, the user can obtain the permission
// keys that they have paid to receive.

// As an initial step, the Registration Manager will turn all 
// the user intake data into registration hash.


// Verify Payment Contract aims to use the customer's address
// and the off-chain transactionID to verify that the status
// of the payment transaction is complete. The Account Data
// oracle will need to include a field that returns true if
// the transaction is complete, and false if it is any other status.
// This code was modeled off the stackoverflow answer here:
// https://stackoverflow.com/questions/70752272/how-to-communicate-with-any-given-chain-from-smart-contract


contract registerSubscriber is  KeeperCompatible {
    constructor() public {}

    address oracleAccountData = address(0x123);

    mapping(address => string) public newRegistrationHashTable;


//  This function is intended to check our off-chain Account Data
//  to verify that the "Payment Complete" = true.
    function requestPaymentCheck(
        address customerAddress, 
        uint128 transactionID, 
        bool paymentComplete) external {
        (bool success, ) = oracleAccountData.call(
            abi.encode(
                customerAddress, 
                transactionID, 
                paymentComplete=true));
        require(success);
    }

    function callback(bool result) external {
        require(msg.sender == oracleAccountData, "This function can be invoked only by the oracle");
    }

//  If the off-chain payment if verified, this function is intended to map 
//  the latest Registration Hash to the user's address to allow us to check 
//  it later and verify that the latest registration is payment verified.
    function newRegistrationHash(
        address customerAddress, 
        uint128 transactionID, 
        bool paymentComplete) public pure returns (bytes32) {
            if (requestPaymentCheck=true) {
            newRegistrationHashTable[customerAddress] = keccak256(abi.encode(
                customerAddress,
                transactionID,
                paymentComplete=true));
        }

}

// Except for verifying that the address is a valid ethereum address,
// this entire contract might be better handled in the Account Data oracle,
// off-chain. Maybe this contract would function to add a marker to the 
// Account Data showing that the address is verified.

// The database storing the Account Data could automatically hash the values
// once the payment is finalized and create a Registration Hash to store in the
// Account Data oracle. Then that Registration Hash would serve as confirmation
// that the payment was verified and would allow the rest of the Creators to run.

// LATER NOTE: this contract had originally included code to validate
// the user's address, but we can use web3.js to check if a contract is valid
// when the user inputs the information on the front end.
// see: https://github.com/joshstevens19/ethereum-bloom-filters/blob/master/README.md#isuserethereumaddressinbloom


