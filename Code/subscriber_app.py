from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from Libraries.web3_contract import load_web3

load_dotenv()

contract, address, w3 = load_web3("../Code/Contracts/ABI/Logger_abi.json")

@dataclass
class interface_block:
    inputTraderAddress: str = ""
    inputSubscriberAddress: str = ""
    inputEmail: str = ""
    inputSubCost: int = 0

subscriptions = []

@st.cache(allow_output_mutation=True)
def setup():
     return interface_block()
interface = setup()

accounts = w3.eth.accounts

if st.sidebar.button("Manage TradeTiger Subscriptions"):
    with st.sidebar.container():
        st.sidebar.write("click the dropdown to view your subscriptions", subscriptions)

st.title("Subscribe to a Trader")

interface.inputEmail = st.text_input("enter email")
interface.inputSubscriberAddress = st.selectbox("Choose Your Wallet Address for Payment", options=accounts)
interface.inputTraderAddress = st.text_input("enter a trader's address")
#sub_cost = 
#interface.inputSubCost = st.

if st.button(f"Send {interface.inputTraderAddress} subCost and Subscribe"):
    tx_hash = w3.contract.functions.subscribe(
        interface.inputTraderAddress,
        interface.subCost
    ).transact({'from': inputSubscriberAddress, 'gas': 1000000})
    receipt = dict(w3.eth.waitForTransactionReceipt(tx_hash))
    st.write("Thanks for subscribing!")
    subscription_data = {
        "traderAddress": inputTraderAddress,
        "subscriberAddress": inputSubscriberAddress,
        "subscriberEmail": inputEmail,
        "paymentConfirmation": receipt["Hash"]
    }
    subscriptions.append(receipt["inputTraderAddress"])
