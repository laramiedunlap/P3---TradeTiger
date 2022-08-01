pragma solidity ^0.8.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/extensions/ERC721Pausable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/extensions/IERC721Metadata.sol";

// This contract runs when a new Trader registers on the platform and registers
// a new Trader License (NFT hash). The license will give the Trader access to the 
// Escrow Contract that holds the Trader's trade log and subscription tokens.

// Once payment is verified by the Registration Manager, the platform will deploy 
// the Trader's Escrow Contract.

// The Trader License can be revoked for violations of policy, and the Trader would
// be locked out of access to the Trader Escrow Contract.

contract TraderSubscriptionCardRegistry is ERC721, ERC721Enumerable, ERC721Pausable {
    constructor() public ERC721("TraderLicense", "TLIC") {}

    struct TraderLicense {
        string TraderName;
        string TraderCredentials;
        address TraderContractAddress;
        string cardJson;
    }

    mapping(uint => TraderLicense) public licenseRegistry;
    
    function imageUri(
        uint256 traderAccessHash) public view returns (string memory imageJson){
        return subscriptionRegistry[traderAccessHash].cardJson;
    }

    function registerTraderLicense(
        address Trader,
        string memory cardSeries,
        address TraderContractAddress,
        string memory cardURI,
        string memory cardJSON
    ) public returns (uint256) {
        if  //  Registration Hash in newRegistrationHashTable
            //  matches RegistrationHash in off-chain Account Data,
            //  then mint the subscriptionAccessHash (variant on tokenId)
            //  and map to the new subscriber.
        uint256 traderAccessHash = totalSupply();

        _mint(Trader, traderLicenseId);
        _setTokenURI(traderLicenseId, cardURI);

        subscriptionRegistry[traderLicenseId] = TraderLicense(
            TraderName, 
            TraderCredentials,
            TraderContractAddress, 
            cardJSON);

        return traderLicenseId;
    }
}
