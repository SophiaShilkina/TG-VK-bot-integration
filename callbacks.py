from aiogram import F
from msg import write_msg, write_msg_with_photo
from botsinit import bot, dp
from updates import *

from aiogram import Router
from keyboards import *
from aiogram.types import CallbackQuery
import asyncio


async def main_bot():
    dp.include_router(router)
    await callback_operations()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


async def callback_operations():
    await send_message_to_user(f"<b>Новая заявка от бота</b>\n\n",
                               keyboard_tg)

router = Router()

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


@router.callback_query(F.data == 'yes')
async def yes(callback: CallbackQuery):
    await callback.message.answer(f'Принято, отправляю\n\n<a href="https://vk.com/gim226206756?sel'
                         f'=">Подключиться в чат</a>')


@router.callback_query(F.data == 'rooms')
async def rooms(callback: CallbackQuery, idu):
    await callback.message.answer('Принято, прошу гостя поменять комнату')
    await mistake_user_room(idu)
    flags['flag'] = True
    if flags['flag']:
        await write_msg(idu, 'Спасибо за понимание! Буду рад помочь вам найти '
                             'подходящий вариант размещения. Отправил данные коллегам.')
        await update_user_message(idu)
        flags['flag'] = False


@router.callback_query(F.data == 'what')
async def what(callback: CallbackQuery):
    await callback.message.answer(f"{message_1}\n\nВыбери пункт или пункты, в \nкоторых есть ошибка",
                                  keyboard_tg1)


@router.callback_query(F.data == '2')
async def mistake2(callback: CallbackQuery):
    message_mistake += '❗даты'
    flags['flag2'] = True
    await callback.message.answer('2 пункт')


@router.callback_query(F.data == '3')
async def mistake3(callback: CallbackQuery):
    message_mistake += '❗число человек'
    flags['flag3'] = True
    await callback.message.answer('3 пункт')


@router.callback_query(F.data == '4')
async def mistake4(callback: CallbackQuery):
    message_mistake += '❗cоотношение человек'
    flags['flag4'] = True
    await callback.message.answer('4 пункт')


@router.callback_query(F.data == '5')
async def mistake5(callback: CallbackQuery):
    message_mistake += '❗комнаты'
    flags['flag5'] = True
    await callback.message.answer('5 пункт')


@router.callback_query(F.data == 'allFail')
async def allFail(callback: CallbackQuery):
    await write_msg(idu, f'Оператор нашел ошибку/несостыковку в заполненной Вами форме, '
                    f'он подключится в диалог ближайшее время чтобы уточнить детали,'
                    f' ожидайте ⏰')
    await callback.message.answer(f'Принято, объясняю долбоебу что он совсем долбоеб\n\n'
                         f'<a href="https://vk.com/gim226206756?sel={idu}">Подключиться в '
                         f'чат</a>')


@router.callback_query(F.data == 'ready')
async def ready(callback: CallbackQuery):

    await write_msg(idu, f'🙀 Оператор нашел ошибку/несостыковку в заполненной Вами форме, '
                    f'на следующих позициях: \n\n{message_mistake}❗\n\nпожалуйста, четко '
                    f'следуйте указаниям бота по заполнению формы.\n\nПросим Вас начать '
                    f'обращать особое внимание на информацию, которая заключена в ❗❗ и '
                    f'заполнить обозначенные пункты повторно ✏')
    await callback.message.answer('Принято, поминутно объясняю долбоебу, где он долбоеб')
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
        await write_msg_with_photo(idu, '🏡 Введите верную комнату (верные комнаты), в '
                                    'которой Вы бы предпочли проживать в нашем хостеле.'
                                    '\n\nУкажите в формате, ❗который указан в списке, '
                                    'без использования заглавных букв (Caps Lock)❗')
        await update_user_room(idu)
        flags['flag5'] = False
    if not (flags['flag2'] and flags['flag3'] and flags['flag4'] and flags['flag5']):
        await write_msg(idu,
                  'Отправил обновленную информацию своим коллегам, ожидайте ⏰')
        await update_user_message(idu)
        message_mistake = ""


@router.callback_query(F.data == 'no')
async def no(callback: CallbackQuery):
    await write_msg(idu, 'Благодарю вас за обращение к нам. К сожалению, я должен сообщить'
                  ' вам, что на даты, которые вы запрашивали, у нас нет свободных мест ни '
                  'в одной комнате.\n\nЕсли вы готовы рассмотреть другие даты вашего '
                  'визита, пожалуйста, сообщите мне об этом, повторно нажав «Начать» и '
                  'оставив заявку снова, или попросите меня позвать оператора, нажав '
                  '«Пригласить оператора», чтобы обсудить с ним вопросы заселения, и мы с '
                  'радостью поможем вам организовать проживание.\n\nС уважением,\nВаш '
                  'персональный чат-бот',
                  keyboard3)
    await callback.message.answer('Принято, отказ')