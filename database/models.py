from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, nullable=False)
    user_name = Column(String(50), nullable=False)

class Chain(Base):
    __tablename__ = "chain"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chain_id = Column(Integer, nullable=False)
    chain_name = Column(String(50), nullable=False)

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, autoincrement=True)
    token_id = Column(Integer, nullable=False)
    token_name = Column(String(50), nullable=False)
    chain_id = Column(Integer, ForeignKey("chain.id"), nullable=False)
    token_address = Column(String(50), nullable=False)
    token_symbol = Column(String(10), nullable=False)
    decimal_count = Column(Integer, nullable=True)
    total_supply = Column(Integer, nullable=False)
    market_cap = Column(Integer, nullable=False)
    price_usd = Column(Integer, nullable=False)
    price_chain = Column(Integer, nullable=False)
    pool_address = Column(String(50), nullable=False)

class Wallet(Base):
    __tablename__ = "wallet"
    id = Column(Integer, primary_key=True, autoincrement=True)
    wallet_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    chain_id = Column(Integer, ForeignKey("chain.id"), nullable=False)
    # tokens_id = Column(Integer, ForeignKey("tokens.id"), nullable=False)

class TokenState(Base):
    __tablename__ = "token_state"
    id = Column(Integer, primary_key=True, autoincrement=True)
    token_state_id = Column(Integer, nullable=False)
    chain_id = Column(Integer, ForeignKey("chain.id"), nullable=False)
    wallet_id = Column(Integer, ForeignKey("wallet.id"), nullable=False)
    token_id = Column(Integer, ForeignKey("tokens.id"), nullable=False)
    balance = Column(Integer, nullable=False)
    pnl = Column(Integer, nullable=False)
    timestamp = Column(Date)
    init_price = Column(Integer, nullable=False)

# Create the SQLite database
DATABASE_URL = 'sqlite:///wallet_tracker.db'
engine = create_engine(DATABASE_URL, echo=True)

# Create the tables
# Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# Insert sample data if needed
# ...

# print("Database and tables created successfully.")
