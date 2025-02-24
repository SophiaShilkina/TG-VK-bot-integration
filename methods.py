import httpx
import random
from config import TOKEN_VK, API_V
import aiofiles
import json


async def send_message(user_id, message, attachment=None, keyboard=None):
    url = 'https://api.vk.com/method/messages.send'
    params = {
        'access_token': TOKEN_VK,
        'v': API_V,
        'user_id': user_id,
        'message': message,
        'random_id': random.randint(1, 1000000)
    }
    if attachment:
        params['attachment'] = attachment
    if keyboard:
        params['keyboard'] = json.dumps(keyboard)

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


async def upload_photo_to_vk():
    try:
        url = 'https://api.vk.com/method/photos.getMessagesUploadServer'
        params = {
            'access_token': TOKEN_VK,
            'v': API_V,
            'group_id': '226206756'
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            url_info = response.json()['response']
            upload_url = url_info.get('upload_url', 'Не указано')

            async with aiofiles.open('docs/prices.jpg', 'rb') as photo:
                file_data = await photo.read()
                upload_response = await client.post(upload_url, files={'photo': ('prices.jpg', file_data, 'image/jpeg')})
                upload_data = upload_response.json()

                url = await save_photo(upload_data['photo'], upload_data['server'], upload_data['hash'])

                return url

    except Exception as e:
        print(f"Ошибка: {e}")
        return None


async def save_photo(photo, server, hash):
    url = 'https://api.vk.com/method/photos.saveMessagesPhoto'
    params = {
        'access_token': TOKEN_VK,
        'v': API_V,
        'photo': photo,
        'server': server,
        'hash': hash
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, params=params)
        response_data = response.json()
        if 'response' not in response_data:
            raise ValueError("Ошибка сохранения фото: " + str(response_data))

        photo_data = response_data['response'][0]
        photo_url = f"photo{photo_data['owner_id']}_{photo_data['id']}"
        return photo_url
