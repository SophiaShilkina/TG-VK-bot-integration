import httpx
import random
from config import TOKEN_VK, API_V


async def send_message(user_id, message):
    url = 'https://api.vk.com/method/messages.send'
    params = {
        'access_token': TOKEN_VK,
        'v': API_V,
        'user_id': user_id,
        'message': message,
        'random_id': random.randint(1, 1000000)
    }
    async with httpx.AsyncClient() as client:
        await client.get(url, params=params)


async def get_fullname(user_id):
    url = 'https://api.vk.com/method/users.get'
    params = {
        'user_ids': user_id,
        'access_token': TOKEN_VK,
        'v': API_V
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            if 'response' in data and len(data['response']) > 0:
                user_info = data['response'][0]
                first_name = user_info.get('first_name', 'Не указано')
                last_name = user_info.get('last_name', 'Не указано')
                fullname = first_name + ' ' + last_name

                return fullname
