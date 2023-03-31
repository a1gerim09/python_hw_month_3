from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from config import bot, dp
from keyboards.client_kb import start_markup
from database.bot_db import sql_command_random
from parser.animation import parser


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


async def get_random_user(message: types.Message):
    random_user = await sql_command_random()
    await message.answer_photo(
        photo=random_user[-1],
        caption=f"{random_user[1]} {random_user[2]} "
                f"{random_user[3]}{random_user[4]} {random_user[5]}"
    )


async def get_animation(message: types.Message):
    animation = parser()
    for anime in animation:
        await message.answer(
            # f"{anime['link']}\n\n"
            f"<b><a href='{anime['link']}'>{anime['title']}</a></b>\n"
            f"#Y{anime['year']}\n"
            f"#{anime['genre']}\n"
            f"#{anime['country']}\n",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("СМОТРЕТЬ", url=anime['link'])
            ),
            parse_mode=ParseMode.HTML
        )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(get_random_user, commands=['get'])
    dp.register_message_handler(get_animation, commands=['animation'])
