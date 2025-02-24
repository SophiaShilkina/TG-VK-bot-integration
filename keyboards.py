from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# клавиатуры ВК

keyboard = {
    "one_time": True,
    "buttons": [
        [
            {
                "action": {
                    "type": "callback",
                    "label": "Все верно",
                    "payload": {
                        "command": "all_right"
                    }
                },
                "color": "positive"
            }
        ],
        [
            {
                "action": {
                    "type": "callback",
                    "label": "📆 Изменить даты",
                    "payload": {
                        "command": "dates_changed"
                    }
                },
                "color": "secondary"
            },
            {
                "action": {
                    "type": "callback",
                    "label": "👔 Изменить число персон",
                    "payload": {
                        "command": "persons_changed"
                    }
                },
                "color": "secondary"
            }
        ],
        [
            {
                "action": {
                    "type": "callback",
                    "label": "👫 Изменить соотношение",
                    "payload": {
                        "command": "genders_changed"
                    }
                },
                "color": "secondary"
            },
            {
                "action": {
                    "type": "callback",
                    "label": "🏡 Изменить комнаты",
                    "payload": {
                        "command": "rooms_changed"
                    }
                },
                "color": "secondary"
            }
        ]
    ]
}

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
