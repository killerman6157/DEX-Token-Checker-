# core/blockchain_data.py

import os
import aiohttp
import json
from web3 import Web3
from config.settings import (
    ETHERSCAN_API_KEY, BSCSCAN_API_KEY, POLYGONSCAN_API_KEY,
    ETH_RPC_URL, BSC_RPC_URL, POLYGON_RPC_URL, SOLANA_RPC_URL
)

# Web3 Instances
w3_eth = Web3(Web3.HTTPProvider(ETH_RPC_URL))
w3_bsc = Web3(Web3.HTTPProvider(BSC_RPC_URL))
w3_polygon = Web3(Web3.HTTPProvider(POLYGON_RPC_URL))

# Generic ERC-20 ABI (for name, supply, decimals)
erc20_abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},
{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},
{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"}]')

async def _fetch_data(url: str, params: dict = None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()

async def get_contract_abi(contract_address: str, chain: str) -> str | None:
    base_url, api_key = "", ""
    if chain == 'eth':
        base_url = "https://api.etherscan.io/api"
        api_key = ETHERSCAN_API_KEY
    elif chain == 'bsc':
        base_url = "https://api.bscscan.com/api"
        api_key = BSCSCAN_API_KEY
    elif chain == 'polygon':
        base_url = "https://api.polygonscan.com/api"
        api_key = POLYGONSCAN_API_KEY
    else:
        return None

    params = {
        'module': 'contract',
        'action': 'getabi',
        'address': contract_address,
        'apikey': api_key
    }
    try:
        data = await _fetch_data(base_url, params)
        if data['status'] == '1':
            return data['result']
    except Exception as e:
        print(f"ABI error {contract_address}: {e}")
    return None

async def get_token_name(contract_address: str, chain: str) -> str:
    try:
        if chain == 'eth' and w3_eth.is_connected():
            contract = w3_eth.eth.contract(address=w3_eth.to_checksum_address(contract_address), abi=erc20_abi)
            return contract.functions.name().call()
        elif chain == 'bsc' and w3_bsc.is_connected():
            contract = w3_bsc.eth.contract(address=w3_bsc.to_checksum_address(contract_address), abi=erc20_abi)
            return contract.functions.name().call()
        elif chain == 'polygon' and w3_polygon.is_connected():
            contract = w3_polygon.eth.contract(address=w3_polygon.to_checksum_address(contract_address), abi=erc20_abi)
            return contract.functions.name().call()
        elif chain == 'sol':
            return await get_solana_token_name(contract_address)
    except Exception as e:
        print(f"Token name error {contract_address}: {e}")
    return "N/A"

async def get_token_supply(contract_address: str, chain: str) -> str:
    try:
        if chain == 'eth' and w3_eth.is_connected():
            contract = w3_eth.eth.contract(address=w3_eth.to_checksum_address(contract_address), abi=erc20_abi)
            supply = contract.functions.totalSupply().call()
            decimals = contract.functions.decimals().call()
            return f"{supply / (10**decimals):,.0f}"
        elif chain == 'bsc' and w3_bsc.is_connected():
            contract = w3_bsc.eth.contract(address=w3_bsc.to_checksum_address(contract_address), abi=erc20_abi)
            supply = contract.functions.totalSupply().call()
            decimals = contract.functions.decimals().call()
            return f"{supply / (10**decimals):,.0f}"
        elif chain == 'polygon' and w3_polygon.is_connected():
            contract = w3_polygon.eth.contract(address=w3_polygon.to_checksum_address(contract_address), abi=erc20_abi)
            supply = contract.functions.totalSupply().call()
            decimals = contract.functions.decimals().call()
            return f"{supply / (10**decimals):,.0f}"
        elif chain == 'sol':
            return await get_solana_total_supply(contract_address)
    except Exception as e:
        print(f"Supply error {contract_address}: {e}")
    return "N/A"

async def get_token_holders(contract_address: str, chain: str) -> int:
    print(f"Lura: API na daban ke buƙata don holders for {chain}.")
    return 0

async def check_ownership_renounced(contract_address: str, abi: str) -> bool:
    return True  # Placeholder

async def check_lp_lock(contract_address: str, abi: str) -> bool:
    return True  # Placeholder

async def get_solana_token_name(token_address: str) -> str:
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenSupply",
            "params": [token_address]
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(SOLANA_RPC_URL, headers=headers, json=payload) as resp:
                data = await resp.json()
                if 'result' in data:
                    return "Solana Token"
    except Exception as e:
        print(f"Solana token name error: {e}")
    return "N/A"

async def get_solana_total_supply(token_address: str) -> str:
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenSupply",
            "params": [token_address]
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(SOLANA_RPC_URL, headers=headers, json=payload) as resp:
                data = await resp.json()
                if 'result' in data and 'value' in data['result']:
                    ui_amount = data['result']['value']['uiAmountString']
                    return ui_amount
    except Exception as e:
        print(f"Solana total supply error: {e}")
    return "N/A"
