import aiosqlite
import logging


async def init_db():
    logging.info("Initializing the database.")
    try:
        async with aiosqlite.connect('action.db') as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                userId INTEGER PRIMARY KEY AUTOINCREMENT,
                act TEXT,
                fullname TEXT,
                data TEXT,
                persons TEXT,
                gender TEXT,
                room TEXT,
                pastRooms TEXT
            )""")
            await db.commit()

    except Exception as e:
        logging.error(f"An error occurred: {e}")
