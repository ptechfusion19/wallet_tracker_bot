from database.db_operations import checke_wallet_no
start_command_text = """This is the official Maestro Wallet bot 🤖 deployed by @MaestroBots.

💰/wallet - Initiates the bot and allows you to add BSC/ETH addresses💰

You can add up to 6 addresses!

Tutorial: https://i.imgur.com/ryeUm15.png

More commands will be added as the community flourishes. Stay tuned!"""




add_wallet_text = """Choose a blockchain you'd like to add a wallet from:"""

no_of_bsc_text = """Reply to this message with your BSC wallet address."""
no_of_eth_text = """Reply to this message with your ETH wallet address."""
no_of_shi_text = """Reply to this message with your SHI wallet address"""

async def wallet_command_text_fun(user_id):
    
    no_of_wallet = await checke_wallet_no(user_id)


    return  f"""💳 You have a total of {no_of_wallet} linked wallet(s) 💳
📢 Maestro - Advertise with us @MaestroMarketer"""
