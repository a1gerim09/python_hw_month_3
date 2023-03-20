from aiogram import types, Dispatcher
from time import sleep
import random
from aiogram import types, Dispatcher
from config import bot, dp


# @dp.message_handler()
async def echo(message: types.Message):
    if not message.text:
        return bot.send_message(
            chat_id=message.from_user.id,
            text=f'Приветик друг - {message.from_user.full_name}'
        )
    try:
        num = int(message.text)
        squared_num = num ** 2
        await bot.send_message(chat_id=message.chat.id, text=str(squared_num))
    except ValueError:
        await bot.send_message(chat_id=message.chat.id, text=message.text)

    if message.text == "game":
            animated_emojis = ['🎯', '🎳', '⚽️', '🏀', '🎰', '🎲']
            random_emoji = random.choice(animated_emojis)
            await message.answer(random_emoji)


def register_handlers_extra(dp: Dispatcher):
    dp.register_message_handler(echo)