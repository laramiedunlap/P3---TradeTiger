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

// The Trader License NFT will also contain the trade information and update the log file
// with an event

contract TraderSubscriptionCardRegistry is ERC721, ERC721Enumerable, ERC721Pausable {
    constructor() public ERC721("TraderLicense", "TLIC") {}

    struct TraderLicense {
        string name;
        string TraderCredentials;
        address TraderContractAddress;
        uint tradeId;
        bool open;
        string symbol;
        string shares;
        string entryPrice;
        string entryTime;
        string exitPrice;
        string exitPrice;
        bool isCall;
        string expirationTimeStamp;
        string strikePrice;
        string licenseJson;
    }

    mapping(uint => TraderLicense) public licenseRegistry;

    event Trade(
        uint256 tokenId, 
        uint tradeId,
        bool open,
        string symbol,
        string shares,
        string entryPrice,
        string entryTime,
        string exitPrice,
        string exitPrice,
        bool isCall,
        string expirationTimeStamp,
        string strikePrice,
        string reportURI, 
        string licenseJson)
    
    function imageUri(
        uint256 tokenId) public view returns (string memory imageJson){
        return subscriptionRegistry[tokenId].cardJson;
    }

    function registerTraderLicense(
        address Trader,
        string memory name,
        address TraderContractAddress,
        string memory tokenURI,
        string memory cardJSON
    ) public returns (uint256) {
        if  //  Registration Hash in newRegistrationHashTable
            //  matches RegistrationHash in off-chain Account Data,
            //  then mint the subscriptionAccessHash (variant on tokenId)
            //  and map to the new subscriber.
        uint256 tokenId = totalSupply();

        _mint(Trader, traderLicenseId);
        _setTokenURI(traderLicenseId, tokenURI);

        subscriptionRegistry[traderLicenseId] = TraderLicense(
            TraderName, 
            TraderCredentials,
            TraderContractAddress, 
            cardJSON);

        return traderLicenseId;
    }

        function logTrade(
        bool open;
        string symbol;
        string shares;
        string entryPrice;
        string entryTime;
        string exitPrice;
        string exitPrice;
        bool isCall;
        string expirationTimeStamp;
        string strikePrice;
        
        ) public returns (uint256) {
            artCollection[tokenId].appraisalValue = newAppraisalValue;

            emit Appraisal(tokenId, newAppraisalValue, reportURI, tokenJSON);

            return (artCollection[tokenId].appraisalValue);
    }
}
