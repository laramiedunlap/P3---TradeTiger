# Exchangable Trading Platform
    # This can/should be its own .py file
from Libraries.alpaca import alpaca
from Libraries.misc import list_to_string
import pandas as pd
trade_platforms = {
    "simulation": "Simulation",
    "alpaca" : "Alpaca",
    "tda": "TD Ameritrade"
}

# TradePlatform Classes
class tradingPlatform :
    contract = None
    def __init__(self, platformType, contract):
        self.contract = contract
        self.platform = platformType
    platform = None
    def __hello__(self):
        return f"This is a {self.platform} trading platform."
    def openTrade(self,TraderAddress,TraderID,Open,Symbol,Size,EntryPrice,EntryTime,ExpirationTimeStamp,Strike,IsCall):
        # To create/send transaction to Contract
        return self.contract.functions.add_trade(
            TraderID,
            Open,
            Symbol,
            Size,
            list_to_string([EntryPrice, EntryTime]),
            list_to_string([Strike, IsCall,ExpirationTimeStamp]),
            ).transact({'from': TraderAddress, 'gas': 1000000})
    def closeTrade(self,TraderAddress,tradeID,exitPrice,exitTime):
        # To create/send transaction to Contract
        return self.contract.functions.close_trade(
            TraderAddress,
            tradeID,
            list_to_string([exitPrice,exitTime])
            ).transact({'from': TraderAddress, 'gas': 1000000})
def init_TradingPlatform(platform, contract):
    if platform == trade_platforms["simulation"]:
        return simulation_TradingPlatform(contract)
    elif platform == trade_platforms["alpaca"]:
        return alpaca_TradingPlatform(contract)
    elif platform == trade_platforms["tda"]:
        return tda_TradingPlatform(contract)
    else:
        return tradingPlatform(None,None)

class simulation_TradingPlatform(tradingPlatform):
    def __init__(self,contract):
        super().__init__(trade_platforms["simulation"],contract)
    def openTrade(self,TraderAddress,Open,Symbol,Size,EntryPrice,ExpirationTimeStamp,Strike,IsCall):
        # Only necessary to send transaction to contract
        super().openTrade()
    def closeTrade(self,TraderAddress,tradeID, ExitPrice):
        # Only necessary to send transaction to contract
        super().closeTrade()

class alpaca_TradingPlatform(tradingPlatform):
    trade_api = alpaca()
    def __init__(self,contract):
        super().__init__(trade_platforms["alpaca"],contract)
    def openTrade(self,TraderAddress,Open,Symbol,Size,EntryPrice,ExpirationTimeStamp,Strike,IsCall):
        # Alpacea trading code
        order = self.trade_api.submit_order(
            # Still need to place:
            #   ExpirationTimeStamp,Strike,IsCall 
            symbol = Symbol,
            qty = Size, #+ fractional_decimals,
            side= "buy",
            type= "market", # Is this what we want?
        )
        success = (order["OrderStatus"] in ["Accepted","AcceptedForBidding","Calculated","DoneForDay","Expired","Filled","New","PartiallyFilled"])
        if success :
            return super().openTrade(TraderAddress,Open,Symbol,Size,EntryPrice,ExpirationTimeStamp,Strike,IsCall)
        return f"{self.platform} Open Trade Failed! - Order Status: {order['OrderStatus']}"
    def closeTrade(self,TraderAddress,tradeID,Symbol,Size,ExitPrice):
        # TODO How does this know the symbol and size?
        # Alpacea trading code
        order = self.trade_api.submit_order(
            # Still need to place:
            #   ExpirationTimeStamp,Strike,IsCall 
            symbol = Symbol,
            qty = Size,
            side= "sell",
            type= "market", # Is this what we want?
        )
        success = (order["OrderStatus"] in ["Accepted","AcceptedForBidding","Calculated","DoneForDay","Expired","Filled","New","PartiallyFilled"])
        if success :
            return super().closeTrade(TraderAddress,tradeID, ExitPrice)
        return f"{self.platform} Close Trade Failed! - Order Status: {order['OrderStatus']}"

class tda_TradingPlatform(tradingPlatform):
    def __init__(self,contract):
        super().__init__(trade_platforms["tda"],contract)
    def openTrade(self,TraderAddress,Open,Symbol,Size,EntryPrice,ExpirationTimeStamp,Strike,IsCall):
        super().openTrade()
        # tda trading code
        return f"{self.platform} Open Trade!"
    def closeTrade(self,TraderAddress,tradeID, ExitPrice):
        super().closeTrade()
        # tda trading code
        return f"{self.platform} Close Trade!"