import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from Libraries.TradingPlatforms import trade_platforms, init_TradingPlatform
from Libraries.web3_contract import load_web3

load_dotenv()

contract, address, w3 = load_web3(".\Code\Contracts\ABI\Contract_abi.json")

st.cache(allow_output_mutation=True)

########## SideBar ##########
trading_platform = None
# Select Trade Type Dropdown
trading_choice = st.sidebar.selectbox("Trading Platform", list(trade_platforms.values()))
# Start Trading Button
if st.sidebar.button("Start Trading"):
     trading_platform = init_TradingPlatform(trading_choice,contract)
     st.sidebar.write(f"You have opened the Trading Platform.\n{trading_platform.__hello__()}")

<<<<<<< HEAD
    with open(Path('../logger_abi.json')) as f:
        logger_abi = json.load(f)

    contract_address = os.getenv("LOGGER_CONTRACT_ADDRESS")

    contract = w3.eth.contract(
        address=contract_address,
        abi=logger_abi
    )

    return contract


contract = load_contract()


st.title("Log a Trade")
=======
########## Trade Setup ##########
st.title("Execute a Trade")
>>>>>>> 6391e61a81f6f567b0d7e78c31a5498fbb3a0ab4
accounts = w3.eth.accounts
inputTraderAddress = st.selectbox("Select Trade User", options=accounts)

if (trading_platform == None):
     st.header("Select Trading Platform to Start Trading")
else:
     ########## Tabs ##########
     tab_open, tab_close = st.tabs(["Open Trade","Close Trade"])
     with tab_open:
          st.header("Opening a Trade")
          inputOpen = 1
          inputSymbol = st.text_input("Symbol")
          inputSize = st.number_input("Size")
          inputFractional_shares = st.number_input("Fractional Shares")
          inputEntryPrice = st.text_input("Entry Price")
          inputExpirationTimeStamp = st.time_input("Expiration") # Hide on Close
          inputStrike = st.text_input("Strike")# Hide on Close
          inputIsCall = st.radio(# Hide on Close
               "Call or Put",
               ('1','0'))
          if inputIsCall == '1':# Hide on Close
               st.write('Call')
          else:
               st.write("Put")
          if st.button("Open Trade"):
               # openTrade(self,TraderAddress,Open,Symbol,Size,Fractional_shares,EntryPrice,ExpirationTimeStamp,Strike,IsCall)
               tx_hash = trading_platform.openTrade(
                    inputTraderAddress,
                    inputOpen,
                    inputSymbol,
                    inputSize,
                    inputFractional_shares,
                    inputEntryPrice,
                    inputExpirationTimeStamp,
                    inputStrike,
                    inputIsCall)
               receipt = w3.eth.waitForTransactionReceipt(tx_hash)
               st.write("Transaction receipt mined:")
               st.write(dict(receipt))
          st.markdown("---")
     with tab_close:
          st.header("Closing a Trade")
          inputOpen = 0
          inputTradeID = st.text_input("Exit Price (Replace with Open Trade Dropdown")
          inputExitPrice = st.text_input("Exit Price (Should just auto fetch (show with a refresh button), rather than input)")
          if st.button("Close Trade"):
               # closeTrade(self,TraderAddress,tradeID, ExitPrice)
               tx_hash = trading_platform.closeTrade(
                    inputTraderAddress,
                    inputTradeID,
                    inputExitPrice
                    )
               receipt = w3.eth.waitForTransactionReceipt(tx_hash)
               st.write("Transaction receipt mined:")
               st.write(dict(receipt))
          st.markdown("---")



