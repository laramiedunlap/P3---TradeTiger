pragma solidity ^0.5.0;

contract tradeLog{
    address payable trader;
    uint256 traderID;
    uint256 logID;

    constructor(
        address  payable newTrader,
        uint256 _traderID
    ) public {
        trader = newTrader;
        traderID = _traderID;
        logID = 0;
    }

    struct log{
        uint256 logID;
        address payable traderAddress;
        string symbol;
        string price; //sell price with "-", buy price with "+"
        string time;
        string shares; //sell shares with "-", buy shares with "+"
    }

    modifier onlyTrader {
        require(msg.sender == trader, "You are not the owner of this trade.");
        _;
    }

    mapping(uint256 =>log) public tradeLogs;

    event addTrade (
        uint256 logID,
        address payable newTraderAddress,
        uint256 traderID,
        string newSymbol,
        string newPrice,
        string newTime,
        string newShares);

    function makeTrade(
        address payable newTraderAddress,
        string memory newSymbol ,
        string memory newPrice,
        string memory newTime,
        string memory newShares
        ) public onlyTrader {
        tradeLogs[logID] = log(logID, newTraderAddress,newSymbol,newPrice,newTime,newShares);
        emit addTrade(logID,newTraderAddress,traderID,newSymbol,newPrice,newTime,newShares);
        logID ++;
        }
}

contract tradeDeployer {
    address payable newTrader;
    uint traderID ;
    constructor(
    ) public {
        traderID = 0 ;
    }
    event moreTrader(uint traderID);
    function addTrader () public returns(uint256){
        newTrader = msg.sender;
        traderID ++ ;
        emit moreTrader(traderID);
        return (traderID);
    }
}
