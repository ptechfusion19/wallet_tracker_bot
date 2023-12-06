from aiogram.filters import CommandStart , Command
from aiogram.types import Message 
from aiogram import Bot, Dispatcher, Router, types
from Messages.message import  wallet_command_text_fun ,  address_add ,  msg_lang_setter
from handlers.ca_action import msg_setter
from handlers.keyborad import wallet_keyborad , adding_Wallet_keyborad , lang_types_btn , wallet_detail_chart_keyboard ,wallet_manage_keyboard
from aiogram.types import CallbackQuery 
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from database.db_operations import insert_user , check_user,insert_wallet , checke_wallet_no , insert_chain,check_chain, delete_chain, delete_wallet , wallet_address_getter , wallet_chain_getter,connected_wallet_list
from handlers.chain_validator import is_valid_eth_address ,is_valid_shi_address
from handlers.ca_action import ButtonClass , lang_setter , ButtonClassDetail,chartButton
from handlers.keyborad import delete_confirmation , wallet_detial_keyboard,wallet_detial_keyboard2 ,wallet_detial_keyboard_inline , show_miss_and_hide_token
from database.db_operations import delete_wallet
from Messages.langobj import setter_lang
from handlers.cleaner import cleaning_wallet_detial_eth , cleaning_wallet_detial_shi
from aiogram.enums.parse_mode import ParseMode
import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Messages.message import detailwallet_message , gain_in_wallet
from aiogram import F
from tabulate import tabulate
router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await msg_lang_setter()
    # await delete_wallet("0x2028018Ad987228dBa4D66261a5e608E48F438de")
    user_checker = await check_user(message.from_user.id)
    # await delete_chain(0)
    chain_checker = await check_chain()
    if chain_checker == False:
        await insert_chain(0,"BSC")
        await insert_chain(1,"ETH")
        await insert_chain(2,"SHI")



    if user_checker == False:
        await insert_user(message.from_user.id , message.from_user.username)
    
    await message.answer(f"{(msg_setter.start_command_text)}!")

    
    

@router.callback_query(lambda callback_query:callback_query.data == "back_to_start")
async def back_to_start(callback_query:types.CallbackQuery):
    wallet_keyboard_button = await wallet_keyborad(callback_query.from_user.username , callback_query.from_user.id)
    await callback_query.bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    walllet_command_text = await wallet_command_text_fun(callback_query.from_user.id)
    await callback_query.message.answer( text=walllet_command_text , reply_markup=wallet_keyboard_button) 


@router.message(Command('wallet'))
async def wallet_Command(message: Message)-> None:
    if await check_user(message.from_user.id) == False:
        insert_user(message.from_user.id , message.from_user.username)
    wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
    walllet_command_text = await wallet_command_text_fun(message.from_user.id)
    await message.answer( text=walllet_command_text , reply_markup=wallet_keyboard_button)    


@router.callback_query(lambda callback_query: callback_query.data == "user_name")
async def user_name_btn(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Username selected.")


@router.callback_query(lambda callback_query: callback_query.data == "add_Wallet")
async def user_add_Wallet(callback_query: types.CallbackQuery):
    await msg_lang_setter()
    add_Wallet_key = await adding_Wallet_keyborad()
    await callback_query.message.answer( msg_setter.add_wallet_text , reply_markup=add_Wallet_key)

@router.callback_query(lambda callback_query:callback_query.data == "BSC" )
async def bsc_input(callback_query: types.CallbackQuery, state: FSMContext ):
    force_reply_bsc = types.ForceReply(input_field_placeholder="0x420F69...")
    await callback_query.message.answer( text=msg_setter.no_of_bsc_text , reply_markup=force_reply_bsc)
    await state.set_state("bsc_wallet_address")


@router.message(StateFilter("bsc_wallet_address"))
async def bsc_wallet_address(message:Message , state:FSMContext)-> None:
    wallet_addres  = message.text
    walllet_command_text = await wallet_command_text_fun(message.from_user.id)
    wallet_detail = await is_valid_eth_address(wallet_addres)
    if wallet_detail:
        no_tot_wallet = await checke_wallet_no(message.from_user.id)
        if no_tot_wallet < 7:
            await insert_wallet(wallet_addres , message.from_user.id , 0 )
            wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
            await message.answer(text=await address_add(wallet_addres ,"bsc"))
            walllet_command_text = await wallet_command_text_fun(message.from_user.id)
            await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)
            state.clear()
        else:
            wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
            await message.answer(text=msg_setter.wallet_limit_text)
            await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)
            state.clear()
    else:
        wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
        await message.reply(text="Invalid address provided!")
        await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)
        state.clear()


    

@router.callback_query(lambda callback_query:callback_query.data == "ETH")
async def eth_input(callback_query: types.CallbackQuery, state: FSMContext):
    force_reply_eth = types.ForceReply(input_field_placeholder="0x420F69...")
    await callback_query.message.answer( text=msg_setter.no_of_eth_text , reply_markup=force_reply_eth)
    await state.set_state("eth_wallet_address")


@router.message(StateFilter("eth_wallet_address"))
async def eth_wallet_address(message:Message , state:FSMContext)-> None:
    wallet_addres  = message.text
    walllet_command_text = await wallet_command_text_fun(message.from_user.id)
    wallet_detail = await is_valid_eth_address(wallet_addres)
    if wallet_detail:
        no_tot_wallet = await checke_wallet_no(message.from_user.id)
        if no_tot_wallet < 7:
            await insert_wallet(wallet_addres , message.from_user.id , 1 )
            wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
            await message.answer(text=await address_add(wallet_addres , "eth"))
            walllet_command_text = await wallet_command_text_fun(message.from_user.id)
            await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)
            state.clear()
        else:
            wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
            await message.answer(text=msg_setter.wallet_limit_text)
            await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)
            state.clear()
    else:
        wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
        await message.reply(text="Invalid address provided!")
        await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)
        state.clear()





@router.callback_query(lambda callback_query:callback_query.data == "SHI")
async def shi_input(callback_query: types.CallbackQuery, state: FSMContext):
    force_reply_shi = types.ForceReply(input_field_placeholder="0x420F69...")
    await callback_query.message.answer( text=msg_setter.no_of_shi_text , reply_markup=force_reply_shi)
    await state.set_state("shi_wallet_address")


@router.message(StateFilter("shi_wallet_address"))
async def shi_wallet_address(message:Message , state:FSMContext)-> None:
    wallet_addres  = message.text
    walllet_command_text = await wallet_command_text_fun(message.from_user.id)
    wallet_detail = await is_valid_shi_address(wallet_addres)
    if wallet_detail:
        no_tot_wallet = await checke_wallet_no(message.from_user.id)
        if no_tot_wallet < 7:
            await insert_wallet(wallet_addres , message.from_user.id , 2 )
            wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
            # await message.answer(text=f"✅ Address \n {wallet_addres} \n (shi) has been successfully added.")
            await message.answer(text=await address_add(wallet_addres , "shi"))
            walllet_command_text = await wallet_command_text_fun(message.from_user.id)
            await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)
            state.clear()
        else:
            wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
            await message.answer(text=msg_setter.wallet_limit_text)
            await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)
            state.clear()
    else:
        wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
        await message.reply(text="Invalid address provided!")
        await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)
        state.clear()


@router.callback_query(lambda callback_query:callback_query.data == "Language_setting")
async def lang_setting(callback_query: types.CallbackQuery):
    lang_keyboard = await lang_types_btn(callback_query.from_user.username)
    await callback_query.bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    walllet_command_text = await wallet_command_text_fun(callback_query.from_user.id)
    await callback_query.message.answer(text=walllet_command_text , reply_markup=lang_keyboard)

@router.callback_query(lambda callback_query:callback_query.data == "Chinese_lang")
async def chinees_lang(callback_query: types.CallbackQuery):
    await setter_lang("chinese")
    await msg_lang_setter()
    wallet_keyboard_button = await wallet_keyborad(callback_query.from_user.username , callback_query.from_user.id)
    walllet_command_text = await wallet_command_text_fun(callback_query.from_user.id)
    await callback_query.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)

@router.callback_query(lambda callback_query:callback_query.data == "English_lang")
async def chinees_lang(callback_query: types.CallbackQuery):
    await setter_lang("English")
    await msg_lang_setter()
    wallet_keyboard_button = await wallet_keyborad(callback_query.from_user.username , callback_query.from_user.id)
    walllet_command_text = await wallet_command_text_fun(callback_query.from_user.id)
    await callback_query.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)

# deleting the wallet

@router.callback_query(ButtonClass.filter(F.btn_type=="delete"))
async def handle_Wallet_cancel(query:types.CallbackQuery,callback_data):
    # wallet_address_get = await wallet_address_getter(callback_data.wallet_id)
    walllet_command_text = await wallet_command_text_fun(query.from_user.id)
    delete_confirm_keyboard = await delete_confirmation(query.from_user.username , query.from_user.id, callback_data.wallet_id)

    await query.message.edit_text(text=walllet_command_text , reply_markup=delete_confirm_keyboard)


#now delete the wallet 

@router.callback_query(ButtonClass.filter(F.btn_type=="confirm"))
async def handle_wallet_delete(query:types.CallbackQuery,callback_data , state:FSMContext):

    await delete_wallet(callback_data.wallet_id)

    await query.message.answer(text=f"✅ Deleted wallet address \n {callback_data.wallet_addres}")
    walllet_command_text = await wallet_command_text_fun(query.from_user.id)
    wallet_keyboard_button = await wallet_keyborad(query.from_user.username , query.from_user.id)
    await query.message.edit_text(text=walllet_command_text ,reply_markup=wallet_keyboard_button)


# wallet detail keyboard 
@router.callback_query(ButtonClass.filter(F.btn_type=="walletDetail"))
async def handle_wallet_button(query:types.CallbackQuery,callback_data,state:FSMContext ):
    chain_checker = await wallet_chain_getter(callback_data.wallet_id)
    try:
        pin = await state.get_data()
        pin = pin['pins']
        if pin == 25:
            pin = 5
    except KeyError:
        pin = 5
    wallet_detail = await wallet_detial_keyboard( callback_data.wallet_no,callback_data.wallet_id,pin)
    wallet_addres = await wallet_address_getter(callback_data.wallet_id)
    formatted_message , tot_display = await detailwallet_message(callback_data.wallet_no,callback_data.wallet_id,wallet_addres[0],chain_checker[0],pin)
    current_time = datetime.datetime.now().strftime("%Y %m %d %H:%M:%S")
    lines = formatted_message.split('\n')
    formatted_message_without_address = "\n".join(
    line.rsplit('|', 2)[0] if '| ' in line else line  # Remove the last part including token['address']
    for line in lines
        )
    await query.message.answer(text=f'''
```Copy
{formatted_message_without_address}
{tot_display}``` ⌚ {current_time}⌚ 
ℹ️ *The bot only display tokens purchased  in the last 30 days\\.*  
🔊 Wallet Tracker  Advertise with us @wallet_taktak_bot''' , reply_markup=wallet_detail, parse_mode="MARKDOWNV2")
    await state.set_data({'formated_Data':formatted_message,'without_address': formatted_message_without_address,'pins':pin,'tot_display':tot_display})
    



@router.callback_query(ButtonClassDetail.filter(F.btn_type=="walt_ads"))
async def handle_wallet_button2(query:types.CallbackQuery,callback_data , state:FSMContext):
    
    formatted_text_all = await state.get_data()
    try:
        pin = await state.get_data()
        pin = pin['pins']
        if pin == 25:
            pin = 5
    except KeyError:
        pin = 5
    chain_checker = await wallet_chain_getter(callback_data.wallet_id)
    wallet_addres = await wallet_address_getter(callback_data.wallet_id)
    wallet_detail = await wallet_detial_keyboard( callback_data.wallet_no,callback_data.wallet_id,pin)
    formatted_message , tot_display = await detailwallet_message(callback_data.wallet_no,callback_data.wallet_id,wallet_addres[0],chain_checker[0],pin)
    lines = formatted_message.split('\n')
    formatted_message_without_address = "\n".join(
    line.rsplit('|', 2)[0] if '| ' in line else line  # Remove the last part including token['address']
    for line in lines
        )
    try:
        gain_data = await state.get_data()
        gain_data = gain_data['gain_in_wallet']
    except KeyError:
        gain_data = "No"
    try:
        market_cap = await state.get_data()
        market_cap = market_cap['market_cap']
    except KeyError:
        market_cap = "No"
    if callback_data.wallet_name == "wallet_address":
        wallet_detail = await wallet_detial_keyboard2( callback_data.wallet_no,callback_data.wallet_id,wallet_addres[0],"wallet_address_added",pin)
        formatted_message , tot_display = await detailwallet_message(callback_data.wallet_no,callback_data.wallet_id,wallet_addres[0],chain_checker[0],pin)
    elif callback_data.wallet_name == "wallet_address_added":
        wallet_detail = await wallet_detial_keyboard2( callback_data.wallet_no,callback_data.wallet_id,wallet_addres[0],"wallet_address",pin)
        formatted_message , tot_display = await detailwallet_message(callback_data.wallet_no,callback_data.wallet_id,wallet_addres[0],chain_checker[0],pin)
    elif callback_data.wallet_name == "shw_mis_hid_tok":
        addresses = [line.split('|')[-1].strip() for line in formatted_message.split('\n')]
        valid_addresses = [address for address in addresses if address]
        symbols = [token.split(':')[0] for token in formatted_message.split('\n')]
        get_buttons = await show_miss_and_hide_token(callback_data.wallet_no , callback_data.wallet_id,valid_addresses ,symbols )
        wallet_detail = get_buttons
        print("shw_mis_hid_tok")
    elif callback_data.wallet_name == "Refresh":
        print("new data")
        print("Refresh")
    elif callback_data.wallet_name == "Mc":
        if market_cap == "No":
            lines = formatted_message.split('\n')
            formatted_message_without_address = "\n".join(
                    line.rsplit('|', 1)[0] if '| ' in line else line  # Remove the last part including token['address']
                    for line in lines
                    )
            market_cap = "yes"
            gain_data = "No"
        else:
            lines = formatted_message.split('\n')
            formatted_message_without_address = "\n".join(
                    line.rsplit('|', 2)[0] if '| ' in line else line  # Remove the last part including token['address']
                    for line in lines
                    )
            market_cap = "No"   
            
        print("Mc")
    elif callback_data.wallet_name == "Gains":
        try:
            if gain_data == "yes":
                formatted_message , tot_display = await gain_in_wallet(wallet_addres[0],chain_checker[0],pin)
                lines = formatted_message.split('\n')
                formatted_message_without_address = "\n".join(
                line.rsplit('|', 3)[0] if '| ' in line else line  # Remove the last part including token['address']
                for line in lines
                )
                gain_data = "No"
                print("remove gains ")
            else:
                formatted_message , tot_display = await gain_in_wallet(wallet_addres[0],chain_checker[0],pin)
                lines = formatted_message.split('\n')
                formatted_message_without_address = "\n".join(
                line.rsplit('|', 2)[0] if '| ' in line else line  # Remove the last part including token['address']
                for line in lines
                )
                print("Gains")
                gain_data = "yes"
                market_cap = "No"
        except KeyError:
            formatted_message , tot_display = await gain_in_wallet(wallet_addres[0],chain_checker[0],pin)
            lines = formatted_message.split('\n')
            formatted_message_without_address = "\n".join(
            line.rsplit('|', 2)[0] if '| ' in line else line  # Remove the last part including token['address']
            for line in lines
            )
            print("Gains")
            
    elif callback_data.wallet_name == "show_token":
        current_wallet_ads = await wallet_address_getter(callback_data.wallet_id)
        await query.message.answer(text=current_wallet_ads[0])
        print("show_token")
    elif callback_data.wallet_name == "pin":
        wallet_detail = await wallet_detial_keyboard( callback_data.wallet_no,callback_data.wallet_id,pin)
        formatted_message , tot_display = await detailwallet_message(callback_data.wallet_no,callback_data.wallet_id,wallet_addres[0],chain_checker[0],pin)
        pin += 5
        print("pin")
    elif callback_data.wallet_name == "Inline":
        print("Inline")
        
    current_time = datetime.datetime.now().strftime("%Y %m %d %H:%M:%S")
    await query.message.edit_text(text=f'''
```Copy
{formatted_message_without_address}
{tot_display}``` ⌚ {current_time}⌚ 
ℹ️ *The bot only display tokens purchased  in the last 30 days\\.*  
🔊 Wallet Tracker  Advertise with us @wallet_taktak_bot''' , reply_markup=wallet_detail, parse_mode="MARKDOWNV2")
    await state.set_data({'formated_Data':formatted_message, 'without_address': formatted_message_without_address , 'gain_in_wallet':gain_data, 'market_cap':market_cap,'pins':pin,'tot_display':tot_display})

    

# charts 
@router.callback_query(ButtonClassDetail.filter(F.btn_type == "charts"))
async def charts(query:types.CallbackQuery,callback_data, state:FSMContext):
    
    formatted_message_all = await state.get_data()
    formatted_message = formatted_message_all['formated_Data']
    tot_display = formatted_message_all['tot_display']
    print(formatted_message)
    addresses = [line.split('|')[-1].strip() for line in formatted_message.split('\n')]
    valid_addresses = [address for address in addresses if address]
    symbols = [token.split(':')[0] for token in formatted_message.split('\n')]

    get_buttons = await wallet_detail_chart_keyboard(symbols , callback_data.wallet_no , callback_data.wallet_id,valid_addresses)
    lines = formatted_message.split('\n')
    formatted_message_without_address = "\n".join(
    line.rsplit('|', 2)[0] if '| ' in line else line  # Remove the last part including token['address']
    for line in lines
        )
    current_time = datetime.datetime.now().strftime("%Y %m %d %H:%M:%S")
    await query.message.edit_text(text=f'''
```Copy
{formatted_message_without_address}
{tot_display}``` ⌚ {current_time}⌚ 
ℹ️ *The bot only display tokens purchased  in the last 30 days\\.*  
🔊 Wallet Tracker  Advertise with us @wallet_taktak_bot''' , reply_markup=get_buttons, parse_mode="MARKDOWNV2")
    await state.set_data({'tot_display':tot_display})
    # await state.set_data({'formated_Data':formatted_message})

@router.callback_query(ButtonClassDetail.filter(F.btn_type  == "Manage_walt"))
async def Manage_walt(query:types.CallbackQuery,callback_data, state:FSMContext):
    removebtn = ""
    get_formatted_text_all =await state.get_data()
    get_formatted_text = get_formatted_text_all['without_address']
    tot_display = get_formatted_text_all['tot_display']
    get_buttons = await wallet_manage_keyboard(callback_data.wallet_no , callback_data.wallet_id,removebtn)

    current_time = datetime.datetime.now().strftime("%Y %m %d %H:%M:%S")
    await query.message.edit_text(text=f'''
    ```Copy
{get_formatted_text}
{tot_display}``` ⌚ {current_time}⌚ 
ℹ️ *The bot only display tokens purchased  in the last 30 days\\.*  
🔊 Wallet Tracker  Advertise with us @wallet_taktak_bot''' , reply_markup=get_buttons, parse_mode="MARKDOWNV2")
    await state.set_state({'without_address':get_formatted_text,'tot_display':tot_display})



    

@router.callback_query(ButtonClass.filter(F.btn_type =="confirm_delete"))
async def confirm_delete(query:types.CallbackQuery , callback_data,state:FSMContext):
    formatted_text_all = await state.get_data()
    formatted_text = formatted_text_all['without_address']
    tot_display = formatted_text_all['tot_display']
    removebtn = "confirmdeletion"
    get_buttons = await wallet_manage_keyboard(callback_data.wallet_no , callback_data.wallet_id,removebtn)
    current_time = datetime.datetime.now().strftime("%Y %m %d %H:%M:%S")
    await query.message.edit_text(text=f'''
    ```Copy
{formatted_text}
{tot_display}``` ⌚ {current_time}⌚ 
ℹ️ *The bot only display tokens purchased  in the last 30 days\\.*  
🔊 Wallet Tracker  Advertise with us @wallet_taktak_bot''' , reply_markup=get_buttons, parse_mode="MARKDOWNV2")
    await state.set_state({'without_address':formatted_text})

@router.callback_query(ButtonClass.filter((F.btn_type =="confirmdeletion")))
async def confirm_delete(query:types.CallbackQuery , callback_data,state:FSMContext):
    wallet_address = await wallet_address_getter(callback_data.wallet_id)
    await delete_wallet(callback_data.wallet_id)
    
    await query.message.answer(text=f"✅ Deleted wallet address \n {wallet_address}")
    walllet_command_text = await wallet_command_text_fun(query.from_user.id)
    wallet_keyboard_button = await wallet_keyborad(query.from_user.username , query.from_user.id)
    await query.message.answer(text=f"{walllet_command_text}",reply_markup=wallet_keyboard_button)

@router.callback_query(lambda callback_query:callback_query.data == "List_wallet")
async def List_wallet(callback_query:types.CallbackQuery):
    wallet_addresses = await connected_wallet_list(callback_query.from_user.id)
    formatted_wallets = []

    for index, wallet_address_tuple in enumerate(wallet_addresses, 1):
       
        wallet_address = wallet_address_tuple[0]

       
        formatted_wallet = f"Wallet {index}: {wallet_address}"
        formatted_wallets.append(formatted_wallet)

    formatted_message = "\n".join(formatted_wallets)
    await callback_query.message.answer(text=f"Connected Wallet: \n {formatted_message}" )

@router.callback_query(ButtonClassDetail.filter(F.btn_type == "walt_inline"))
async def walt_inline(query:types.CallbackQuery , callback_data , state:FSMContext):
    try:
        pin = await state.get_data()
        pin = pin['pins']
        if pin == 25:
            pin = 5
    except KeyError:
        pin = 5
    formatted_text_all = await state.get_data()
    formatted_text = formatted_text_all['without_address']
    tot_display = formatted_text_all['tot_display']
    try:
        formatted_text_table = formatted_text_all['table_text']
    except KeyError:
        formatted_text_table = ""
    getting_button_text = query.data.replace('get_text_','')
    print(getting_button_text)
    last_part = getting_button_text.split(':')[-1]
    print(last_part)
    last_part2 = [line.split('|')[-1].strip() for line in formatted_text.split('\n') if line.strip()]
    print(last_part2)
    gain_in_wallet = ""
    market_cap = ""
    try:
        market_cap = formatted_text_all['market_cap']
    except KeyError:
        print("no market_Cap found ")
    try:
        gain_in_wallet = formatted_text_all['gain_in_wallet']
    except KeyError:
        print("no gain found")

    
    if market_cap == "yes":
        if last_part == "Inline":
            keyboard = await wallet_detial_keyboard_inline(callback_data.wallet_no , callback_data.wallet_id, 'Table',pin)
            rows = [line.split('|') for line in formatted_text.strip().split('\n')]
            headers = ["Symbol", "USD", "ETH" , "Market_Cap"]
            data = [{headers[i]: row[i].strip() for i in range(len(headers))} for row in rows]
            formatted_text_table = tabulate(data, headers="keys", tablefmt="fancy_grid")
            msg_to_show = formatted_text_table
            market_cap = "yes"

        else:
            formatted_text = formatted_text
            keyboard = await wallet_detial_keyboard_inline(callback_data.wallet_no , callback_data.wallet_id, 'Inline',pin)
            market_cap = "yes"
            msg_to_show = formatted_text



    elif gain_in_wallet == "yes":
        if last_part == "Inline":
            keyboard = await wallet_detial_keyboard_inline(callback_data.wallet_no , callback_data.wallet_id,'Table',pin)
            rows = [line.split('|') for line in formatted_text.strip().split('\n')]

            # Extract headers and rows for tabulate
            headers = ["Symbol", "USD", "ETH" , "CHANGE"]
            data = [{headers[i]: row[i].strip() for i in range(len(headers))} for row in rows]

            # Convert data to table format
            formatted_text_table = tabulate(data, headers="keys", tablefmt="fancy_grid")
            msg_to_show = formatted_text_table
            gain_in_wallet = "yes"
        else:

            formatted_text = formatted_text

            keyboard = await wallet_detial_keyboard_inline(callback_data.wallet_no , callback_data.wallet_id, 'Inline',pin)
            msg_to_show = formatted_text
            gain_in_wallet = "yes"
    else:
        if last_part == "Inline":
            keyboard = await wallet_detial_keyboard_inline(callback_data.wallet_no , callback_data.wallet_id,'Table',pin)
            rows = [line.split('|') for line in formatted_text.strip().split('\n')]

            # Extract headers and rows for tabulate
            headers = ["Symbol", "USD", "ETH" ]
            data = [{headers[i]: row[i].strip() for i in range(len(headers))} for row in rows]

            # Convert data to table format
            formatted_text_table = tabulate(data, headers="keys", tablefmt="fancy_grid")
            msg_to_show = formatted_text_table
            gain_in_wallet = "No"
        else:

            formatted_text = formatted_text
            keyboard = await wallet_detial_keyboard_inline(callback_data.wallet_no , callback_data.wallet_id, 'Inline',pin)
            msg_to_show = formatted_text
            gain_in_wallet = "No"
    
    current_time = datetime.datetime.now().strftime("%Y %m %d %H:%M:%S")
    await query.message.edit_text(text=f'''
    ```Copy
{msg_to_show}
{tot_display}``` ⌚ {current_time}⌚ 
    ℹ️ *The bot only display tokens purchased  in the last 30 days\\.*  
    🔊 Wallet Tracker  Advertise with us @wallet_taktak_bot''' , reply_markup=keyboard, parse_mode="MARKDOWNV2")
    await state.set_data({'without_address':formatted_text, 'gain_in_wallet':gain_in_wallet ,'market_cap':market_cap,'table_text':formatted_text_table,'tot_display':tot_display})