from vk_api.longpoll import VkLongPoll, VkEventType
import asyncio
from datetime import datetime, timedelta
import aiosqlite

from msg import write_msg
from vksession import vk_session
from keyboards import *
from updates import *
from actionsdb import checking_user_in_database, changing_act

longpoll = VkLongPoll(vk_session)



async def message_handler(event, db):

    userAct = '0'
    current_step = "confirm"
    while_blok = 0

    idu = event.user_id
    message_text = event.text.lower()

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

        userAct = "get_persons"
        await changing_act(idu, userAct)

    elif changing_act(idu, userAct) == "get_persons":
        get_data = vk_ms.messages.getHistory(user_id=idu, count=1)['items'][0]['text']
        sql.execute(f'UPDATE users SET data = "{get_data}" WHERE userId = "{idu}"')
        await write_msg(idu, '2⃣ Отлично, сколько гостей будет в вашей компании? 👔\n\n'
                                 '❗Необходимо указать только число❗\n\n'
                                 'Просим обратить ваше внимание, что проживать в нашем хостеле могут '
                                 'только дети возрастом начиная 📌от 14 лет📌 и старше.')
        sql.execute(f"UPDATE users SET act = 'get_gender' WHERE userId = {idu}")
        db.commit()
        userAct = sql.execute(f'SELECT act FROM users WHERE userId = "{idu}"').fetchone()[0]
    elif userAct == "get_gender":
        get_persons = vk_ms.messages.getHistory(user_id=idu, count=1)['items'][0]['text']
        sql.execute(f'UPDATE users SET persons = "{get_persons}" WHERE userId = "{idu}"')
        await write_msg(idu, '3⃣ Скажите, пожалуйста, соотношение мужчин и женщин в вашей '
                                 'группе?\n\n👫 Укажите в формате:\n\n❗Число мужчин / число женщин❗\n\n'
                                 ', например, 4 мужчин/2 женщин. Если персон какого-то пола не '
                                 'заезжает, укажите 0.')
        sql.execute(f"UPDATE users SET act = 'get_room' WHERE userId = {idu}")
        db.commit()
        userAct = sql.execute(f'SELECT act FROM users WHERE userId = "{idu}"').fetchone()[0]
    elif userAct == "get_room":
        get_gender = vk_ms.messages.getHistory(user_id=idu, count=1)['items'][0]['text']
        sql.execute(f'UPDATE users SET gender = "{get_gender}" WHERE userId = "{idu}"')
        await vk_ms.messages.send(peer_id=idu,
                            message='4⃣ Есть ли у вас предпочтения в выборе комнаты? Предлагаем Вам '
                                    'ознакомиться со списком и прайсом.\n\n🏡 Выбранные Вами желаемые '
                                    'комнаты укажите в формате, ❗который указан в списке, без '
                                    'использования заглавных букв (Caps Lock)❗\n\n, например, 4-ех '
                                    'женский. Напишите, "желаемых комнат нет", если предпочтений '
                                    'не имеется.',
                            random_id=random.randint(1, 1000000),
                            attachment=attachment())
        sql.execute(f"UPDATE users SET act = 'check' WHERE userId = {idu}")
        db.commit()
        userAct = sql.execute(f'SELECT act FROM users WHERE userId = "{idu}"').fetchone()[0]
    elif userAct == "check":
        sql.execute(f"UPDATE users SET act = 'wait' WHERE userId = {idu}")
        get_room = vk_ms.messages.getHistory(user_id=idu, count=1)['items'][0]['text']
        sql.execute(f'UPDATE users SET room = "{get_room}" WHERE userId = "{idu}"')
        sql.execute(f'UPDATE users SET pastRooms = "{get_room}" WHERE userId = "{idu}"')
        db.commit()
        userAct = sql.execute(f'SELECT act FROM users WHERE userId = "{idu}"').fetchone()[0]
    if userAct == "wait":
        while current_step != "exit":
            while while_blok != 1:
                await write_msg(idu,
                          f'Спасибо, я внимательно все записал. Проверьте, пожалуйста, '
                          f'правильность введенных данных:\n\n'
                          f'📆 Даты: {sql.execute(
                              f'SELECT data FROM users '
                              f'WHERE userId = "{idu}"').fetchone()[0]}\n'
                          f'👔 Количество персон: {sql.execute(
                              f'SELECT persons FROM users '
                              f'WHERE userId = "{idu}"').fetchone()[0]}\n'
                          f'👫 Мужчины и женщины: {sql.execute(
                              f'SELECT gender FROM users '
                              f'WHERE userId = "{idu}"').fetchone()[0]}\n'
                          f'🏡 Комнаты: {sql.execute(
                              f'SELECT room FROM users '
                              f'WHERE userId = "{idu}"').fetchone()[0]}\n', keyboard)
                while_blok += 1

            user_message_received_end = vk_ms.messages.getHistory(user_id=idu, count=1)[
                'items'][0]['text']
            if user_message_received_end == 'Все верно':
                current_step = "exit"
            elif user_message_received_end == '📆 Изменить даты':
                current_step = "dates"
            elif user_message_received_end == '👔 Изменить число персон':
                current_step = "persons"
            elif user_message_received_end == '👫 Изменить соотношение':
                current_step = "gender"
            elif user_message_received_end == '🏡 Изменить комнаты':
                current_step = "room"

            if current_step == "dates":
                await write_msg(idu, 'Хорошо, введите верные даты, соблюдая данный '
                                         'формат:\n\n❗дд.мм.гг – дд.мм.гг❗')
                from_id = event.user_id
                for event in VkLongPoll(vk_session).listen():
                    if event.type == VkEventType.MESSAGE_NEW:
                        if event.user_id == from_id:
                            get_data = vk_ms.messages.getHistory(user_id=idu, count=1)[
                                'items'][0]['text']
                            sql.execute(
                                f'UPDATE users SET data = "{get_data}" '
                                f'WHERE userId = "{idu}"')
                            db.commit()
                            current_step = "confirm"
                            while_blok = 0
                            break

            elif current_step == "persons":
                await write_msg(idu, 'Хорошо, отправьте число человек, которое '
                                         'должно заехать.')
                from_id = event.user_id
                for event in VkLongPoll(vk_session).listen():
                    if event.type == VkEventType.MESSAGE_NEW:
                        if event.user_id == from_id:
                            get_persons = vk_ms.messages.getHistory(user_id=idu, count=1)[
                                'items'][0]['text']
                            sql.execute(f'UPDATE users SET persons = "{get_persons}" '
                                        f'WHERE userId = "{idu}"')
                            db.commit()
                            break
                await write_msg(event.user_id,
                          'Хорошо, введите верное соотношение, соблюдая данный формат'
                          ' и используя только числа:\n\n❗Число мужчин / число женщин❗')
                for event in VkLongPoll(vk_session).listen():
                    if event.type == VkEventType.MESSAGE_NEW:
                        if event.user_id == from_id:
                            get_gender = vk_ms.messages.getHistory(user_id=idu, count=1)[
                                'items'][0]['text']
                            sql.execute(f'UPDATE users SET gender = "{get_gender}" '
                                        f'WHERE userId = "{idu}"')
                            db.commit()
                            current_step = "confirm"
                            while_blok = 0
                            break

            elif current_step == "gender":
                await write_msg(event.user_id,
                          'Хорошо, введите верное соотношение, соблюдая данный формат и '
                          'используя только числа:\n\n❗Число мужчин / число женщин❗')
                from_id = event.user_id
                for event in VkLongPoll(vk_session).listen():
                    if event.type == VkEventType.MESSAGE_NEW:
                        if event.user_id == from_id:
                            get_gender = vk_ms.messages.getHistory(user_id=idu, count=1)[
                                'items'][0]['text']
                            sql.execute(f'UPDATE users SET gender = "{get_gender}" '
                                        f'WHERE userId = "{idu}"')
                            db.commit()
                            current_step = "confirm"
                            while_blok = 0
                            break

            elif current_step == "room":
                await vk_ms.messages.send(peer_id=idu,
                                    message='Хорошо, введите верную комнату (верные комнаты), в '
                                            'которой Вы бы предпочли проживать в нашем хостеле.',
                                    random_id=random.randint(1, 1000000),
                                    attachment=attachment())
                from_id = event.user_id
                for event in VkLongPoll(vk_session).listen():
                    if event.type == VkEventType.MESSAGE_NEW:
                        if event.user_id == from_id:
                            get_room = vk_ms.messages.getHistory(user_id=idu, count=1)[
                                'items'][0]['text']
                            sql.execute(f'UPDATE users SET room = "{get_room}" '
                                        f'WHERE userId = "{idu}"')
                            sql.execute(f'UPDATE users SET pastRooms = "{get_room}" '
                                        f'WHERE userId = "{idu}"')
                            db.commit()
                            current_step = "confirm"
                            while_blok = 0
                            break
    if message_text == 'все верно':
        sql.execute(f"UPDATE users SET act = 'go' WHERE userId = {idu}")
        current_step = "confirm"
        while_blok = 0
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
        sql.execute(f'UPDATE users SET fullname = "{fullname}" WHERE userId = "{idu}"')
        db.commit()
        userAct = sql.execute(f'SELECT act FROM users WHERE userId = "{idu}"').fetchone()[0]
    elif message_text == 'прочитал(а) и принимаю правила':
        message_1 = None
        await write_msg(event.user_id,
                  'Я отправил эту информацию своим коллегам. '
                  'Она поможет им подобрать для вас самые комфортные условия проживания.')
        await write_msg(event.user_id,
                  'Время ожидания ответа на заявку:\n\n'
                  '⏰ Варьируется от 2 до 15 минут в дневное время.\n\n'
                  'После, оператор подключится в чат, чтобы начать организацию вашей поездки.')

        message_1 = f'1. Имя: <b>{sql.execute(f'SELECT fullname FROM users '
                                              f'WHERE userId = "{idu}"').fetchone()[0]}</b>\n'
        message_1 += f'2. Даты: <b>{sql.execute(
            f'SELECT data FROM users WHERE userId = "{idu}"').fetchone()[0]}</b>\n'
        message_1 += f'3. Человек: <b>{sql.execute(
            f'SELECT persons FROM users WHERE userId = "{idu}"').fetchone()[0]}</b>\n'
        message_1 += f'4. М/Ж: <b>{sql.execute(
            f'SELECT gender FROM users WHERE userId = "{idu}"').fetchone()[0]}</b>\n'
        message_1 += f'5. Комнаты: <b>{sql.execute(
            f'SELECT room FROM users WHERE userId = "{idu}"').fetchone()[0]}</b>'

        if message_1 != 0:

            message_mistake = ""
            userAct1 = '0'
            flag = False
            flag2 = False
            flag3 = False
            flag4 = False
            flag5 = False
            user_message_received = False

            bot.send_message(chat_id=channel_id,
                             text='<b>Новая заявка от бота</b>\n\n' + message_1,
                             parse_mode='html',
                             reply_markup=keyboard_tg)

            @bot.callback_query_handler(func=lambda callback: callback.data)
            def check_callback_data(callback):
                print("111")
                global message_mistake, userAct1, flag, flag2, flag3, flag4, flag5, \
                    user_message_received
                if callback.data == 'yes':
                    write_msg(idu,
                              '😸 На ваши даты есть места! Скоро оператор подключится в чат.')
                    bot.send_message(callback.message.chat.id,
                                     f'Принято, отправляю\n\n<a href="https://vk.com/gim226206756?sel'
                                     f'={idu}">Подключиться в чат</a>', parse_mode='html')

                if callback.data == 'rooms':
                    bot.send_message(callback.message.chat.id, 'Принято, прошу гостя поменять комнату')
                    mistake_user_room(idu)
                    flag = True
                    if flag:
                        write_msg(idu, 'Спасибо за понимание! Буду рад помочь вам найти '
                                       'подходящий вариант размещения. Отправил данные коллегам.')
                        update_user_message(idu)
                        flag = False

                if callback.data == 'what':
                    bot.edit_message_text(chat_id=channel_id,
                                          message_id=callback.message.message_id,
                                          text=message_1 + "\n\nВыбери пункт или пункты, в "
                                                           "\nкоторых есть ошибка",
                                          parse_mode='html',
                                          reply_markup=keyboard_tg1)
                if callback.data == '2':
                    message_mistake += '❗даты'
                    flag2 = True
                    bot.send_message(callback.message.chat.id, '2 пункт')
                if callback.data == '3':
                    message_mistake += '❗число человек'
                    flag3 = True
                    bot.send_message(callback.message.chat.id, '3 пункт')
                if callback.data == '4':
                    message_mistake += '❗cоотношение человек'
                    flag4 = True
                    bot.send_message(callback.message.chat.id, '4 пункт')
                if callback.data == '5':
                    message_mistake += '❗комнаты'
                    flag5 = True
                    bot.send_message(callback.message.chat.id, '5 пункт')
                if callback.data == 'allFail':
                    write_msg(idu,
                              f'Оператор нашел ошибку/несостыковку в заполненной Вами форме, '
                              f'он подключится в диалог ближайшее время чтобы уточнить детали,'
                              f' ожидайте ⏰')
                    bot.send_message(callback.message.chat.id,
                                     f'Принято, объясняю долбоебу что он совсем долбоеб\n\n'
                                     f'<a href="https://vk.com/gim226206756?sel={idu}">Подключиться в '
                                     f'чат</a>', parse_mode='html')
                if callback.data == 'ready':
                    write_msg(idu,
                              f'🙀 Оператор нашел ошибку/несостыковку в заполненной Вами форме, '
                              f'на следующих позициях: \n\n{message_mistake}❗\n\nпожалуйста, четко '
                              f'следуйте указаниям бота по заполнению формы.\n\nПросим Вас начать '
                              f'обращать особое внимание на информацию, которая заключена в ❗❗ и '
                              f'заполнить обозначенные пункты повторно ✏')
                    bot.send_message(callback.message.chat.id,
                                     'Принято, поминутно объясняю долбоебу, где он долбоеб')
                    if flag2:
                        write_msg(idu, '📆 Пожалуйста, введите даты заезда и выезда, '
                                       'соблюдая данный формат:\n\n❗дд.мм.гг – дд.мм.гг❗')
                        update_user_data(idu)
                        flag2 = False
                    if flag3:
                        write_msg(idu,
                                  '👔 Введите число человек, которое должно заехать.\n\n❗Необходимо '
                                  'отправить только цифру❗')
                        update_user_persons(idu)
                        flag3 = False
                    if flag4:
                        write_msg(idu,
                                  '👫 Введите верное соотношение, соблюдая данный формат и используя '
                                  'только числа:\n\n❗Число мужчин / число женщин❗')
                        update_user_gender(idu)
                        flag4 = False
                    if flag5:
                        vk_ms.messages.send(peer_id=idu,
                                            message='🏡 Введите верную комнату (верные комнаты), в '
                                                    'которой Вы бы предпочли проживать в нашем хостеле.'
                                                    '\n\nУкажите в формате, ❗который указан в списке, '
                                                    'без использования заглавных букв (Caps Lock)❗',
                                            random_id=random.randint(1, 1000000),
                                            attachment=attachment())
                        update_user_room(idu)
                        flag5 = False
                    if not (flag2 and flag3 and flag4 and flag5):
                        write_msg(idu,
                                  'Отправил обновленную информацию своим коллегам, ожидайте ⏰')
                        update_user_message(idu)
                        message_mistake = ""

                if callback.data == 'no':
                    write_msg(idu,
                              'Благодарю вас за обращение к нам. К сожалению, я должен сообщить'
                              ' вам, что на даты, которые вы запрашивали, у нас нет свободных мест ни '
                              'в одной комнате.\n\nЕсли вы готовы рассмотреть другие даты вашего '
                              'визита, пожалуйста, сообщите мне об этом, повторно нажав «Начать» и '
                              'оставив заявку снова, или попросите меня позвать оператора, нажав '
                              '«Пригласить оператора», чтобы обсудить с ним вопросы заселения, и мы с '
                              'радостью поможем вам организовать проживание.\n\nС уважением,\nВаш '
                              'персональный чат-бот',
                              keyboard3)
                    bot.send_message(callback.message.chat.id, 'Принято, отказ')

    elif message_text == 'позвать оператора':
        bot.send_message(chat_id=channel_id,
                         text=f'Гость <b>{sql.execute(
                              f'SELECT fullname FROM users '
                              f'WHERE userId = "{event.user_id}"').fetchone()[0]}</b> '
                              f'просит подключиться в чат.\n\n'
                              f'<a href="https://vk.com/gim226206756?sel={idu}">Подключиться '
                              f'в чат</a>',
                         parse_mode='html')
        await write_msg(idu, 'Направил Вашу просьбу коллегам, ожидайте ⏰')


# Главный асинхронный цикл
async def main_loop(db):
    while True:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                await message_handler(event, db)

                # Устанавливаем время окончания сессии (например, через 10 минут)
                session_end_time = datetime.now() + timedelta(minutes=60)

                # Ожидаем завершения сессии или получения нового сообщения
                while datetime.now() < session_end_time:
                    # Время для обработки сообщений или других операций
                    await asyncio.sleep(0.2)  # Чтобы не блокировать основной цикл
