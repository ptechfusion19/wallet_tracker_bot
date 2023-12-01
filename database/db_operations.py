import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from database.models import engine, Base, User, Chain, Token, Wallet, TokenState, session
from sqlalchemy import func

        

    


async def close_session():
    if session:
        session.close()

async def insert_user( chat_id, user_name):
    new_user = User(chat_id=chat_id,  user_name=user_name)
    session.add(new_user)
    session.commit()

async def check_user(  user_id):
    old_user =  session.query(User).filter_by(chat_id=user_id).first()
    print(old_user)
    if old_user:
        return True 
    else:
        return False

async def insert_chain( chain_id, chain_name):
    new_chain = Chain(chain_id=chain_id, chain_name=chain_name)
    session.add(new_chain)
    session.commit()

async def check_chain():
    chain_chk = session.query(Chain).filter_by(chain_id=0).first()
    if chain_chk:
        return True
    else:
        return False
    

async def insert_token( token_id, token_name, chain_id, token_address, token_symbol, decimal_count, total_supply, market_cap, price_usd, price_chain, pool_address):
    new_token = Token(
        token_id=token_id,
        token_name=token_name,
        chain_id=chain_id,
        token_address=token_address,
        token_symbol=token_symbol,
        decimal_count=decimal_count,
        total_supply=total_supply,
        market_cap=market_cap,
        price_usd=price_usd,
        price_chain=price_chain,
        pool_address=pool_address
    )
    session.add(new_token)
    session.commit()

async def insert_wallet(wallet_id, user_id, chain_id):
    new_wallet = Wallet(wallet_address=wallet_id, user_id=user_id, chain_id=chain_id)
    session.add(new_wallet)
    session.commit()

async def get_wallet_id_address(user_id):
    wallets = session.query(Wallet.id).filter(Wallet.user_id == user_id).all()
    wallet_addresses = session.query(Wallet.wallet_address).filter(Wallet.user_id == user_id).all()
    wallet_ids = [wallet[0] for wallet in wallets]
    wallets_ads = [wallet[0] for wallet in wallet_addresses]
    return wallet_ids , wallets_ads

async def wallet_address_getter(wallet_id):
    get_wallet_ads = session.query(Wallet.wallet_address).filter(Wallet.id == wallet_id).first()
    return get_wallet_ads

async def wallet_chain_getter(wallet_id):
    get_wallet_chain = session.query(Wallet.chain_id).filter(Wallet.id == wallet_id).first()
    print(get_wallet_chain)
    return get_wallet_chain

async def checke_wallet_no(user_id):
    check_wallet =  session.query(func.count(Wallet.id)).filter_by(user_id=user_id).scalar()
    no_of_wallets = 0
    if check_wallet:
        no_of_wallets = check_wallet
        return no_of_wallets
    else:
        return no_of_wallets

async def connected_wallet_list(user_id):
    wallet_addresses = (
    session.query(Wallet.wallet_address)
    .filter(Wallet.user_id == user_id)
    .all()
)
    return wallet_addresses

    

async def insert_token_state( token_state_id, chain_id, wallet_id, token_id, balance, pnl, timestamp, init_price):
    new_token_state = TokenState(
        token_state_id=token_state_id,
        chain_id=chain_id,
        wallet_id=wallet_id,
        token_id=token_id,
        balance=balance,
        pnl=pnl,
        timestamp=timestamp,
        init_price=init_price,
    )
    session.add(new_token_state)
    session.commit()

async def delete_user( user_id):
    user_to_delete = session.query(User).filter_by(user_id=user_id).first()
    session.delete(user_to_delete)
    session.commit()

async def delete_chain( chain_id):                
    chain_to_delete =  session.query(Chain).filter_by(chain_id=chain_id).first()
    session.delete(chain_to_delete)
    session.commit()

async def delete_token( token_id):
    token_to_delete = session.query(Token).filter_by(token_id=token_id).first()
    session.delete(token_to_delete)
    session.commit()


    

async def delete_wallet( wallet_id):
    wallet_to_delete = session.query(Wallet).filter_by(id=wallet_id).first()
    session.delete(wallet_to_delete)
    session.commit()

async def delete_token_state( token_state_id):
    token_state_to_delete = session.query(TokenState).filter_by(token_state_id=token_state_id).first()
    session.delete(token_state_to_delete)
    session.commit()