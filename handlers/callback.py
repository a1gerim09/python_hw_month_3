from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import bot, dp


@dp.callback_query_handler(text='button_1')
async def quiz_2(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton('NEXT', callback_data='button_2')
    markup.add(button_1)

    question = 'Сколько языков программирования существует?'
    answer = [
        'неизвестно',
        'может 5',
        'без понятия',
        'не более 700',
        'около 9000'
    ]
    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=4,
        explanation='Стыдно не знать!',
        open_period=10,
        reply_markup=markup
    )


async def quiz_3(call: types.CallbackQuery):
    question = 'За какое время можно выучить программирование?'
    answer = [
        'за 3 месяца',
        'за 5 лет',
        'зависит от самого человека',
        'за полгода',
        'за 1 год'
    ]
    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation='Ответ зависит от желания человека',
        open_period=20
    )


def register_handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(quiz_2, text='button_1')
    dp.register_callback_query_handler(quiz_3, text='button_2')