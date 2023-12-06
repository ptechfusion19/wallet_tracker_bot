from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.db_operations import checke_wallet_no , get_wallet_id_address
from handlers.ca_action import ButtonClass , ButtonClassDetail, chartButton
from handlers.ca_action import lang_setter


async def wallet_keyborad(user_name,user_id):

    
    no_of_Wallets = await checke_wallet_no(user_id)
    
    button1 = InlineKeyboardButton(text=f"{user_name} wallet  " , callback_data="user_name")
    
    button2 = InlineKeyboardButton(text="Add Wallet" , callback_data="add_Wallet")
    # button3 = InlineKeyboardButton(text="Language" , callback_data="Language_setting")
    wallet_ids , wallet_ads = await get_wallet_id_address(user_id)
    if no_of_Wallets > 0:
        btn_list = []
        for i in range(no_of_Wallets):
            btn_list.append(InlineKeyboardButton(text=f"wallet {i}", callback_data=ButtonClass(btn_type="walletDetail",wallet_id=wallet_ids[i],wallet_addres=wallet_ads[i],wallet_no=str(i)).pack()))
            btn_list.append(InlineKeyboardButton(text="❌", callback_data=ButtonClass(btn_type="delete",wallet_id=wallet_ids[i],wallet_addres=wallet_ads[i],wallet_no=str(i)).pack()))
           
        
        # Assuming button1, button2, button3 are defined somewhere in your code
        builder = InlineKeyboardBuilder([[button1, button2], btn_list])
        builder.adjust(1, 1, 2, 2, 2, 2)

    else:
        button4 = InlineKeyboardButton(text=f"{no_of_Wallets} wallet's" , callback_data="total_wallet")
        builder = InlineKeyboardBuilder([[button1,button2,button4]])
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
    button3 = InlineKeyboardButton(text="🇺🇸" , callback_data="English_lang")
    button4 = InlineKeyboardButton(text="🇨🇳" , callback_data="Chinese_lang")

    builder = InlineKeyboardBuilder([[button1 , button2 , button3 , button4]])

    builder.adjust(1,1,2)
    keyboard3 = builder.as_markup()

    return keyboard3



#confirm deletion keyborad 

async def delete_confirmation(user_name,user_id,wallet_id):

    
    no_of_Wallets = await checke_wallet_no(user_id)
    
    button1 = InlineKeyboardButton(text=f"{user_name} wallet  " , callback_data="user_name")
    
    button2 = InlineKeyboardButton(text="Add Wallet" , callback_data="add_Wallet")
    # button3 = InlineKeyboardButton(text="Language" , callback_data="Language_setting")
    wallet_ids , wallet_ads = await get_wallet_id_address(user_id)
    if no_of_Wallets > 0:
        btn_list = []
        for i in range(no_of_Wallets):
            if wallet_id == wallet_ids[i]:
                btn_list.append(InlineKeyboardButton(text=f"wallet {i}", callback_data=ButtonClass(btn_type="walletDetail",wallet_id=wallet_ids[i],wallet_addres=wallet_ads[i],wallet_no=str(i)).pack()))
                btn_list.append(InlineKeyboardButton(text="Confirm", callback_data=ButtonClass(btn_type="confirm",wallet_id=wallet_ids[i],wallet_addres=wallet_ads[i],wallet_no=str(i)).pack()))
            else:              
                btn_list.append(InlineKeyboardButton(text=f"wallet {i}", callback_data=ButtonClass(btn_type="walletDetail",wallet_id=wallet_ids[i],wallet_addres=wallet_ads[i],wallet_no=str(i)).pack()))
                btn_list.append(InlineKeyboardButton(text="❌", callback_data=ButtonClass(btn_type="walletDetail",wallet_id=wallet_ids[i],wallet_addres=wallet_ads[i],wallet_no=str(i)).pack()))
           
        
        # Assuming button1, button2, button3 are defined somewhere in your code
        builder = InlineKeyboardBuilder([[button1, button2], btn_list])
        builder.adjust(1, 1, 2, 2, 2, 2)

    else:
        button4 = InlineKeyboardButton(text=f"{no_of_Wallets} wallet's" , callback_data="total_wallet")
        builder = InlineKeyboardBuilder([[button1,button2,button4]])
        builder.adjust(1,2,1)

    keyboard = builder.as_markup()

    return keyboard


# wallet detial keyboard 

async def wallet_detial_keyboard(wallet_no,wallet_id,pin):
    wallet_no_button = InlineKeyboardButton(text=f"Wallet {wallet_no}",callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="wallet_address").pack())
    show_token = InlineKeyboardButton(text="Show Missing and Hide Existing Tokens" , callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no,wallet_name="shw_mis_hid_tok").pack())
    refresh = InlineKeyboardButton(text="Refresh", callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="Refresh").pack())
    Mc = InlineKeyboardButton(text="MC" ,callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="Mc").pack())
    Gains = InlineKeyboardButton(text="Gains" , callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="Gains").pack())
    note_book  = InlineKeyboardButton(text="📃" ,callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="show_token").pack())
    chart_wallet  = InlineKeyboardButton(text="📈" ,callback_data=ButtonClassDetail(btn_type="charts" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="chart").pack())
    pin_wallet  = InlineKeyboardButton(text=f"📌{pin}" ,callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="pin").pack())
    Manage_wallet  = InlineKeyboardButton(text="Manage" , callback_data=ButtonClassDetail(btn_type="Manage_walt" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="Manage").pack())
    inline_wallet = InlineKeyboardButton(text="Inline" ,callback_data=ButtonClassDetail(btn_type="walt_inline" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="Inline").pack())

    builder3 = InlineKeyboardBuilder([[wallet_no_button , show_token,refresh,Mc , Gains , note_book,chart_wallet,pin_wallet,Manage_wallet,inline_wallet]])
    builder3.adjust(1,1,3,3,3)
    keyborad = builder3.as_markup()

    return keyborad

async def wallet_detial_keyboard_inline(wallet_no,wallet_id,text,pin):
    
    wallet_no_button = InlineKeyboardButton(text=f"Wallet {wallet_no}",callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="wallet_address").pack())
    show_token = InlineKeyboardButton(text="Show Missing and Hide Existing Tokens" , callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no,wallet_name="shw_mis_hid_tok").pack())
    refresh = InlineKeyboardButton(text="Refresh", callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="Refresh").pack())
    Mc = InlineKeyboardButton(text="MC" ,callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="Mc").pack())
    Gains = InlineKeyboardButton(text="Gains" , callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="Gains").pack())
    note_book  = InlineKeyboardButton(text="📃" ,callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="show_token").pack())
    chart_wallet  = InlineKeyboardButton(text="📈" ,callback_data=ButtonClassDetail(btn_type="charts" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="chart").pack())
    pin_wallet  = InlineKeyboardButton(text=f"📌{pin}" ,callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="pin").pack())
    Manage_wallet  = InlineKeyboardButton(text="Manage" , callback_data=ButtonClassDetail(btn_type="Manage_walt" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="Manage").pack())
    inline_wallet = InlineKeyboardButton(text=text ,callback_data=ButtonClassDetail(btn_type="walt_inline" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name=text).pack())

    builder3 = InlineKeyboardBuilder([[wallet_no_button , show_token,refresh,Mc , Gains , note_book,chart_wallet,pin_wallet,Manage_wallet,inline_wallet]])
    builder3.adjust(1,1,3,3,3)
    keyborad = builder3.as_markup()

    return keyborad

async def wallet_detial_keyboard2(wallet_no,wallet_id,wallet_ads,wallet_ads_adder,pin):
    if wallet_ads_adder == "wallet_address_added":
        wallet_no_button = InlineKeyboardButton(text=f"{wallet_ads}",callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name=wallet_ads_adder).pack())
    else:
        wallet_no_button = InlineKeyboardButton(text=f"Wallet {wallet_no}",callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name=wallet_ads_adder).pack())

    show_token = InlineKeyboardButton(text="Show Missing and Hide Existing Tokens" , callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no,wallet_name="shw_mis_hid_tok").pack())
    refresh = InlineKeyboardButton(text="Refresh", callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="Refresh").pack())
    Mc = InlineKeyboardButton(text="MC" ,callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="Mc").pack())
    Gains = InlineKeyboardButton(text="Gains" , callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="Gains").pack())
    note_book  = InlineKeyboardButton(text="📃" ,callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="show_token").pack())
    chart_wallet  = InlineKeyboardButton(text="📈" ,callback_data=ButtonClassDetail(btn_type="charts" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="chart").pack())
    pin_wallet  = InlineKeyboardButton(text=f"📌{pin}" ,callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="pin").pack())
    Manage_wallet  = InlineKeyboardButton(text="Manage" , callback_data=ButtonClassDetail(btn_type="Manage_walt" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="Manage").pack())
    inline_wallet = InlineKeyboardButton(text="Inline" ,callback_data=ButtonClassDetail(btn_type="walt_inline" , wallet_id=wallet_id,wallet_no=wallet_no , wallet_name="Inline").pack())

    builder3 = InlineKeyboardBuilder([[wallet_no_button , show_token,refresh,Mc , Gains , note_book,chart_wallet,pin_wallet,Manage_wallet,inline_wallet]])
    builder3.adjust(1,1,3,3,3)
    keyborad = builder3.as_markup()


    return keyborad

async def show_miss_and_hide_token(wallet_no,wallet_id ,valid_addresses, symbols):
    wallet_no_button = InlineKeyboardButton(text=f"Wallet {wallet_no}", callback_data=ButtonClassDetail(btn_type="walt_mis_hide",wallet_id=wallet_id,wallet_no=wallet_no,wallet_name="wallet_address").pack())
    wallet_add_token = InlineKeyboardButton(text=f"Add Token" ,callback_data=ButtonClassDetail(btn_type="walt_mis_hide",wallet_id=wallet_id,wallet_no=wallet_no,wallet_name="Add_token").pack())
    wallet_return =  InlineKeyboardButton(text=f"Return & Refresh" ,callback_data=ButtonClassDetail(btn_type="walt_ads",wallet_id=wallet_id,wallet_no=wallet_no,wallet_name="Refresh").pack())
    symbol_btn_list = []
    for j,i in enumerate(symbols):
        
        symbol_btn_list.append(InlineKeyboardButton(text=f"🟢 {i}", callback_data=chartButton(btn_type="walt_hiding",wallet_address=valid_addresses[j]).pack()))

    wallet_disbale_tokens = InlineKeyboardButton(text=f"Show Disabled Tokens" , callback_data=ButtonClassDetail(btn_type="showdisabletoken" , wallet_id=wallet_id,wallet_no=wallet_no,wallet_name="Showdisabledtoken").pack())
    symbol_btn_list.append(wallet_disbale_tokens)
    builder = InlineKeyboardBuilder([[wallet_no_button,wallet_add_token,wallet_return] , symbol_btn_list ])
    builder.adjust(1,2,3,3,1)
    keyboard = builder.as_markup()
    return keyboard

    

async def wallet_detail_chart_keyboard(symbols,wallet_no,wallet_id , valid_addresses):
    
    wallet_no_button = InlineKeyboardButton(text=f"Wallet {wallet_no}" , callback_data=ButtonClassDetail(btn_type="walt_chart", wallet_id=wallet_id , wallet_no=wallet_no , wallet_name="wallet_address").pack())
    wallet_return_button = InlineKeyboardButton(text="Return" , callback_data=ButtonClassDetail(btn_type="walt_ads" , wallet_id=wallet_id , wallet_no=wallet_no, wallet_name="return").pack())
    symbol_btn_list = []
    wallet_url = "https://www.dextools.io/app/ether/pair-explorer/"
    for j,i in enumerate(symbols):
        
        symbol_btn_list.append(InlineKeyboardButton(text=f"{i}", url=wallet_url + valid_addresses[j], callback_data=chartButton(btn_type="showinfo",wallet_address=valid_addresses[j]).pack()))

    builder = InlineKeyboardBuilder([[wallet_no_button , wallet_return_button ] , symbol_btn_list])
    builder.adjust(1,1,3,3)
    keyboard = builder.as_markup()
    return keyboard


async def wallet_manage_keyboard(wallet_no ,wallet_id , removebtn):
    wallet_no_button = InlineKeyboardButton(text=f"Wallet {wallet_no}" , callback_data=ButtonClassDetail(btn_type="walt_manage", wallet_id=wallet_id , wallet_no=wallet_no , wallet_name="walt_manage").pack())
    wallet_return = InlineKeyboardButton(text="Return" , callback_data=ButtonClassDetail(btn_type="walt_ads", wallet_id=wallet_id , wallet_no=wallet_no , wallet_name="walt_manage").pack())
    wallet_add = InlineKeyboardButton(text="Add" , callback_data="add_Wallet")
    wallet_list = InlineKeyboardButton(text="List" , callback_data="List_wallet")
    if removebtn == "":
        wallet_remove = InlineKeyboardButton(text="Remove" , callback_data=ButtonClass(btn_type="confirm_delete" , wallet_id=wallet_id , wallet_addres="NA" , wallet_no=wallet_no).pack())
    elif removebtn == "confirmdeletion":
        wallet_remove = InlineKeyboardButton(text="Confirm" , callback_data=ButtonClass(btn_type=f"{removebtn}" , wallet_id=wallet_id , wallet_addres="NA" , wallet_no=wallet_no).pack())

    builder = InlineKeyboardBuilder([[wallet_no_button , wallet_return , wallet_add , wallet_list , wallet_remove]])
    builder.adjust(1,3,2)

    keyboard = builder.as_markup()
    return keyboard