import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Mysql DB Engine
engine = create_engine(
    'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(settings.MYSQL_USER, settings.MYSQL_PASSWORD, settings.MYSQL_HOST, int(settings.MYSQL_PORT),
                                                 settings.MYSQL_DATABASE), pool_pre_ping=True,
    pool_recycle=60)  # can add port after host
session_factory = sessionmaker(bind=engine, autocommit=True, autoflush=True)
Session = scoped_session(session_factory)
