from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db.db_models import Item
from dotenv import load_dotenv
import os

load_dotenv()


DATABASE_URL =  os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_all_items():
    session = SessionLocal()
    items = session.query(Item).all()
    session.close()
    return items

def take_item(name: str, quantity: int, size: str, color: str):
    session = SessionLocal()
    try:
        item = session.query(Item).filter_by(name=name, size=size, color=color).first()

        if item:
            if item.quantity >= quantity:
                item.quantity -= quantity
                session.commit()
                print(f"{quantity} units of {name} (Size: {size}, Color: {color}) were taken. Remaining: {item.quantity}.")
            else:
                print(f"Not enough {name} (Size: {size}, Color: {color}) in stock. Only {item.quantity} left.")
        else:
            print(f"Item {name} (Size: {size}, Color: {color}) not found.")
    except Exception as e:
        session.rollback()
        print(f"Error while processing: {e}")
    finally:
        session.close()