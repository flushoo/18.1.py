import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = '7845273206:AAHRf0erN0Ois96wESI83rUi1rRxTpPpDig'
logging.basicConfig(level=logging.INFO)


dp = Dispatcher ()


@dp.message()

async def send_welcome(message: types.message):
    if message.text == "Привет!":
        await message.reply("И тебе привет!")
        return
        
    if message.text== "Пока":
        await message.reply("До встречи!")
        return
    
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


    
async def main() -> None:
    bot = Bot (token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling (bot)
    
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
asyncio.run(main())
