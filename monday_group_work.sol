pragma solidity ^0.5.0; 

contract gradeable_trades {

    address payable traderAddress ;

    struct trade {
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
    
        modifier onlyTrader {
            require(msg.sender == traderAddress)
        }

    function add_open_trade public onlyTrader(trade) {

    }

    function close_open_trade {

    }


}