from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils.config import get_system_config

db_config = get_system_config()['db']

DB_URL = 'postgresql://{user}:{pw}@{host}:{port}/{db}'.format(
    user=db_config['username'],
    pw=db_config['password'],
    host=db_config['host'],
    port=db_config['port'],
    db=db_config['name']
    )

engine = create_engine(DB_URL, echo=True)

create_session = sessionmaker(bind=engine)
db_session = scoped_session(create_session)
Base = declarative_base()
Base.query = db_session.query_property()
