from aiogram.filters.callback_data import CallbackData

class ButtonClass(CallbackData, prefix="btn"):
    btn_type:str
    wallet_id: int
    wallet_addres: str
    wallet_no : int




class lang_setter:
    def __init__(self):
        self.lang = ""

    

class msg_setter:
    def __init__(self):
        self.start_command_text = ""
        self.add_wallet_text = ""
        self.no_of_bsc_text = ""
        self.no_of_eth_text = ""
        self.no_of_shi_text = ""
        self.wallet_limit_text = ""

