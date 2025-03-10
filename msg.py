import random
from bots_init import vk_session, bot
from upload import attachment
from config import CHANNEL_ID
from aiogram.enums import ParseMode


async def write_msg(user_id, message, keyboard=None):

    post = {
        'user_id': user_id,
        'message': message,
        'random_id': random.randint(1, 1000000),
    }

    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()
    else:
        post = post

    vk_session.method('messages.send', post)


async def write_msg_with_photo(peer_id, message):

    post = {
        'peer_id': peer_id,
        'message': message,
        'random_id': random.randint(1, 1000000),
        'attachment': await attachment()
    }

    vk_session.method('messages.send', post)


async def send_message_to_admin(message_text, reply_markup):
    try:
        await bot.send_message(CHANNEL_ID, message_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
