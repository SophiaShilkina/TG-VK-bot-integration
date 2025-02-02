from bots_init import vk_ms
import asyncio
import logging
import aiosqlite


async def msg_valid(idu):
    while_exit = 0
    while while_exit != 1:
        try:
            message_text = vk_ms.messages.getHistory(user_id=idu, count=1)['items'][0]['text'].lower()
            if len(message_text) < 31:
                logging.info(f"Получено сообщение: '{message_text}' от пользователя {idu}")
                if message_text == 'начать' or message_text == 'start':
                    userAct = "start"
                elif message_text == 'все верно':
                    userAct = "go"
                elif message_text == 'прочитал(а) и принимаю правила':
                    userAct = "ok"
                elif message_text == 'позвать оператора':
                    userAct = "admin"
                else:
                    userAct = "exit"
                    await asyncio.sleep(2)

                async with aiosqlite.connect('action.db') as db:
                    await db.execute('UPDATE users SET act = ? WHERE userId = ?', (userAct, idu,))
                    await db.commit()

                return userAct

        except Exception as e:
            logging.error(f"An error occurred: {e}")
        await asyncio.sleep(1)
