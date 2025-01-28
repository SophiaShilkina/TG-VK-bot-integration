from callbacks import main_bot
from basiclogic import main_loop
import asyncio
import logging
from database import init_db

import time


async def main():
    await init_db()
    await asyncio.gather(main_bot(), main_loop())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        time.sleep(5)
        pass
