from database.db_operations import checke_wallet_no
from handlers.keyborad  import wallet_keyborad
from handlers.ca_action import lang_setter
from Messages.langobj import getter_lang
from handlers.ca_action import msg_setter
from handlers.keyborad import wallet_detial_keyboard, wallet_detial_keyboard2
from handlers.chain_validator import is_valid_eth_address ,is_valid_shi_address
from handlers.cleaner import cleaning_wallet_detial_eth , cleaning_wallet_detial_shi
async def msg_lang_setter():
    language = getter_lang()
    if  language == 'chinese':
        # msg_setter.start_command_text = """This is the official Maestro Wallet bot 🤖 deployed by @MaestroBots.

        # 💰/wallet - Initiates the bot and allows you to add BSC/ETH addresses💰

        # You can add up to 6 addresses!

        # Tutorial: https://i.imgur.com/ryeUm15.png

        # More commands will be added as the community flourishes. Stay tuned!"""

        # msg_setter.add_wallet_text = """Choose a blockchain you'd like to add a wallet from:"""
        # msg_setter.no_of_bsc_text = """Reply to this message with your BSC wallet address."""
        # msg_setter.no_of_eth_text = """Reply to this message with your ETH wallet address."""
        # msg_setter.no_of_shi_text = """Reply to this message with your SHI wallet address."""
        # msg_setter.wallet_limit_text = """YOUR LIMIR OF ADDIND WALLET IS EXCEDED """

        msg_setter.start_command_text = """这是 @MaestroBots 部署的官方 Maestro 钱包机器人 🤖。

        💰/wallet - 启动机器人并允许您添加 BSC/ETH 地址💰

        您最多可以添加 6 个地址！

        教程：https://i.imgur.com/ryeUm15.png

        随着社区的繁荣，将添加更多命令。敬请关注！"""
        

        msg_setter.add_wallet_text = """选择您想要添加钱包的区块链："""

        
        
        msg_setter.no_of_bsc_text = """使用您的 BSC 钱包地址回复此消息。"""

        
        msg_setter.no_of_eth_text = """使用您的 ETH 钱包地址回复此消息。"""

        
        msg_setter.no_of_shi_text = """使用您的 SHI 钱包地址回复此消息。"""
        msg_setter.wallet_limit_text = """您添加钱包的限制已超出"""


    else:
        # msg_setter.start_command_text = """这是 @MaestroBots 部署的官方 Maestro 钱包机器人 🤖。

        # 💰/wallet - 启动机器人并允许您添加 BSC/ETH 地址💰

        # 您最多可以添加 6 个地址！

        # 教程：https://i.imgur.com/ryeUm15.png

        # 随着社区的繁荣，将添加更多命令。敬请关注！"""
        

        # msg_setter.add_wallet_text = """选择您想要添加钱包的区块链："""

        
        
        # msg_setter.no_of_bsc_text = """使用您的 BSC 钱包地址回复此消息。"""

        
        # msg_setter.no_of_eth_text = """使用您的 ETH 钱包地址回复此消息。"""

        
        # msg_setter.no_of_shi_text = """使用您的 SHI 钱包地址回复此消息。"""
        # msg_setter.wallet_limit_text = """您添加钱包的限制已超出"""

        msg_setter.start_command_text = """This is the official Maestro Wallet bot 🤖 deployed by @MaestroBots.

        💰/wallet - Initiates the bot and allows you to add BSC/ETH addresses💰

        You can add up to 6 addresses!

        Tutorial: https://i.imgur.com/ryeUm15.png

        More commands will be added as the community flourishes. Stay tuned!"""

        msg_setter.add_wallet_text = """Choose a blockchain you'd like to add a wallet from:"""
        msg_setter.no_of_bsc_text = """Reply to this message with your BSC wallet address."""
        msg_setter.no_of_eth_text = """Reply to this message with your ETH wallet address."""
        msg_setter.no_of_shi_text = """Reply to this message with your SHI wallet address."""
        msg_setter.wallet_limit_text = """YOUR LIMIR OF ADDIND WALLET IS EXCEDED """

        

    


async def wallet_command_text_fun(user_id):
    
    no_of_wallet = await checke_wallet_no(user_id)
    lang =  getter_lang()
    if lang == "chinese":
        return  f"""💳 您总共有 {no_of_wallet} 个关联钱包 💳
    📢 Maestro - 与我们一起做广告@MaestroMarketer"""
    else:
        return f"""💳 You have a total of {no_of_wallet} linked wallet(s) 💳
    📢 Maestro - Advertise with us @MaestroMarketer"""


async def address_add(wallet_address, chain):
    lang =  getter_lang()

    if lang == "chinese":
        return f"""✅ 地址 \n {wallet_address} \n {chain} 已成功添加。"""
    else:
        return f"""✅ Address \n {wallet_address} \n {chain} has been successfully added."""


async def detailwallet_message(wallet_no,wallet_id,wallet_addres,chain_id):


    if chain_id == 0:
       print("bsc")
    elif chain_id == 1:
        
        wallet_detial_data = await is_valid_eth_address(wallet_addres)
        coin_symbols_holder_count =  await cleaning_wallet_detial_eth(wallet_detial_data)
    elif chain_id == 2:
        
        wallet_detial_data = await is_valid_shi_address(wallet_addres)
        coin_symbols_holder_count =  await cleaning_wallet_detial_shi(wallet_detial_data)

    try:
        sorted_detail = sorted(coin_symbols_holder_count, key=lambda x: x['tot_amount_in_usd'], reverse=True)
        top_tokens = sorted_detail[:5]
        formatted_message = "\n".join(
            
            f"{token['symbol']}:  | {token['tot_amount_in_usd']}$ USD | {token['total_amount_in_eth']} ETH | {token['market_cap']} MC | {token['address']}"
            for token in top_tokens
        )

        return formatted_message
    except TypeError:
        return "the wallet has no info"


#for gains 
async def gain_in_wallet(wallet_addres, chain_id):
    if chain_id == 0:
       print("bsc")
    elif chain_id == 1:
        
        wallet_detial_data = await is_valid_eth_address(wallet_addres)
        coin_symbols_holder_count =  await cleaning_wallet_detial_eth(wallet_detial_data)
    elif chain_id == 2:
        
        wallet_detial_data = await is_valid_shi_address(wallet_addres)
        coin_symbols_holder_count =  await cleaning_wallet_detial_shi(wallet_detial_data)

    try:
        sorted_detail = sorted(coin_symbols_holder_count, key=lambda x: x['tot_amount_in_usd'], reverse=True)
        top_tokens = sorted_detail[:5]
        formatted_message = "\n".join(
            f"{token['symbol']}:  | {token['tot_amount_in_usd']}$ USD | {token['total_amount_in_eth']} ETH | {token['price_change']} % "
            f"{':🟢:' if token['price_change'] >= 0 else ':🟠:' if -2 <= token['price_change'] < 0 else ':🔴:'}"
            f"| {token['market_cap']}"
            f"| {token['address']}"
            
  
            for token in top_tokens
        )

        return formatted_message
    except TypeError:
        return "the wallet has no info ABOUT GAINS"

