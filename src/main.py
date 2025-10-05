import asyncio
import logging
import sys
from os import getenv

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.enums.chat_type import ChatType
from aiogram.types import Message
from aiogram import F

_ = load_dotenv()

TOKEN = getenv("BOT_API_TOKEN")

dp = Dispatcher()


@dp.message(
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}), F.text.contains("hw")
)
async def handle_hw(message: Message):
    await message.reply("Записано")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    asyncio.run(main())
