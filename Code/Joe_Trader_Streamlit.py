import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))


@st.cache(allow_output_mutation=True)
def load_contract():

    with open(Path('./sample_logger_contract_abi.json')) as f:
        logger_abi = json.load(f)

    contract_address = os.getenv("LOGGER_CONTRACT_ADDRESS")

    contract = w3.eth.contract(
        address=contract_address,
        abi=logger_abi
    )

    return contract


contract = load_contract()


st.title("Log a Trade")
accounts = w3.eth.accounts
inputTraderAddress = st.selectbox("Select Trade User", options=accounts)
inputOpen = st.radio(
     "Open or Close a Trade",
     ('1','0'))

if inputOpen == '1':
     st.write('Open Trade')
else:
     st.write("Close Trade")

inputSymbol = st.text_input("Symbol")
inputSize = st.number_input("Size")
inputFractional_shares = st.number_input("Fractional Shares")
if inputOpen == '1':
     inputEntryPrice = st.text_input("Entry Price")
else: inputExitPrice = st.text_input("Exit Price")
inputExpirationTimeStamp = st.time_input("Expiration") # Hide on Close
inputStrike = st.text_input("Strike")# Hide on Close
inputIsCall = st.radio(# Hide on Close
     "Call or Put",
     ('1','0'))

if inputIsCall == '1':# Hide on Close
     st.write('Call')
else:
     st.write("Put")
if st.button("Log Trade"):
    tx_hash = contract.functions.add_trade(inputTraderAddress,
    inputOpen,
    inputSymbol,
    inputSize,
    inputFractional_shares,
    inputEntryPrice,
    inputExitPrice,
    inputExpirationTimeStamp,
    inputStrike,
    inputIsCall
    ).transact({'from': address, 'gas': 1000000})

    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
st.markdown("---")