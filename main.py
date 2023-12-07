from aiogram.utils import executor
import admin
import other
from create_bot import dp


async def on_startup(_):
    print("Бот вышел в онлайн")


admin.register_handler_admin(dp)
other.register_handler_other(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
