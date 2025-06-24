import os
import aiohttp
import json
from web3 import Web3

# Daga config/settings.py
from config.settings import (
    ETHERSCAN_API_KEY, BSCSCAN_API_KEY, POLYGONSCAN_API_KEY,
    ETH_RPC_URL, BSC_RPC_URL, POLYGON_RPC_URL, SOLANA_RPC_URL
)

# Web3 instances for EVM chains
w3_eth = Web3(Web3.HTTPProvider(ETH_RPC_URL))
w3_bsc = Web3(Web3.HTTPProvider(BSC_RPC_URL))
w3_polygon = Web3(Web3.HTTPProvider(POLYGON_RPC_URL))

async def _fetch_data(url: str, params: dict = None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()

async def get_contract_abi(contract_address: str, chain: str = 'eth') -> str | None:
    base_url = ""
    api_key = ""
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
        print(f"Chain '{chain}' ba'a goyi bayan ta ba don samun ABI a halin yanzu.")
        return None

    params = {
        'module': 'contract',
        'action': 'getabi',
        'address': contract_address,
        'apikey': api_key
    }
    try:
        data = await _fetch_data(base_url, params)
        if data and data['status'] == '1' and data['result']:
            return data['result']
        print(f"Kasa samun ABI for {contract_address} on {chain}: {data.get('message', 'No result')}")
        return None
    except Exception as e:
        print(f"Kuskure yayin samun ABI for {contract_address}: {e}")
        return None

async def get_token_name(contract_address: str, chain: str = 'eth') -> str:
    w3 = None
    if chain == 'eth' and w3_eth.is_connected(): w3 = w3_eth
    elif chain == 'bsc' and w3_bsc.is_connected(): w3 = w3_bsc
    elif chain == 'polygon' and w3_polygon.is_connected(): w3 = w3_polygon

    if w3:
        try:
            erc20_abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]')
            token_contract = w3.eth.contract(address=w3.to_checksum_address(contract_address), abi=erc20_abi)
            return token_contract.functions.name().call()
        except Exception as e:
            print(f"Kuskure yayin samun sunan token {contract_address} on {chain}: {e}")
    return "N/A"

async def get_token_supply(contract_address: str, chain: str = 'eth') -> str:
    w3 = None
    if chain == 'eth' and w3_eth.is_connected(): w3 = w3_eth
    elif chain == 'bsc' and w3_bsc.is_connected(): w3 = w3_bsc
    elif chain == 'polygon' and w3_polygon.is_connected(): w3 = w3_polygon

    if w3:
        try:
            erc20_abi = json.loads('[{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"}]')
            token_contract = w3.eth.contract(address=w3.to_checksum_address(contract_address), abi=erc20_abi)
            supply = token_contract.functions.totalSupply().call()
            decimals = token_contract.functions.decimals().call()
            return f"{supply / (10**decimals):,.0f}"
        except Exception as e:
            print(f"Kuskure yayin samun total supply {contract_address} on {chain}: {e}")
    return "N/A"

async def get_token_holders(contract_address: str, chain: str = 'eth') -> int:
    print(f"Lura: Ana buƙatar API na musamman don samun cikakken adadin holders a {chain}.")
    return 0

async def check_ownership_renounced(contract_address: str, abi: str) -> bool:
    return True

async def check_lp_lock(contract_address: str, abi: str) -> bool:
    return True

# -------- SOLANA SUPPORT ----------

async def get_solana_token_data(contract_address: str) -> dict | None:
    try:
        async with aiohttp.ClientSession() as session:
            url = SOLANA_RPC_URL
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getTokenSupply",
                "params": [contract_address]
            }
            async with session.post(url, json=payload) as resp:
                res = await resp.json()
                value = res.get("result", {}).get("value", {})
                return {
                    "token_name": "N/A",
                    "total_supply": value.get("uiAmountString", "N/A"),
                    "holders_count": 0,
                    "ownership_renounced": False,
                    "lp_locked": False
                }
    except Exception as e:
        print(f"Kuskure yayin fetching Solana token data: {e}")
        return None
            
