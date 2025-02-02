from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
keyboard_tg = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да, места есть', callback_data='yes')],
    [InlineKeyboardButton(text='Нет мест в указанной комнате', callback_data='rooms')],
    [InlineKeyboardButton(text='Неправильно заполнено »', callback_data='what')],
    [InlineKeyboardButton(text='Нет, мест нет', callback_data='no')]
])

keyboard_tg1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='2 пункт', callback_data='2'),
     InlineKeyboardButton(text='3 пункт', callback_data='3')],
    [InlineKeyboardButton(text='4 пункт', callback_data='4'),
     InlineKeyboardButton(text='5 пункт', callback_data='5')],
    [InlineKeyboardButton(text='Готово', callback_data='ready')],
    [InlineKeyboardButton(text='Неверно 2-5 пункты', callback_data='allFail')]
])
