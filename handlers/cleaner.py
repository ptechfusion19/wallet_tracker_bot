
import requests
import json
async def cleaning_wallet_detial_eth(wallet_detial_data):

    wallet_symbol_and_counthold2 = []
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "ethereum",
        "vs_currencies": "usd"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        eth_price = data.get("ethereum", {}).get("usd")
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")

    print(wallet_detial_data)
    url = f'https://api.dexscreener.com/latest/dex/tokens/{wallet_detial_data[0].get("tokenInfo").get("address")}'

    for item in wallet_detial_data:
        print(item)
        token_info = item.get('tokenInfo', {})
        token_tot_balance = float(item.get('balance'))
        symbol = token_info.get('symbol')
        address = token_info.get('address')
        decimals =  float(token_info.get('decimals'))
        amount_in_dec = float(token_tot_balance /(10 ** decimals))
        if address not in url:
            url = url+','+address
        
    response_from_token_add = requests.get(url)
    response_from_token_add = response_from_token_add.json()
    print(response_from_token_add)    
    pairs = response_from_token_add['pairs']
    for pair_info in pairs:
        # pairs_info = json.loads(pairs_info)
        if pair_info:
            # pairs_info = dict(pairs_info)  
            # for pair_info in pairs_info:
            print(pair_info)
            try:
                if pair_info['labels'][0] == "v2":
                    token_price_in_usd = float(pair_info['priceUsd'])
                    token_price_in_eth = float(eth_price)
                    price_change = float(pair_info['priceChange'].get('h24'))
                    market_cap = float(pair_info['fdv'])
        
                    total_in_usd = float(token_price_in_usd * amount_in_dec)
                    total_in_eth = float(total_in_usd / token_price_in_eth)
                    print(total_in_usd)

                    if symbol is not None and address is not None:
                        wallet_symbol_and_counthold2.append({'symbol': symbol, 'tot_amount_in_usd': total_in_usd , 'total_amount_in_eth':total_in_eth,'price_change':price_change,'market_cap':market_cap , 'address':address})
            except KeyError:
                print("nothing ")
    return wallet_symbol_and_counthold2



async def cleaning_wallet_detial_shi(wallet_detial_data):
    wallet_symbol_and_counthold2 = []
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "ethereum",
        "vs_currencies": "usd"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        eth_price = data.get("ethereum", {}).get("usd")
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
    print(wallet_detial_data[0])
    url = f'https://api.dexscreener.com/latest/dex/tokens/{wallet_detial_data[0].get("address")}'
    for item in wallet_detial_data:
        address_token = item['address']
        symbol = item['symbol']
        value_amount = float(item['value'])
        decimals_val = float(item['decimals'])
        display_amount = float(value_amount / (10 ** decimals_val))
        if address_token not in url:
            url = url+','+address_token
        # response_from_token_add = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{address_token}")
    response_from_token_add = requests.get(url)
    response_from_token = response_from_token_add.json() 
    pairs_info = response_from_token['pairs']
    if pairs_info: 
        try:
            for pair_info in pairs_info: 
                token_price_in_usd = float(pair_info['priceUsd'])
                price_change = float(pair_info['priceChange'].get('h24'))
                market_cap = float(pair_info['fdv'])
                token_price_in_eth = float(eth_price)
                total_in_usd = float(token_price_in_usd * display_amount)
                total_in_eth = float(total_in_usd / token_price_in_eth)
                if symbol is not None and address_token is not None:
                    wallet_symbol_and_counthold2.append({'symbol': symbol, 'tot_amount_in_usd': total_in_usd ,'total_amount_in_eth':total_in_eth, 'price_change':price_change,'market_cap':market_cap ,'address':address_token })
        except KeyError:
                return None            
    return wallet_symbol_and_counthold2