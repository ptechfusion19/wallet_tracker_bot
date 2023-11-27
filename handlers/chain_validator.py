import web3




import requests
import time
async def is_valid_eth_address(address):
    
    url = f"https://api.ethplorer.io/getAddressInfo/{address}?apiKey=freekey"
   
    try:
        # Make the GET request
        response = requests.get(url)
       
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            thirty_days_ago_timestamp = int(time.time()) - 30 * 24 * 60 * 60
            # Filter the response data
            latest_data_last_30_days = [
                token_data for token_data in data['tokens']
                if token_data['tokenInfo']['lastUpdated'] >= thirty_days_ago_timestamp
            ]
            return latest_data_last_30_days
            # for Transaction in latest_data_last_30_days:
            #     print(Transaction,'\n')
        else:
            return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None


async def is_valid_shi_address(address):
    
    url = f"https://www.shibariumscan.io/api/v2/addresses/{address}/tokens?type=ERC-20"
   
    
        # Make the GET request
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print(f" ............................................{data}......................................")
        token_info_list = data['items']
        result_list = []

        for token_info in token_info_list:
            token_data = token_info['token']
            result_list.append({
                'symbol': token_data['symbol'],
                'address': token_data['address'],
                'value': token_info['value']
            })
        
        return result_list

# if __name__ == "__main__":
#     # Launch the web scraping task
#     getAddress_detail('0x71C7656EC7ab88b098defB751B7401B5f6d8976F')





