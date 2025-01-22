import random
from vksession import vk_session


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

