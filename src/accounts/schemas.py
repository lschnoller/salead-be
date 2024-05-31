from pydantic import BaseModel, EmailStr, conint, Field


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


class RoleBase(BaseModel):
    name: str
    description: str | None = None


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleInDBBase(RoleBase):
    id: int

    class Config:
        from_attributes = True


class Role(RoleInDBBase):
    pass


class UserBase(BaseModel):
    account_admin: bool = False
    email: EmailStr
    phone: conint = Field(None, ge=10**12, le=10**13-1)  # phone number should be a 13-digit integer
    first_name: str
    last_name: str
    is_active: bool = True


class UserCreate(UserBase):
    password: str
    account_id: int
    role_id: int


class UserUpdate(UserBase):
    password: str | None = None
    account_id: int
    role_id: int


class UserInDBBase(UserBase):
    id: int
    hashed_password: str
    account: Account
    role: Role

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass
