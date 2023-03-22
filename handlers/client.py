from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot, dp
from keyboards.client_kb import start_markup


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer('Hello world!', reply_markup=start_markup)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer('Погугли')


@dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton('NEXT', callback_data='button_1')
    markup.add(button_1)

    question = 'Какой самый старый язык программирования?'
    answer = [
        'С++',
        'Java',
        'Kotlin',
        'Python',
        'Fortran'
    ]
    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=4,
        explanation='Вот и узнали',
        open_period=5,
        reply_markup=markup
    )


@dp.message_handler(commands=['mem'])
async def send_mem(message: types.Message):
    photo = open('media/cat_mem.jpg', 'rb')
    await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption='Задумался')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
