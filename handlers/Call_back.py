from aiogram.filters import CommandStart , Command
from aiogram.types import Message
from aiogram import Bot, Dispatcher, Router, types
from Messages.message import start_command_text , wallet_command_text_fun , add_wallet_text , no_of_bsc_text, no_of_eth_text, no_of_shi_text
from handlers.keyborad import wallet_keyborad , adding_Wallet_keyborad , lang_types_btn
from aiogram.types import CallbackQuery 
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from database.db_operations import insert_user , check_user,insert_wallet , checke_wallet_no , insert_chain,check_chain, delete_chain, delete_wallet , wallet_address_getter
from handlers.chain_validator import is_valid_eth_address
from handlers.ca_action import ButtonClass
from handlers.keyborad import delete_confirmation
from database.db_operations import delete_wallet
from aiogram import F
router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
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
    
    await message.answer(f"{(start_command_text)}!")

    
    

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
    add_Wallet_key = await adding_Wallet_keyborad()
    await callback_query.message.answer( add_wallet_text , reply_markup=add_Wallet_key)

@router.callback_query(lambda callback_query:callback_query.data == "BSC" )
async def bsc_input(callback_query: types.CallbackQuery, state: FSMContext ):
    force_reply_bsc = types.ForceReply(input_field_placeholder="0x420F69...")
    await callback_query.message.answer( text=no_of_bsc_text , reply_markup=force_reply_bsc)
    await state.set_state("bsc_wallet_address")


@router.message(StateFilter("bsc_wallet_address"))
async def bsc_wallet_address(message:Message , state:FSMContext)-> None:
    wallet_addres  = message.text
    walllet_command_text = await wallet_command_text_fun(message.from_user.id)
    if is_valid_eth_address(wallet_addres):
        no_tot_wallet = await checke_wallet_no(message.from_user.id)
        if no_tot_wallet < 4:
            await insert_wallet(wallet_addres , message.from_user.id , 0 )
            wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
            await message.answer(text=f"✅ Address \n {wallet_addres} \n (bsc) has been successfully added.")
            walllet_command_text = await wallet_command_text_fun(message.from_user.id)
            await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)
        else:
            wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
            await message.answer(text=f"YOUR LIMIR OF ADDIND WALLET IS EXCEDED ")
            await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)
    else:
        wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
        await message.reply(text="Invalid address provided!")
        await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)


    

@router.callback_query(lambda callback_query:callback_query.data == "ETH")
async def eth_input(callback_query: types.CallbackQuery, state: FSMContext):
    force_reply_eth = types.ForceReply(input_field_placeholder="0x420F69...")
    await callback_query.message.answer( text=no_of_eth_text , reply_markup=force_reply_eth)
    await state.set_state("eth_wallet_address")


@router.message(StateFilter("eth_wallet_address"))
async def eth_wallet_address(message:Message , state:FSMContext)-> None:
    wallet_addres  = message.text
    walllet_command_text = await wallet_command_text_fun(message.from_user.id)
    if is_valid_eth_address(wallet_addres):
        no_tot_wallet = await checke_wallet_no(message.from_user.id)
        if no_tot_wallet < 4:
            await insert_wallet(wallet_addres , message.from_user.id , 1 )
            wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
            await message.answer(text=f"✅ Address \n {wallet_addres} \n (eth) has been successfully added.")
            walllet_command_text = await wallet_command_text_fun(message.from_user.id)
            await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)
        else:
            wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
            await message.answer(text=f"YOUR LIMIR OF ADDIND WALLET IS EXCEDED ")
            await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)
    else:
        wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
        await message.reply(text="Invalid address provided!")
        await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)






@router.callback_query(lambda callback_query:callback_query.data == "SHI")
async def shi_input(callback_query: types.CallbackQuery, state: FSMContext):
    force_reply_shi = types.ForceReply(input_field_placeholder="0x420F69...")
    await callback_query.message.answer( text=no_of_shi_text , reply_markup=force_reply_shi)
    await state.set_state("shi_wallet_address")


@router.message(StateFilter("shi_wallet_address"))
async def shi_wallet_address(message:Message , state:FSMContext)-> None:
    wallet_addres  = message.text
    walllet_command_text = await wallet_command_text_fun(message.from_user.id)
    if is_valid_eth_address(wallet_addres):
        no_tot_wallet = await checke_wallet_no(message.from_user.id)
        if no_tot_wallet < 4:
            await insert_wallet(wallet_addres , message.from_user.id , 2 )
            wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
            await message.answer(text=f"✅ Address \n {wallet_addres} \n (shi) has been successfully added.")
            walllet_command_text = await wallet_command_text_fun(message.from_user.id)
            await message.answer(text=walllet_command_text , reply_markup=wallet_keyboard_button)
        else:
            wallet_keyboard_button = await wallet_keyborad(message.from_user.username , message.from_user.id)
            await message.answer(text=f"YOUR LIMIR OF ADDIND WALLET IS EXCEDED ")
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