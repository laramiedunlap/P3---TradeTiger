# Exchangable Trading Platform
    # This can/should be its own .py file
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
    def openTrade():
        # Only necessary to send transaction to contract
        super().openTrade()
    def closeTrade():
        # Only necessary to send transaction to contract
        super().closeTrade()

class alpaca_TradingPlatform(tradingPlatform):
    def __init__(self,contract):
        super().__init__(trade_platforms["alpaca"],contract)
    def openTrade(self):
        super().openTrade()
        # Alpacea trading code
        return f"{self.platform} Open Trade!"
    def closeTrade(self):
        super().closeTrade()
        # Alpacea trading code
        return f"{self.platform} Close Trade!"

class tda_TradingPlatform(tradingPlatform):
    def __init__(self,contract):
        super().__init__(trade_platforms["tda"],contract)
    def openTrade(self):
        super().openTrade()
        # tda trading code
        return f"{self.platform} Open Trade!"
    def closeTrade(self):
        super().closeTrade()
        # tda trading code
        return f"{self.platform} Close Trade!"