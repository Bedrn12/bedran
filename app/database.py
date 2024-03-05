from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname:port numbrt>/<database_name>'     so these are the credentials we provide SQL alchemy to connect our database


#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Bedran123@localhost:5432/fastapi' 

#The code below allows for more flexibility because the connection details are fetched from a configuration file, environment variables, or some other source, making it easier to change the database configuration without modifying the code.
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()     # we can just copy and paste from line 9 to 13 for every project we do

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

