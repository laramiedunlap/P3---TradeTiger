import alpaca_trade_api as aplpaca
from alpaca_trade_api.rest import REST, TimeFrame
import os
from dotenv import load_dotenv
from web3 import Web3
from pathlib import Path
import json
load_dotenv()

import alpaca_trade_api as aplpaca
from alpaca_trade_api.rest import REST, TimeFrame
import os
import time
import pandas as pd

from web3 import Web3
from pathlib import Path

import json
from io import StringIO

from dotenv import load_dotenv
load_dotenv()

from itertools import zip
import atexit

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
            self.new_sub_filter = self.contract.events.newSub.createFilter(fromBlock="latest")
            
        return None
    
    def verify_trade(self):
        pass           
    
def load_deployer_contract(*args):
    if not args:
        contract_address = os.getenv("DEPLOYER_ADDRESS") 
        with open(Path('deployer.json')) as f:
                deployer_abi = json.load(f)

        deployer_contract = w3.eth.contract(
            address=contract_address,
            abi=deployer_abi)
    else:
        try:
            contract_address = args[0].strip()
            with open(Path('deployer.json')) as f:
                    deployer_abi = json.load(f)

            deployer_contract = w3.eth.contract(
                address=contract_address,
                abi=deployer_abi)
        except:
            return 0, print(f"this address doesn't seem to work: {args[0].strip()}")
        
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

print(f"This is your deployer address {deployer.address}")
question = input("Would you like to change it? (y/n)")
if question.strip() == "y":
    user_deployer_addr = input("please provide a new deployer address")
    deployer, trader_dict = load_deployer_contract(user_deployer_addr)
print("--------------------------")



# Create a filter to find new log contracts
new_log_filter = deployer.events.logCreated.createFilter(fromBlock="latest")
sub_df = pd.DataFrame(columns=(['TraderId', 'subNum', 'subAddr']))

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
        new_sub_event = handle_new_trade(trader_dict[key].new_sub_filter.get_new_entries())
        if new_trade_event:
            print("--------------------------")
            print((new_trade_event))
            print("--------------------------")
        if new_close_trade_event:
            new_close_trade_event[0]["TraderId"] = key 
            print("--------------------------")
            print((new_close_trade_event))
            print("--------------------------")
        if new_sub_event:
            print("--------------------------")
            print(new_sub_event)
            print("--------------------------")
            sub_df = sub_df.append(new_sub_event[0]['args'], ignore_index=True)
                
    time.sleep(3)