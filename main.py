from vksession import bot
from basiclogic import main_loop
import asyncio
from database import init_db

import time


if __name__ == '__main__':
    try:
        asyncio.run(init_db())
        asyncio.run(main_loop())
        bot.polling()
    except (KeyboardInterrupt, SystemExit):
        time.sleep(5)
        pass
