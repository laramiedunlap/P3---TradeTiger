# Exchangable Trading Platform
    # This can/should be its own .py file
import alpaca
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
    def openTrade(self,TraderAddress,Open,Symbol,Size,Fractional_shares,EntryPrice,ExpirationTimeStamp,Strike,IsCall):
        # To create/send transaction to Contract
        return self.contract.functions.add_trade(
            TraderAddress,
            Open,
            Symbol,
            Size,
            Fractional_shares,
            EntryPrice,
            # ExitPrice,
            ExpirationTimeStamp,
            Strike,
            IsCall
            ).transact({'from': TraderAddress, 'gas': 1000000})
    def closeTrade(self,TraderAddress,tradeID, ExitPrice):
        # To create/send transaction to Contract
        return self.contract.functions.close_trade(
            TraderAddress,
            tradeID,
            ExitPrice,
            ).transact({'from': TraderAddress, 'gas': 1000000})
def init_TradingPlatform(platform, contract):
    if platform == trade_platforms["simulation"]:
        return simulation_TradingPlatform(contract)
    elif platform == trade_platforms["alpaca"]:
        return alpaca_TradingPlatform(contract)
    elif platform == trade_platforms["tda"]:
        return tda_TradingPlatform(contract)
    else:
        return tradingPlatform(None)

class simulation_TradingPlatform(tradingPlatform):
    def __init__(self,contract):
        super().__init__(trade_platforms["simulation"],contract)
    def openTrade(self,TraderAddress,Open,Symbol,Size,Fractional_shares,EntryPrice,ExpirationTimeStamp,Strike,IsCall):
        # Only necessary to send transaction to contract
        super().openTrade()
    def closeTrade(self,TraderAddress,tradeID, ExitPrice):
        # Only necessary to send transaction to contract
        super().closeTrade()

class alpaca_TradingPlatform(tradingPlatform):
    trade_api = alpaca()
    def __init__(self,contract):
        super().__init__(trade_platforms["alpaca"],contract)
    def openTrade(self,TraderAddress,Open,Symbol,Size,Fractional_shares,EntryPrice,ExpirationTimeStamp,Strike,IsCall):
        # Alpacea trading code
        fractional_decimals = Fractional_shares/(10**len(str(Fractional_shares)))
        self.trade_api.submit_order(
            # Still need to place:
            #   ExpirationTimeStamp,Strike,IsCall 
            symbol = Symbol,
            qty = Size + fractional_decimals,
            side= "buy",
            type= "market", # Is this what we want?
            time_in_force = "day", # Is this what we want?
            limit_price = EntryPrice, # Is this what we want?
            stop_price = None,
            client_order_id = None,
            extended_hours = None,
            order_class = None,
            take_profit = None,
            stop_loss = None,
            trail_price = None,
            trail_percent = None,
            notional = None
        )
        success = True # @TODO
        if success :
            return super().openTrade(TraderAddress,Open,Symbol,Size,Fractional_shares,EntryPrice,ExpirationTimeStamp,Strike,IsCall)
        return f"{self.platform} Open Trade Fail!"
    def closeTrade(self,TraderAddress,tradeID, ExitPrice):
        super().closeTrade()
        # Alpacea trading code
        return f"{self.platform} Close Trade!"

class tda_TradingPlatform(tradingPlatform):
    def __init__(self,contract):
        super().__init__(trade_platforms["tda"],contract)
    def openTrade(self,TraderAddress,Open,Symbol,Size,Fractional_shares,EntryPrice,ExpirationTimeStamp,Strike,IsCall):
        super().openTrade()
        # tda trading code
        return f"{self.platform} Open Trade!"
    def closeTrade(self,TraderAddress,tradeID, ExitPrice):
        super().closeTrade()
        # tda trading code
        return f"{self.platform} Close Trade!"