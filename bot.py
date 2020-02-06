from credential.telegram import key as telegramKey
from credential.mongoDb import key as mongoDbKey
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from pymongo import MongoClient
import json
import logging
import datetime

def bot():

    client = MongoClient(mongoDbKey)
    mydb = client['videmaker']
    db = mydb['themes']

    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=telegramKey)
    dp = Dispatcher(bot)

    content={
        'theme': '',
        'date': '',
        'ready': 0
    }

    @dp.message_handler(commands=['help'])
    async def sendHelp(message: types.Message):
        await message.reply('Me envie um tema para um video')
        await message.reply('Exemplo: Tema god of war')

    @dp.message_handler(Text(contains='Tema', ignore_case=True), state='*')
    async def getTheme(message: types.Message):
        try:
            removeTheme = message.text.split()[1:]
            theme = ' '.join(removeTheme)
            content['theme'] = theme
            content['date'] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            db.update_one({'_id': theme}, {'$set': content}, upsert=True)
            theme = f'Seu tema é {theme}'
        except TypeError:
            theme = "Erro"
        print(theme)
        await message.reply(theme)
        

    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    bot()