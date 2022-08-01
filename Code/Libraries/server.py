import streamlit as st
import alpaca_trade_api as aplpaca
from alpaca_trade_api.rest import REST, TimeFrame
import os
import time
from dotenv import load_dotenv

from web3 import Web3
from pathlib import Path

import json
from io import StringIO

class Grader:
    # add event filters to Grader class 
    def __init__(self, trader_id, log_address):
        self.trader_id = trader_id
        self.log_address = log_address
        
    def load_contract(self):
        contract_address = self.log_address
        with open(Path('logger.json')) as f:
            logger_abi = json.load(f)
            
            self.contract = w3.eth.contract(
            address=contract_address,
            abi=logger_abi)
            
            self.new_trade_filter = self.contract.events.newTrade.createFilter(fromBlock="latest")
            self.close_trade_filter = self.contract.events.newCloseTrade.createFilter(fromBlock="latest")
            
        return None
    
    def verify_trade(self):
        pass        
    

def load_deployer_contract():
    contract_address = os.getenv("DEPLOYER_ADDRESS") 
    with open(Path('deployer.json')) as f:
            deployer_abi = json.load(f)

    deployer_contract = w3.eth.contract(
        address=contract_address,
        abi=deployer_abi
        )
    trader_dict = {}
    return deployer_contract, trader_dict

def load_contract_new(log_addr):
    contract_address = log_addr
    with open(Path('logger.json')) as f:
            logger_abi = json.load(f)

    logger_contract = w3.eth.contract(
        address=contract_address,
        abi=logger_abi
            )
    return logger_contract

def handle_new_log(event):
    io = StringIO((Web3.toJSON(event)))
    return json.load(io)
    

def handle_new_trade(event):
    io = StringIO((Web3.toJSON(event)))
    return json.load(io)


w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))


# Instantiate deployer and trader dictionary
deployer, trader_dict = load_deployer_contract()

deployer.address

# Create a filter to find new log contracts
new_log_filter = deployer.events.logCreated.createFilter(fromBlock="latest")

# Listen
print("Starting while loop...")
while True:
    # 1) Listen for new traders creating trading logs
    new_log_event = handle_new_log(new_log_filter.get_new_entries())
    if new_log_event:
        print("--------------------------")
        print((new_log_event[0]['args']))
        print("--------------------------")
        
        # add the information to a Grader object stored at that trader's ID variable
        new_log = new_log_event[0]['args']
        trader_dict[new_log['TraderId']]=Grader(new_log['TraderId'], new_log['newLogAddress'])
        trader_dict[new_log['TraderId']].load_contract()
            
    
    # loop through each trader and look for new trades at their log's contract address
    for key in trader_dict.keys():
        new_trade_event = handle_new_trade(trader_dict[key].new_trade_filter.get_new_entries())
        new_close_trade_event = handle_new_trade(trader_dict[key].close_trade_filter.get_new_entries())
        if new_trade_event:
            print("--------------------------")
            print((new_trade_event))
            print("--------------------------")
        if new_close_trade_event:
            new_close_trade_event[0]["TraderId"] = key 
            print("--------------------------")
            print((new_close_trade_event))
            print("--------------------------")  
                
    time.sleep(3)