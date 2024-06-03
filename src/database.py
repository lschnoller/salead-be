from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = 'postgresql+asyncpg://postgres:Lucas123@127.0.0.1:5430/salead'

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(bind=engine, _class=AsyncSession, expire_on_commit=False)


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


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
