
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
    symbol = []
    address = []
    address.append(wallet_detial_data[0].get("tokenInfo").get("address").lower())
    amount_in_dec =  []
    j = 0
    for item in wallet_detial_data:
        print(item)
        token_info = item.get('tokenInfo', {})
        token_tot_balance = float(item.get('balance'))
        symbol.append(token_info.get('symbol'))    
        decimals =  float(token_info.get('decimals'))
        amount_in_dec.append(float(token_tot_balance /(10 ** decimals)))
        if token_info.get('address') not in url:
            address.append(token_info.get('address').lower())
            url = url+','+token_info.get('address')
            j += 1
            
    
    i = 0
    print(url)
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
                address_checker = pair_info['baseToken'].get('address') 
                quote_token_ads =  pair_info['quoteToken'].get('address')
                if address_checker.lower() in address or quote_token_ads.lower() in address:
                    token_price_in_usd = float(pair_info['priceUsd'])
                    token_price_in_eth = float(eth_price)
                    price_change = float(pair_info['priceChange'].get('h24'))
                    market_cap = float(pair_info['fdv'])
        
                    total_in_usd = float(token_price_in_usd * amount_in_dec[i])
                    total_in_eth = float(total_in_usd / token_price_in_eth)
                    print(total_in_usd)

                    if symbol[i] is not None and address[i] is not None:
                        total_in_usd = round(total_in_usd,2)
                        total_in_eth ='{:.3f}'.format(total_in_eth)
                        wallet_symbol_and_counthold2.append({'symbol': symbol[i], 'tot_amount_in_usd': total_in_usd , 'total_amount_in_eth':total_in_eth,'price_change':price_change,'market_cap':market_cap , 'address':address[i]})
                        i += 1
                        try:
                            address.remove(address_checker.lower())
                            
                        except ValueError:
                            try:
                                address.remove(quote_token_ads.lower())
                                print("nothing found")
                            except ValueError:
                                print("nothing found")
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
    symbol = []
    address = []
    address.append(wallet_detial_data[0].get("address").lower())
    amount_in_dec =  []
    j = 0
    for item in wallet_detial_data:
        
        symbol.append(item['symbol'])
        value_amount = float(item['value'])
        decimals_val = float(item['decimals'])
        amount_in_dec.append(float(value_amount / (10 ** decimals_val)))
        if item['address'] not in url:
            address.append(item['address'].lower())
            url = url+','+item['address']
            j += 1
        # response_from_token_add = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{address_token}")
    i = 0
    response_from_token_add = requests.get(url)
    response_from_token = response_from_token_add.json() 
    pairs_info = response_from_token['pairs']
    if pairs_info: 
        try:
            for pair_info in pairs_info: 
                address_checker = pair_info['baseToken'].get('address') 
                quote_token_ads =  pair_info['quoteToken'].get('address')
                if address_checker.lower() in address or quote_token_ads.lower() in address:
                    token_price_in_usd = float(pair_info['priceUsd'])
                    price_change = float(pair_info['priceChange'].get('h24'))
                    market_cap = float(pair_info['fdv'])
                    token_price_in_eth = float(eth_price)
                    total_in_usd = float(token_price_in_usd * amount_in_dec[i])
                    total_in_eth = float(total_in_usd / token_price_in_eth)
                    if symbol[i] is not None and address[i] is not None:
                        total_in_usd = round(total_in_usd,2)
                        total_in_eth = '{:.3f}'.format(total_in_eth)
                        wallet_symbol_and_counthold2.append({'symbol': symbol[i], 'tot_amount_in_usd': total_in_usd ,'total_amount_in_eth':total_in_eth, 'price_change':price_change,'market_cap':market_cap ,'address':address[i] })
                        i += 1
                        try:
                            address.remove(address_checker.lower())
                            
                        except ValueError:
                            try:
                                address.remove(quote_token_ads.lower())
                                print("nothing found")
                            except ValueError:
                                print("nothing found")
        except KeyError:
                return None            
    return wallet_symbol_and_counthold2