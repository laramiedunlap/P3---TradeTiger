pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/IERC721.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Mintable.sol";

// This contract runs when a new subscription is registered.
// In exchange for a flat card minting purchase fee, the platform
// will mint a subscription NFT that acts as a key to gain access to the
// content behind a Trader's paywall.

// In conjunction with the Trader the platform issues a "subscription card,"
// similar to a trading card, that serves to create the subscription access hash
// but also as a collectible. When the subscriber is paying the subscription fee
// the subscription access hash is whitelisted for that particular trader. If the 
// subscriber cancels then the access hash is taken off the white list, but the
// subscriber has purchased the NFT and owns it outright. If the subscription cards
// retain any trading or collectible value then they become an added incentive to use
// the platform.

contract registerSubscription is ERC721Full {
    constructor() public ERC721Full("SubscriptionKey", "KEY") {}

    struct SubscriptionKey {
        name cardName;
        address subscriberAddress;
        address traderAddress;
        uint256 initialValueUSD;
        string subscriptionTimeStamp;
        string artJson;
    }

    mapping(uint256 => SubscriptionKey) public subscriptionRegistry;
    
    function imageUri(
        uint256 tokenId

    ) public view returns (string memory imageJson){
        return subscriptionRegistry[tokenId].artJson;
    }


    function registerSubscription(
        address owner,
        string memory cardName,
        address traderAddress,
        uint256 initialValueUSD,
        string memory tokenURI,
        string memory tokenJSON
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        subscriptionRegistry[tokenId] = Artwork(cardName, traderAddress, initialValueUSD, tokenJSON);

        return tokenId;
    }