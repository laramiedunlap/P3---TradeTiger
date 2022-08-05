pragma solidity ^0.8.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol";

// Subscription fees will be collected in USD or 1 to 1 USD equivalent 
// and placed in a bank account.

// At least initially, the majority of subscription fees are expected to be 
// collected through traditional fiat channels (i.e. paypal). 
// The platform will also be set up to collect cryptocurrencies but will
// target USD first in order to build trust with a broader audience.

// A token is still necessary to represent the stored USD on the blockchain.

// The TTToken contract creates tokens that represent 1:1 the dollars that a
// subscriber has deposited when it is triggered by a confirmation message 
// from the business bank account. The 1:1 representative tokens are then 
// transferred to the subscriber, first, to make the record that the money started with
// them. Then the tokens move directly into the escrow contract of the Trader that
// the subscriber is following.

contract TTToken is ERC20 {
    constructor() ERC20("TTToken", "TTT") {}

    modifier onlyServer {
        require(msg.sender == server, "You are not the server");
        _;
    }

//  Add function to collect verified subscription payment information from the 
//  Account Manager Oracle and mint tokens in a 1:1 USD to token ratio, and
//  then transfer (first) to subscriber, and (second) automatically re-route
//  to the Trader Escrow Contract that the subscriber has subscribed to.
    function mintSubscriptionTokens() public {
        _mint()
    }
}
