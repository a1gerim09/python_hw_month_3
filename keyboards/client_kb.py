from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=3
)

start_button = KeyboardButton('/start')
quiz_button = KeyboardButton('/quiz')
help_button = KeyboardButton('/help')

share_location = KeyboardButton('Share Location', request_location=True)
share_contact = KeyboardButton('Share Contact', request_contact=True)

start_markup.add(
    start_button,
    quiz_button,
    help_button,
    share_location,
    share_contact
)

cancel_button = KeyboardButton("CANCEL")

cancel_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
).add(
    cancel_button
)

gender_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
).add(
    KeyboardButton("Женщина"),
    KeyboardButton("Мужчина"),
    cancel_button
)

submit_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
).add(
    KeyboardButton("ДА"),
    KeyboardButton("НЕТ")
)
