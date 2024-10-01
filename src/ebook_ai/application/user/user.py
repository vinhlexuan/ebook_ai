from application.auth import encode_token, get_hashed_password, verify_password
from application.user.user_repository import UserRepository
from models import user
from ports.routers.schemas.user_schema import LoginResponse, UserResponse, SignUpSchema


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
        pass

    def create_user(self, user_schema: SignUpSchema) -> UserResponse:
        user_dict = user_schema.model_dump()
        plain_password = user_dict.pop("password")
        user_dict["password"] = get_hashed_password(plain_password)
        user_dict["role_id"] = 2
        user_model = self.repository.create_user(user_dict)
        user_model.__dict__.pop("_sa_instance_state")
        print(user_model.__dict__)
        return UserResponse(
            **user_model.__dict__
        )
    
    def update_role(self, user_id: int, role_id: int) -> None:
        self.repository.update_role(user_id, role_id)
        pass

    def login(self, user_schema: SignUpSchema) -> LoginResponse:
        user_dict = user_schema.model_dump()
        plain_password = user_dict.pop("password")
        user_model = self.repository.login(user_dict)
        if not verify_password(plain_password, user_model.password):
            raise Exception("Password is incorrect")
        user_model.__dict__.pop("_sa_instance_state")
        user_model.__dict__.pop("password")
        return LoginResponse(
            access_token=encode_token(user_model.__dict__)
    )
