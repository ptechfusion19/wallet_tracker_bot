from aiogram.filters.callback_data import CallbackData

class ButtonClass(CallbackData, prefix="btn"):
    btn_type:str
    wallet_id: int
    wallet_addres: str
