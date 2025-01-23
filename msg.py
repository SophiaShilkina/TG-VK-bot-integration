import random
from vksession import vk_session
from upload import attachment


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
        'attachment': attachment()
    }

    vk_session.method('messages.send', post)
