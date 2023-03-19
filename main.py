from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from decouple import config
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = config("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer('Hello world!')


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


@dp.callback_query_handler(text='button_1')
async def quiz_2(call: types.CallbackQuery):
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
    )


@dp.message_handler(commands=['mem'])
async def send_mem(message: types.Message):
    photo = open('media/cat_mem.jpg', 'rb')
    await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption='Задумался')


@dp.message_handler(content_types=types.ContentType.TEXT)
async def echo(message: types.Message):
    if not message.text:
        return
    try:
        num = int(message.text)
        squared_num = num ** 2
        await bot.send_message(chat_id=message.chat.id, text=str(squared_num))
    except ValueError:
        await bot.send_message(chat_id=message.chat.id, text=message.text)


@dp.message_handler()
async def echo(message: types.Message):
    if message.text == 'python':
        await message.answer('I love it!')
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f'Приветик друг - {message.from_user.full_name}'
        )
        await message.answer(f'This is an answer method! {message.message_id}')
        await message.reply('This is a reply method!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
