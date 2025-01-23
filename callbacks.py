from sett import CHAT_ID
from msg import write_msg
from keyboards import *
from updates import *
from vksession import bot


async def callback_operations(idu, message_1):
    print(111)
    message_mistake = ""
    flags = {
        'userAct1': False,
        'flag': False,
        'flag2': False,
        'flag3': False,
        'flag4': False,
        'flag5': False,
        'user_message_received': False,
    }

    bot.send_message(chat_id=CHAT_ID,
                     text='<b>Новая заявка от бота</b>\n\n' + message_1,
                     parse_mode='html',
                     reply_markup=keyboard_tg)

    @bot.callback_query_handler(func=lambda callback: True)
    async def check_callback_data(callback):
        nonlocal message_mistake
        print("1111")
        if callback.data == 'yes':
            print("2222")
            await write_msg(idu,
                      '😸 На ваши даты есть места! Скоро оператор подключится в чат.')
            bot.send_message(callback.message.chat.id,
                             f'Принято, отправляю\n\n<a href="https://vk.com/gim226206756?sel'
                             f'={idu}">Подключиться в чат</a>', parse_mode='html')

        if callback.data == 'rooms':
            bot.send_message(callback.message.chat.id, 'Принято, прошу гостя поменять комнату')
            await mistake_user_room(idu)
            flags['flag'] = True
            if flags['flag']:
                await write_msg(idu, 'Спасибо за понимание! Буду рад помочь вам найти '
                               'подходящий вариант размещения. Отправил данные коллегам.')
                await update_user_message(idu)
                flags['flag'] = False

        if callback.data == 'what':
            bot.edit_message_text(chat_id=CHAT_ID,
                                  message_id=callback.message.message_id,
                                  text=message_1 + "\n\nВыбери пункт или пункты, в "
                                                   "\nкоторых есть ошибка",
                                  parse_mode='html',
                                  reply_markup=keyboard_tg1)
        if callback.data == '2':
            message_mistake += '❗даты'
            flags['flag2'] = True
            bot.send_message(callback.message.chat.id, '2 пункт')
        if callback.data == '3':
            message_mistake += '❗число человек'
            flags['flag3'] = True
            bot.send_message(callback.message.chat.id, '3 пункт')
        if callback.data == '4':
            message_mistake += '❗cоотношение человек'
            flags['flag4'] = True
            bot.send_message(callback.message.chat.id, '4 пункт')
        if callback.data == '5':
            message_mistake += '❗комнаты'
            flags['flag5'] = True
            bot.send_message(callback.message.chat.id, '5 пункт')
        if callback.data == 'allFail':
            await write_msg(idu,
                      f'Оператор нашел ошибку/несостыковку в заполненной Вами форме, '
                      f'он подключится в диалог ближайшее время чтобы уточнить детали,'
                      f' ожидайте ⏰')
            bot.send_message(callback.message.chat.id,
                             f'Принято, объясняю долбоебу что он совсем долбоеб\n\n'
                             f'<a href="https://vk.com/gim226206756?sel={idu}">Подключиться в '
                             f'чат</a>', parse_mode='html')

        if callback.data == 'ready':
            await write_msg(idu,
                      f'🙀 Оператор нашел ошибку/несостыковку в заполненной Вами форме, '
                      f'на следующих позициях: \n\n{message_mistake}❗\n\nпожалуйста, четко '
                      f'следуйте указаниям бота по заполнению формы.\n\nПросим Вас начать '
                      f'обращать особое внимание на информацию, которая заключена в ❗❗ и '
                      f'заполнить обозначенные пункты повторно ✏')
            bot.send_message(callback.message.chat.id,
                             'Принято, поминутно объясняю долбоебу, где он долбоеб')
            if flags['flag2']:
                await write_msg(idu, '📆 Пожалуйста, введите даты заезда и выезда, '
                               'соблюдая данный формат:\n\n❗дд.мм.гг – дд.мм.гг❗')
                await update_user_data(idu)
                flags['flag2'] = False
            if flags['flag3']:
                await write_msg(idu,
                          '👔 Введите число человек, которое должно заехать.\n\n❗Необходимо '
                          'отправить только цифру❗')
                await update_user_persons(idu)
                flags['flag3'] = False
            if flags['flag4']:
                await write_msg(idu,
                          '👫 Введите верное соотношение, соблюдая данный формат и используя '
                          'только числа:\n\n❗Число мужчин / число женщин❗')
                await update_user_gender(idu)
                flags['flag4'] = False
            if flags['flag5']:
                vk_ms.messages.send(peer_id=idu,
                                    message='🏡 Введите верную комнату (верные комнаты), в '
                                            'которой Вы бы предпочли проживать в нашем хостеле.'
                                            '\n\nУкажите в формате, ❗который указан в списке, '
                                            'без использования заглавных букв (Caps Lock)❗',
                                    random_id=random.randint(1, 1000000),
                                    attachment=attachment())
                await update_user_room(idu)
                flags['flag5'] = False
            if not (flags['flag2'] and flags['flag3'] and flags['flag4'] and flags['flag5']):
                await write_msg(idu,
                          'Отправил обновленную информацию своим коллегам, ожидайте ⏰')
                await update_user_message(idu)
                message_mistake = ""

        if callback.data == 'no':
            await write_msg(idu,
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
