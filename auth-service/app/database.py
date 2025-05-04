import os
from dotenv import load_dotenv

from databases import Database

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

def get_sqlalchemy_url():
    return os.getenv('DATABASE_URL')

DATABASE_URL = get_sqlalchemy_url()

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()

Base = declarative_base()