import aiosqlite


# Проверяем пользователя в базе данных
async def checking_user_in_database(idu):
    async with aiosqlite.connect('action.db') as db:
        async with db.execute(f'SELECT userId FROM users WHERE userId = "{idu}"') as cursor:
            user_in_database = await cursor.fetchone()
            if user_in_database is None:
                await db.execute(
                    'INSERT INTO users (userId, act, fullname, data, persons, gender, room, pastRooms) '
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (idu, 'get_data', '0', '0', '0', '0', '0', '0')
                )
                await db.commit()
            else:
                await db.execute(f'UPDATE users SET act = get_data WHERE userId = "{idu}"')


# Переходим на шаг get_persons
async def changing_act(idu, userAct):
    async with aiosqlite.connect('action.db') as db:
        await db.execute(f"UPDATE users SET act = {userAct} WHERE userId = {idu}")
        await db.commit()
        async with db.execute(f'SELECT act FROM users WHERE userId = "{idu}"') as cursor:
            userAct = cursor.fetchone()[0]
            return userAct
