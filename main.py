# Подключаем библиотеки
import os
import random
import time
from datetime import datetime

import googleapiclient.discovery
import httplib2
import numpy as np
import telebot
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from access_file_in_google_sheet import give_access_from_google_drive
from authorization import authorization
from download_send_file import download_file_from_google_sheet
from read_remains_google import reading_from_remains_sheet
from read_sales_google import reading_from_sells_sheet

# from authorization import *

telegram_support_acc = '@molodoi008'
GMAIL_ACCOUNT = 'nkabarbek@gmail.com'
BOT_TOKEN = '6045455125:AAHaNlRQOww3BHNe3rVms0BI9beuUiGD9d4'
CREDENTIALS_FILE = r"C:\Users\Nurgissa\PycharmProjects\TeleBotSheet\key_for_google_cloud\speedy-toolbox-384010-87d27fc12adc.json"  # Имя файла с закрытым ключом, вы должны подставить свое
spreadsheet_id = '1rZG1wfIw7oetjxISh-8Z7jrPT3KBvZJr-B8dExGU_uA'

sheets_name_and_id = {696285621: "Пж",
                      116876809: "Ост",
                      1336947730: "Права"}  # dictionary with id of sheets

bot = telebot.TeleBot(BOT_TOKEN)

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])  # Пишем названия гугл апишек с которыми будем работать

httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
service = discovery.build('sheets', 'v4', http=httpAuth)  # Выбираем работу с таблицами и 4 версию API

# THIS PART OF CODE IS NEEDED TO OPEN ACCESS FOR VIEW AND EDITING DATA

driveService = googleapiclient.discovery.build('drive', 'v3',
                                               http=httpAuth)  # Выбираем работу с Google Drive и 3 версию API


# access = driveService.permissions().create(
#     fileId = spreadsheet_id,
#     body = {'type': 'user', 'role': 'writer', 'emailAddress': GMAIL_ACCOUNT},  # Открываем доступ на редактирование нужно заменить почту gmail на вашу
#     fields = 'id',
#     sendNotificationEmail=False
# ).execute()
# THIS PART OF CODE IS NEEDED TO OPEN ACCESS FOR VIEW AND EDITING DATA

def start():
    print("Please, choose a sells or remains 1/2? ")
    choice = int(input())
    if choice == 1:
        reading_from_sells_sheet()
    elif choice == 2:
        reading_from_remains_sheet()
    else:
        print("There no such variants, please choose correct one from 1 or 2")
        start()

keyboard_sell_remain = InlineKeyboardMarkup()
sells_button = InlineKeyboardButton('Продажи', callback_data='sell_button')
remains_button = InlineKeyboardButton('Остатки', callback_data='remains_button')
keyboard_sell_remain.add(sells_button, remains_button)

@bot.message_handler(commands=['start', 'get'])
def send_hello_message(message):
    username = message.from_user.username
    print(username)
    bot.reply_to(message, "Добро пожаловать в бот", reply_markup=keyboard_sell_remain)


@bot.callback_query_handler(func=lambda call: True)
def handle_button_press(call):
    if call.data == 'sell_button':
        bot.edit_message_reply_markup(call.message.chat.id,
                                      call.message.message_id,
                                      reply_markup=None)

        city_name = authorization(call.message.chat.id)
        if len(city_name) == 0:
            bot.send_message(call.message.chat.id,
                             f"К сожалению, у вас нету доступа к данным свяжитесь с {telegram_support_acc}")
        elif city_name == 'Альфа':
            bot.send_message(call.message.chat.id,
                             "Введите название города,"
                             "по которому хотите получить данные")
            bot.register_next_step_handler(call.message, get_city_name_from_sells)
        else:
            bot.send_message(call.message.chat.id, "Введите номер месяца, по которому вы хотите получить данные или же 0 если хотите получить все данные")

            @bot.message_handler()
            def get_month_number(message):
                month_number = str(message.text)
                if month_number.isdigit():
                    month_number = int(month_number)
                    if month_number == 0 or 1 <= month_number <= 12:
                        bot.send_message(call.message.chat.id, "Ваш запрос обрабатывается, пожалуйста подождите")
                        reading_from_sells_sheet(city_name, month_number, call.message.chat.id)
                    else:
                        bot.send_message(message.chat.id, f"{month_number} месяца не существует")
                        bot.send_message(message.chat.id, "Для возобновления работы нажмите /get ")
                else:
                    bot.send_message(message.chat.id, f"{message.text} не является месяцом")
                    bot.send_message(message.chat.id, "Для возобновления работы нажмите /get ")
    elif call.data == 'remains_button':
        bot.edit_message_reply_markup(call.message.chat.id,
                                      call.message.message_id,
                                      reply_markup=None)

        city_name = authorization(call.message.chat.id)
        if len(city_name) == 0:
            bot.send_message(call.message.chat.id,
                             f"К сожалению, у вас нету доступа к данным свяжитесь с {telegram_support_acc}")
            bot.send_message(call.chat.id, "Для возобновления работы нажмите /get ")

        elif city_name == 'Альфа':
            bot.send_message(call.message.chat.id,
                             "Введите название города,"
                             "по которому хотите получить данные")
            bot.register_next_step_handler(call.message, get_city_name_from_remains)
        else:
            bot.send_message(call.message.chat.id, "Ваш запрос обрабатывается, пожалуйста подождите")
            reading_from_remains_sheet(city_name, call.message.chat.id)


def get_city_name_from_remains(message):
    city_name = str(message.text)
    city_name = city_name.title()
    if len(city_name) > 0:
        bot.send_message(message.chat.id, "Ваш запрос обрабатывается, пожалуйста подождите")
        reading_from_remains_sheet(city_name, message.chat.id)
    else:
        bot.send_message(message.chat.id, f"Города {city_name} не существует")
        bot.send_message(message.chat.id, "Для возобновления работы нажмите /get ")



def get_city_name_from_sells(message):
    city_name = str(message.text)
    city_name = city_name.title()
    if len(city_name) > 0:
        bot.send_message(message.chat.id,
                         "Введите номер месяца, по которому вы хотите получить данные или же 0 если хотите получить все данные")
        bot.register_next_step_handler(message, get_admin_month_of_city_from_sells, city_name)
    else:
        bot.send_message(message.chat.id, f"Города {city_name} не существует")
        bot.send_message(message.chat.id, "Для возобновления работы нажмите /get ")


def get_admin_month_of_city_from_sells(message, city_name):
    month_check = str(message.text)
    if month_check.isdigit():
        month_number = int(message.text)
        if month_number == 0 or 1 <= month_number <= 12:
            bot.send_message(message.chat.id, "Ваш запрос обрабатывается, пожалуйста подождите")
            reading_from_sells_sheet(city_name, month_number, message.chat.id)
        else:
            bot.send_message(message.chat.id, f"{month_number} месяца не существует")
            bot.send_message(message.chat.id, "Для возобновления работы нажмите /get ")
    else:
        bot.send_message(message.chat.id, f"{message.text} не является месяцом")
        bot.send_message(message.chat.id, "Для возобновления работы нажмите /get ")


bot.polling(none_stop=True)
