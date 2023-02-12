import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


def main():
    with open('key.txt', encoding='utf-8') as f:
        key_i = f.readline().rstrip()
        key_tg = f.readline().rstrip()

    openai.api_key = key_i
    bot = Bot(token=key_tg)
    dp = Dispatcher(bot)

    async def start_bot(_):
        print('Бот онлайн!')

    @dp.message_handler(commands=['start'])
    async def com_start(message: types.Message):
        await message.reply('Привет! Я бот сделанный на основе ИИ. Спроси у меня что хочешь и я постараюсь ответить.')


    @dp.message_handler()
    async def send(message: types.Message):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message.text,
            temperature=0.9,
            max_tokens=1000,

            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=["You:"]
        )
        await message.reply(response['choices'][0]['text'])

    executor.start_polling(dp, skip_updates=True,on_startup=start_bot)

    pass


if __name__ == '__main__':
    main()
