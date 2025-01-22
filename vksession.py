from sett import TOKEN_VK
import vk_api
import asyncio
from concurrent.futures import ThreadPoolExecutor


vk_session = vk_api.VkApi(token=TOKEN_VK)
vk_ms = vk_session.get_api()


import vk_api


def get_vk_session(token):
    vk_session = vk_api.VkApi(token=token)
    return vk_session.get_api()


async def main():
    # Замените TOKEN_VK на ваш токен
    TOKEN_VK = "ваш_токен"

    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        vk_ms = await loop.run_in_executor(pool, get_vk_session, TOKEN_VK)

    # Теперь вы можете использовать vk_ms для асинхронных задач
    print(vk_ms)


# Запуск асинхронной функции
asyncio.run(main())
