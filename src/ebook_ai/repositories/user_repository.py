from application.user.user_repository import UserRepository
from sqlalchemy.orm import Session
import traceback
from models.user import User

class UserRepositoryOnSQLA(UserRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_user(self, user_dict: dict) -> User:
        try:
            db_user = User(
                **user_dict
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except Exception as e:
            self.db.rollback()
            traceback.print_exc()
            raise e
        
    def update_role(self, user_id: int, role_id: int) -> None:
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise Exception("User not found")
            user.role_id = role_id
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            traceback.print_exc()
            raise e
        
    def login(self, user_dict: dict) -> User:
        try:
            user = self.db.query(User).filter(User.email == user_dict["email"]).first()
            if not user:
                raise Exception("User not found")
            return user
        except Exception as e:
            self.db.rollback()
            traceback.print_exc()
            raise e