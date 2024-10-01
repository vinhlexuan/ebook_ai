from fastapi import FastAPI

from application.user.user import UserService
from ports.routers.translator import TranslatorRouter
from ports.database.database import engine, get_db, Base
from ports.routers.user import UserRouter
from repositories import user_repository
from repositories.user_repository import UserRepositoryOnSQLA

class Module:
    def __init__(self):
        self.app = FastAPI()
        db = next(get_db())
        repository = UserRepositoryOnSQLA(db)
        user_service = UserService(repository)
        user_router = UserRouter(user_service)
        translation_router = TranslatorRouter() 
        self.app.include_router(user_router.router)
        self.app.include_router(translation_router.router)
        Base.metadata.create_all(bind=engine)
