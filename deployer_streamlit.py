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

    with open(Path('./sample_deployer_contract_abi.json')) as f:
        deployer_abi = json.load(f)

    contract_address = os.getenv("DEPLOYER_CONTRACT_ADDRESS")

    contract = w3.eth.contract(
        address=contract_address,
        abi=deployer_abi
    )

    return contract

contract = load_contract()
accounts = w3.eth.accounts
st.title("Add a New Trader")
newestTraderAddress = st.text_input("New Trader's Address")

if st.button("Add Trader"):
        tx_hash = contract.functions.createLog().transact({'from': newestTraderAddress, 'gas': 1000000})
        st.write(f"You've successfully registered a new trader.")

st.markdown("---")