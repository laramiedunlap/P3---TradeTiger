import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

def load_web3(abi_path):

    with open(Path(abi_path)) as f:
        logger_abi = json.load(f)

    contract_address = os.getenv("LOGGER_CONTRACT_ADDRESS")

    contract = w3.eth.contract(
        address=contract_address,
        abi=logger_abi
    )

    return contract,contract_address,w3

def load_custom_web3(abi_path,contactAddress):

    with open(Path(abi_path)) as f:
        logger_abi = json.load(f)

    contract = w3.eth.contract(
        address=contactAddress,
        abi=logger_abi
    )

    return contract,contactAddress,w3