import asyncio
import logging
import sys
from os import getenv
import re

from aiogram.filters.callback_data import CallbackData
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    Message,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

from middleware import AuthMiddleware
from service.classes import ClassService
from service.group import GroupService
from service.task import TaskService
from service.user import UserService

_ = load_dotenv()

TOKEN = getenv("BOT_API_TOKEN")

dp = Dispatcher()
router = Router()


_ = dp.message.middleware(AuthMiddleware())


class ICallbackData(CallbackData, prefix="my_action"):
    action: str
    key: int | str


@dp.message(CommandStart())
async def handle_start(message: Message):
    _ = await message.reply("HELLO")


# except:
# _ = await message.reply("Произошла неизвестная ошибка")


@dp.message(Command("classes"))
async def handle_create_task(message: Message):
    user_id = message.from_user.id

    if not user_id:
        _ = await message.reply(
            "На данный момент запись осуществляется только пользователями."
        )
        return

    builder = InlineKeyboardBuilder()

    classes = ClassService.get_classes_by_user_id(str(user_id))

    if not classes:
        _ = await message.reply("У Вас нет добавленных предметов.")
        return

    for id, name, _ in classes:
        __ = builder.row(
            InlineKeyboardButton(
                text=name,
                callback_data=ICallbackData(action="get_class_tasks", key=id).pack(),
            )
        )

    _ = await message.reply(str(classes), reply_markup=builder.as_markup())


@dp.message(Command("newclass", "new_class", "newcl"))
async def handle_create_class(message: Message):
    user_id = message.from_user.id

    if not user_id:
        _ = await message.reply("Предмет создать может только пользователь")
        return

    match = re.match(r"\/(?:newclass|new_class|newcl) ([^ ]{3,})", str(message.text))

    if not match:
        _ = await message.reply("Невалидное название")
        return

    class_name = match.group(1)

    status = ClassService.create_class(class_name, str(user_id))

    _ = await message.reply(f"Создан предмет: {class_name, status}")


@dp.message(Command("newgrp", "new_group", "newgroup"))
async def handle_create_group(message: Message):
    match = re.match(r"\/(?:newgrp|new_group|newgroup) ([^ ]{3,})", str(message.text))

    if not match:
        _ = await message.reply("Невалидное название")
        return
    group_name = match.group(1)

    group = GroupService.create(group_name)

    _ = await message.reply(f"Группа создана: {group[0]}")


@dp.message(Command("group", "set_group"))
async def handle_set_group(message: Message):
    groups = GroupService.list()

    if groups == []:
        _ = await message.reply("Список групп пуст. Создайте группу")
        return

    builder = InlineKeyboardBuilder()

    for group in groups:
        _ = builder.row(
            InlineKeyboardButton(
                text=str(group[0]),
                callback_data=ICallbackData(action="join_group", key=group[0]).pack(),
            )
        )

    _ = await message.reply(text="Выбирай", reply_markup=builder.as_markup())


@dp.callback_query()
async def handle_join_group(call: CallbackQuery, **data):
    # @TODO: fix this (?)
    if not call.message:
        pass

    user_id = call.from_user.id

    if not (call.data):
        return

    data = ICallbackData.unpack(call.data)

    action, key = data.action, data.key

    match action:
        case "join_group":
            group_name = str(key)

            group = GroupService.find_by_name(group_name)

            if group is None:
                _ = await call.message.reply("Ошибка: группы не существует!")
                _ = await call.answer()
                return

            try:
                _ = UserService.join_group(str(user_id), group_name)
                _ = await call.message.reply(
                    f"Вы успешно присоединились к группе {group[0]}"
                )
                _ = await call.answer()
            except:
                _ = await call.message.reply(
                    f"Не удалось присоединиться к группе {group[0]}"
                )
                _ = await call.answer()
                pass

            _ = await call.answer()
            return
        case "get_class_tasks":
            class_id = int(key)

            tasks = TaskService.get_tasks(class_id)

            _ = await call.message.reply(f"{tasks}")

            _ = await call.answer()
            return
        case _:
            pass


# Main loop
async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    asyncio.run(main())
