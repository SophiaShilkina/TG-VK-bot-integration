import aiosqlite
from bots_init import vk_ms
import asyncio
import logging
import re
from msg import write_msg


# Проверяем пользователя в базе данных
async def checking_user_in_database(idu):
    async with aiosqlite.connect('action.db') as db:
        async with db.execute('SELECT userId FROM users WHERE userId = ?', (idu,)) as cursor:
            user_in_database = await cursor.fetchone()
            if user_in_database is None:
                await db.execute(
                    'INSERT INTO users (userId, act, fullname, data, persons, gender, room, pastRooms) '
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (idu, 'start', '0', '0', '0', '0', '0', '0')
                )
                await db.commit()

        async with db.execute('SELECT act FROM users WHERE userId = ?', (idu,)) as cursor:
            result = await cursor.fetchone()
            if result is not None:
                userAct = result[0]
                return userAct
            else:
                return None


# Изменение шага и заполнение базы пользовательскими данными
async def saving_between_responses(idu, userAct):
    while_exit = 0
    while while_exit != 1:
        try:
            await asyncio.sleep(1)
            message_text = vk_ms.messages.getHistory(user_id=idu, count=1)['items'][0]['text']
            if len(message_text) < 50:
                if userAct == 'data':
                    if not re.match(r'^\s*\d{1,2}\.\d{1,2}\.\d{2}\s*[\s\-–—]{1,5}\s*\d{1,2}\.\d{1,2}\.\d{2}\s*\.*\s*$',
                             message_text):
                        await write_msg(idu,
                                        'Ваше сообщение не соответствует формату. Пожалуйста, пришлите даты '
                                        'еще раз, придерживаясь формата:\n\nдд.мм.гг – дд.мм.гг')
                    continue
                if userAct == 'persons':
                    if not re.match(r'^\s*\d{1,3}\s*\.*\s*$', message_text):
                        await write_msg(idu, 'Ваше сообщение не соответствует формату. Пожалуйста, пришлите '
                                     'количество человек еще раз, придерживаясь формата:\n\nТолько число.')
                    continue
                if userAct == 'gender':
                    if not re.match(r'^\s*\d{1,3}\s*[МЖмужчинаещ]*\s*[\\/]\s*\d{1,3}\s*[МЖмужчинаещ]*\s*\.*\s*$',
                         message_text):
                        await write_msg(idu,'Ваше сообщение не соответствует формату. Пожалуйста, пришлите '
                                            'соотношение человек еще раз, придерживаясь формата:\n\n'
                                            'Число мужчин / Число женщин.')
                    continue

                async with aiosqlite.connect('action.db') as db:
                    await db.execute(f'UPDATE users SET act = ?, {userAct} = ? WHERE userId = ?',
                                     (userAct, message_text, idu,))
                    if userAct == "room":
                        await db.execute('UPDATE users SET pastRooms = ? WHERE userId = ?', (message_text, idu,))
                    await db.commit()
                    async with db.execute('SELECT act FROM users WHERE userId = ?', (idu,)) as cursor:
                        result = await cursor.fetchone()
                        if result is not None:
                            userAct = result[0]
                    while_exit = 1
                    return userAct

        except Exception as e:
            logging.error(f"An error occurred: {e}")
        await asyncio.sleep(1)


# Изменение шага
async def changing_act(idu, userAct):
    async with aiosqlite.connect('action.db') as db:
        await db.execute('UPDATE users SET act = ? WHERE userId = ?', (userAct, idu,))
        await db.commit()


# Ответ пользователю с его ранее введенными данными на проверку
async def presentation_of_information(idu):
    async with aiosqlite.connect('action.db') as db:
        async with db.execute('SELECT * FROM users WHERE userId = ?', (idu,)) as cursor:
            record = await cursor.fetchone()
            if record:
                dates, persons, gender, room = record[3], record[4], record[5], record[6]
            else:
                dates, persons, gender, room = None, None, None, None

            text = (f'Спасибо, я внимательно все записал. Проверьте, пожалуйста, '
                    f'правильность введенных данных:\n\n'
                    f'📆 Даты: {dates}\n'
                    f'👔 Количество персон: {persons}\n'
                    f'👫 Мужчины и женщины: {gender}\n'
                    f'🏡 Комнаты: {room}\n')
            return text


# Внесение имени пользователя в бд
async def get_fullname(event):
    try:
        logging.info(f"Получение имени пользователя для ID: {event.user_id}")
        user_get = vk_ms.users.get(user_ids=event.user_id)
        fullname = user_get[0]['first_name'] + ' ' + user_get[0]['last_name']
        logging.info(f"Получено имя: {fullname}")
        async with aiosqlite.connect('action.db') as db:
            await db.execute('UPDATE users SET fullname = ? WHERE userId = ?', (fullname, event.user_id,))
            await db.commit()
        return fullname
    except Exception as e:
        logging.error(f"Ошибка при получении имени пользователя: {e}")
        return None


# Подготовка текста сообщения с информацией от пользователя админу
async def information_to_admin(idu):
    async with aiosqlite.connect('action.db') as db:
        async with db.execute('SELECT * FROM users WHERE userId = ?', (idu,)) as cursor:
            record = await cursor.fetchone()
            if record:
                name, dates, persons, gender, room = record[2], record[3], record[4], record[5], record[6]
            else:
                name, dates, persons, gender, room = None, None, None, None, None

        message_1 = (f'1. Имя: <b>{name}</b>\n'
                     f'2. Даты: <b>{dates}</b>\n'
                     f'3. Человек: <b>{persons}</b>\n'
                     f'4. М/Ж: <b>{gender}</b>\n'
                     f'5. Комнаты: <b>{room}</b>')
        return message_1


async def return_user_name(idu):
    async with aiosqlite.connect('action.db') as db:
        async with db.execute('SELECT fullname FROM users WHERE userId = ?', (idu,)) as cursor:
            result = await cursor.fetchone()
            if result is not None:
                fullname = result[0]
                return fullname
            else:
                return None
