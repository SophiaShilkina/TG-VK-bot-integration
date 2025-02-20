from base import async_session
from models import UsersBase
from methods import get_fullname, send_message
from responses_logic import message_handler
from sqlalchemy import select, update
import re


# Проверяем пользователя в базе данных и возвращаем его шаг
async def check_user_in_database_and_return_act(user_id) -> str:
    async with (async_session() as session):
        stmt = select(UsersBase.userId).where(UsersBase.userId == user_id)
        result = await session.execute(stmt)

        user_in_database = result.scalar_one_or_none()

        if user_in_database is None:
            fullname = await get_fullname(user_id)

            session.add_all(
                [
                    UsersBase(userId=user_id, act='start', fullname=fullname, dates=None,
                              persons=None, genders=None, rooms=None, pastRooms=None),
                ]
            )
            await session.commit()

        stmt = select(UsersBase.act).where(UsersBase.userId == user_id)
        result = await session.execute(stmt)

        act = result.scalar_one_or_none()

        return act


# Валидация сообщений пользователя
async def message_validation(user_id, user_act, message_incoming) -> str:
    async with (async_session() as session):
        if user_act == 'dates':
            if not re.match(r'^\s*\d{1,2}\.\d{1,2}\.\d{2}\s*[\s\-–—]{1,5}\s*\d{1,2}\.\d{1,2}\.\d{2}\s*\.*\s*$',
                            message_incoming):
                user_act = 'dates_mistake'

        if user_act == 'persons':
            if not re.match(r'^\s*\d{1,3}\s*\.*\s*$', message_incoming):
                user_act = 'persons_mistake'

        if user_act == 'gender':
            if not re.match(r'^\s*\d{1,3}\s*[МЖмужчинаещ]*\s*[\\/]\s*\d{1,3}\s*[МЖмужчинаещ]*\s*\.*\s*$',
                            message_incoming):
                user_act = 'gender_mistake'

        stmt = update(UsersBase).where(UsersBase.userId == user_id).values(act=user_act)
        await session.execute(stmt)
        await session.commit()

        return user_act


commands_tpl = ('начать', '📆 изменить даты', '👔 изменить число персон', '👫 изменить соотношение',
                '🏡 изменить комнаты', 'все верно', 'прочитал(а) и принимаю правила', 'позвать оператора')
acts_tpl = ('start', 'dates', 'dates_mistake', 'persons', 'persons_mistake', 'genders', 'genders_mistake',
            'rooms')


# Реализация логики шагов пользователя через словарь
def changed_act(user_act) -> str:
    changed_acts_dict = {'start': 'dates',
                         'dates': 'persons',
                         'persons': 'genders',
                         'genders': 'rooms'}
    user_act = changed_acts_dict.get(user_act)
    return user_act


async def user_act_handler(user_id, user_act, message_incoming, acts_tuple=acts_tpl):
    async with (async_session() as session):
        if message_incoming == 'начать' or message_incoming == 'start':
            messages_outgoing = message_handler(user_act)
            if type(messages_outgoing) is tuple:
                for message_outgoing in messages_outgoing:
                    await send_message(user_id, message_outgoing)
            else:
                await send_message(user_id, messages_outgoing)

            stmt = update(UsersBase).where(UsersBase.userId == user_id).values(act=changed_act(user_act))
            await session.execute(stmt)
            await session.commit()
            return

        if user_act in acts_tuple:
            if user_act in ('dates', 'persons', 'genders', 'rooms'):
                user_act = await message_validation(user_id, user_act, message_incoming)
                if user_act in ('dates', 'persons', 'genders', 'rooms'):
                    await send_message(user_id, message_handler(user_act))
                    column_value = {user_act: message_incoming}
                    stmt = update(UsersBase).where(UsersBase.userId == user_id).values(**column_value,
                                                                                       act=changed_act(user_act))
                    await session.execute(stmt)
                    await session.commit()
                    return

                else:
                    await send_message(user_id, message_handler(user_act))
                    stmt = update(UsersBase).where(UsersBase.userId == user_id).values(act=user_act.split('_')[0])
                    await session.execute(stmt)
                    await session.commit()
                    return
