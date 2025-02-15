import os


base_path = os.path.dirname(os.path.abspath(__file__))
settings_file_path = os.path.join(base_path, 'docs/tokens.txt')


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
print(f'{TOKEN_VK, TOKEN_TG, CHANNEL_ID}')
