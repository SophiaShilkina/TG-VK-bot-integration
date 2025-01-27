import aiosqlite
import time
from botsinit import vk_ms
from keyboards import keyboard_tg
from msg import send_message_to_admin, write_msg_with_photo


async def update_user_data(idu):
    while_exit = 0
    while while_exit != 1:
        try:
            message_text = vk_ms.messages.getHistory(user_id=idu, count=1)['items'][0]['text']
            if len(message_text) < 89:
                async with aiosqlite.connect("action.db") as db:
                    await db.execute(f'UPDATE users SET data = ? WHERE userId = ?', (message_text, idu,))
                    await db.commit()
                    while_exit = 1
                    return message_text.text

        except:
            pass
        time.sleep(1)


async def update_user_persons(idu):
    while_exit = 0
    while while_exit != 1:
        try:
            message_text = vk_ms.messages.getHistory(user_id=idu, count=1)['items'][0]['text']
            if len(message_text) < 84:
                async with aiosqlite.connect("action.db") as db:
                    await db.execute(f'UPDATE users SET persons = ? WHERE userId = ?', (message_text, idu,))
                    await db.commit()
                    while_exit = 1
                    return message_text.text

        except:
            pass
        time.sleep(1)


async def update_user_gender(idu):
    while_exit = 0
    while while_exit != 1:
        try:
            message_text = vk_ms.messages.getHistory(user_id=idu, count=1)['items'][0]['text']
            if len(message_text) < 108:
                async with aiosqlite.connect("action.db") as db:
                    await db.execute(f'UPDATE users SET gender = ? WHERE userId = ?', (message_text, idu,))
                    await db.commit()
                    while_exit = 1
                    return message_text.text

        except:
            pass
        time.sleep(1)


async def update_user_room(idu):
    while_exit = 0
    while while_exit != 1:
        try:
            message_text = vk_ms.messages.getHistory(user_id=idu, count=1)['items'][0]['text']
            if len(message_text) < 186:
                async with aiosqlite.connect("action.db") as db:
                    await db.execute(f'UPDATE users SET room = ? WHERE userId = ?', (message_text, idu,))
                    await db.execute(f'UPDATE users SET pastRooms = ? WHERE userId = ?', (message_text, idu,))
                    await db.commit()
                    while_exit = 1
                    return message_text.text

        except:
            pass
        time.sleep(1)


async def update_user_message(idu):
    async with aiosqlite.connect("action.db") as db:
        async with db.execute(f'SELECT * FROM users WHERE userId = ?', (idu,)) as cursor:
            record = await cursor.fetchone()
            if record:
                name, dates, persons, gender, room = record[2], record[3], record[4], record[5], record[6]
            else:
                name, dates, persons, gender, room = None, None, None, None, None

        await send_message_to_admin('<b>Исправленные данные от гостя:</b>\n\n'
                                   f'1. Имя: <b>{name}</b>\n'
                                   f'2. Даты: <b>{dates}</b>\n'
                                   f'3. Человек: <b>{persons}</b>\n'
                                   f'4. М/Ж: <b>{gender}</b>\n'
                                   f'5. Комнаты: <b>{room}</b>',
                                   keyboard_tg)


async def mistake_user_room(idu):
    async with aiosqlite.connect("action.db") as db:
        async with db.execute(f'SELECT pastRooms FROM users WHERE userId = ?', (idu,)) as cursor:
            tuple_past_room = await cursor.fetchone()
            if tuple_past_room:
                pastRoom = tuple_past_room[0]
            else:
                pastRoom = None

    await write_msg_with_photo(idu, f'🛏 К сожалению, в выбранной Вами комнате на данные даты '
                                      f'мест нет.\n\nПожалуйста, посмотрите другие доступные '
                                      f'варианты и сообщите нам, какую комнату Вы бы хотели '
                                      f'забронировать. Мы постараемся найти для Вас подходящий '
                                      f'вариант размещения. Спасибо за понимание!\n\n🔙 Ваш '
                                      f'прошлый выбор комнаты: '
                                      f'{pastRoom}')

    while_exit = 0
    while while_exit != 1:
        try:
            message_text = vk_ms.messages.getHistory(user_id=idu, count=1)['items'][0]['text']
            if len(message_text) < 282:
                async with aiosqlite.connect("action.db") as db:
                    await db.execute(f'UPDATE users SET room = ? WHERE userId = ?', (message_text, idu,))
                    async with db.execute(f'SELECT * FROM users WHERE userId = ?', (idu,)) as cursor:
                        rooms = await cursor.fetchone()

                        if rooms:
                            room, past_room = rooms[0], rooms[0]

                        else:
                            room, past_room = None, None

                        summation = room + past_room

                    await db.execute(f'UPDATE users SET pastRooms = ? WHERE userId = ?', (summation, idu,))
                    await db.commit()
                    while_exit = 1
                    return message_text.text
        except:
            pass
        time.sleep(1)
