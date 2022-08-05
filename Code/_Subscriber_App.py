from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import os
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from Libraries.web3_contract import load_custom_web3

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

@dataclass
class interface_block:
    inputTraderLogAddress: str = ""
    inputSubscriberAddress: str = ""
    inputEmail: str = ""
    inputSubCost: int = 0
    subscriptions = []
    sub_df = pd.DataFrame()
    subscription_data_df = pd.DataFrame()

@st.cache(allow_output_mutation=True)
def setup():
     return interface_block()
interface = setup()

accounts = w3.eth.accounts

if st.sidebar.button("Manage TradeTiger Subscriptions"):
    with st.sidebar.container():
        st.sidebar.write("Click the dropdown to view your subscriptions", interface.subscriptions)

st.title("Subscribe to a Trader")

interface.inputEmail = st.text_input("Enter email")
interface.inputSubscriberAddress = st.selectbox("Choose Your Wallet Address for Payment", options=accounts)
interface.inputTraderLogAddress = st.text_input("Enter a trader's log address")
if interface.inputTraderLogAddress != "":
    try: 
        contract, address, w3 = load_custom_web3("../Code/Libraries/logger.json",interface.inputTraderLogAddress)
        interface.inputSubCost = contract.functions.viewSubCost().call()
        st.write(f"Subscription Fee: {interface.inputSubCost}")
        traderID_filter = contract.events.newSub.createFilter(fromBlock="latest")
    except:
        st.write("Please try a different trader log address")

if st.button("Subscribe"):

    tx_hash = contract.functions.subscribe(
    ).transact({'from': interface.inputSubscriberAddress, 'gas': 1000000, 'value': interface.inputSubCost})
    receipt = dict(w3.eth.waitForTransactionReceipt(tx_hash))
    st.write("Thanks for subscribing!")
    st.write(receipt)
    st.balloons()
    interface.subscription_data_df = pd.DataFrame({
        "trader_log_address": interface.inputTraderLogAddress,
        "subscriber_address": interface.inputSubscriberAddress,
        "email_address": interface.inputEmail,
        "trade_id": traderID_filter.get_new_entries()[0]['args']["TraderId"]
    }, index=[0])
    if not(os.path.exists("../Code/Libraries/sub.csv")):
        interface.sub_df = interface.subscription_data_df.copy()
    else:
        interface.sub_df = pd.read_csv('../Code/Libraries/sub.csv', index_col=[0])
        interface.sub_df = interface.sub_df.append(interface.subscription_data_df)
    #sub_df.reset_index(inplace=True)
    interface.sub_df.to_csv('../Code/Libraries/sub.csv')
    interface.subscriptions.append(interface.inputTraderLogAddress)
