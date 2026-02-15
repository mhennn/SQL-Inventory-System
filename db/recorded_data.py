from sqlalchemy import create_engine, Integer, String, Float, Date, DateTime
from sqlalchemy.orm import declarative_base, Session, Mapped, mapped_column
from db.database import DataContent
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

recorded_data_engine = create_engine(os.getenv('BACKUP_DATABASE'))

Base = declarative_base()

class Stocks(Base):
    __tablename__ = "record_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    registration_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    barcode: Mapped[str] = mapped_column(String(250), nullable=True)
    item_name: Mapped[str] = mapped_column(String(250), nullable=True)
    quantity: Mapped[int] = mapped_column(String(250), nullable=True)
    item_price: Mapped[float] = mapped_column(Float, nullable=True)
    selling_price: Mapped[float] = mapped_column(Float, nullable=True)
    register_by: Mapped[str] = mapped_column(String(250), nullable=True)
    deletion_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=True)

Base.metadata.create_all(recorded_data_engine)

class Records:
    def __init__(self):
        self.data_content = DataContent()

    def get_record_data(self, barcode):
        df = self.data_content.get_data(barcode)

        if df is not None and not df.empty:
            df = df.drop('id', axis=1)
            df['deletion_date'] = datetime.now().replace(second=0, microsecond=0)
            df.to_sql("record_data", recorded_data_engine, if_exists="append", index=False)