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
    struct gradableTrade {
        uint tradeNum ;
        address payable traderAddress ;
        bool open ; //open == True, closed == False
        string symbol ;
        string size ; // use negative for short position
        string entry ; // price, time
        string exit ; // price, time
        //options data //"30-7-2022, 27.20, 1"
        string optionData ; //strike, isCall, expirationTimeStamp
        //Server Functions
        bool Verified ;
    }
    // gradableTrade blankTrade = gradableTrade(
    //     115792089237316195423570985008687907853269984665640564039457584007913129639935, //Nonce (solidity true max int)
    //     address(0), // traderAddress
    //     false, // open
    //     "", // symbol
    //     "", // size
    //     "", // entryPrice
    //     "", // entryTime
    //     "", // exitPrice
    //     "", //exitTime
    //     "", // expirationTimeStamp
    //     "", // strike
    //     false, // isCall
    //     false //Verified
    // );
    modifier onlyTrader {
        require(msg.sender == trader, "You are not the trader associated with this log!");
        _;
    }
    modifier onlyServer {
        require(msg.sender == server, "You are not the server");
        _;
    }
    mapping(uint256 => gradableTrade) public log;
    //might want to do this as well for a permenant record
    // event Logging(uint256 logNum, trade newTrade);
    event newTrade (
        uint TraderId,
        address payable inputTraderAddress,
        uint tradeNum,
        bool inputOpen,
        string inputSymbol,
        string inputSize,
        string inputEntry,
        string inputOptionsData);
    function openTrade (
        address payable inputTraderAddress,
        bool inputOpen,
        string memory inputSymbol,
        string memory inputSize,
        string memory inputEntry,
        string memory inputOptionsData
        ) public onlyTrader {
        log[tradeNum] = gradableTrade(
            tradeNum,
            inputTraderAddress,
            inputOpen,
            inputSymbol,
            inputSize,
            inputEntry,
            "",
            inputOptionsData,
            false
        );
        emit newTrade(
        TraderId,
        inputTraderAddress,
        tradeNum,
        inputOpen,
        inputSymbol,
        inputSize,
        inputEntry,
        inputOptionsData);
        tradeNum ++;
    }
    event newCloseTrade(uint tradeID, string exit);
    function closeTrade(
        uint256 tradeID,
        string memory inputExit
        ) public onlyTrader {
        log[tradeID].exit = inputExit;
        emit newCloseTrade(tradeID, inputExit);
    }
    function setVerification(
        uint tradeID ,
        bool Verification
    ) public onlyServer{
        log[tradeID].Verified = Verification ;
    }
    // function clear_log() public onlyServer {
    //     for(uint256 i=0; i <= tradeNum; i++) {
    //         log[i] = blankTrade;
    //     }
    //     tradeNum = 0;
    // }
    function checkTrader () public view returns(address payable) {
        return (trader);
    }
    function checkServer () public view returns(address payable) {
        return (server);
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
        deployer_address = address(this) ;
        TraderId = 0 ;
    }
    event logCreated(uint TraderId, address newLogAddress);
    function createLog () public returns(address){
        newestTrader = msg.sender;
        TraderId ++ ;
        logger log = new logger(newestTrader, server, TraderId);
        emit logCreated(TraderId, address(log));
        return address(log);
    }
}