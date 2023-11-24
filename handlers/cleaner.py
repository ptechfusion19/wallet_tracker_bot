
async def cleaning_wallet_detial(wallet_detial_data):

    wallet_symbol_and_counthold = []
    
    for item in wallet_detial_data:
        token_info = item.get('tokenInfo', {})
        symbol = token_info.get('symbol')
        holders_count = token_info.get('holdersCount')

        if symbol is not None and holders_count is not None:
            wallet_symbol_and_counthold.append({'symbol': symbol, 'holdersCount': holders_count})

    return wallet_symbol_and_counthold



