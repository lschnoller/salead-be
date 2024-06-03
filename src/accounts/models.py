from ..database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import relationship


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    domain_url = Column(String, unique=True)
    business_name = Column(String)
    type = Column(String)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(ForeignKey("accounts.id"))
    role = Column(String)
    account_admin = Column(Boolean, default=False)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    phone = Column(BigInteger, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)

    account = relationship("Account", back_populates="users")  # 1-to-many relationship between accounts and users


Account.users = relationship("User", order_by=User.first_name, back_populates="account")  # reverse: many-to-1 relationship between users and accounts
