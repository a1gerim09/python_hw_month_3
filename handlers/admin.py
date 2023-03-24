from aiogram import types, Dispatcher
from config import ADMINS, bot
from database.bot_db import sql_command_all, sql_command_delete
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def ban(message: types.Message):
    if message.chat.type != 'private':
        if message.from_user.id not in ADMINS:
            await message.answer('Создай своего бота!')
        elif not message.reply_to_message:
            await message.answer('Команда должна быть ответом на сообщение.')
        else:
            await bot.kick_chat_member(
                message.chat.id,
                message.reply_to_message.from_user.id
            )
            await message.answer(f'{message.from_user.first_name} Админ кикнул '
                                 f'{message.reply_to_message.from_user.full_name}')
    else:
        message.answer('Пиши в группе!')


async def pin(message: types.Message):
    if message.chat.type != "private":
        if message.from_user.id not in ADMINS:
            await message.answer("Пишите дальше")
        elif not message.reply_to_message:
            await message.answer("Команда должна быть ответом на сообщение!")
        else:
            await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)


async def delete_data(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer('Создай своего бота!')
    else:
        users = await sql_command_all()
        for user in users:
            await message.answer_photo(
                photo=user[-1],
                caption=f"{user[1]} {user[2]} "
                        f"{user[3]}{user[4]} {user[5]}",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(f'DELETE {user[1]}',
                                         callback_data=f'DELETE {user[0]}')
                )
            )


async def complete_delete(call: types.CallbackQuery):
    await sql_command_delete(call.data.replace('DELETE', ''))
    await call.answer(text='УДАЛЕНО', show_alert=True)
    await call.message.delete()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(ban, commands=['ban'], commands_prefix='!/')
    dp.register_message_handler(delete_data, commands=["del"])
    dp.register_callback_query_handler(complete_delete,
                                       lambda call: call.data and call.data.startswith('DELETE '))
