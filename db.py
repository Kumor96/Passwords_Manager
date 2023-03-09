from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import create_engine, MetaData, Integer, String, Column, Table

Base = declarative_base()


class Credentials(Base):
    __tablename__="credentials"
    id = Column(Integer, primary_key=True)
    portal = Column(String)
    login = Column(String)
    password = Column(String)

class DB:
    def __init__(self, engine):
        self.engine = engine

    def add_credentials(self, portal, login, password):
        with Session(self.engine) as session:
            credential = Credentials(portal=portal, login=login, password=password)
            session.add_all([credential])
            session.commit()
    def load_password(self):
        credentials = []
        with Session(self.engine) as session:
            categories = session.query(Credentials).all()
            for category in categories:
                credentials.append((category.portal, category.login, category.password))
        return credentials

    def create_tables(self):
        meta = MetaData()

        credentials = Table(
            'credentials', meta,
            Column('id',Integer, primary_key=True),
            Column('portal',String),
            Column('login',String),
            Column('password',String)
        )

        meta.create_all(self.engine)