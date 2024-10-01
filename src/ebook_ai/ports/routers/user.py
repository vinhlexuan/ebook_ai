from application.user.user import UserService
from fastapi import APIRouter, Body, Depends

from application.auth import verify_token
from .schemas.user_schema import LoginResponse, UpdateRoleSchema, UserResponse, SignUpSchema

class UserRouter:
    def __init__(self, service: UserService) -> None:
        self.service = service
        self.router = APIRouter()
        self.router.post("/signup", response_model=UserResponse)(self.create_user)
        self.router.post("/update_role", response_model=None)(self.update_role)
        self.router.post("/login", response_model=LoginResponse)(self.login)

    def create_user(self, user_create: SignUpSchema = Body(...)) -> UserResponse:
        result = self.service.create_user(user_create)
        return result
    
    def update_role(self, role_schema: UpdateRoleSchema = Body(...), current_user_dict = Depends(verify_token)) -> None:
        user_id = current_user_dict["id"]
        self.service.update_role(user_id, role_schema.role_id)
        return None
    
    def login(self, user_login: SignUpSchema = Body(...)) -> LoginResponse:
        result = self.service.login(user_login)
        return result
    
    
