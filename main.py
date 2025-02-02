from callbacks import main_bot
from basic_logic import main_loop
import asyncio
import logging
from database import init_db


async def main():
    await init_db()
    await asyncio.gather(main_bot(), main_loop())


async def shutdown():
    logging.info("Shutting down...")
    await asyncio.sleep(5)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        asyncio.run(shutdown())
        pass
