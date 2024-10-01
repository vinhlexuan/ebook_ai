from pydantic import BaseModel

class UserSchema(BaseModel):
    email: str
    role_id: int

class LoginSchema(BaseModel):
    email: str
    password: str

class SignUpSchema(BaseModel):
    email: str
    password: str

class UpdatePasswordSchema(BaseModel):
    password: str
    role_id: int

class UpdateRoleSchema(BaseModel):
    role_id: int

class LoginResponse(BaseModel):
    access_token: str

class UserResponse(UserSchema):
    id: int
    class Config:
        from_attributes = True