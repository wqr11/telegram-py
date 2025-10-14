from collections.abc import Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Any

from service.user import UserService


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ):
        if not event.from_user or not event.from_user.id:
            _ = await event.reply("Бот может быть использован только пользователями")
            return None

        user_id = str(event.from_user.id)

        user = UserService.find_user_by_id(user_id)

        if not user:
            user = UserService.create_user(user_id, event.from_user.full_name)
            _ = await event.reply(f"Пользователь создан: {event.from_user.full_name}")

        data["user"] = user

        return await handler(event, data)
