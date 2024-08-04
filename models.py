from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'
    id = Column(String, primary_key=True)
    symbol = Column(String)
    qty = Column(Integer)
    side = Column(String)
    order_type = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    filled_at = Column(DateTime)

class Trade(Base):
    __tablename__ = 'trades'
    id = Column(String, primary_key=True)
    symbol = Column(String)
    qty = Column(Integer)
    price = Column(Float)
    side = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_engine('sqlite:///tradingBot.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()