from pydantic import BaseModel, EmailStr, conint, Field
from ..enums import Role


class AccountBase(BaseModel):
    domain_url: str
    business_name: str


class AccountCreate(AccountBase):
    pass


class AccountUpdate(AccountBase):
    pass


class AccountInDBBase(AccountBase):
    id: int

    class Config:
        from_attributes = True


class Account(AccountInDBBase):
    pass


class UserBase(BaseModel):
    account_admin: bool = False
    email: EmailStr
    phone: conint = Field(None, ge=10**12, le=10**13-1)  # phone number should be a 13-digit integer
    first_name: str
    last_name: str
    is_active: bool = True
    role: Role


class UserCreate(UserBase):
    hashed_password: str
    account_id: int


class UserUpdate(UserBase):
    hashed_password: str | None = None
    account_id: int


class UserInDBBase(UserBase):
    id: int
    hashed_password: str
    account: Account

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass
