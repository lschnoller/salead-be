from pydantic import BaseModel, UrlStr, EmailStr, conint, Field
from ..enums import Industry


class CompanyBase(BaseModel):
    industry: Industry | None = None
    name: str
    description: str | None = None
    website_url: UrlStr | None = None
    logo_url: UrlStr | None = None
    crunchbase_url: UrlStr | None = None
    number_of_employees: int = 1


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    pass


class CompanyInDBBase(CompanyBase):
    id: int

    class Config:
        orm_mode = True


class Company(CompanyInDBBase):
    pass


class ContactBase(BaseModel):
    manager_id: int | None = None
    first_name: str
    last_name: str
    email: EmailStr
    phone: conint = Field(None, ge=10**12, le=10**13-1)  # phone number should be a 13-digit integer
    linkedin_url: UrlStr | None = None
    position: str
    description: str | None = None
    priority: conint = Field(None, ge=1, le=5)
    complete: bool = False
    status: int = 1  # 1 = Active, 2 = Inactive, 3 = Completed


class ContactCreate(ContactBase):
    company_id: int


class ContactUpdate(ContactBase):
    company_id: int | None = None


class ContactInDBBase(ContactBase):
    id: int
    company: Company

    class Config:
        orm_mode = True


class Contact(ContactInDBBase):
    pass
