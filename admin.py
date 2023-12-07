from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
import excel_work
from aiogram.dispatcher.filters import Text
from create_bot import TOKEN
from keyboard import admin_kb
from aiogram.dispatcher import FSMContext


class Lock(StatesGroup):
    us_id = State()


class Unlock(StatesGroup):
    us_id = State()


async def admin(message: types.Message):
    x = await excel_work.find_us(message.from_user.id)
    await excel_work.admin(x[1])
    await message.answer("Приветствую админа!", reply_markup=admin_kb)


async def lock_us_id(message: types.Message):
    if await excel_work.check_for_admin(message.from_user.id):
        await message.answer("Введите id юзера, которого хотите заблокировать")
        await Lock.us_id.set()
    else:
        await message.answer("Ты не админ!")


async def lock_us(message: types.Message, state: FSMContext):
    us_id = message.text
    if str(us_id) == str(message.from_user.id):
        await message.answer("Вы не можете заблокировать себя)")
        await state.finish()
    else:
        x = await excel_work.lock_unlock(str(us_id), 'Заблок')
        if x is not False:
            await message.answer(f"Пользователь {x} успешно заблокирован")
            await state.finish()
        else:
            await message.answer(f"Пользователь с id {us_id} не найден")
            await state.finish()


async def unlock_us_id(message: types.Message):
    if await excel_work.check_for_admin(message.from_user.id):
        await message.answer("Введите id юзера, которого хотите разблокировать")
        await Unlock.us_id.set()
    else:
        await message.answer("Ты не админ!")


async def unlock_us(message: types.Message, state: FSMContext):
    us_id = message.text
    if str(us_id) == str(message.from_user.id):
        await message.answer("Вы не можете разблокировать себя)")
        await state.finish()
    else:
        x = await excel_work.lock_unlock(str(us_id), 'Разблок')
        if x is not False:
            await message.answer(f"Пользователь {x} успешно разблокирован")
            await state.finish()
        else:
            await message.answer(f"Пользователь с id {us_id} не найден")
            await state.finish()


async def send_excel_file(message: types.Message):
    if await excel_work.check_for_admin(message.from_user.id):
        await message.answer(f"На данный момент всего {await excel_work.users_rows()} пользователей.\nПодробно вы можете помотреть в файле ниже")
        with open('Таблица пользователей.xlsx', 'rb') as file:
            await message.answer_document(file)
    else:
        await message.answer("Ты не админ!")


async def state_cansel(message: types.Message, state: FSMContext):
    cur_state = state.get_state()
    if cur_state is None:
        return
    await state.finish()
    await message.answer("Действие отменено")


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(state_cansel, state="*", commands="stop")
    dp.register_message_handler(state_cansel, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(admin, Text(TOKEN))
    dp.register_message_handler(lock_us_id, Text("Заблокировать❌"))
    dp.register_message_handler(lock_us, state=Lock.us_id)
    dp.register_message_handler(unlock_us_id, Text("Разблокировать🔓"))
    dp.register_message_handler(unlock_us, state=Unlock.us_id)
    dp.register_message_handler(send_excel_file, Text("Просмотр пользователей📱"))
