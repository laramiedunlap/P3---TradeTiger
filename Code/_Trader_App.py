from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from Libraries.TradingPlatforms import trade_platforms, init_TradingPlatform, tradingPlatform
from Libraries.web3_contract import load_web3
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

load_dotenv()

contract, address, w3 = load_web3("logger.json")

def plot_chart(symbol, period, interval):
     df = yf.download(tickers=symbol, period=period, interval=interval)
     fig = go.Figure(data=[go.Candlestick(x=df.index,
                              open=df['Open'],
                              high = df['High'],
                              low= df['Low'],
                              close = df['Close']              
                                        
                                             
                                             )])
     currentPrice = df["Close"][-1]
     # fig.update_layout(xaxis_rangeslider_visible=False)
     return fig, f'{currentPrice:.2f}'

def options_chain(symbol):
    """Returns the entire option chain for a symbol to a dataframe"""
    
    tk = yf.Ticker(symbol)
    # Expiration dates
    exps = tk.options

    # Get options for each expiration
    options = pd.DataFrame()
    for e in exps:
        opt = tk.option_chain(e)
        opt = pd.DataFrame().append(opt.calls).append(opt.puts)
        opt['expirationDate'] = e
        options = options.append(opt, ignore_index=True)

    # Get expiration Date
    options['expirationDate'] = pd.to_datetime(options['expirationDate'])
    options['dte'] = (options['expirationDate'] - datetime.datetime.today()).dt.days / 365
    options['expirationDate'] = pd.DatetimeIndex(options['expirationDate']).date
    
    # Boolean column if the option is a CALL
    options['CALL'] = options['contractSymbol'].str[4:].apply(
        lambda x: "C" in x)
    
    # Calculate the midpoint of the bid-ask
    options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)
    options['mark'] = (options['bid'] + options['ask']) / 2 
    
    # Drop unnecessary columns
    options = options.drop(columns = ['contractSize', 'currency', 'lastTradeDate'])

    return options
@dataclass
class interface_block:
     trading_choice : str = "Simulation"
     trading_platform : tradingPlatform = tradingPlatform(None,None)
     inputTraderAddress : str = ""
     inputOpen : bool = True
     inputSymbol : str = ""
     inputSize : int = 0
     inputEntryPrice : int = 0
     inputEntryTime : datetime = datetime.datetime.now().strftime("%H:%M:%S")
     inputExpirationTimeStamp : datetime = datetime.datetime.now().strftime("%H:%M:%S")
     inputStrike : int = 0
     inputIsCall : bool = False
     inputTradeID : int = 0
     inputExitPrice : int = 0
     inputExitTime : datetime = datetime.datetime.now().strftime("%H:%M:%S")
     interval : str = "5m"
     period : str = "5d"

@st.cache(allow_output_mutation=True)
def setup():
     return interface_block()
interface = setup()

########## SideBar ##########

# Select Trade Type Dropdown
interface.trading_choice = st.sidebar.selectbox("Trading Platform", list(trade_platforms.values()))
# Start Trading Button
if st.sidebar.button("Start Trading"):
     interface.trading_platform = init_TradingPlatform(interface.trading_choice,contract)
     st.sidebar.write(f"You have opened the Trading Platform.\n{interface.trading_platform.__hello__()}")

########## Trade Setup ##########
st.title("Execute a Trade")
accounts = w3.eth.accounts
interface.inputTraderAddress = st.selectbox("Select Trade User", options=accounts)

if (interface.trading_platform.platform == None):
     st.header("Select Trading Platform to Start Trading")
else:
     ########## Tabs ##########
     tab_open, tab_close = st.tabs(["Open Trade","Close Trade"])
     with tab_open:
          # All Trading Code
          st.header("Opening a Trade")
          interface.inputOpen = True
          interface.inputSymbol = st.text_input("Symbol", key="open", value="")
          interface.inputSize = st.number_input("Size")
          interface.interval = st.selectbox("select a bar interval", ["1m","2m","5m","15m","30m","60m","90m","1d","1wk"],index=2)
          interface.period = st.selectbox("select a bar lookback period",options=["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"],index=0)
          # Manual Entry Trading Code
          if interface.trading_platform.platform == trade_platforms["manual"]:
               interface.inputEntryPrice = st.text_input("Entry Price")
               interface.inputEntryTime = st.text_input("Entry Time")
          # Non-Manual Entry Trading Code
          elif interface.inputSymbol != "":
               interface.fig, priceNow = plot_chart(interface.inputSymbol,interface.period,interface.interval)
               st.plotly_chart(interface.fig, use_container_width=False)
               # priceNow = interface.trading_platform.price_checker.current_price(interface.inputSymbol)
               timeNow = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
               st.write(f"Current Price: {priceNow}")
               st.write(f"Current Time: {timeNow}")
               if st.button("Refresh Open Price and Time"):
                    interface.fig, priceNow = plot_chart(interface.inputSymbol,interface.period,interface.interval)
                    timeNow = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
          # All Trading Code (Options Data)
          if (interface.trading_platform.platform != trade_platforms["alpaca"]):
               interface.inputExpirationTimeStamp = st.text_input("Expiration",value="None")
               interface.inputStrike = st.text_input("Strike",value="None")
               interface.inputIsCall = st.radio(
                    "Option",
                    ('N/A','Call','Put'))
          if st.button("Open Trade"):
               # openTrade(self,TraderAddress,Open,Symbol,Size,EntryPrice,ExpirationTimeStamp,Strike,IsCall)
               if interface.trading_platform.platform != trade_platforms["manual"]: # Non-manual Entry Code
                    interface.fig, priceNow = plot_chart(interface.inputSymbol,interface.period,interface.interval)
                    interface.inputEntryPrice = priceNow
                    interface.inputEntryTime = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
               tx_hash = interface.trading_platform.openTrade(
                    interface.inputTraderAddress,
                    interface.inputOpen,
                    interface.inputSymbol,
                    interface.inputSize,
                    interface.inputEntryPrice,
                    interface.inputEntryTime,
                    interface.inputExpirationTimeStamp,
                    interface.inputStrike,
                    interface.inputIsCall)
               receipt = dict(w3.eth.waitForTransactionReceipt(tx_hash))
               st.write("Transaction receipt mined:")
               st.write(receipt)
          st.markdown("---")
     with tab_close:
          # All Trading Code
          st.header("Closing a Trade")
          interface.inputOpen = False
          interface.inputTradeID = st.text_input("Trade to Close")
          interface.inputSymbol = st.text_input("Symbol", key="close", value="")
          interface.inputSize = st.number_input("Size", key="closesize")
          # Manual Entry Trading Code
          if interface.trading_platform.platform == trade_platforms["manual"]:
               interface.inputExitPrice = st.text_input("Exit Price")
               interface.inputExitTime = st.text_input("Exit Time")
          # Non-Manual Entry Trading Code
          elif interface.inputSymbol != "":
               interface.fig, priceNow = plot_chart(interface.inputSymbol,interface.period,interface.interval)
               timeNow = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
               st.write(f"Current Price: {priceNow}")
               st.write(f"Current Time: {timeNow}")
               if st.button("Refresh Close Price and Time"):
                    interface.fig, priceNow = plot_chart(interface.inputSymbol,interface.period,interface.interval)
                    timeNow = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
          if st.button("Close Trade"):
               if interface.trading_platform.platform != trade_platforms["manual"]: # Non-manual Entry Code
                    interface.fig, priceNow = plot_chart(interface.inputSymbol,interface.period,interface.interval)
                    interface.inputExitPrice = priceNow
                    interface.inputExitTime = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
               tx_hash = interface.trading_platform.closeTrade(
                    interface.inputTraderAddress,
                    interface.inputTradeID,
                    interface.inputSymbol,
                    interface.inputSize,
                    interface.inputExitPrice,
                    interface.inputExitTime
                    )
               receipt = dict(w3.eth.waitForTransactionReceipt(tx_hash))
               st.write("Transaction receipt mined:")
               st.write(receipt)
          st.markdown("---")



