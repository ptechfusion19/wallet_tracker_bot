from aiogram.filters import CommandStart , Command
from aiogram.types import Message 
from aiogram import Bot, Dispatcher, Router, types
from Messages.message import  wallet_command_text_fun ,  address_add ,  msg_lang_setter
from handlers.ca_action import msg_setter
from handlers.keyborad import wallet_keyborad , adding_Wallet_keyborad , lang_types_btn
from aiogram.types import CallbackQuery 
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from database.db_operations import insert_user , check_user,insert_wallet , checke_wallet_no , insert_chain,check_chain, delete_chain, delete_wallet , wallet_address_getter , wallet_chain_getter
from handlers.chain_validator import is_valid_eth_address ,is_valid_shi_address
from handlers.ca_action import ButtonClass , lang_setter
from handlers.keyborad import delete_confirmation , wallet_detial_keyboard,wallet_detial_keyboard2
from database.db_operations import delete_wallet
from Messages.langobj import setter_lang
from handlers.cleaner import cleaning_wallet_detial_eth , cleaning_wallet_detial_shi
from aiogram.enums.parse_mode import ParseMode
import datetime
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
        else:
            wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
            await message.answer(text=msg_setter.wallet_limit_text)
            await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)
    else:
        wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
        await message.reply(text="Invalid address provided!")
        await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)


    

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
        else:
            wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
            await message.answer(text=msg_setter.wallet_limit_text)
            await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)
    else:
        wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
        await message.reply(text="Invalid address provided!")
        await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)






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
        else:
            wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
            await message.answer(text=msg_setter.wallet_limit_text)
            await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)
    else:
        wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
        await message.reply(text="Invalid address provided!")
        await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)


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
async def handle_wallet_delete(query:types.CallbackQuery,callback_data):

    await delete_wallet(callback_data.wallet_id)

    await query.message.answer(text=f"✅ Deleted wallet address \n {callback_data.wallet_addres}")
    walllet_command_text = await wallet_command_text_fun(query.from_user.id)
    wallet_keyboard_button = await wallet_keyborad(query.from_user.username , query.from_user.id)
    await query.message.answer(text=walllet_command_text ,reply_markup=wallet_keyboard_button)


# wallet detail keyboard 
@router.callback_query(ButtonClass.filter(F.btn_type=="walletDetail"))
async def handle_wallet_button(query:types.CallbackQuery,callback_data ):

    chain_checker = await wallet_chain_getter(callback_data.wallet_id)
    if chain_checker[0] == 0:
        print("bsc")
    elif chain_checker[0] == 1:
        wallet_detail = await wallet_detial_keyboard( callback_data.wallet_no,callback_data.wallet_id,callback_data.wallet_addres)
        wallet_detial_data = await is_valid_eth_address(callback_data.wallet_addres)
        coin_symbols_holder_count =  await cleaning_wallet_detial_eth(wallet_detial_data)
    elif chain_checker[0] == 2:
        wallet_detail = await wallet_detial_keyboard(callback_data.wallet_no,callback_data.wallet_id,callback_data.wallet_addres)
        wallet_detial_data = await is_valid_shi_address(callback_data.wallet_addres)
        # print(wallet_detial_data)
        coin_symbols_holder_count = await cleaning_wallet_detial_shi(wallet_detial_data)
        print("shibarium")
    sorted_detail = sorted(coin_symbols_holder_count, key=lambda x: x['tot_amount_in_usd'], reverse=True)
    top_tokens = sorted_detail[:5]
    formatted_message = "\n".join(
        f"{token['symbol']}:  | {token['tot_amount_in_usd']}$ USD"
        for token in top_tokens
    )
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await query.message.answer(text=f"{formatted_message}  \n⌚ ---{current_time}--- ⌚ \n ℹ️ The bot only display tokens purchased  in the last 30 days. \n 🔊 Wallet Tracker - Advertise with us @wallet_taktak_bot" , reply_markup=wallet_detail)



@router.callback_query(ButtonClass.filter(F.btn_type=="wallet_addres"))
async def handle_wallet_button(query:types.CallbackQuery,callback_data ):

    chain_checker = await wallet_chain_getter(callback_data.wallet_id)
    if chain_checker[0] == 0:
        print("bsc")
    elif chain_checker[0] == 1:
        wallet_detail = await wallet_detial_keyboard2(callback_data.wallet_no, callback_data.wallet_id, callback_data.wallet_addres)
        wallet_detial_data = await is_valid_eth_address(callback_data.wallet_addres)
        coin_symbols_holder_count =  await cleaning_wallet_detial_eth(wallet_detial_data)
    elif chain_checker[0] == 2:
        wallet_detail = await wallet_detial_keyboard2(callback_data.wallet_no, callback_data.wallet_id, callback_data.wallet_addres)
        wallet_detial_data = await is_valid_shi_address(callback_data.wallet_addres)
        # print(wallet_detial_data)
        coin_symbols_holder_count = await cleaning_wallet_detial_shi(wallet_detial_data)
        print("shibarium")
    sorted_detail = sorted(coin_symbols_holder_count, key=lambda x: x['tot_amount_in_usd'], reverse=True)
    top_tokens = sorted_detail[:5]
    formatted_message = "\n".join(
        f"{token['symbol']}:  | {token['tot_amount_in_usd']}$ USD"
        for token in top_tokens
    )
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await query.message.edit_text(text=f"{formatted_message}  \n⌚ ---{current_time}--- ⌚ \n ℹ️ The bot only display tokens purchased  in the last 30 days. \n 🔊 Wallet Tracker - Advertise with us @wallet_taktak_bot" , reply_markup=wallet_detail)
