pragma solidity 0.5.0;

contract logger {
    address payable trader;
    address payable server;
    uint256 TraderId;
    uint tradeNum;


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

    struct Gradable_Trade {
        uint tradeNum ;
        address payable traderAddress ;
        bool open ; //open == True, closed == False
        string symbol ;
        int size ; // use negative for short position 
        int fractional_shares ;
        uint entryPrice ;
        uint exitPrice ;
        uint expirationTimeStamp ;
        uint strike ;
        bool isCall ;

    }

    
    Gradable_Trade blankTrade = Gradable_Trade(
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


    mapping(uint256 => Gradable_Trade) public log;
    //might want to do this as well for a permenant record
    // event Logging(uint256 logNum, trade newTrade);

    event newTrade (
        uint TraderId,
        address payable inputTraderAddress,
        uint tradeNum, 
        bool inputOpen,
        string inputSymbol,
        int inputSize,
        int inputFractional_shares,
        uint inputEntryPrice,
        uint inputExitPrice,
        uint inputExpirationTimeStamp,
        uint inputStrike,
        bool inputIsCall); 

    function add_trade (
        address payable inputTraderAddress,
        bool inputOpen,
        string memory inputSymbol,
        int inputSize,
        int inputFractional_shares,
        uint inputEntryPrice,
        uint inputExitPrice,
        uint inputExpirationTimeStamp,
        uint inputStrike,
        bool inputIsCall
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
        inputIsCall); //Might be nice to do

        tradeNum += 1;
    }
    // function closeTrade () {}

    function clear_log() public onlyServer {
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
