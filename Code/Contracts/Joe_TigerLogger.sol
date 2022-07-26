pragma solidity 0.5.0;

contract logger {
    address payable trader;
    uint256 number_of_trades;

    struct Gradable_Trade {
        uint Nonce ;
        address payable traderAddress ;
        bool open ; //open == True, closed == False
        string symbol ;
        int size ; // use negative for short position 
        int fractional_shares ;
        uint entryPrice ;
        uint exitPrice ;
        // bool long ; // keeping shares non-negative
        // bool isOption ; 
        uint expirationTimeStamp ;
        uint strike ;
        bool isCall ; 
    }

    mapping(uint256 => Gradable_Trade) public log;
    //might want to do this as well for a permenant record
    // event Logging(uint256 logNum, trade newTrade);

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
        //Best way to make it so ONLY the server can do this?
        // require(msg.sender == server, "Only the server can clear the logs");
        _;
    }

    constructor(
        address payable newTrader
    ) public { //Should check ERC20Detailed to be sure I am including all the security
        trader = newTrader;
        number_of_trades = 0;
    }


    function add_trade(
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
        log[number_of_trades] = Gradable_Trade(
            number_of_trades,
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
        // emit Logging(number_of_trades, trade); //Might be nice to do
        number_of_trades += 1;
    }

    function clear_log() public onlyServer {
        for(uint256 i=0; i <= number_of_trades; i++) {
            log[i] = blankTrade;
        }
        number_of_trades = 0;
    }
}

contract deployer {
    address public log_address;


    constructor(
        address payable trader
    ) public {
        logger log = new logger(trader);
    }
}