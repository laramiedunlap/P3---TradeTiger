pragma solidity ^0.8.0;

// This is a simulated bank account for the purposes of this project.
// The bank account receives subscription fees from subscribers in USD,
// confirms receipt to TTToken, stores subscriptions, and disburses them
// at the end of the grading period.

// This contract can be basic because it's a dummy for an actual bank account.

contract BankAccount {
    address payable accountOwner = TTaccountNumber;

    /*
    * The receiveSubscriptionPayments function should take in all
    * subscription payments (in simulated USD) and print an event log
    * confirming that funds from the subscriber address have been received.
    * The bank account stores the subscriber fees in a pool until ready
    * to be disbursed.
    * The TTTokens are representations of these USD assets.
    */
    function receiveSubscriptionPayments() public payable {}
    // Add event log


    /*
    * The routeMintingPayments function should take in all
    * minting payments (in simulated USD) and print an event log
    * confirming that a one-time minting payment from the subscriber address 
    * has been received.
    * The bank account then immediately disburses the funds according to the
    * agreed-upon distribution percentage: a portion to the Trader, and a portion
    * to the Trade Tiger platform. 
    * These funds are always in USD, and never converted to TTToken.
    */
    function routeMintingPayments() public payable {}
    // Add event log - if necessary?
    // Add routers


    /*
    * The disbursePayments function should be triggered
    * on a fixed date every month after the grading period ends.
    * At that time the bank account will receive information about how
    * the funds will be disbursed from the TTTokens and Grading contract.
    * Subscribers and Traders can then choose to receive money in USD,
    * or to keep the money in TTToken to use more easily on the platform.
    */
    function withdraw(uint amount, address payable recipient) public {
        require(recipient == accountOwner, "You don’t own this account!");
        return recipient.transfer(amount);
    }
    // Decide if we need any more functionality than just abilit to withdraw.

    function() external payable {}
}
