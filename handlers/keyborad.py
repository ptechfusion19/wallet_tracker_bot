from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.db_operations import checke_wallet_no
async def wallet_keyborad(user_name,user_id):

    
    no_of_Wallets = await checke_wallet_no(user_id)
    
    button1 = InlineKeyboardButton(text=f"{user_name} wallet  " , callback_data="user_name")
    
    button2 = InlineKeyboardButton(text="Add Wallet" , callback_data="add_Wallet")
    button3 = InlineKeyboardButton(text="Language" , callback_data="Language_setting")
    if no_of_Wallets > 0:
        btn_list = []
        for i in range(no_of_Wallets):
            btn = InlineKeyboardButton(text=f"wallet {1}" , callback_data=f"wallet_{i}")
            btn_cancel = InlineKeyboardBuilder(text="❌" , callback_data=f"wallet_cancel_{i}")
        btn_list.append(btn,btn_cancel)
        builder = InlineKeyboardBuilder([[button1,button2,button3],btn_list])
        builder.adjust(1,2,2,2,2,2)
    else:
        button4 = InlineKeyboardButton(text=f"{no_of_Wallets} wallet's" , callback_data="total_wallet")
        builder = InlineKeyboardBuilder([[button1,button2,button3,button4]])
        builder.adjust(1,2,1)


    
    

    
    keyboard = builder.as_markup()

    return keyboard


async def adding_Wallet_keyborad():

    button1 = InlineKeyboardButton(text="BSC" , callback_data="BSC")
    button2 = InlineKeyboardButton(text="ETH" , callback_data="ETH")
    button3 = InlineKeyboardButton(text="SHI" , callback_data="SHI")

    builder = InlineKeyboardBuilder([[button1, button2 , button3]])
    builder.adjust(3)
    keyboard2 = builder.as_markup()

    return keyboard2

async def lang_types_btn(user_name):

    button1 = InlineKeyboardButton(text=f"{user_name} wallet" , callback_data="user_name")
    button2 = InlineKeyboardButton(text="Return" , callback_data="back_to_start")
    button3 = InlineKeyboardButton(text="🇷🇺" , callback_data="Russian_lang")
    button4 = InlineKeyboardButton(text="🇨🇳" , callback_data="Chinees_lang")

    builder = InlineKeyboardBuilder([[button1 , button2 , button3 , button4]])

    builder.adjust(1,1,2)
    keyboard3 = builder.as_markup()

    return keyboard3