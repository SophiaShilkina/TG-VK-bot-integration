from base import async_session
from models import UsersBase
from methods import get_fullname, send_message
from responses_logic import message_handler
from sqlalchemy import select, update
import re


# Проверяем пользователя в базе данных и возвращаем его шаг
async def check_user_in_database_and_return_act(user_id):
    async with (async_session() as session):
        stmt = select(UsersBase.userId).where(UsersBase.userId == user_id)
        result = await session.execute(stmt)

        user_in_database = result.scalars_one_or_none()

        if user_in_database is None:
            fullname = await get_fullname(user_id)

            session.add_all(
                [
                    UsersBase(userId=user_id, act='start', fullname=fullname, data=None,
                              persons=None, gender=None, room=None, pastRooms=None),
                ]
            )
            await session.commit()

        stmt = select(UsersBase.act).where(UsersBase.userId == user_id)
        act = await session.execute(stmt)

        return act


# Валидация сообщений пользователя
async def message_validation(user_id, user_act, message):
    async with (async_session() as session):
        if user_act == 'dates':
            if not re.match(r'^\s*\d{1,2}\.\d{1,2}\.\d{2}\s*[\s\-–—]{1,5}\s*\d{1,2}\.\d{1,2}\.\d{2}\s*\.*\s*$',
                            message):
                user_act = 'dates_mistake'

        if user_act == 'persons':
            if not re.match(r'^\s*\d{1,3}\s*\.*\s*$', message):
                user_act = 'persons_mistake'

        if user_act == 'gender':
            if not re.match(r'^\s*\d{1,3}\s*[МЖмужчинаещ]*\s*[\\/]\s*\d{1,3}\s*[МЖмужчинаещ]*\s*\.*\s*$',
                            message):
                user_act = 'gender_mistake'

        stmt = update(UsersBase).where(UsersBase.userId == user_id).values(userAct=user_act)
        await session.execute(stmt)
        await session.commit()

        return user_act


commands_tpl = ('начать', '📆 изменить даты', '👔 изменить число персон', '👫 изменить соотношение',
                '🏡 изменить комнаты', 'все верно', 'прочитал(а) и принимаю правила', 'позвать оператора')
acts_tpl = ('start', 'dates', 'dates_mistake', 'persons', 'persons_mistake', 'genders', 'genders_mistake',
            'rooms')


async def user_act_handler(user_id, user_act, message, acts_tuple=acts_tpl):
    async with (async_session() as session):
        if message == 'начать' or message == 'start':
            messages = message_handler(user_act)
            for message in messages:
                await send_message(user_id, message)

            stmt = update(UsersBase).where(UsersBase.userId == user_id).values(userAct='dates')
            await session.execute(stmt)
            await session.commit()

        if user_act in acts_tuple:
            if user_act in ('dates', 'persons', 'genders', 'rooms'):
                user_act = await message_validation(user_id, user_act, message)
                if user_act in ('dates', 'persons', 'genders', 'rooms'):
                    column_value = {user_act: message}
                    stmt = update(UsersBase).where(UsersBase.userId == user_id).values(**column_value)
                    await session.execute(stmt)
                    await session.commit()
                else:
                    await send_message(user_id, message_handler(user_act))
                    user_act = user_act.split('_')[0]
                    stmt = update(UsersBase).where(UsersBase.userId == user_id).values(userAct=user_act)
                    await session.execute(stmt)
                    await session.commit()
