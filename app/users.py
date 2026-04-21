import os
import uuid
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from .db import User, get_user_db


SECRET = os.getenv("SECRET_PASS")


class UseManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        return await super().on_after_register(user, request)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        return await super().on_after_forgot_password(user, token, request)

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        return await super().on_after_request_verify(user, token, request)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UseManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy():
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)
