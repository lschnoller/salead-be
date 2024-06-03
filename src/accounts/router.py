from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from passlib.context import CryptContext
from . import models, schemas
# from .models import User, Account
# from .schemas import Account, User
from ..auth.services import get_current_user
from ..dependencies import get_db


router = APIRouter(
    prefix='/user',
    tags=['user']
)

db_dependency = Annotated[Session, Depends(get_db)]
auth_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.post('register-account', status_code=status.HTTP_201_CREATED, response_model=schemas.Account)
async def register_account(account: schemas.Account, db: db_dependency):
    db.add(models.Account(**account.model_dump()))
    db.commit()
    return account


@router.post('/sign-up', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def sign_up(account: schemas.AccountCreate, user: schemas.UserCreate, db: db_dependency):
    # add the account to db, then get the account id and add the user with the account id
    db_account = models.Account(**account.model_dump())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    user.account_id = db_account.id
    user.hashed_password = bcrypt_context.hash(user.hashed_password)
    db.add(models.User(**user.model_dump()))
    db.commit()

    return user


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: auth_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(models.User).filter(models.User.id == user.get('id')).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: auth_dependency, db: db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(models.User).filter(models.User.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


@router.put("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phonenumber(user: auth_dependency, db: db_dependency,
                             phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(models.User).filter(models.User.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
