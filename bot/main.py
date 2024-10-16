import telebot
import requests
from telebot import types
from config import settings
from schema import WeatherInfo
from pydantic import ValidationError
from typing import Dict

bot = telebot.TeleBot(settings.BOT_TOKEN)
user_data: Dict[int, Dict[str, str]] = {}


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row('/setcity', '/weather')
    bot.send_message(message.chat.id,
                     'Привет! Хочешь узнать свежую информацию о МТУСИ?',
                     reply_markup=keyboard)
    user_id = message.from_user.id
    user_data[user_id] = {}
    bot.reply_to(message, "Привет! Я бот для просмотра прогноза погоды. Используй команду /setcity для выбора города.")


def save_city(message):
    user_id = message.from_user.id
    city = message.text.strip().lower().title()

    user_data[user_id]['city'] = city
    bot.reply_to(message, f"Город установлен: {city}")


@bot.message_handler(commands=['setcity'])
def set_city(message):
    user_id = message.from_user.id

    if user_id not in user_data:
        user_data[user_id] = {}

    msg = bot.reply_to(message, "Введите ваш город:")
    bot.register_next_step_handler(msg, save_city)


@bot.message_handler(commands=['weather'])
def get_weather(message):
    user_id = message.from_user.id
    city = user_data.get(user_id, {}).get('city')
    if not city:
        bot.reply_to(message, "Сначала установи свой город с помощью команды /setcity <город>.")
        return

    try:
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather",
            params={
                'q': city,
                'appid': settings.API_KEY,
                'units': 'metric',
                'lang': 'ru'
            }
        )
        response.raise_for_status()
        data = response.json()
        weather_info = WeatherInfo(**data)
        weather_message = (
            f"Погода в {city}:\n"
            f"{weather_info.weather[0].description[0].upper() + weather_info.weather[0].description[1:].lower()}\n"
            f"Температура: {weather_info.main.temp}°C\n"
            f"Ощущается как: {weather_info.main.feels_like}°C\n"
            f"Минимальная температура: {weather_info.main.temp_min}°C\n"
            f"Максимальная температура: {weather_info.main.temp_max}°C"
        )
        bot.reply_to(message, weather_message)

    except requests.HTTPError as http_err:
        if response.status_code == 404:
            bot.reply_to(message, f"Город '{city}' не найден. Пожалуйста, проверьте название.")
        else:
            bot.reply_to(message, "Произошла ошибка при получении данных о погоде.")
    except ValidationError as ve:
        bot.reply_to(message, "Ошибка при обработке данных о погоде.")



bot.polling()
