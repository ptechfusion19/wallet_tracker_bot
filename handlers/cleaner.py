
import requests
async def cleaning_wallet_detial_eth(wallet_detial_data):

    wallet_symbol_and_counthold = []
    
    print(wallet_detial_data)
    for item in wallet_detial_data:
        print(item)
        token_info = item.get('tokenInfo', {})
        token_tot_balance = float(item.get('balance'))
        symbol = token_info.get('symbol')
        address = token_info.get('address')
        decimals =  float(token_info.get('decimals'))
        amount_in_dec = float(token_tot_balance /(10 ** decimals))
        response_from_token_add = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{address}")
        response_from_token_add = response_from_token_add.json()
        
        pairs_info = response_from_token_add['pairs']
        if pairs_info:  
            for pair_info in pairs_info:
                
                if pair_info['labels'][0] == "v2":
                    token_price_in_usd = float(pair_info['priceUsd'])
                    
                    
                    total_in_usd = float(token_price_in_usd * amount_in_dec)
                    print(total_in_usd)

                    if symbol is not None and address is not None:
                        wallet_symbol_and_counthold.append({'symbol': symbol, 'tot_amount_in_usd': total_in_usd})

    return wallet_symbol_and_counthold



async def cleaning_wallet_detial_shi(wallet_detial_data):
    wallet_symbol_and_counthold = []
    for item in wallet_detial_data:
        address_token = item['address']
        symbol = item['symbol']
        value_amount = float(item['value'])
        decimals_val = float(item['decimals'])
        display_amount = float(value_amount / (10 ** decimals_val))
        response_from_token_add = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{address_token}")
        response_from_token = response_from_token_add.json() 
        pairs_info = response_from_token['pairs']
        if pairs_info: 
            for pair_info in pairs_info: 
                token_price_in_usd = float(pair_info['priceUsd'])
                total_in_usd = float(token_price_in_usd * display_amount)
                if symbol is not None and address_token is not None:
                    wallet_symbol_and_counthold.append({'symbol': symbol, 'tot_amount_in_usd': total_in_usd})

    return wallet_symbol_and_counthold