from config import TOKEN_VK, TOKEN_TG

import vk_api
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router

vk_session = vk_api.VkApi(token=TOKEN_VK)
vk_ms = vk_session.get_api()


bot = Bot(token=TOKEN_TG)
dp = Dispatcher(storage=MemoryStorage())


async def main_bot():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

router = Router()
