// This file is my mark up of LD_TigerLogger.sol, since it was the most recently updated version.
// Posting my understanding of the solidity code;
// Proposed stylistic revisions;
// And questions about code for contract walkthrough later.

pragma solidity 0.5.0;

contract logger {
    address payable trader;
    address payable server;
    uint256 TraderId;
    uint tradeNum;

// LK Note to Self: The underscore is a modifier that ensures that only the 
// owner of the contract can call this function.

// LK Questions: 
// -- Checking my understanding: we set this up so each trader is the owner 
//    of their own contract?
// -- How are we creating trader IDs? 
// -- Would it help the functionality to create a separate contract
//    to register traders first and create a unique log ID, and then once 
//    registered they will have access to use/own the logger contract?

    constructor(
        address payable newTrader,
        address payable _server,
        uint _TraderId
    ) public { //Should check ERC20Detailed to be sure I am including all the security
        trader = newTrader;
        server = _server;
        TraderId = _TraderId;
        tradeNum = 0;
    }

// LK: Changed all variables to snake case to keep it consistent
    struct gradableTrade {
        uint tradeNum ;
        address payable traderAddress ;
        bool open ; //open == True, closed == False
        string symbol ;
        int size ; // use negative for short position 
        int fractionalShares ;
// LK: Changed entry price and exit price to strings
        string entryPrice ;
        string exitPrice ;
        uint expirationTimeStamp ;
        uint strike ;
        bool isCall ;

    }

    
    gradableTrade blankTrade = gradableTrade(
        115792089237316195423570985008687907853269984665640564039457584007913129639935, //Nonce (solidity true max int)
        address(0), // traderAddress
        false, // open
        "0", // symbol
        0, // size
        0, // fractional_shares
        0, // entryPrice
        0, // exitPrice
        0, // expirationTimeStamp
        0, // strike
        false // isCall
    );
    
    modifier onlyTrader {
        require(msg.sender == trader, "You are not the trader associated with this log!");
        _;
    }
    
    modifier onlyServer {
        require(msg.sender == server, "You are not the server");
        //Best way to make it so ONLY the server can do this?
        
        _;
    }

// LK Question: 
// -- Checking my understanding: the mapping seems critical to create a usable log. 
//    Looking at our current log files I'm not sure how we would pull the data
//    that we need for queries and grading.

    mapping(uint256 => gradableTrade) public tradeLog;
    //might want to do this as well for a permanant record
    // event Logging(uint256 logNum, trade newTrade);

// LK: Changed inputEntryPrice and inputExitPrice to strings since we can't input floats
    event openTrade (
        uint TraderId,
        address payable inputTraderAddress,
        uint tradeNum, 
        bool inputOpen,
        string inputSymbol,
        int inputSize,
        int inputFractional_shares,
        string inputEntryPrice,
        string inputExitPrice,
        uint inputExpirationTimestamp,
        uint inputStrike,
        bool inputIsCall,
        uint256 timestamp); 
// LK: Checking my understanding: the inputExpirationTimestamp is only for certain types
//     of trades, not all trades?
// LK: Added timestamp to log file.

// LK: Changed inputEntryPrice and inputExitPrice to strings
// LK: Added timestamp
    function add_trade (
        address payable inputTraderAddress,
        bool inputOpen,
        string memory inputSymbol,
        int inputSize,
        int inputFractional_shares,
        string memory inputEntryPrice,
        string memory inputExitPrice,
// LK: Checking my understanding: the expiration date is only for certain types
//     of trades, not all trades?
        uint inputExpirationTimestamp,
        uint inputStrike,
        bool inputIsCall,
// LK: Added block timestamp
        uint256 timestamp
        ) public onlyTrader {
        log[tradeNum] = Gradable_Trade(
            tradeNum,
            inputTraderAddress,
            inputOpen,
            inputSymbol,
            inputSize,
            inputFractional_shares,
            inputEntryPrice,
            inputExitPrice,
            inputExpirationTimeStamp,
            inputStrike,
            inputIsCall
        );
        emit newTrade(
        TraderId,
        inputTraderAddress,
        tradeNum, 
        inputOpen,
        inputSymbol,
        inputSize,
        inputFractional_shares,
        inputEntryPrice,
        inputExitPrice,
        inputExpirationTimeStamp,
        inputStrike,
        inputIsCall, //Might be nice to do
// LK: Adding block timestamp to the log file
        block.timestamp); 

// LK Note to Self: the tradeNum provides a unique identifier for each trade
// Checking my understanding: is that all it is supposed to do or is it intended
// to serve any other functions?
        tradeNum += 1;
    }
    // function closeTrade () {}

// LK Question: is the intent of this function to clear the tradeNum at the
// end of each grading period? And if yes, it seems potentially confusing to
// have trader logs that contain multiple tradeNum 1, 2, 3.. etc. that reset
// every month.
    function clearLog() public onlyServer {
        for(uint256 i=0; i <= tradeNum; i++) {
            log[i] = blankTrade;
        }
        tradeNum = 0;
    }

    // Event -- emit check for server address
    
    
    function checkServer () public view returns(address payable, address payable)  { 
        
        return (server, trader) ;
    }
}

contract deployer {
    
    address public deployer_address;
    address payable server;
    address payable newestTrader;
    uint TraderId ;

    constructor(
    ) public {
        server = msg.sender ;
        deployer_address = address(this);
        TraderId = 0 ; 
    }

    event logCreated(uint TraderId, address newLogAddress);
    
    function createLog () public returns(address){
        newestTrader = msg.sender;
        TraderId += 1 ;
        logger log = new logger(newestTrader, server, TraderId);


        emit logCreated(TraderId, address(log));


        return address(log);


    }
}
