from ..database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import relationship


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    domain_url = Column(String, unique=True)
    business_name = Column(String)
    type = Column(String)


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(ForeignKey("accounts.id"))
    role_id = Column(ForeignKey("roles.id"))
    account_admin = Column(Boolean, default=False)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    phone = Column(BigInteger, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    account = relationship("Account", back_populates="users")  # 1-to-many relationship between accounts and users
    role = relationship("Role", back_populates="users")  # 1-to-many relationship between roles and users


Account.users = relationship("User", order_by=User.first_name, back_populates="account")  # reverse: many-to-1 relationship between users and accounts
Role.users = relationship("User", order_by=User.first_name, back_populates="role")  # reverse: many-to-1 relationship between users and roles
