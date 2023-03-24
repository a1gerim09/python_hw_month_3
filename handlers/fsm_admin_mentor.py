from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import client_kb
from config import ADMINS
from database.bot_db import sql_command_insert


class FSMAdmin(StatesGroup):
    id = State()
    name = State()
    age = State()
    gender = State()
    direction = State()
    group = State()
    photo = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.chat.type == "private":
        await FSMAdmin.name.set()
        await message.answer("Как Вас зовут?", reply_markup=client_kb.cancel_markup)
    else:
        await message.answer("Пишите пожалуйста, в группу!")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("Сколько Вам лет?", reply_markup=client_kb.cancel_markup)


async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пишите числами!")
    elif int(message.text) < 18 or int(message.text) > 50:
        await message.answer("Вы не прошли возрастное ограничение!")
    else:
        async with state.proxy() as data:
            data['age'] = message.text
        await FSMAdmin.next()
        await message.answer("Укажите пол?", reply_markup=client_kb.gender_markup)


async def load_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
    await FSMAdmin.next()
    await message.answer("Укажите направление?", reply_markup=client_kb.cancel_markup)


async def load_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text
    await FSMAdmin.next()
    await message.answer("Какая группа?", reply_markup=client_kb.cancel_markup)


async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
    await FSMAdmin.next()
    await message.answer("Ваше фото", reply_markup=client_kb.cancel_markup)


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await message.answer_photo(
            photo=data['photo'],
            caption=f"Имя: {data['name']}"
                    f"\nВозраст: {data['age']}"
                    f"\nПол: {data['gender']}"
                    f"\nНаправление: {data['direction']}"
                    f"\nГруппа: {data['group']}")
    await FSMAdmin.next()
    await message.answer("Всё верно?", reply_markup=client_kb.submit_markup)


async def submit(message: types.Message, state: FSMContext):
    if message.text == "ДА":
        await sql_command_insert(state)
        await state.finish()
        await message.answer("Вы зарегистрированы!")
    elif message.text == "НЕТ":
        await state.finish()
        await message.answer("Пока!")
    else:
        await message.answer("Заполняйте правильно!")


async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.finish()
        await message.answer("Отменено!")


def register_handlers_fsm_admin_mentor(dp: Dispatcher):
    dp.register_message_handler(cancel, Text(equals="cancel", ignore_case=True), state='*')
    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_gender, state=FSMAdmin.gender)
    dp.register_message_handler(load_direction, state=FSMAdmin.direction)
    dp.register_message_handler(load_group, state=FSMAdmin.group)
    dp.register_message_handler(load_photo, state=FSMAdmin.photo,
                                content_types=['photo'])
    dp.register_message_handler(submit, state=FSMAdmin.submit)
