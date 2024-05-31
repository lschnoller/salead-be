from sqlalchemy import create_engine, Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = 'postgresql+psycopg2://postgres:Lucas123@127.0.0.1:5430/salead'

engine = create_engine(DATABASE_URL, connect_args={})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.utcnow()

    @declared_attr
    def __mapper_args__(cls):
        return {
            "polymorphic_on": cls.deleted_at,
            "with_polymorphic": "*"
        }

    @classmethod
    def query_active(cls, session):
        return session.query(cls).filter(cls.deleted_at.is_(None))

    @classmethod
    def query_all(cls, session):
        return session.query(cls)
