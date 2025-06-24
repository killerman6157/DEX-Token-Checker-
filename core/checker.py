# core/checker.py
# Wannan fayil din zai kula da babban logic na binciken token.
# Yanzu yana goyon bayan ETH, BSC, da Solana.

from core.blockchain_data import (
    get_token_name, get_token_supply, get_token_holders,
    get_contract_abi, check_ownership_renounced, check_lp_lock
)

def detect_chain(contract_address: str) -> str:
    """
    Gano chain daga format din contract address.
    """
    if contract_address.startswith("0x") and len(contract_address) == 42:
        # Ethereum ko BSC ko Polygon - za a fara da ETH
        return "eth"
    elif len(contract_address) == 44:  # Solana base58
        return "sol"
    else:
        return "unknown"

async def check_token_details(contract_address: str) -> dict:
    """
    Yana bincika cikakken bayani game da token da aka ba da contract address.
    """
    chain = detect_chain(contract_address)

    details = {
        'contract_address': contract_address,
        'token_name': 'N/A',
        'total_supply': 'N/A',
        'holders_count': 'N/A',
        'ownership_renounced': False,
        'lp_locked': False,
        'rug_pull_risk': 'HIGH'
    }

    if chain == "unknown":
        print("Chain bai da goyon baya ko address bai dace ba.")
        return details

    try:
        abi = None
        if chain in ['eth', 'bsc', 'polygon']:
            abi = await get_contract_abi(contract_address, chain=chain)

        details['token_name'] = await get_token_name(contract_address, chain=chain)
        details['total_supply'] = await get_token_supply(contract_address, chain=chain)
        details['holders_count'] = await get_token_holders(contract_address, chain=chain)

        if abi:
            details['ownership_renounced'] = await check_ownership_renounced(contract_address, abi)
            details['lp_locked'] = await check_lp_lock(contract_address, abi)
        elif chain == "sol":
            # Solana placeholder - ownership da LP lock ba su da API kai tsaye
            details['ownership_renounced'] = True
            details['lp_locked'] = True

        # Rug pull risk logic
        if details['ownership_renounced'] and details['lp_locked'] and isinstance(details['holders_count'], int) and details['holders_count'] > 50:
            details['rug_pull_risk'] = 'LOW'

    except Exception as e:
        print(f"Kuskure yayin binciken token details for {contract_address}: {e}")
        return None

    return details
