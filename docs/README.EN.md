# TG-VK-bot-integration ![GitHub Repo stars](https://img.shields.io/github/stars/SophiaShilkina/TG-VK-bot-integration)

![Static Badge](https://img.shields.io/badge/SophiaShilkina-TG--VK--bot--integration-TG--VK--bot--integration)
![GitHub top language](https://img.shields.io/github/languages/top/SophiaShilkina/TG-VK-bot-integration)
![GitHub](https://img.shields.io/github/license/SophiaShilkina/TG-VK-bot-integration)
![vk-api version](https://img.shields.io/badge/vk--api-11.9.9-8a2be2)
![aiogram version](https://img.shields.io/badge/aiogram-3.17.0-ff970f)
![aiosqlite version](https://img.shields.io/badge/aiosqlite-0.20.0-9f8200)

## Multilanguage README [![en readme](https://img.shields.io/badge/lang-en-en)](https://github.com/SophiaShilkina/TG-VK-bot-integration/blob/master/docs/README.EN.md) [![ru readme](https://img.shields.io/badge/lang-ru-ff6347)](https://github.com/SophiaShilkina/TG-VK-bot-integration/blob/master/docs/README.md)

https://github.com/user-attachments/assets/07f5c16e-b10a-417d-a3ad-d74dbc6f5d08

This project is a VKontakte bot for prompt response to customer requests. By eliminating waiting 
time for user responses and instantly notifying the administrator in Telegram about new requests 
with built-in moderation capabilities can help improve the conversion rate of the community. Effective 
moderation of requests and quick feedback with users are key aspects that contribute to an improved 
customer experience.

## Description

This bot automates the process of handling messages from customers, transferring some tasks to 
Telegram. This allows administrators to respond to requests faster, manage dialogues and provide 
a high level of service.

## Functionality

- Automatic messaging to customers in the VK chat bot.
- Collection of required information from users.
- Notifications to administrators in Telegram regarding new requests.
- Real-time moderation and management of the bot's responses.
- The ability to moderate and manage bot responses by multiple administrators.
- User-friendly customizable interface with the capability to extend functionality.

## Installation

1. **Download the Source code(zip/tar.gz) from the latest release** or navigate 
to the desired directory and clone the repository:
   ```bash
   git clone https://github.com/SophiaShilkina/TG-VK-bot-integration.git
   
2. Install the dependencies:
   ```bash
   pip install -r docs/requirements.txt
   ```
   
3. Configure environment variables for VK and Telegram API by modifying **token.txt**:
   ```copy
   TOKEN_VK=vk1.a.ABC123***********************
   TOKEN_TG=123***:ABCQWE*********
   CHANNEL_ID=-123*********
   ```
   
## Usage

1. Replace **prices.jpg** with your file. Note that in the original project, the function
`write_msg_with_photo(peer_id, messege)` has a static parameter `attachment()`. 
If you need to send multiple different images, create additional functions in **upload.py**.


2. Run the bot:
   ```bash
   python main.py
   ```
3. Interact with the bot through VKontakte; it will automatically send messages to the 
administrator in Telegram.

### Contribution

If you want to contribute to the project, please create a branch with your changes 
and open a pull request.

### License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.

### Contacts

If you have any questions or suggestions about cooperation, you can contact me on Telegram: 
[Sophia](https://t.me/ShilkinaSK).