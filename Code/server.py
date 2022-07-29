import streamlit as st
import alpaca_trade_api as aplpaca
from alpaca_trade_api.rest import REST, TimeFrame
import os
import time
from dotenv import load_dotenv

from web3 import Web3
from pathlib import Path
import json
load_dotenv()





w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

def load_contract():
    contract_address = os.getenv("LOGGER_CONTRACT_ADDRESS") #could make this variable
    with open(Path('logger.json')) as f:
            logger_abi = json.load(f)

    logger_contract = w3.eth.contract(
    address=contract_address,
    abi=logger_abi
        )
    return logger_contract

def handle_new_trade(event):
    return (Web3.toJSON(event))
    
    
contract = load_contract() 

event_filter = contract.events.newTrade.createFilter(fromBlock="latest")

event = handle_new_trade(event_filter.get_all_entries())

print((event))
print("--------------------------")
print(type(event))






# print(type((event_filter.get_all_entries())))
# while True:
#     print((event_filter.get_new_entries()))
#     time.sleep(5)
# while True: 
#     if event_filter.get_new_entries():
#         print(type(event_filter.get_new_entries()))
#         print("\n")
#         print("-------------")
#     