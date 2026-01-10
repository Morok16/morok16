from ipaddress import collapse_addresses
from pyexpat.errors import messages

# class Shapae(ABC):
#     def __init__(self,x , y):
#         self.x = x
#         self.y = y
#     @abstractmethod
#     def area (self):
#         pass
#     def show_info(self):
#         print(f"координаты {self.x},{self.y},площадь:{self.area}")
# class Rectongle(Shape):
#     def __init__(self, x, y, width,height):
#         super().__init__(x, y)
#         self.width = width
#         self.height = height
#     def area(self):
#         print(self.width * self.height)
# class Circle(Shape):
#     def __init__(self,R,x,y):
#         super().__init__(x,y)
#         self.R = R
#     def area(self):
#         print(3.14 * (self.R ** 2))
#
# r = Rectongle(20 ,10 , 45 ,76)
# c = Circle( 34 ,343,34)
# print(r)
# print(c)
# from abc import ABC , abstractmethod
# class MusicalInstrument(ABC):
#     def __init__(self, title):
#         self.title = title
#     @abstractmethod
#     def play (self):
#         pass
# class Piano(MusicalInstrument):
#     def __init__(self,title,keys):
#         super().__init__(title)
#         self.keys = keys
#     def play(self):
#         print(f"Играет мелодия:{self.title}")
# class Guitar(MusicalInstrument):
#     def __init__(self,strings,title):
#         self.strings = strings
#         super().__init__(title)
#     def play(self):
#         print(f"играют акорды:{self.title}")
# p = Piano( 23 , 43)
# g = Guitar(3 , 24)
# print(p)
# print(g)
# from abc import ABC , abstractmethod
# class Hero(ABC):
#     def __init__(self,name ,hp ,damage):
#         self.hp = hp
#         self.name = name
#         self.damage = damage
#     @abstractmethod
#     def attack (self):
#         pass
#     def get_status(self):
#         print(f"name{self.name}/hp{self.hp}/damage{self.damage}/hp{100}")
# class Fighter(Hero):
#     def __init__(self,strength,name,hp,damage):
#         self.strength = strength
#         super().__init__(name,hp,damage)
#     def attack(self):
#         print(f"{self.hp - (self.strength * self.attack)})")
# class Healer(Hero):
#     def __init__(self,name,hp,damage,heal_power):
#         super().__init__(hp,damage,name)
#         self.heal_power  = heal_power
#     def attack(self):
#         print(f"{self.hp - (self.damage * 0.8)}")
#     def heal(self):
#         print(f"{self.heal_power * 10}")
# class Defendor(Hero):
#     def __init__(self,damage,name,hp,armor):
#         super().__init__(name,hp,damage)
#         self.armor = armor
#     def hp (self):
#         print(f"(self.armor * 0.01) * amount")
#     def attack(self):
#         print(f"{self.hp - self.damage}")
# class Mage(Hero):
#     def __init__(self,magic_power,hp,damage,name):
#         super().__init__(hp,damage,name)
#         self.magic_power = magic_power
#     def attack (self):
#         print(f"{self.hp - (self.damage * self.magic_power)}")
#     def curse(self):
#         print(f"{self.damage - (self.magic_power * 2)}")
#     f = Fighter(23 ,"хомяк",100,50)
#     f.get_status()
import os
import sys
import re
import json
import logging
import requests
import gdown
import numpy as np
from random import randint
from datetime import datetime
from flask import Flask, request
from PIL import Image, ImageOps
import telebot
from tensorflow.keras.models import load_model
import tensorflow as tf
from telebot import util

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    sys.exit("Ошибка: Переменная API_TOKEN  не задана в переменных окружения")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
data = {"users":{}}

if not os.path.exists('data.json') or os.path.getsize("data.json") == 0 :
    with open("data.json","w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False , indent=4)
else:
    with open("data.json","r",encoding="utf-8")as f:
        data = json.load(f)
@app.route("/")
def index():
    return"Bot is running!"
@app.route("/{API_TOKEN}",methods=["POST"])
def wedhook():
    try:
        json_str = request.get_data(as_text=True)
        update = telebot.types.Ubdate.de_json(json_str)
        if update:
            bot.process_new_updates([update])
    except Exception as e:
        app.logger.exception("Webhook error: %s", e)
    return'',200



@bot.message_handler(commands = ['start'])
def start(message):
    user_id = message.chat.id
    if str(user_id) not in data ["users"]:
        data["users"][str(user_id)] = {}
        bot.send_message(message.chat.id,"Привет как тебя завут?")
        data['users'][str(user_id)]['awaiting'] = "name"
        return
    elif data['users'][str(user_id)]["awaiting"] == "age":
        bot.send_message(message.chat.id,"Сколько тебе лет ?")
        data["users"][str(user_id)]['awaiting'] = "age"
        return
    elif data["users"][str(user_id)]["awaiting"] == "city":
        bot.send_message(message.chat.id,"Из какого ты города?")
        data["users"][str(user_id)]['awaiting'] = "city"
        return
    elif data["users"][str(user_id)]['awaiting'] == "vehical":
        bot.send_message(message.chat.id,"На какой машине ты ездишь?")
        data["users"][str(user_id)['awaiting']] = "vehical"


    keybord = telebot.types.ReplyKeyboardMarkup(resize_keyboard= True)
    dice_button = telebot.types.KeyboardButton("игра в кубик")
    slot_button = telebot.types.KeyboardButton("игровая рулетка")
    country_button = telebot.types.KeyboardButton("Игра в страны")

    keybord.add(dice_button, slot_button, country_button)

    bot.send_message(message.chat.id,f"Привет {data['users'][str(user_id)]['name']}!",reply_markup= keybord)
    bot.send_message(message.chat.id,"Привет",reply_markup=keybord)

@bot.message_handler(commands= ['arbieten'])
def arbieten(message):
    bot.send_message(message.chat.id,"Sie mussen in der Rhine Metal-Fabrick arbeiten(ты обязан работать на заводе райн метал ")
    print(message.text)
@bot.message_handler(commands= ['gehalt'])
def salary(message):
    bot.send_message(message.chat.id,"Sie erhalten ainhundertfunfundzwanzig Reichmark(ты будешь получать стодвадцатьпять райхсмарок ")
    print(message.text)
@bot.message_handler(commands= ['bundeswehr'])
def army(message):
    bot.send_message(message.chat.id,"Sie mussen ihren Wehrdienst in der Bundeswehr ableisten(Ты должен отслужить в армии бундесвера)")
    print(message.text)
@bot.message_handler(commands= ['familia'])
def family(message):
    bot.send_message(message.chat.id,"Du musst eine Familie haben(ты должен иметь семью)")
    print(message.text)
@bot.message_handler(commands=['Adolf_Aloisovich'])
def adi(message):
    bot.send_message(message.chat.id,"MAN MUSS ADOLF ALOISOVICH(вы доожны любить алоисовича)")
    print(message.text)

@bot.message_handler(content_types=['text'])
def answer(message):
    user_id = message.chat.id
    if data["users"][str(user_id)]["awaiting"] == "name":
        data["users"][str(user_id)]['name'] = message.text
        data["users"][str(user_id)]['awaiting'] = "age"
        bot.send_message(message.chat.id,f"Приятно познакомиться ,{data['users'][str(user_id)]['name']}")
        start(message)
        json.dump(data,open("data.json","w",encoding = "utf-8"),ensure_ascii=False, indent = 4)
        return
    elif data["users"][str(user_id)]["awaiting"] == "age":
        data["users"][str(user_id)]['age'] = message.text
        data["users"][str(user_id)]['awaiting'] = "city"
        start(message)
        json.dump(data,open("data.json","w",encoding = "utf-8"),ensure_ascii=False, indent = 4)
        return
    elif data["users"][str(user_id)]["awaiting"] == "city":
        data["users"][str(user_id)]['city'] = message.text
        data["users"][str(user_id)]['awaiting'] = "vehical"
        start(message)
        json.dump(data,open("data.json","w",encoding = "utf-8"),ensure_ascii=False, indent = 4)
        return
    elif data["users"][str(user_id)]["awaiting"] == "vehical":
        data["users"][str(user_id)]['vehical'] = message.text
        data["users"][str(user_id)]['awaiting'] = None
    if message.text =='Привет':
        bot.send_message(message.chat.id,'HEIL')
    elif message.text == "Как дела?":
        bot.send_message(message.chat.id,'Sehr gut')
    elif message.text == "игра в кубик":
        dice(message)
    elif message.text == 'игровая рулетка':
        slot(message)
    elif message.text == "Как тебя завут?":
        bot.send_message(message.chat.id,'Ich bin ein Man')
    elif message.text =="Какая твоя национальность":
        bot.send_message(message.chat.id,'du bist mussen bin arien')
    elif message.text =="Игра в страны":
        start_country_game(message)

    else:
        bot.send_message(message.chat.id,"Verpiss dich")
    print (message.text)


def dice(message):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
    btn1 = telebot.types.InlineKeyboardButton("1",callback_data="1")
    btn2 = telebot.types.InlineKeyboardButton("2",callback_data="2")
    btn3 = telebot.types.InlineKeyboardButton("3",callback_data="3")
    btn4 = telebot.types.InlineKeyboardButton("4",callback_data="4")
    btn5 = telebot.types.InlineKeyboardButton("5",callback_data="5")
    btn6 = telebot.types.InlineKeyboardButton("6",callback_data="6")
    keyboard.add(btn1,btn6,btn4,btn3,btn2,btn5)
    bot.send_message(message.chat.id,"Угадай число на кубике",reply_markup=keyboard)
@bot.callback_query_handler(func = lambda call: call.data in ('1','2','3','4','5','6'))
def throwDice(call):
    value = bot.send_dice(call.message.chat.id,emoji="").dice.value
    if str(value) == call.data:
        bot.send_message(call.message.chat.id,"Ты угадал")
    else:
        bot.send_message(call.message.chat.id,"Попробуй еще раз")
def slot(message):
    value = bot.send_dice(message.chat.id,emoji='🎰').dice.value
    if value in (1, 22, 43):
        bot.send_message(message.chat.id,"Sieg(победа)")
    elif value in (16, 32, 48):
        bot.send_message(message.chat.id,"sieg!(победа)")
    elif value == 64:
        bot.send_message(message.chat.id,"Jackpot!")
    else:
        bot.send_message(message.chat.id,"Депни еще разок ")


















if __name__ == '__main__':
    server_url = os.getenv("RENDER_EXTREMAL_URL")
    if server_url and API_TOKEN:
        webhook_url = f"{server_url.rstrip('/')}/{API_TOKEN}"
        try:
            r = requests.get(f"https://api.telegram.org/bot{API_TOKEN}/setWebhook",
                             params={"url": webhook_url},timeout=10)
            logging.info("Webhook установлен: %s",r.text)
        except Exception as e:
            logging.exception(f"Ошибка при установке webhook:{e}")
        port = int(os.getenv("PORT",10000))
        logging.info("Starting server on port %s",port)
        app.run(host="0.0.0.0",port=port)
    else:
        logging.info("запуск бота в режиме pooling")
        bot.remove_webhook()
        bot.infinity_polling(timeout=60)





