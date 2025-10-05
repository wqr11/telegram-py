import asyncio
import logging
import sys
from os import getenv

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

from service.group import GroupService
from service.user import UserService

_ = load_dotenv()

TOKEN = getenv("BOT_API_TOKEN")

dp = Dispatcher()
router = Router()


class ICallbackData(CallbackData, prefix="my_action"):
    action: str
    key: int | str


@dp.message(CommandStart())
async def handle_start(message: Message):
    # try:
    if not (message.from_user and message.from_user.id):
        _ = await message.reply("Пользователь неизвестен!")
        return

    user_id = message.from_user.id
    user = UserService.find_user_by_id(str(user_id))
    full_name = message.from_user.full_name

    if user is None:
        _ = UserService.create_user(user_id, full_name)
        _ = await message.reply(f"Создан пользователь: {full_name}")
    else:
        _ = await message.reply(f"Привет, {user[1]}")


# except:
# _ = await message.reply("Произошла неизвестная ошибка")


@dp.message(Command("set_group"))
async def handle_set_group(message: Message):
    groups = GroupService.list()

    if groups == []:
        _ = await message.reply("Список групп пуст. Создайте группу")
        return

    builder = InlineKeyboardBuilder()

    for group in groups:
        _ = builder.add(
            InlineKeyboardButton(
                text=str(group[0]),
                callback_data=ICallbackData(action="join_group", key=group[0]).pack(),
            )
        )

    _ = await message.reply(text="Выбирай", reply_markup=builder.as_markup())


@dp.callback_query()
async def handle_join_group(call: CallbackQuery):
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
                _ = await message.reply(
                    f"Не удалось присоединиться к группе {group[0]}"
                )
                _ = await call.answer()
                pass

            _ = await call.answer()
        case _:
            pass


# Main loop
async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    asyncio.run(main())
