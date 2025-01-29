# TG-VK-bot-integration ![GitHub Repo stars](https://img.shields.io/github/stars/SophiaShilkina/TG-VK-bot-integration)

![Static Badge](https://img.shields.io/badge/SophiaShilkina-TG--VK--bot--integration-TG--VK--bot--integration)
![GitHub top language](https://img.shields.io/github/languages/top/SophiaShilkina/TG-VK-bot-integration)
![GitHub](https://img.shields.io/github/license/SophiaShilkina/TG-VK-bot-integration)
![vk-api version](https://img.shields.io/badge/vk--api-11.9.9-8a2be2)
![aiogram version](https://img.shields.io/badge/aiogram-3.17.0-ff970f)
![aiosqlite version](https://img.shields.io/badge/aiosqlite-0.20.0-9f8200)

## Multilanguage README [![en readme](https://img.shields.io/badge/lang-en-ff6347)](https://github.com/SophiaShilkina/TG-VK-bot-integration/blob/master/docs/README.EN.md) [![ru readme](https://img.shields.io/badge/lang-ru-ru)](https://github.com/SophiaShilkina/TG-VK-bot-integration/blob/master/docs/README.md)


https://github.com/user-attachments/assets/07f5c16e-b10a-417d-a3ad-d74dbc6f5d08

Этот проект представляет собой бота ВКонтакте для оперативного 
реагирования на заявки клиентов. За счет отсутствия времени ожидания 
ответов со стороны пользователя и мгновенного уведомления 
администратора в Telegram о новых заявках с их встроенной модерацией, 
бот помогает увеличить конверсию сообщества. Эффективная модерация 
запросов и быстрая обратная связь с пользователями — ключевые аспекты, 
способствующие улучшению клиентского опыта.

## Описание

Данный бот автоматизирует процесс обработки сообщения от клиентов, 
перенося часть задач в Telegram. Это позволяет администраторам 
быстрее реагировать на запросы, управлять диалогами и обеспечивать 
высокий уровень обслуживания.

## Функциональность

- Автоматическая отправка сообщений клиентам в чат-боте VK.
- Сбор требуемой информации от пользователя.
- Уведомления для администраторов в Telegram о новых заявках.
- Возможность модерации и управления ответами бота в режиме реального времени.
- Возможность модерации и управления ответами бота несколькими администраторами.
- Легко настраиваемый интерфейс и возможность расширения функционала.

## Установка

1. Перейдите в желаемую директорию и склонируйте репозиторий:
   ```bash
   git clone https://github.com/SophiaShilkina/TG-VK-bot-integration.git
   
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
   
3. Настройте переменные окружения для VK и Telegram API, изменив 
**token.txt**:
   ```copy
   TOKEN_VK=vk1.a.5SlB465OXbRkv5nio****************************************
   TOKEN_TG=729******:AAHD********************
   CHANNEL_ID=-100*******
   ```
   
## Использование

1. Замените **prices.jpg** на свой файл. Обратите внимание, что в 
оригинале проекта функция `write_msg_with_photo(peer_id, messege)` 
имеет постоянный параметр `attachment()`. Если вам необходимо 
отправлять несколько разных изображений, создайте дополнительные 
функции в **upload.py**.


2. Запустите бота:
   ```bash
   python main.py
   ```
3. Взаимодействуйте с ботом через ВКонтакте, он будет автоматически 
отправлять сообщения администратору в Telegram.

### Вклад

Если вы хотите внести свой вклад в проект, пожалуйста, создайте ветку
с вашим изменением и откройте pull request.

### Лицензия

Этот проект лицензирован на условиях Apache License 2.0. Подробности 
смотрите в LICENSE файле.

### Контакты

Если у вас есть вопросы или предложения о сотрудничестве, вы можете связаться со мной в Телеграм: 
[Sophia](https://t.me/ShilkinaSK).