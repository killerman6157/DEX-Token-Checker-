# core/checker.py
# Wannan fayil din zai kula da babban logic na binciken token.
# Zai hada bayanan da aka kwaso daga API.

from core.blockchain_data import (
    get_token_name, get_token_supply, get_token_holders,
    get_contract_abi, check_ownership_renounced, check_lp_lock
)

def detect_chain(contract_address: str) -> list:
    """
    Fahimci yiwuwar chain daga contract address.
    A yanzu, muna gwada duka EVM chains (eth, bsc, polygon).
    """
    if contract_address.startswith("0x") and len(contract_address) == 42:
        return ['eth', 'bsc', 'polygon']  # Dukkansu EVM chains
    else:
        return ['unknown']

async def check_token_details(contract_address: str) -> dict:
    """
    Yana bincika cikakken bayani game da token da aka ba da contract address.
    Yana dawo da dict mai dauke da bayanai kamar rug pull risk, ownership, LP lock, holders, etc.
    """

    details = {
        'contract_address': contract_address,
        'token_name': 'N/A',
        'total_supply': 'N/A',
        'holders_count': 'N/A',
        'ownership_renounced': False,
        'lp_locked': False,
        'rug_pull_risk': 'HIGH'  # Default to HIGH risk
    }

    possible_chains = detect_chain(contract_address)

    if 'unknown' in possible_chains:
        print(f"Chain type ba'a gane ba ko ba'a goyi bayan ba: {contract_address}")
        return details

    for chain in possible_chains:
        try:
            abi = await get_contract_abi(contract_address, chain=chain)
            if not abi:
                continue  # Gwada chain na gaba

            details['token_name'] = await get_token_name(contract_address, chain=chain)
            details['total_supply'] = await get_token_supply(contract_address, chain=chain)
            details['holders_count'] = await get_token_holders(contract_address, chain=chain)
            details['ownership_renounced'] = await check_ownership_renounced(contract_address, abi)
            details['lp_locked'] = await check_lp_lock(contract_address, abi)

            # Rug pull logic
            if details['ownership_renounced'] and details['lp_locked'] and details['holders_count'] > 50:
                details['rug_pull_risk'] = 'LOW'
            else:
                details['rug_pull_risk'] = 'HIGH'

            break  # Idan mun sami data daga wannan chain, ba sai mun ci gaba da gwaji ba

        except Exception as e:
            print(f"Kuskure yayin binciken token a {chain}: {e}")
            continue  # Gwada chain na gaba

    return details
            
