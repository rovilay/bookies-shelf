from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from ..settings import DATABASE_URL

print(DATABASE_URL)

engine = create_engine(DATABASE_URL)

DB_session = sessionmaker(bind=engine)

Base = declarative_base()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from .__models import User, Book, Favourite
    Base.metadata.create_all(bind=engine)


def drop_db():
    from .__models import User, Book, Favourite
    Base.metadata.drop_all(bind=engine)
    
