import os


base_path = os.path.dirname(os.path.abspath(__file__))
settings_file = os.path.join(base_path, 'tokens.txt')


def read_config(settings_file):
    config = {}
    with open(settings_file, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config


config = read_config(settings_file)
TOKEN_VK = config['TOKEN_VK']
TOKEN_TG = config['TOKEN_TG']
CHANNEL_ID = config['CHAT_ID']
print(f'{TOKEN_VK, TOKEN_TG, CHANNEL_ID}')
