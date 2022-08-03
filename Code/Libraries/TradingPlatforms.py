# Exchangable Trading Platform
    # This can/should be its own .py file
from Libraries.alpaca import alpaca
from Libraries.misc import list_to_string
trade_platforms = {
    "simulation": "Manual Entry",
    "alpaca" : "Alpaca"
}

# TradePlatform Classes
class tradingPlatform :
    contract = None
    platform = None
    price_checker = None
    def __init__(self, platformType, contract):
        self.contract = contract
        self.platform = platformType
        self.price_checker = alpaca()
    def __hello__(self):
        return f"This is a {self.platform} trading platform."
    def openTrade(self,TraderAddress,Open,Symbol,Size,EntryPrice,EntryTime,ExpirationTimeStamp,Strike,IsCall):
        # To create/send transaction to Contract
        return self.contract.functions.openTrade(
            TraderAddress,
            Open,
            Symbol,
            str(Size),
            list_to_string([EntryPrice, EntryTime]), #EntryPriceEntryTime
            list_to_string([Strike, IsCall, ExpirationTimeStamp]) #OptionsData
            ).transact({'from': TraderAddress, 'gas': 1000000})
    def closeTrade(self,TraderAddress,tradeID,Symbol,Size,ExitPrice,ExitTime):
        # To create/send transaction to Contract
        return self.contract.functions.closeTrade(
            int(tradeID),
            list_to_string([ExitPrice,ExitTime])
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
    def openTrade(self,TraderAddress,Open,Symbol,Size,EntryPrice,EntryTime,ExpirationTimeStamp,Strike,IsCall):
        # Only necessary to send transaction to contract
        return super().openTrade(TraderAddress,Open,Symbol,Size,EntryPrice,EntryTime,ExpirationTimeStamp,Strike,IsCall)
    def closeTrade(self,TraderAddress,tradeID,Symbol,Size,ExitPrice,ExitTime):
        # Only necessary to send transaction to contract
        return super().closeTrade(TraderAddress,tradeID,Symbol,Size,ExitPrice,ExitTime)

class alpaca_TradingPlatform(tradingPlatform):
    trade_api = alpaca()
    def __init__(self,contract):
        super().__init__(trade_platforms["alpaca"],contract)
    def openTrade(self,TraderAddress,Open,Symbol,Size,EntryPrice,EntryTime,ExpirationTimeStamp,Strike,IsCall):
        # Alpacea trading code
        order = self.trade_api.submit_order(
            # Still need to place:
            #   ExpirationTimeStamp,Strike,IsCall 
            symbol = Symbol,
            qty = Size, #+ fractional_decimals,
            side= "buy",
            type= "market", # Is this what we want?
        )
        success = (order.status in ["accepted","accepted_for_bidding","calculated","done_for_day","filled","new","partially_filled"])
        if success :
            return super().openTrade(TraderAddress,Open,Symbol,Size,EntryPrice,EntryTime,ExpirationTimeStamp,Strike,IsCall)
        return f"{self.platform} Open Trade Failed! - Order Status: {order['OrderStatus']}"
    def closeTrade(self,TraderAddress,tradeID,Symbol,Size,ExitPrice,ExitTime):
        # Alpacea trading code
        order = self.trade_api.submit_order(
            # Still need to place:
            #   ExpirationTimeStamp,Strike,IsCall 
            symbol = Symbol,
            qty = Size,
            side= "sell",
            type= "market", # Is this what we want?
        )
        success = (order.status in ["accepted","accepted_for_bidding","calculated","done_for_day","filled","new","partially_filled"])
        if success :
            return super().closeTrade(TraderAddress,tradeID,Symbol,Size,ExitPrice,ExitTime)
        return f"{self.platform} Close Trade Failed! - Order Status: {order['OrderStatus']}"

class tda_TradingPlatform(tradingPlatform):
    def __init__(self,contract):
        super().__init__(trade_platforms["simulation"],contract)
    def openTrade(self,TraderAddress,Open,Symbol,Size,EntryPrice,EntryTime,ExpirationTimeStamp,Strike,IsCall):
        # Only necessary to send transaction to contract
        return super().openTrade(TraderAddress,Open,Symbol,Size,EntryPrice,EntryTime,ExpirationTimeStamp,Strike,IsCall)
    def closeTrade(self,TraderAddress,tradeID,Symbol,Size,ExitPrice,ExitTime):
        # Only necessary to send transaction to contract
        return super().closeTrade(TraderAddress,tradeID,Symbol,Size,ExitPrice,ExitTime)