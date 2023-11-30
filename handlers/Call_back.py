from aiogram.filters import CommandStart , Command
from aiogram.types import Message 
from aiogram import Bot, Dispatcher, Router, types
from Messages.message import  wallet_command_text_fun ,  address_add ,  msg_lang_setter
from handlers.ca_action import msg_setter
from handlers.keyborad import wallet_keyborad , adding_Wallet_keyborad , lang_types_btn , wallet_detail_chart_keyboard
from aiogram.types import CallbackQuery 
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from database.db_operations import insert_user , check_user,insert_wallet , checke_wallet_no , insert_chain,check_chain, delete_chain, delete_wallet , wallet_address_getter , wallet_chain_getter
from handlers.chain_validator import is_valid_eth_address ,is_valid_shi_address
from handlers.ca_action import ButtonClass , lang_setter , ButtonClassDetail,chartButton
from handlers.keyborad import delete_confirmation , wallet_detial_keyboard,wallet_detial_keyboard2
from database.db_operations import delete_wallet
from Messages.langobj import setter_lang
from handlers.cleaner import cleaning_wallet_detial_eth , cleaning_wallet_detial_shi
from aiogram.enums.parse_mode import ParseMode
import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Messages.message import detailwallet_message , gain_in_wallet
from aiogram import F
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
        if no_tot_wallet < 4:
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
        if no_tot_wallet < 4:
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
        if no_tot_wallet < 4:
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
    await query.message.answer(text=walllet_command_text ,reply_markup=wallet_keyboard_button)


# wallet detail keyboard 
@router.callback_query(ButtonClass.filter(F.btn_type=="walletDetail"))
async def handle_wallet_button(query:types.CallbackQuery,callback_data,state:FSMContext ):
    chain_checker = await wallet_chain_getter(callback_data.wallet_id)
    
    wallet_detail = await wallet_detial_keyboard( callback_data.wallet_no,callback_data.wallet_id)
    wallet_addres = await wallet_address_getter(callback_data.wallet_id)
    formatted_message = await detailwallet_message(callback_data.wallet_no,callback_data.wallet_id,wallet_addres[0],chain_checker[0])
    current_time = datetime.datetime.now().strftime("%Y %m %d %H:%M:%S")
    lines = formatted_message.split('\n')
    formatted_message_without_address = "\n".join(
    line.rsplit('|', 1)[0] if '| ' in line else line  # Remove the last part including token['address']
    for line in lines
        )
    await query.message.answer(text=f'''
```Copy
{formatted_message_without_address}``` ⌚ {current_time}⌚ 
ℹ️ *The bot only display tokens purchased  in the last 30 days\\.*  
🔊 Wallet Tracker  Advertise with us @wallet_taktak_bot''' , reply_markup=wallet_detail, parse_mode="MARKDOWNV2")
    await state.set_data({'formated_Data':formatted_message})



@router.callback_query(ButtonClassDetail.filter(F.btn_type=="walt_ads"))
async def handle_wallet_button2(query:types.CallbackQuery,callback_data , state:FSMContext):
    

    chain_checker = await wallet_chain_getter(callback_data.wallet_id)
    wallet_addres = await wallet_address_getter(callback_data.wallet_id)
    wallet_detail = await wallet_detial_keyboard( callback_data.wallet_no,callback_data.wallet_id)
    formatted_message = await detailwallet_message(callback_data.wallet_no,callback_data.wallet_id,wallet_addres[0],chain_checker[0])
    lines = formatted_message.split('\n')
    formatted_message_without_address = "\n".join(
    line.rsplit('|', 1)[0] if '| ' in line else line  # Remove the last part including token['address']
    for line in lines
        )
    if callback_data.wallet_name == "wallet_address":
        wallet_detail = await wallet_detial_keyboard2( callback_data.wallet_no,callback_data.wallet_id,wallet_addres[0])
        formatted_message = await detailwallet_message(callback_data.wallet_no,callback_data.wallet_id,wallet_addres[0],chain_checker[0])
    elif callback_data.wallet_name == "shw_mis_hid_tok":
        print("shw_mis_hid_tok")
    elif callback_data.wallet_name == "Refresh":
        print("Refresh")
    elif callback_data.wallet_name == "Mc":
        print("Mc")
    elif callback_data.wallet_name == "Gains":
        formatted_message = await gain_in_wallet(wallet_addres[0],chain_checker[0])
        lines = formatted_message.split('\n')
        formatted_message_without_address = "\n".join(
        line.rsplit('|', 1)[0] if '| ' in line else line  # Remove the last part including token['address']
        for line in lines
        )
        print("Gains")
    elif callback_data.wallet_name == "show_token":
        print("show_token")
    elif callback_data.wallet_name == "pin":
        print("pin")
    elif callback_data.wallet_name == "Manage":
        print("Manage")
    elif callback_data.wallet_name == "Price":
        print("Price")
    elif callback_data.wallet_name == "Inline":
        print("Inline")
        
    current_time = datetime.datetime.now().strftime("%Y %m %d %H:%M:%S")
    await query.message.edit_text(text=f'''
```Copy
{formatted_message_without_address}``` ⌚ {current_time}⌚ 
ℹ️ *The bot only display tokens purchased  in the last 30 days\\.*  
🔊 Wallet Tracker  Advertise with us @wallet_taktak_bot''' , reply_markup=wallet_detail, parse_mode="MARKDOWNV2")
    await state.set_data({'formated_Data':formatted_message})

    

# charts 
@router.callback_query(ButtonClassDetail.filter(F.btn_type == "charts"))
async def charts(query:types.CallbackQuery,callback_data, state:FSMContext):
    formatted_message = await state.get_data()
    formatted_message = formatted_message['formated_Data']
    print(formatted_message)
    addresses = [line.split('|')[-1].strip() for line in formatted_message.split('\n')]
    valid_addresses = [address for address in addresses if address]
    symbols = [token.split(':')[0] for token in formatted_message.split('\n')]

    get_buttons = await wallet_detail_chart_keyboard(symbols , callback_data.wallet_no , callback_data.wallet_id,valid_addresses)
    lines = formatted_message.split('\n')
    formatted_message_without_address = "\n".join(
    line.rsplit('|', 1)[0] if '| ' in line else line  # Remove the last part including token['address']
    for line in lines
        )
    current_time = datetime.datetime.now().strftime("%Y %m %d %H:%M:%S")
    await query.message.edit_text(text=f'''
```Copy
{formatted_message_without_address}``` ⌚ {current_time}⌚ 
ℹ️ *The bot only display tokens purchased  in the last 30 days\\.*  
🔊 Wallet Tracker  Advertise with us @wallet_taktak_bot''' , reply_markup=get_buttons, parse_mode="MARKDOWNV2")
    # await state.set_data({'formated_Data':formatted_message})
    
    


# @router.callback_query(chartButton.filter(F.btn_type == "showinfo"))
# async def showinfo(query:types.CallbackQuery,callback_data):
#     wallet_addres = callback_data.wallet_address
#     wallet_url = "https://www.dextools.io/app/ether/pair-explorer/"
#     keyboard = InlineKeyboardMarkup().add(
#         InlineKeyboardButton("Open URL", url=f"{wallet_url}{wallet_addres}")
#     )
#     await query.answer(f"Open this link? \n {wallet_addres} \n {wallet_url}" , show_alert=True , reply_markup=keyboard)


