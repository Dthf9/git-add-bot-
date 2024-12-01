from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import asyncio
import requests

TOKEN = '7704086214:AAHe9WUgkKp3Qs-SBr-ju_5XZiON0x_keHI'
bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer('Привет. Чтобы узнать погоду, напиши название города.')

@dp.message(Command('help'))
async def send_help(message: types.Message):
    await message.reply("Я могу выполнять следующие команды:/start — Приветствиеn, /help — Помощь")



@dp.message(F.text)
async def get_weather(message: types.Message):
    city = message.text
    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
        weather_data = requests.get(url).json()

        temperature = weather_data['main']['temp']
        temperature_feels = weather_data['main']['feels_like']
        wind_speed = weather_data['wind']['speed']
        cloud_cover = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']

        await message.answer(f'Температура воздуха: {temperature}°C\n'
                             f'Ощущается как: {temperature_feels}°C\n'
                             f'Ветер: {wind_speed} м/с\n'
                             f'Облачность: {cloud_cover}\n'
                             f'Влажность: {humidity}%')
    except KeyError:
        await message.answer(f'Не удалось узнать погоду')



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
