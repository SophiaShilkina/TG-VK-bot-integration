import os
import aiofiles


base_path = os.path.dirname(os.path.abspath(__file__))
settings_file_path = os.path.join(base_path, 'docs/tokens.txt')
CACHE_FILE = 'docs/photo_cache.txt'


def read_config(file_path):
    config_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config_dict[key] = value
    return config_dict


config = read_config(settings_file_path)
TOKEN_VK = config['TOKEN_VK']
TOKEN_TG = config['TOKEN_TG']
CHANNEL_ID = config['CHANNEL_ID']
CONFIRMATION = config['CONFIRMATION']
API_V = config['API_V']
SECRET = config['SECRET']
print(TOKEN_VK, TOKEN_TG, CHANNEL_ID, CONFIRMATION, API_V, SECRET, sep='\n')


async def cache_photo_url(photo_url):
    async with aiofiles.open(CACHE_FILE, 'w') as file:
        await file.write(photo_url)


async def get_cached_photo_url():
    if os.path.exists(CACHE_FILE):
        async with aiofiles.open(CACHE_FILE, 'r') as file:
            return await file.read()
    return None
