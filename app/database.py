from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import Session
from .settings import SettingsLocal

engine = create_engine(SettingsLocal.DATABASE_URL)

metadata = MetaData()
metadata.reflect(engine)

DeclarativeBase = declarative_base()

AutoBase = automap_base(metadata=metadata)
AutoBase.prepare(engine)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))