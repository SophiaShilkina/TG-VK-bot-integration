from vk_api.longpoll import VkLongPoll, VkEventType

from msg import *
from vksession import vk_session
from keyboards import *
from updates import *
from actionsdb import *
from vksession import bot
from callbacks import callback_operations
from sett import CHAT_ID

longpoll = VkLongPoll(vk_session)


async def message_handler(idu, message_text, event):
    userAct = "0"
    while_blok = 0

    await checking_user_in_database(idu)

    # Начало сеанса
    if message_text == 'начать' or message_text == 'start':
        print(f"Начинаю сессию с пользователем {idu}")
        await write_msg(idu,
                  'Привет!💙\nЯ чат-бот вашего любимого хостела. Рад познакомиться с вами сегодня.')
        await write_msg(idu,
                  'Давайте вместе организуем ваше идеальное пребывание в нашем уютном хостеле '
                  'всего за 4⃣ шага.')
        await write_msg(idu,
                  '1⃣ Для начала, скажите мне, пожалуйста, в какие даты вы планируете у нас '
                  'остановиться?\n\n'
                  '📆 Укажите даты в формате:\n\n❗дд.мм.гг – дд.мм.гг❗\n\n'
                  ', одним сообщением, где первая дата –  предпочитаемая для заезда, вторая – '
                  'для выезда.')

        userAct = "data"
        userAct = await saving_between_responses(idu, userAct)

    if userAct == "data":
        await write_msg(idu, '2⃣ Отлично, сколько гостей будет в вашей компании? 👔\n\n'
                                 '❗Необходимо указать только число❗\n\n'
                                 'Просим обратить ваше внимание, что проживать в нашем хостеле могут '
                                 'только дети возрастом начиная 📌от 14 лет📌 и старше.')

        userAct = "persons"
        await saving_between_responses(idu, userAct)

    if userAct == "persons":
        await write_msg(idu, '3⃣ Скажите, пожалуйста, соотношение мужчин и женщин в вашей '
                                 'группе?\n\n👫 Укажите в формате:\n\n❗Число мужчин / число женщин❗\n\n'
                                 ', например, 4 мужчин/2 женщин. Если персон какого-то пола не '
                                 'заезжает, укажите 0.')

        userAct = "gender"
        await saving_between_responses(idu, userAct)

    if userAct == "gender":
        await write_msg_with_photo(idu, '4⃣ Есть ли у вас предпочтения в выборе комнаты? Предлагаем Вам '
                                    'ознакомиться со списком и прайсом.\n\n🏡 Выбранные Вами желаемые '
                                    'комнаты укажите в формате, ❗который указан в списке, без '
                                    'использования заглавных букв (Caps Lock)❗\n\n, например, 4-ех '
                                    'женский. Напишите, "желаемых комнат нет", если предпочтений '
                                    'не имеется.')

        userAct = "room"
        await saving_between_responses(idu, userAct)

        userAct = "wait"
        await changing_act(idu, userAct)

    if userAct == "wait":
        while userAct != "exit":
            while while_blok != 1:
                await write_msg(idu, await presentation_of_information(idu), keyboard)
                while_blok += 1

            async def history_while():
                await asyncio.sleep(1)
                user_message_received = vk_ms.messages.getHistory(user_id=idu, count=1)['items'][0]['text']
                return user_message_received

            if await history_while() == 'Все верно':
                userAct = "exit"
            elif await history_while() == '📆 Изменить даты':
                userAct = "data"
            elif await history_while() == '👔 Изменить число персон':
                userAct = "persons"
            elif await history_while() == '👫 Изменить соотношение':
                userAct = "gender"
            elif await history_while() == '🏡 Изменить комнаты':
                userAct = "room"

            if userAct == "data":
                await write_msg(idu, 'Хорошо, введите верные даты, соблюдая данный '
                                         'формат:\n\n❗дд.мм.гг – дд.мм.гг❗')
                await saving_between_responses(idu, userAct)
                userAct = "confirm"
                await changing_act(idu, userAct)
                while_blok = 0

            if userAct == "persons":
                await write_msg(idu, 'Хорошо, отправьте число человек, которое '
                                         'должно заехать.')
                await saving_between_responses(idu, userAct)
                userAct = "gender"
                await changing_act(idu, userAct)

                await write_msg(event.user_id,
                          'Хорошо, введите верное соотношение, соблюдая данный формат'
                          ' и используя только числа:\n\n❗Число мужчин / число женщин❗')
                await saving_between_responses(idu, userAct)
                userAct = "confirm"
                await changing_act(idu, userAct)
                while_blok = 0

            elif userAct == "gender":
                await write_msg(event.user_id,
                          'Хорошо, введите верное соотношение, соблюдая данный формат и '
                          'используя только числа:\n\n❗Число мужчин / число женщин❗')
                await saving_between_responses(idu, userAct)
                userAct = "confirm"
                await changing_act(idu, userAct)
                while_blok = 0

            elif userAct == "room":
                await write_msg_with_photo(idu,
                                           'Хорошо, введите верную комнату (верные комнаты), в '
                                           'которой Вы бы предпочли проживать в нашем хостеле.')
                await saving_between_responses(idu, userAct)
                userAct = "confirm"
                await changing_act(idu, userAct)
                while_blok = 0

    if message_text == 'все верно':
        userAct = "go"
        await changing_act(idu, userAct)

        await write_msg(idu,
                  'Прежде чем отправить заявку на проживание в нашем хостеле, мы хотели бы '
                  'обратить ваше внимание на важные правила, которые необходимо соблюдать во время '
                  'вашего пребывания.\n\n✅ Пожалуйста, ознакомьтесь с полным списком правил проживания '
                  'и подтвердите свое согласие.')
        await write_msg(idu,
                  '🌎 ПРАВИЛА ВНУТРЕННЕГО РАСПОРЯДКА «КРИСТОФЕР ХОСТЕЛ» 🌎\n\n1⃣  Чистота и '
                  'порядок!\n• Убирать и мыть за собой посуду и кухонные принадлежности;\n• '
                  'Поддерживать порядок в комнатах;\n• Не оставлять свои личные вещи в местах общего '
                  'пользования;\n • Не хранить и не употреблять продукты питания в комнатах.\n2⃣  '
                  'Уважение!\n• Соблюдать режим тишины с 24:00 до 07:00;\n• Использовать стиральную '
                  'машину с 09:00 до 21:00.\n\n🚫 КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО 🚫\n• Курение, употребление'
                  ' и распространение наркотических веществ, употребление алкоголя - выселение;\n• '
                  'Проявление агрессии и всех признаков насилия к окружающим;\n• Хранение взрывчатых '
                  'и легко воспламеняющихся веществ, оружия, наркотиков, ртути, химических и '
                  'радиоактивных веществ;\n• Приглашение на территорию '
                  'хостела посторонних гостей, продажа своих услуг или товаров.\n\n⏰ ПРАВИЛА ЗАЕЗДА И '
                  'ВЫЕЗДА ⏰\n• Заезд возможен после 13:00, выезд в 12:00;\n• Раннее заселение или '
                  'поздний выезд возможны✅, при наличии свободных мест. Стоит учесть, что услуга '
                  'оплачивается отдельно за дополнительную плату;\n• В случае выезда раньше оплаченной '
                  'даты, администрация не возвращает денежные средства, внесенные за проживание;\n• '
                  'Гость обязан заранее предупредить о продлении брони. В случае неоплаты до 12:00, '
                  'администрация вправе заселить другого гостя.\n\nНам будет очень жаль, но ради '
                  'душевного спокойствия наших гостей и конечно персонала хостела, администрация '
                  'оставляет за собой право на выселение любого проживающего в случае нарушения '
                  'общественного порядка и правил проживания, без возврата денежных средств.',
                  keyboard2)
        user_get = vk_ms.users.get(user_ids=event.user_id)
        fullname = user_get[0]['first_name'] + ' ' + user_get[0]['last_name']
        await get_user_name(idu, fullname)

    elif message_text == 'прочитал(а) и принимаю правила':
        await write_msg(event.user_id,
                  'Я отправил эту информацию своим коллегам. '
                  'Она поможет им подобрать для вас самые комфортные условия проживания.')
        await write_msg(event.user_id,
                  'Время ожидания ответа на заявку:\n\n'
                  '⏰ Варьируется от 2 до 15 минут в дневное время.\n\n'
                  'После, оператор подключится в чат, чтобы начать организацию вашей поездки.')

        message_1 = await information_to_admin(idu)
        print(message_1)

        if message_1 != 0:
            print(11)
            await callback_operations(idu, message_1)
            message_1 = ""

    elif message_text == 'позвать оператора':
        bot.send_message(chat_id=CHAT_ID,
                         text=f'Гость <b>{return_user_name(idu)}</b> '
                              f'просит подключиться в чат.\n\n'
                              f'<a href="https://vk.com/gim226206756?sel={idu}">Подключиться '
                              f'в чат</a>',
                         parse_mode='html')
        await write_msg(idu, 'Направил Вашу просьбу коллегам, ожидайте ⏰')


# Главный асинхронный цикл
async def main_loop():
    while True:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                idu = event.user_id
                message_text = event.text.lower()
                await message_handler(idu, message_text, event)
