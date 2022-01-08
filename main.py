from os import getenv

from vkbottle import Bot

import message_handler

bot = Bot(getenv("TOKEN"))
bot.set_blueprints(message_handler.bp)
bot.run_polling()
