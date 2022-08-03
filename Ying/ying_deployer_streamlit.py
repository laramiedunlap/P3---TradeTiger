import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# setup and provider access layer
load_dotenv()

# print(os.getenv("SMART_CONTRACT_ADDRESS"))

# access ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
# print(w3.eth.accounts) test the code

accounts = w3.eth.accounts

# contract access
# access/make code reference to the smart contract on the bc
@st.cache(allow_output_mutation=True)
def load_contract():

    # where is the contract
    contractAddress = os.getenv("DEPLOYER_ADDRESS")

    # what's in it?
    with open(Path("deployer.json")) as file:

        deployerContractABI = json.load(file)

    contract = w3.eth.contract(
        address=contractAddress,
        abi=deployerContractABI
    )
    return contract

contract = load_contract()
# streamlit application
st. title("WELCOM TO REGISTRERING NEW TRADER!")

trader = st.text_input("Please enter your address: ")

if st.button("Register New Trader"):
    txn_hash = contract.functions.addTrader(trader).transact({
        "from":trader,
        "gas": 1000000
    })
    st.write(f"Congrats on registering trader successfully")