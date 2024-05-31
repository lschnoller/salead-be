from ..database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from ..enums import Industry


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True)
    industry = Column(Industry)
    name = Column(String)
    description = Column(String)
    website_url = Column(String)
    logo_url = Column(String)
    crunchbase_url = Column(String)
    number_of_employees = Column(Integer)


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("contact.id"))
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(BigInteger)
    linkedin_url = Column(String)
    position = Column(String)
    description = Column(String)
    sold_once = Column(Boolean, default=False)
    status = Column(Integer, default=1)  # 1 = Active, 2 = Inactive, 3 = Completed

    company = relationship("Company", back_populates="contacts")  # 1-to-many relationship between Company and Contact


Company.contacts = relationship("Contact", order_by=Contact.position, back_populates="company")  # reverse: many-to-1 relationship between Contact and Company
