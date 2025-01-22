from sett import TOKEN_TG

import asyncio
import time
import telebot


bot = telebot.TeleBot(TOKEN_TG)

if __name__ == '__main__':
    try:
        bot.polling()
    except (KeyboardInterrupt, SystemExit):
        time.sleep(5)
        pass
