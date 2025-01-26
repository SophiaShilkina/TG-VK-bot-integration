from tryp import main_bot
from basiclogic import main_loop
import asyncio
import logging
from database import init_db

import time


if __name__ == '__main__':
    try:
        asyncio.run(init_db())
        asyncio.run(main_loop())
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main_bot())
    except (KeyboardInterrupt, SystemExit):
        time.sleep(5)
        pass
