from credential.telegram import key
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import json

def bot(filepath):
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=key)
    dp = Dispatcher(bot)

    content={
        'theme': ''
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
            with open(filepath, 'w', encoding='utf-8') as save:
                json.dump(content,save)
            theme = f'Seu tema é {theme}'
        except TypeError:
            theme = "Erro"
        print(theme)
        await message.reply(theme)
        

    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    bot('./theme.json')