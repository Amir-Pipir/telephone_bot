from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
import excel_work
from keyboard import inline_key, phone_button
from aiogram.dispatcher.filters import Text
from create_bot import bot
import re


class Reg(StatesGroup):
    name = State()
    phone = State()


async def start(message: types.Message):
    x = await excel_work.find_us(message.from_user.id)
    if x is False:
        await message.answer("Здравствуйте, для начала работы с нашим ботом, вам нужно пройти регистрацию, напишите ваше ФИО")
        await Reg.name.set()
    else:
        await message.answer(f"Здравствуйте, {x[0]}")


async def number(message: types.Message, state: FSMContext):
    us_name = message.text
    pattern = r'^[а-яА-ЯёЁ\s]+$'
    if bool(re.match(pattern, us_name)) is False or len(us_name.split()) != 3:
        await message.answer("Пожалуйста, напишите киррилицей и полностью ФИО")
    else:
        async with state.proxy() as data:
            data['name'] = us_name
        await message.answer("А теперь ваш номер телефона", reply_markup=phone_button)
        await Reg.next()


async def fin_reg(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    async with state.proxy() as data:
        username = data['name']
    await excel_work.new_user(message.from_user.id, username, phone_number, 'user', "Разблок")
    await state.finish()
    await message.answer("Вы успешно прошли регистрацию, теперь напишите модель устройства, которая вас интересует)")


async def fin_reg2(message: types.Message, state: FSMContext):
    phone_number = message.text
    pattern = r'^(\+7|8)9\d{9}$'
    if re.match(pattern, phone_number):
        async with state.proxy() as data:
            username = data['name']
        await excel_work.new_user(message.from_user.id, username, phone_number, 'user', "Разблок")
        await state.finish()
        await message.answer("Вы успешно прошли регистрацию, теперь напишите модель устройства, которая вас интересует)")
    else:
        await message.answer("Сообщение не является номером телефона, попробуйте еще раз")


async def find_phones(message: types.Message):
    if await excel_work.check_users(message.from_user.id):
        z = await excel_work.excel_read(message.text.lower().split())
        if len(z) > 10:
            await message.answer("Слишком много совпадений, попробуйте написать поточнее)")
        elif len(z) != 0:
            await bot.send_message(message.chat.id, "Вот что я нашел", reply_markup=await inline_key(z))
        else:
            await message.answer("Нет совпадений")
    else:
        await message.answer("Вы заблокированы!")


async def phones_info(call: types.CallbackQuery):
    res = await excel_work.find_info(call.data.replace("p_", ""))
    mes = [f'{res[0]}',
           f'Замена стекла(с гарантией): {res[1]}',
           f'Замена стекла(Сапфир): {res[2]}',
           f'Замена тача(с гарантией): {res[3]}',
           f'Замена микросхемы: {res[4]}',
           f'Замена заднего стекла(большое отверстие): {res[5]}',
           f'Замена стекла камеры: {res[6]}',
           f'Разборка/сборка устройства: {res[7]}',
           f'Вклейка дисплея: {res[8]}',
           f'Ориентировочный срок переклейки: {res[9]}']
    fin_mes = ''
    for x in mes:
        if x[-1] != 'e':
            fin_mes += f'{x}\n'
    await call.message.edit_text(fin_mes)


def register_handler_other(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(number, state=Reg.name)
    dp.register_message_handler(fin_reg, state=Reg.phone, content_types=types.ContentType.CONTACT)
    dp.register_message_handler(fin_reg2, state=Reg.phone)
    dp.register_message_handler(find_phones)
    dp.register_callback_query_handler(phones_info, Text(startswith='p_'))
