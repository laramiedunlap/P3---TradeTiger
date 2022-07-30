pragma solidity 0.5.0;

contract logger {
    address payable trader;
    uint256 traderID;
    address payable server;
    uint256 number_of_trades;
    uint256 subscriptionCost_inWei;
    uint256 number_of_subscribers;
    mapping(uint256 => address) public subscribers;

    constructor(
        address payable newTrader,
        address payable _server,
        uint256 _traderID
    ) public { //Should check ERC20Detailed to be sure I am including all the security
        trader = newTrader;
        traderID = _traderID;
        server = _server;
        number_of_trades = 0;
        number_of_subscribers = 0;
        subscriptionCost_inWei = 3065346022;
    }
    
    modifier onlyTrader {
        require(msg.sender == trader, "You are not this logs trader!");
        _;
    }
    modifier onlyServer {
        require(msg.sender == server, "You are not the server!");
        _;
    }

    struct Gradable_Trade {
        uint TradeId ;
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
    mapping(uint256 => Gradable_Trade) public log;

    function open_trade(
        address payable inputTraderAddress,
        bool inputOpen,
        string memory inputSymbol,
        int inputSize,
        int inputFractional_shares,
        uint inputEntryPrice,
        uint inputExpirationTimeStamp,
        uint inputStrike,
        bool inputIsCall
        ) public onlyTrader {
        log[number_of_trades] = Gradable_Trade(
            number_of_trades,
            inputTraderAddress,
            inputOpen,
            inputSymbol,
            inputSize,
            inputFractional_shares,
            inputEntryPrice,
            0,
            inputExpirationTimeStamp,
            inputStrike,
            inputIsCall
        );
        number_of_trades++;
    }
    function close_trade(
        uint256 tradeID,
        uint inputExitPrice
        ) public onlyTrader {
        log[tradeID].exitPrice = inputExitPrice;
        // emit Logging(number_of_trades, trade); //Might be nice to do
        number_of_trades++;
    }

    function clear_log() public onlyServer {
        for(uint256 i=0; i < number_of_trades; i++) {
            log[i] = blankTrade;
        }
        number_of_trades = 0;
    }

    function checkTrader () public view returns(address payable) {
        return (trader);
    }
    function checkServer () public view returns(address payable) {
        return (server);
    }

    // returning/sharing mappings is a bit tricky, not impossible but tricky, saving challenge for later
    // function viewLog() public view returns(mapping(uint256 => Gradable_Trade)) {
    //     //This should ONLY be executable by the Trader OR a Subscriber...
    //     return log;
    // }
    // function checkSubscribers () public view returns(mapping(uint256 => address)) {
    //     return (subscribers);
    // }

    function checkSubscriptionNumbers () public view returns(uint256) {
        return (number_of_subscribers);
    }
    function addSubscriber() public {
        //Transfer subscription amount to Logger
        subscribers[number_of_subscribers];
        number_of_subscribers++;
    }
    function clearSubscriber() public onlyServer {
        for(uint256 i=0; i < number_of_subscribers; i++) {
            subscribers[i] = address(0);
        }
        number_of_subscribers = 0;
    }
}

contract deployer {
    address public deployer_address;
    address payable server;
    address payable newestTrader;
    uint TraderID ;

    constructor(
    ) public {
        server = msg.sender ;
        deployer_address = address(this);
        TraderID = 0 ; 
    }

    event logCreated(uint TraderID, address newLogAddress);
    
    function createLog () public returns(address){
        newestTrader = msg.sender;
        TraderID ++ ;
        logger log = new logger(newestTrader, server, TraderID);


        emit logCreated(TraderID, address(log));


        return address(log);


    }
}