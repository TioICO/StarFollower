"""
Defines model(s) for sqlalchemy
"""
# third party
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine

Base = declarative_base()

class Star(Base):
    __tablename__ = "stars"
    starred_by    = Column(String)
    repo_id       = Column(Integer, primary_key=True)
    stars         = Column(Integer)
    #owner_name    = Column(String)
    #owner_url     = Column(String)
    pushed_at     = Column(String)
    repo_name     = Column(String)
    repo_url      = Column(String)
    description   = Column(String)
    language      = Column(String)

def init_db(db_path : str):
    engine = create_engine(db_path, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()
