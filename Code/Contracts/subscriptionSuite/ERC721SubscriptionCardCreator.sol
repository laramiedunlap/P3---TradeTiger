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
        string name;
        address TraderContractAddress;
        uint256 cardValue;
        string cardJson;
    }

    mapping(uint => SubscriptionCard) public subscriptionRegistry;
    
    function imageUri(
        uint256 tokenId) public view returns (string memory imageJson){
        return subscriptionRegistry[tokenId].cardJson;
    }

    function registerSubscriptionCard(
        address owner,
        string memory name,
        address TraderContractAddress,
        uint256 purchasePriceUSD,
        string memory tokenURI,
        string memory cardJSON
    ) public returns (uint256) {
        if  //  Registration Hash in newRegistrationHashTable
            //  matches RegistrationHash in off-chain Account Data,
            //  then mint the tokenId
            //  and map to the new subscriber.
        uint256 subscriptionAccessHash = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        subscriptionRegistry[tokenId] = SubscriptionCard(
            name, 
            TraderContractAddress, 
            cardValue, 
            cardJSON);

        return tokenId;
    }
}