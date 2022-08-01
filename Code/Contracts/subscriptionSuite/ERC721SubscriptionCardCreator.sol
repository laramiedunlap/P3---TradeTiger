pragma solidity ^0.8.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/extensions/ERC721Pausable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/extensions/ERC721Enumerable.sol";

// This contract runs when a new subscription is verified and registered.
// In exchange for confirmation that the subscriber has paid the initial 
// subscription access fee, the platform will mint a subscription NFT that 
// acts as a key to gain access to the content behind a Trader's paywall.

// The Trader Subscription Card matches the subscriber to the Trader Escrow Contract
// that they have subscribed to. The Trader Card is an NFT that creates the subscription 
// access hash and also gives ownership rights for the Trader Card to the subscriber. 
// When the subscriber is paying the subscription fee
// the subscription access hash is whitelisted for that particular trader. If the 
// subscriber cancels then the access hash is taken off the white list, but the
// subscriber has purchased the NFT and owns it outright. If the subscription cards
// retain any trading or collectible value then they become an added incentive to use
// the platform.

contract TraderSubscriptionCardRegistry is ERC721, ERC721Enumerable, ERC721Pausable {
    constructor() public ERC721("SubscriptionCards", "CARDS") {}

    struct SubscriptionCard {
        string cardSeries;
        address TraderContractAddress;
        uint256 cardValue;
        string cardJson;
    }

    mapping(uint => SubscriptionCard) public subscriptionRegistry;
    
    function imageUri(
        uint256 subscriptionAccessHash) public view returns (string memory imageJson){
        return subscriptionRegistry[subscriptionAccessHash].cardJson;
    }

    function registerSubscriptionCard(
        address subscriber,
        string memory cardSeries,
        address TraderContractAddress,
        uint256 purchasePriceUSD,
        string memory cardURI,
        string memory cardJSON
    ) public returns (uint256) {
        if  //  Registration Hash in newRegistrationHashTable
            //  matches RegistrationHash in off-chain Account Data,
            //  then mint the subscriptionAccessHash (variant on tokenId)
            //  and map to the new subscriber.
        uint256 subscriptionAccessHash = totalSupply();

        _mint(subscriber, subscriptionAccessHash);
        _setTokenURI(subscriptionAccessHash, cardURI);

        subscriptionRegistry[subscriptionAccessHash] = SubscriptionCard(
            cardSeries, 
            TraderContractAddress, 
            cardValue, 
            cardJSON);

        return subscriptionAccessHash;
    }
}