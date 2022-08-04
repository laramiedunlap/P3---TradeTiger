# import os
# import json
# from web3 import Web3
# from pathlib import Path
# from dotenv import load_dotenv
# import streamlit as st

# load_dotenv()

# w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))


# @st.cache(allow_output_mutation=True)
# def load_contract():

#     with open(Path('./sample_logger_contract_abi.json')) as f:
#         logger_abi = json.load(f)

#     contract_address = os.getenv("LOGGER_CONTRACT_ADDRESS")

#     contract = w3.eth.contract(
#         address=contract_address,
#         abi=logger_abi
#     )

#     return contract


# contract = load_contract()


# st.title("Log a Trade")
# accounts = w3.eth.accounts
# inputTraderAddress = st.selectbox("Select Trade User", options=accounts)
# inputOpen = st.radio(
#      "Open or Close a Trade",
#      ('1','0'))

# if inputOpen == '1':
#      st.write('Open Trade')
# else:
#      st.write("Close Trade")

# inputSymbol = st.text_input("Symbol")
# inputSize = st.text_input("Size")
# inputFractional_shares = st.text_input("Fractional Shares")
# inputEntryPrice = st.text_input("Entry Price")
# inputExitPrice = st.text_input("Exit Price")
# inputExpirationTimeStamp = st.text_input("Expiration")
# inputStrike = st.text_input("Strike")
# inputIsCall = st.radio(
#      "Call or Put",
#      ('1','0'))

# if inputIsCall == '1':
#      st.write('Call')
# else:
#      st.write("Put")
# if st.button("Log Trade"):
#     tx_hash = contract.functions.add_trade(inputTraderAddress,
#     inputOpen,
#     inputSymbol,
#     inputSize,
#     inputFractional_shares,
#     inputEntryPrice,
#     inputExitPrice,
#     inputExpirationTimeStamp,
#     inputStrike,
#     inputIsCall
#     ).transact({'from': address, 'gas': 1000000})

#     receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#     st.write("Transaction receipt mined:")
#     st.write(dict(receipt))
# st.markdown("---")

from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
from web3 import Web3
from pathlib import Path
import sys
import threading
import os
from dotenv import load_dotenv
import streamlit as st
from Libraries.TradingPlatformsTest import trade_platforms, init_TradingPlatform, tradingPlatform
from Libraries.web3_contract import load_web3

# sys.setrecursionlimit(10**6)
# threading.stack_size(2**26)
load_dotenv()

contract, address, w3 = load_web3("logger.json")

@dataclass
class interface_block:
     trading_choice : str = "Simulation"
     trading_platform : tradingPlatform = tradingPlatform(None,None)
     inputTraderAddress : str = ""
     inputOpen : bool = True
     inputSymbol : str = ""
     inputSize : int = 0
     inputEntryPrice : int = 0
     inputEntryTime : datetime = datetime.datetime.utcnow().strftime("%H:%M:%S")
     inputExpirationTimeStamp : datetime = datetime.datetime.utcnow().strftime("%H:%M:%S")
     inputStrike : int = 0
     inputIsCall : bool = False
     inputTradeID : int = 0
     inputExitPrice : int = 0
     inputExitTime : datetime = datetime.datetime.utcnow().strftime("%H:%M:%S")

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
          """TODO Separate into multiple columns One Stock one Options using st.columns"""
          st.header("Opening a Trade")
          interface.inputOpen = True
          interface.inputSymbol = st.text_input("Symbol")
          interface.inputSize = st.number_input("Size")
          interface.inputEntryPrice = st.text_input("Entry Price")
          interface.inputEntryTime = st.time_input("Entry Time")
          interface.inputExpirationTimeStamp = st.time_input("Expiration")
          interface.inputStrike = st.text_input("Strike")
          interface.inputIsCall = st.radio(
               "Call or Put",
               ('1','0'))
          if interface.inputIsCall == '1': # TODO This causes a reset of the display
               st.write('Call')
          else:
               st.write("Put")
          if st.button("Open Trade"):
               # openTrade(self,TraderAddress,Open,Symbol,Size,Fractional_shares,EntryPrice,ExpirationTimeStamp,Strike,IsCall)
               tx_hash = interface.trading_platform.openTrade(
                    interface.inputTraderAddress,
                    interface.inputOpen,
                    interface.inputSymbol,
                    interface.inputSize,
                    interface.inputEntryPrice, #TODO AUTO FILL
                    interface.inputEntryTime, #TODO AUTO FILL
                    interface.inputExpirationTimeStamp,
                    interface.inputStrike,
                    interface.inputIsCall)
               receipt = dict(w3.eth.waitForTransactionReceipt(tx_hash))
               st.write("Transaction receipt mined:")
               st.write(receipt)
          st.markdown("---")
     with tab_close:
          st.header("Closing a Trade")
          interface.inputOpen = False
          interface.inputTradeID = st.text_input("Trade to Close (Replace with Open Trade Dropdown")
          interface.inputExitPrice = st.text_input("Exit Price (Should just auto fetch (show with a refresh button?), rather than input)")
          interface.inputEntryTime = st.time_input("Exit Time")
          if st.button("Close Trade"):
               # closeTrade(self,TraderAddress,tradeID, ExitPrice)
               tx_hash = interface.trading_platform.closeTrade(
                    interface.inputTraderAddress,
                    interface.inputTradeID,
                    interface.inputExitPrice
                    )
               receipt = dict(w3.eth.waitForTransactionReceipt(tx_hash))
               st.write("Transaction receipt mined:")
               st.write(receipt)
          st.markdown("---")



