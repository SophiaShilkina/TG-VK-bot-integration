from sett import TOKEN_VK, TOKEN_TG
import vk_api
import telebot


vk_session = vk_api.VkApi(token=TOKEN_VK)
vk_ms = vk_session.get_api()


bot = telebot.TeleBot(TOKEN_TG)
