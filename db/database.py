from sqlalchemy import create_engine, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, Session, Mapped, mapped_column
import sqlite3
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'inventory_system_database.db')
engine = create_engine(f"sqlite:///{db_path}")

Base = declarative_base()

class Stocks(Base):
    __tablename__ = "stocks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    registration_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    barcode: Mapped[str] = mapped_column(String(250), nullable=True)
    item_name: Mapped[str] = mapped_column(String(250), nullable=True)
    quantity: Mapped[int] = mapped_column(String(250), nullable=True)
    item_price: Mapped[float] = mapped_column(Float, nullable=True)
    selling_price: Mapped[float] = mapped_column(Float, nullable=True)
    register_by: Mapped[str] = mapped_column(String(250), nullable=True)

Base.metadata.create_all(engine)

class DataContent:
    def __init__(self):
        self.connect_database = sqlite3.connect('db/inventory_system_database.db')

    def add_content(self,barcode, item, quantity, price, selling_price, registrator):
        with Session(engine) as session:
            created_date = datetime.now().replace(second=0, microsecond=0)
            registered_item = Stocks(registration_date=created_date,barcode=barcode, item_name=item, quantity=int(quantity),
                               item_price=float(price), selling_price=float(selling_price),
                               register_by=registrator)
            session.add(registered_item)
            session.commit()

    def get_data(self, params=None):
        SQL = """
        SELECT *
        FROM stocks
        WHERE barcode = ?
        """
        return pd.read_sql_query(SQL, self.connect_database, params=(params,))
    
    def delete_data(self, barcode_id):
        with Session(engine) as session:
            session.query(Stocks).filter(Stocks.barcode == barcode_id).delete()
            session.commit()

    def get_all_data(self):
        with Session(engine) as session:
            all_data = session.query(Stocks).all()
            for data in all_data:
                df = pd.DataFrame(data.__dict__ for data in all_data).drop('_sa_instance_state', axis=1)
                return df