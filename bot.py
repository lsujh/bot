# -*- coding: utf-8 -*-

import requests
import telebot
from datetime import datetime

from config import token

bot = telebot.TeleBot(token)
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f14f45730dee91a89c48c0b485ff20b1&lang=uk'

@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    content = {word.lower() for word in message.text.split()}
    good = {'добре', 'ок', 'класно'}
    bad = {'погано', 'так собі'}
    if 'привіт' in content:
        bot.send_message(message.from_user.id, f'Привіт {message.from_user.first_name.capitalize()}. Як справи?')

    elif 'погода' in content:
        city = message.text.split()[1]
        res = requests.get(url.format(city)).json()
        if res['cod'] == 200:
            msg = f"<b>Погода в м. <i>{city.capitalize()}</i> на {datetime.today().date()} </b> \n \
                                           {res['weather'][0]['description']}\n \
                                           тиск - {res['main']['pressure']}\n \
                                           вологість - {res['main']['humidity']} %\n \
                                           мінімальна температура - {res['main']['temp_min']} \u2103 \n \
                                           максимальна температура - {res['main']['temp_max']} \u2103 \n \
                                           швидкість вітру - {res['wind']['speed']} м\с\n \
                                           хмарність - {res['clouds']['all']} %"
            bot.send_message(message.from_user.id, msg, parse_mode='HTML')
        else:
            bot.send_message(message.from_user.id, f'Вибач сталася помилка. {res["message"]} "{city.capitalize()}"')
    elif "/help" in content:
        bot.send_message(message.from_user.id, "Напиши Привіт")
    elif 'пока' in content:
        bot.send_message(message.from_user.id, 'Прощай')
    elif content & good:
        bot.send_message(message.from_user.id, 'Радий за тебе.')
        bot.send_message(message.from_user.id, 'Поговоримо про погоду. \nНапиши <погода назва міста>')
    elif content & bad:
        bot.send_message(message.from_user.id, 'Співчуваю.')
        bot.send_message(message.from_user.id, 'Поговоримо про погоду. \nНапиши <погода назва міста>')
    else:
        bot.send_message(message.from_user.id, "Я тебе не розумію. Напиши /help.")


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)


