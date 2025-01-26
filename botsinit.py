from config import TOKEN_VK, TOKEN_TG

import vk_api
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

vk_session = vk_api.VkApi(token=TOKEN_VK)
vk_ms = vk_session.get_api()

bot = Bot(token=TOKEN_TG)
dp = Dispatcher(storage=MemoryStorage())
