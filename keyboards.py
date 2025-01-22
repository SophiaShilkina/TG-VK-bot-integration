from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from telebot import types

# клавиатуры ВК

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Все верно', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('📆 Изменить даты', color=VkKeyboardColor.SECONDARY)
keyboard.add_button('👔 Изменить число персон', color=VkKeyboardColor.SECONDARY)
keyboard.add_line()
keyboard.add_button('👫 Изменить соотношение', color=VkKeyboardColor.SECONDARY)
keyboard.add_button('🏡 Изменить комнаты', color=VkKeyboardColor.SECONDARY)

keyboard2 = VkKeyboard(one_time=True)
keyboard2.add_button('Прочитал(а) и принимаю правила', color=VkKeyboardColor.POSITIVE)

keyboard3 = VkKeyboard(one_time=True)
keyboard3.add_button('Начать', color=VkKeyboardColor.POSITIVE)
keyboard3.add_button('Позвать оператора', color=VkKeyboardColor.SECONDARY)

keyboard4 = VkKeyboard(one_time=True)
keyboard4.add_button('Заполнить повторно ✏', color=VkKeyboardColor.POSITIVE)

keyboard5 = VkKeyboard(one_time=True)
keyboard5.add_button('Начать', color=VkKeyboardColor.POSITIVE)

# клавиатуры ТГ

keyboard_tg = types.InlineKeyboardMarkup()
key_yes = types.InlineKeyboardButton(text='Да, места есть', callback_data='yes')
keyboard_tg.add(key_yes)
key_rooms = types.InlineKeyboardButton(text='Нет мест в указанной комнате', callback_data='rooms')
keyboard_tg.add(key_rooms)
key_what = types.InlineKeyboardButton(text='Неправильно заполнено »', callback_data='what')
keyboard_tg.add(key_what)
key_no = types.InlineKeyboardButton(text='Нет, мест нет', callback_data='no')
keyboard_tg.add(key_no)

keyboard_tg1 = types.InlineKeyboardMarkup()
key_2 = types.InlineKeyboardButton(text='2 пункт', callback_data='2')
key_3 = types.InlineKeyboardButton(text='3 пункт', callback_data='3')
keyboard_tg1.add(key_2, key_3)
key_4 = types.InlineKeyboardButton(text='4 пункт', callback_data='4')
key_5 = types.InlineKeyboardButton(text='5 пункт', callback_data='5')
keyboard_tg1.add(key_4, key_5)
key_ready = types.InlineKeyboardButton(text='Готово', callback_data='ready')
keyboard_tg1.add(key_ready)
key_allFail = types.InlineKeyboardButton(text='Неверно 2-5 пункты', callback_data='allFail')
keyboard_tg1.add(key_allFail)