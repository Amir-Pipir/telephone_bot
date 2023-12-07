from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


async def inline_key(val):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for x in val:
        keyboard.add(InlineKeyboardButton(text=x, callback_data=f'p_{x[:62]}'))
    return keyboard


phone_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True))


admin_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add("Заблокировать❌", "Разблокировать🔓", "Просмотр пользователей📱")
