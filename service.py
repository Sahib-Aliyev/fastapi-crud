from models import User
from schema import *
from sqlalchemy.orm import Session
from exceptions import UserNotFoundException , InvalidPassword , UserAlreadyExist
from utility import *



def get_user_from_db(*,username: str, db: Session):
    user = db.query(User).filter(User.username==username).first()
    if not user:
        raise UserNotFoundException()
    return {"Username":user.username}


def create_user_in_db(*,data: UserCreateSchema, db: Session):
    hash_password=hashPassword(data.password)
    user_in_db=db.query(User).filter(User.username==data.username).first()
    if user_in_db:
        raise UserAlreadyExist()
    new_user = User(username=data.username,password=hash_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg":"New user is created"}


def change_password_in_db(*,current_username:str,data: UserUpdateSchema,db: Session):
    if not db.query(User).filter_by(username=current_username).first():
        raise UserNotFoundException()
    result=db.query(User.username, User.password).filter_by(username=current_username).first()
    if verifyPassword(result.password,data.password):
        new_hash_password=hashPassword(data.new_password)
        db.query(User).filter(User.username==current_username).update({"password":new_hash_password})
        db.commit()
        return {"msg":"Password is changed"}
    else:
        raise InvalidPassword()
    
def delete_user_in_db(*, data: UserDeleteSchema,db: Session):
    user_in_db = db.query(User).filter(User.username==data.username).first()
    if not user_in_db:
        raise UserNotFoundException()
    db.delete(user_in_db)
    db.commit()
    return {"msg":"User is deleted"}