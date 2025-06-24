# core/checker.py
# Wannan fayil din zai kula da babban logic na binciken token.
# Zai hada bayanan da aka kwaso daga API.

from core.blockchain_data import (
    get_token_name, get_token_supply, get_token_holders,
    get_contract_abi, check_ownership_renounced, check_lp_lock
)

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
        'rug_pull_risk': 'HIGH' # Default to HIGH risk
    }

    try:
        # Samu ABI da sauran basic info
        # Zaka iya zaɓar chain din daidai da contract address din anan, misali ta hanyar prefixes ko data.
        # A nan, mun bar default 'eth' ne kawai don misali.
        abi = await get_contract_abi(contract_address, chain='eth')
        # Ba lallai bane duk contract ya dawo da ABI kai tsaye, musamman idan ba verified bane.
        # Don haka, idan ABI bata samu ba, za mu ci gaba da wasu binciken idan zai yiwu ko mu dawo da kuskure.

        details['token_name'] = await get_token_name(contract_address, chain='eth')
        details['total_supply'] = await get_token_supply(contract_address, chain='eth')
        details['holders_count'] = await get_token_holders(contract_address, chain='eth')

        if abi: # Idan an samu ABI, sai a ci gaba da bincike mai zurfi
            details['ownership_renounced'] = await check_ownership_renounced(contract_address, abi)
            details['lp_locked'] = await check_lp_lock(contract_address, abi)

        # Logic na rug pull risk
        # Wannan za'a inganta shi sosai. A yanzu, misali ne kawai na shawarwari.
        # Ainihin binciken rug pull yana buƙatar nazarin code, liquidity, history, da dai sauransu.
        if details['ownership_renounced'] and details['lp_locked'] and details['holders_count'] > 50:
            details['rug_pull_risk'] = 'LOW'
        else:
            details['rug_pull_risk'] = 'HIGH' # Idan akwai daya daga cikin abubuwan bai cika ba, zai zama HIGH

    except Exception as e:
        print(f"Kuskure yayin binciken token details for {contract_address}: {e}")
        return None

    return details
  
