# core/blockchain_data.py
# Wannan fayil din zai kula da hadaka da APIs na blockchain daban-daban.

import os
import aiohttp # Don async HTTP requests
import json
from web3 import Web3 # Zaka iya amfani da web3.py don hulda da EVM chains

# Daga config/settings.py
from config.settings import (
    ETHERSCAN_API_KEY, BSCSCAN_API_KEY, POLYGONSCAN_API_KEY,
    ETH_RPC_URL, BSC_RPC_URL, POLYGON_RPC_URL
)

# Web3 instances for EVM chains
# Tabbatar an haɗa da RPC URLs daidai
w3_eth = Web3(Web3.HTTPProvider(ETH_RPC_URL))
w3_bsc = Web3(Web3.HTTPProvider(BSC_RPC_URL))
w3_polygon = Web3(Web3.HTTPProvider(POLYGON_RPC_URL))

async def _fetch_data(url: str, params: dict = None) -> dict:
    """Helper function don fetching data daga API."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
            return await response.json()

async def get_contract_abi(contract_address: str, chain: str = 'eth') -> str | None:
    """Samu ABI na contract daga Etherscan/BscScan/Polygonscan."""
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
    # Zaka iya kara sauran chains anan (misali, don Solscan, SuiScan, Tonscan)
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
    """Samu sunan token."""
    w3 = None
    if chain == 'eth' and w3_eth.is_connected(): w3 = w3_eth
    elif chain == 'bsc' and w3_bsc.is_connected(): w3 = w3_bsc
    elif chain == 'polygon' and w3_polygon.is_connected(): w3 = w3_polygon
    # Kaddamar da sauran chains

    if w3:
        try:
            # Generic ERC-20 ABI portion for name, symbol, totalSupply, decimals
            erc20_abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"}]')
            token_contract = w3.eth.contract(address=w3.to_checksum_address(contract_address), abi=erc20_abi)
            return token_contract.functions.name().call()
        except Exception as e:
            print(f"Kuskure yayin samun sunan token {contract_address} on {chain}: {e}")
    return "N/A"

async def get_token_supply(contract_address: str, chain: str = 'eth') -> str:
    """Samu total supply na token."""
    w3 = None
    if chain == 'eth' and w3_eth.is_connected(): w3 = w3_eth
    elif chain == 'bsc' and w3_bsc.is_connected(): w3 = w3_bsc
    elif chain == 'polygon' and w3_polygon.is_connected(): w3 = w3_polygon

    if w3:
        try:
            erc20_abi = json.loads('[{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"}]')
            token_contract = w3.eth.contract(address=w3.to_checksum_address(contract_address), abi=erc20_abi)
            supply = token_contract.functions.totalSupply().call()
            decimals = token_contract.functions.decimals().call()
            return f"{supply / (10**decimals):,.0f}"
        except Exception as e:
            print(f"Kuskure yayin samun total supply {contract_address} on {chain}: {e}")
    return "N/A"

async def get_token_holders(contract_address: str, chain: str = 'eth') -> int:
    """Samu adadin holders na token."""
    # Wannan yana buƙatar wani API na daban kamar Arbiscan, Covalent, ko Nansen, waɗanda ke bayar da bayanai game da holders.
    # A nan misali ne kawai. Zaka buƙaci haɗawa da wani API mai inganci.
    print(f"Lura: Ana buƙatar API na musamman don samun cikakken adadin holders a {chain}. Wannan shine misali kawai.")
    if chain == 'eth':
        # Misali don Etherscan (amma baya bayar da cikakken holders count kai tsaye kyauta)
        # Zaka iya amfani da API kamar "Token Holders list" daga CoinGecko/CoinMarketCap idan kana da enterprise plan ko wani service
        return 0 # Ainihin adadin zai fito ne daga wani API na daban
    return 0

async def check_ownership_renounced(contract_address: str, abi: str) -> bool:
    """Bincika ko an raba ikon mallakar contract."""
    # Wannan yana da sarkakiya sosai kuma yana buƙatar nazarin ABI da contract code.
    # Gabaɗaya, yana nufin neman functions kamar `renounceOwnership()`, ko kuma babu wani `transferOwnership()` function da mai contract zai iya kira.
    # Don ainihin aiki, za ka buƙaci gano owner address (idan akwai) da kuma duba idan an canja shi zuwa null address ko wani address mara amfani.
    # A matsayin misali na farko, zamu dawo da True kawai.
    return True # Placeholder: Ka saka cikakken logic anan.

async def check_lp_lock(contract_address: str, abi: str) -> bool:
    """Bincika ko an kulle Liquidity Pool."""
    # Yana buƙatar binciken daftarin contract ko kuma haɗawa da sabis na "LP lock checker".
    # Yawancin lokaci ana kulle LP a cikin smart contract na musamman ko a dApps kamar UniCrypt, DxSale, Team.Finance.
    # Wannan bincike ne mai zurfi. A matsayin misali na farko, zamu dawo da True kawai.
    return True # Placeholder: Ka saka cikakken logic anan.
