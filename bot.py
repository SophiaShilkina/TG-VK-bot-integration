import vk_api
from vk_api import VkUpload, VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton
import random
import requests
import telebot
from telebot import types
import threading

user_states = {}

token = "vk1.a.EbIR8ZKa8CHcKOWZ7QC4bw_AG-V7i5J64SMuWtSRxFW0wIgt7q4XoHTOqEBS7qTBAymLEbB9YbuguCVOgJyr0er9mj4MORRjKf6mq-xp\
         RGQu25XuVAQVBQNYJRMMNLEylGZGxwZilXkBPdGGFH1rH43bM3pGqqaGkTVpomviQUWtjZFYzID36ps1UVsp5jDBmD-82-jxbEp9BSyysMTdIA"
bot = telebot.TeleBot('7398853580:AAHST7_8FQQUbMEbJ-ajUwNPrUd2j_8XM6Y')
token_tg = "7398853580:AAHST7_8FQQUbMEbJ-ajUwNPrUd2j_8XM6Y"
url = "https://api.telegram.org/bot"
channel_id = "-1002152258508"
url += token_tg
method = url + "/sendMessage"

session = vk_api.VkApi(token="vk1.a.EbIR8ZKa8CHcKOWZ7QC4bw_AG-V7i5J64SMuWtSRxFW0wIgt7q4XoHTOqEBS7qTBAymLEbB9YbuguCVOgJy\
                              r0er9mj4MORRjKf6mq-xpRGQu25XuVAQVBQNYJRMMNLEylGZGxwZilXkBPdGGFH1rH43bM3pGqqaGkTVpomviQUWt\
                              jZFYzID36ps1UVsp5jDBmD-82-jxbEp9BSyysMTdIA")
vk_session = vk_api.VkApi(token="vk1.a.EbIR8ZKa8CHcKOWZ7QC4bw_AG-V7i5J64SMuWtSRxFW0wIgt7q4XoHTOqEBS7qTBAymLEbB9YbuguCVO\
                              gJyr0er9mj4MORRjKf6mq-xpRGQu25XuVAQVBQNYJRMMNLEylGZGxwZilXkBPdGGFH1rH43bM3pGqqaGkTVpomviQ\
                              UWtjZFYzID36ps1UVsp5jDBmD-82-jxbEp9BSyysMTdIA")
user_message_received = False
user_message_received2 = False
user_message_received3 = False
current_step = "confirm"
random_id = random.randint(1, 1000000)
while_blok = 0
message_1 = 0


def write_msg(user_id, message, keyboard=None, keyboard2=None, keyboard3=None):

    post = {
        'user_id': user_id,
        'message': message,
        'random_id': random.randint(1, 1000000),
    }

    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()
    elif keyboard2 != None:
        post["keyboard"] = keyboard2.get_keyboard()
    elif keyboard3 != None:
        post["keyboard"] = keyboard3.get_keyboard()
    else:
        post = post

    session.method('messages.send', post)


keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Все верно', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('Изменить даты', color=VkKeyboardColor.SECONDARY)
keyboard.add_button('Изменить число персон', color=VkKeyboardColor.SECONDARY)
keyboard.add_line()
keyboard.add_button('Изменить соотношение', color=VkKeyboardColor.SECONDARY)

keyboard2 = VkKeyboard(one_time=True)
keyboard2.add_button('Прочитал и принимаю правила', color=VkKeyboardColor.POSITIVE)

keyboard3 = VkKeyboard(one_time=True)
keyboard3.add_button('Начать', color=VkKeyboardColor.POSITIVE)
keyboard3.add_button('Позвать оператора', color=VkKeyboardColor.SECONDARY)


vk_ms = vk_session.get_api()

for event in VkLongPoll(session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        message_text = event.text.lower()
        if message_text == 'начать':
            fullname = None
            get_data = None
            get_persons = None
            get_gender = None
            message_1 = None
            write_msg(event.user_id,
                      'Привет!💙\nЯ чат-бот вашего любимого хостела. Рад познакомиться с вами сегодня.')
            write_msg(event.user_id,
                      'Давайте вместе организуем ваше идеальное пребывание в нашем уютном хостеле всего '
                      'за 3⃣ шага.')
            write_msg(event.user_id,
                      '1⃣ Для начала, скажите мне, пожалуйста, в какие даты вы планируете у нас '
                      'остановиться?\n\n'
                      '📆 Укажите даты в формате:\n\n❗дд.мм.гг – дд.мм.гг❗\n\n'
                      ', одним сообщением, где первая дата –  предпочитаемая для заезда, вторая – для выезда.')
            user_message_received = True

        elif user_message_received:
            get_data = vk_ms.messages.getHistory(user_id=event.user_id, count=1)['items'][0]['text']
            print(get_data)
            write_msg(event.user_id, '2⃣ Отлично, сколько гостей будет в вашей компании? 👔\n\n'
                                     '❗Необходимо указать только число❗')
            user_message_received = False
            user_message_received2 = True

        elif user_message_received2:
            get_persons = vk_ms.messages.getHistory(user_id=event.user_id, count=1)['items'][0]['text']
            print(get_persons)
            write_msg(event.user_id, '3⃣ Скажите, пожалуйста, соотношение мужчин и женщин в вашей группе?\n\n'
                                     '👫 Укажите в формате:\n\n❗Число мужчин / число женщин❗\n\n'
                                     ', например, 4 мужчин/2 женщин. Если персон какого-то пола не заезжает, '
                                     'укажите 0.')
            user_message_received2 = False
            user_message_received3 = True
        elif user_message_received3:
            get_gender = vk_ms.messages.getHistory(user_id=event.user_id, count=1)['items'][0]['text']
            print(get_gender)
            user_message_received3 = False
            while current_step != "exit":
                while while_blok != 1:
                    write_msg(event.user_id, 'Спасибо, я внимательно все записал. Проверьте, пожалуйста, '
                                             'правильность введенных данных:\n\n'
                              f'📆 Даты: {get_data}\n'
                              f'👔 Количество персон: {get_persons}\n'
                              f'👫 Мужчины и женщины: {get_gender}\n\n', keyboard)
                    while_blok += 1

                user_message_received_end = vk_ms.messages.getHistory(user_id=event.user_id, count=1)['items'][0][
                    'text']
                if user_message_received_end == 'Все верно':
                    current_step = "exit"
                elif user_message_received_end == 'Изменить даты':
                    current_step = "dates"
                elif user_message_received_end == 'Изменить число персон':
                    current_step = "persons"
                elif user_message_received_end == 'Изменить соотношение':
                    current_step = "gender"

                if current_step == "dates":
                    write_msg(event.user_id, 'Хорошо, введите верные даты, соблюдая данный формат:\n\n'
                                             '❗дд.мм.гг – дд.мм.гг❗')
                    from_id = event.user_id
                    for event in VkLongPoll(session).listen():
                        if event.type == VkEventType.MESSAGE_NEW:
                            if event.user_id == from_id:
                                get_data = vk_ms.messages.getHistory(user_id=event.user_id, count=1)['items'][0]['text']
                                print(get_data)
                                current_step = "confirm"
                                while_blok = 0
                                break

                elif current_step == "persons":
                    write_msg(event.user_id, 'Хорошо, отправьте число человек, которое должно заехать.')
                    from_id = event.user_id
                    for event in VkLongPoll(session).listen():
                        if event.type == VkEventType.MESSAGE_NEW:
                            if event.user_id == from_id:
                                get_persons = vk_ms.messages.getHistory(user_id=event.user_id, count=1)['items'][0][
                                    'text']
                                print(get_persons)
                                break
                    write_msg(event.user_id,
                              'Хорошо, введите верное соотношение, соблюдая данный формат и используя только '
                              'числа:\n\n'
                              '❗Число мужчин / число женщин❗')
                    for event in VkLongPoll(session).listen():
                        if event.type == VkEventType.MESSAGE_NEW:
                            if event.user_id == from_id:
                                get_gender = \
                                vk_ms.messages.getHistory(user_id=event.user_id, count=1)['items'][0]['text']
                                print(get_gender)
                                current_step = "confirm"
                                while_blok = 0
                                break

                elif current_step == "gender":
                    write_msg(event.user_id,
                              'Хорошо, введите верное соотношение, соблюдая данный формат и используя только '
                              'числа:\n\n'
                              '❗Число мужчин / число женщин❗')
                    from_id = event.user_id
                    for event in VkLongPoll(session).listen():
                        if event.type == VkEventType.MESSAGE_NEW:
                            if event.user_id == from_id:
                                get_gender = vk_ms.messages.getHistory(user_id=event.user_id, count=1)['items'][0][
                                    'text']
                                print(get_gender)
                                current_step = "confirm"
                                while_blok = 0
                                break
        elif message_text == 'все верно':
            current_step = "confirm"
            while_blok = 0
            write_msg(event.user_id,
                      'Прежде чем отправить заявку на проживание в нашем хостеле, мы хотели бы обратить ваше '
                      'внимание на важные правила, которые необходимо соблюдать во время вашего пребывания. \n\n'
                      '✅ Пожалуйста, ознакомьтесь с полным списком правил проживания и подтвердите свое согласие.')
            write_msg(event.user_id,
                      '🌎 ПРАВИЛА ВНУТРЕННЕГО РАСПОРЯДКА «КРИСТОФЕР ХОСТЕЛ» 🌎\n\n1⃣  Чистота и порядок\n'
                      '• Убирать и мыть за собой посуду и кухонные принадлежности;\n• Поддерживать порядок в '
                      'комнатах;\n• Не оставлять свои личные вещи в местах общего пользования;\n •Не хранить и не '
                      'употреблять продукты питания в комнатах.\n2⃣  Уважение\n• Соблюдать режим тишины с 24:00 до '
                      '07:00;\n• Использовать стиральную машину с 09:00 до 21:00.\n\n🚫 КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО 🚫\n'
                      '• Курение, употребление и распространение наркотических веществ, употребление алкоголя - '
                      'выселение;\n• Проявление агрессии и всех признаков насилия к окружающим;\n• Хранение взрывчатых '
                      'и легко воспламеняющихся веществ, оружия, наркотиков, ртути, химических и радиоактивных '
                      'веществ;\n• Приглашение на территорию хостела посторонних гостей, продажа своих услуг или '
                      'товаров.\n\n⏰ ПРАВИЛА ЗАЕЗДА И ВЫЕЗДА ⏰\n• Заезд возможен после 13:00, выезд в 12:00;\n• '
                      'Раннее заселение или поздний выезд возможны✅, при наличии свободных мест. Стоит учесть, что '
                      'услуга оплачивается отдельно за дополнительную плату;\n• В случае выезда раньше оплаченной '
                      'даты, администрация не возвращает денежные средства, внесенные за проживание;\n• Гость обязан '
                      'заранее предупредить о продлении брони. В случае неоплаты до 12:00, администрация вправе '
                      'заселить другого гостя.\n\nНам будет очень жаль, но ради душевного спокойствия наших гостей и '
                      'конечно персонала хостела, администрация оставляет за собой право на выселение любого '
                      'проживающего в случае нарушения общественного порядка и правил проживания, без возврата '
                      'денежных средств.',
                      keyboard2)
            user_get = vk_ms.users.get(user_ids=event.user_id)
            fullname = user_get[0]['first_name'] + ' ' + user_get[0]['last_name']
            print(fullname)

        elif message_text == 'прочитал и принимаю правила':
            write_msg(event.user_id,
                      'Я отправил эту информацию своим коллегам. '
                      'Она поможет им подобрать для вас самые комфортные условия проживания.')
            write_msg(event.user_id,
                      'Время ожидания ответа на заявку:\n\n'
                      '⏰ Варьируется от 2 до 15 минут в дневное время.\n\n'
                      'После, оператор подключится в чат, чтобы начать организацию вашей поездки.')

            message_1 = '<b>Новая заявка от бота</b>\n\n'
            message_1 += f'Имя: <b>{fullname}</b>\n'
            message_1 += f'Даты: <b>{get_data}</b>\n'
            message_1 += f'Человек: <b>{get_persons}</b>\n'
            message_1 += f'М/Ж: <b>{get_gender}</b>'

            print(message_1)
            if message_1 != 0:
                def send_telegram(text: str):
                    r = requests.post(method, data={
                        "chat_id": channel_id,
                        "parse_mode": 'html',
                        "text": message_1,
                        "reply_markup": keyboard_tg.to_json()
                    })

                    if r.status_code != 200:
                        raise Exception("post_text error")

                @bot.callback_query_handler(func=lambda callback: callback.data)
                def check_callback_data(callback):
                    if callback.data == 'yes':
                        write_msg(event.user_id,
                                  'На ваши даты есть места! Скоро оператор подключится в чат.')
                        bot.send_message(callback.message.chat.id, 'Принято, отправляю')
                    elif callback.data == 'no':
                        write_msg(event.user_id,
                                  'Благодарю вас за обращение к нам. К сожалению, я должен сообщить вам, что '
                                  'на даты, которые вы запрашивали, у нас нет свободных мест.\n\nЕсли вы готовы '
                                  'рассмотреть другие даты вашего визита, пожалуйста, сообщите мне об этом, повторно '
                                  'нажав «Начать» и оставив заявку снова, или попросите меня позвать оператора,'
                                  ' нажав «Пригласить оператора», чтобы обсудить с ним вопросы заселения, и мы с '
                                  'радостью поможем вам организовать проживание.\n\nС уважением,\nВаш персональный '
                                  'чат-бот',
                                  keyboard3)
                        bot.send_message(callback.message.chat.id, 'Принято, отказ')

                    elif callback.data == 'what':
                        write_msg(event.user_id,
                                  'Оператор нашел ошибку/несостыковку в заполненной Вами форме, он '
                                  'подключится в диалог ближайшее время чтобы уточнить детали, ожидайте.')
                        bot.send_message(callback.message.chat.id, 'Принято, объясняю долбоебу что он долбоеб')

                if __name__ == '__main__':
                    keyboard_tg = types.InlineKeyboardMarkup()
                    key_yes = types.InlineKeyboardButton(text='Да, места есть', callback_data='yes')
                    keyboard_tg.add(key_yes)
                    key_no = types.InlineKeyboardButton(text='Нет, мест нет', callback_data='no')
                    keyboard_tg.add(key_no)
                    key_what = types.InlineKeyboardButton(text='Неправильно заполнено', callback_data='what')
                    keyboard_tg.add(key_what)
                    send_telegram("hello world!")
                    bot_thread = threading.Thread(target=bot.polling)
                    bot_thread.start()
        elif message_text == 'позвать оператора':
            def send_telegram2(text: str):
                r = requests.post(method, data={
                    "chat_id": channel_id,
                    "parse_mode": 'html',
                    "text": f'Гость <b>{fullname}</b> просит подключиться в чат.',
                })

                if r.status_code != 200:
                    raise Exception("post_text error")

                write_msg(event.user_id, 'Направил Вашу просьбу коллегам, ожидайте.')

            if __name__ == '__main__':
                send_telegram2("hello world!")
