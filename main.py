# Подключаем библиотеки
import os
from datetime import datetime

import googleapiclient.discovery
import httplib2
import numpy as np
import telebot
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

telegram_support_acc = '@molodoi008'
GMAIL_ACCOUNT = 'nkabarbek@gmail.com'
BOT_TOKEN = '6045455125:AAHaNlRQOww3BHNe3rVms0BI9beuUiGD9d4'
CREDENTIALS_FILE = 'key_for_google_cloud/speedy-toolbox-384010-87d27fc12adc.json'  # Имя файла с закрытым ключом, вы должны подставить свое
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

def give_access_from_google_drive(city_spreadSheetId):
    try:
        access = driveService.permissions().create(
            fileId=city_spreadSheetId,
            body={'type': 'user', 'role': 'writer', 'emailAddress': GMAIL_ACCOUNT},
            # Открываем доступ на редактирование нужно заменить почту gmail на вашу
            fields='id',
            sendNotificationEmail=False
        ).execute()
    except googleapiclient.errors.HttpError as error:
        print(f'Произошла ошибка: {error}')
    # TAKING CITY NAME AS AN INPUT AND CREATING NEW SPREADSHEET

def download_file_from_google_sheet(spreadsheetId, city_name, chatId, document_name):
    # Set the format you want to export the file to
    EXPORT_MIMETYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    # Set the path where you want to save the exported file
    EXPORT_PATH = r"C:\Users\Nurgissa\PycharmProjects\TeleBotSheet\downloads"
    EXPORT_PATH = EXPORT_PATH + f'\{document_name}' + ".xlsx"
    # Save the file to a specific directory
    file_content = driveService.files().export(fileId=spreadsheetId, mimeType=EXPORT_MIMETYPE).execute()
    with open(EXPORT_PATH, 'wb') as f:
        f.write(file_content)

    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d_%H-%M")

    # specify the full path of the old file and the new file name
    standard_file_path_name = r'C:\Users\Nurgissa\PycharmProjects\TeleBotSheet\downloads'
    standard_file_path_name = standard_file_path_name + f'\{document_name}' + ".xlsx"

    standard_file_path = r'C:\Users\Nurgissa\PycharmProjects\TeleBotSheet\downloads'

    dynamic_file_name = f"\{city_name}_{document_name}_{formatted_time}.xlsx"
    new_file_path_name = standard_file_path + dynamic_file_name

    try:
        os.rename(standard_file_path_name, new_file_path_name)
        print("File renamed successfully.")
    except OSError as error:
        print(error)

    document_path = new_file_path_name
    document = open(document_path, 'rb')
    bot.send_document(chatId, document)
    document.close()
    print(document_path)

    try:
        os.rename(new_file_path_name, standard_file_path_name)
        print("File renamed successfully.")
    except OSError as error:
        print(error)

def reading_from_remains_sheet(city_name, chatId):
    sheet_name = "Ост"
    row_count = 0
    top_values = []
    city_values = []
    column_count = 0
    city_number = 0

    result_values = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=sheet_name).execute()
    values_data = result_values['values']

    for row in values_data:
        if row_count < 5:
            row_count += 1
            top_values.append(row)
        else:
            row_count += 1
            if row[0] == city_name:
                city_values.append(row)
                city_number += 1
                column_count = len(row)
    if len(city_values) > 0:
        title = f"{city_name}_Список_Остатков"
        spreadsheet = service.spreadsheets().create(body={
            'properties': {'title': city_name, 'locale': 'ru_RU'},
            'sheets': [{
                'properties': {
                    'sheetType': 'GRID',
                    'sheetId': 0,
                    'title': title,
                    'gridProperties': {'rowCount': 5 + city_number + 1, 'columnCount': column_count}
                }
            }]
        }).execute()
        city_spreadSheetId = spreadsheet['spreadsheetId']

        #
        #
        #
        give_access_from_google_drive(city_spreadSheetId)
        #
        #
        #

        city_range = f"{title}!A6:M{city_number + 6}"
        top_range = f"{title}!A1:M5"

        if values_data:
            city_body = {
                'values': city_values
            }
            top_body = {
                'values': top_values
            }
            try:
                result = service.spreadsheets().values().update(
                    spreadsheetId=city_spreadSheetId,
                    range=city_range,
                    valueInputOption='USER_ENTERED',
                    body=city_body
                ).execute()
            except googleapiclient.errors.HttpError as error:
                print(f'Произошла ошибка: {error}')

            try:
                result_top = service.spreadsheets().values().update(
                    spreadsheetId=city_spreadSheetId,
                    range=top_range,
                    valueInputOption='USER_ENTERED',
                    body=top_body
                ).execute()
            except googleapiclient.errors.HttpError as error:
                print(f'Произошла ошибка: {error}')

            batch_update_requests = {
                "requests": [
                    {
                        'updateDimensionProperties': {
                            'range': {
                                'dimension': 'COLUMNS',
                                'startIndex': 1,
                                'endIndex': 2,  # update all columns
                                'sheetId': 0,
                            },
                            'properties': {
                                'pixelSize': 500,  # replace with the desired pixel size
                                'hiddenByUser': False,  # replace with the desired visibility setting
                            },
                            'fields': 'pixelSize,hiddenByUser'
                        }
                    }
                ]
            }

            try:
                request = service.spreadsheets().batchUpdate(spreadsheetId=city_spreadSheetId,
                                                             body=batch_update_requests)
                response = request.execute()
            except googleapiclient.errors.HttpError as error:
                print(f'Произошла ошибка: {error}')

            document_name = "remains"
            download_file_from_google_sheet(city_spreadSheetId, title, chatId, document_name)

            print('https://docs.google.com/spreadsheets/d/' + city_spreadSheetId)
            try:
                driveService.files().delete(fileId=city_spreadSheetId).execute()
            except googleapiclient.errors.HttpError as error:
                print(f'Произошла ошибка: {error}')
        else:
            print("Values data is null")
    else:
        bot.send_message(chatId, "Города с таким названием нету в базе данных")


def reading_from_sells_sheet(city_name, month_number, chatId):
    sheet_name = "Пж"
    row_count = 0
    top_values = []
    city_values = []
    column_count = 0

    result_values = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=sheet_name).execute()
    values_data = result_values['values']

    for row in values_data:
        if row_count < 7:
            row_count += 1
            if row_count != 6:
                top_values.append(row)
        else:
            row_count += 1
            if row[0] == city_name:
                city_values.append(row)
                column_count = len(row)
    if len(city_values) > 0:
        if 0 < month_number < 13:
            columns_to_delete = []
            for i in range(4, column_count):
                if month_number * 5 - 2 < i < month_number * 5 + 4:
                    pass
                else:
                    columns_to_delete.append(i)

            for i in top_values:
                while len(i) != 89:
                    i.append('')

            # Create a 2D array
            values_of_top = np.array(top_values)
            values_of_city = np.array(city_values)

            # Delete columns 1 and 2
            top_values = np.delete(values_of_top, columns_to_delete, axis=1)
            city_values = np.delete(values_of_city, columns_to_delete, axis=1)

            city_values = city_values.tolist()
            top_values = top_values.tolist()

        title = ''
        city_spreadSheetId = ''

        try:
            result_style = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=[sheet_name],
                                                      includeGridData=True).execute()
            values_style = result_style['sheets'][0]['data'][0]['rowData']

            title = f"{city_name}_Список_Продаж"
            spreadsheet = service.spreadsheets().create(body={
                'properties': {'title': city_name, 'locale': 'ru_RU'},
                'sheets': [{
                    'properties': {
                        'sheetType': 'GRID',
                        'sheetId': 0,
                        'title': title,
                        'gridProperties': {'rowCount': row_count + 1000, 'columnCount': column_count + 1000}
                    }
                }]
            }).execute()
            city_spreadSheetId = spreadsheet['spreadsheetId']
        except googleapiclient.errors.HttpError as error:
            print(f'Произошла ошибка: {error}')

        #
        #
        give_access_from_google_drive(city_spreadSheetId)
        #
        #

        city_range = f"{title}!A8:CK{row_count + 8}"
        top_range = f"{title}!A1:CK78"

        if 0 < month_number < 13:
            city_range = f"{title}!A8:CK{row_count}"
            top_range = f"{title}!A1:CK7"

        if values_data:
            body = {
                'values': city_values
            }
            top_body = {
                'values': top_values
            }

            try:
                result = service.spreadsheets().values().update(
                    spreadsheetId=city_spreadSheetId,
                    range=city_range,
                    valueInputOption='USER_ENTERED',
                    body=body
                ).execute()
            except googleapiclient.errors.HttpError as error:
                print(f'Произошла ошибка: {error}')
            try:
                result_top = service.spreadsheets().values().update(
                    spreadsheetId=city_spreadSheetId,
                    range=top_range,
                    valueInputOption='USER_ENTERED',
                    body=top_body
                ).execute()
            except googleapiclient.errors.HttpError as error:
                print(f'Произошла ошибка: {error}')
            batch_update_requests = {
                "requests": [
                    {
                        "updateCells": {
                            "rows":
                                [
                                    values_style
                                ],
                            "start": {
                                "sheetId": 0
                            },
                            "fields": "userEnteredFormat"
                        }
                    },
                    {
                        'updateDimensionProperties': {
                            'range': {
                                'dimension': 'COLUMNS',
                                'startIndex': 1,
                                'endIndex': 2,  # update all columns
                                'sheetId': 0,
                            },
                            'properties': {
                                'pixelSize': 500,  # replace with the desired pixel size
                                'hiddenByUser': False,  # replace with the desired visibility setting
                            },
                            'fields': 'pixelSize,hiddenByUser'
                        }
                    }
                ]
            }
            try:
                request = service.spreadsheets().batchUpdate(spreadsheetId=city_spreadSheetId,
                                                             body=batch_update_requests)
                response = request.execute()
            except googleapiclient.errors.HttpError as error:
                print(f'Произошла ошибка: {error}')
            document_name = "sells"
            download_file_from_google_sheet(city_spreadSheetId, title, chatId, document_name)
            print('https://docs.google.com/spreadsheets/d/' + city_spreadSheetId)
            driveService.files().delete(fileId=city_spreadSheetId).execute()
        else:
            print("Values data is null")
    else:
        bot.send_message(chatId, "Города с таким названием нету в базе данных")

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

def authorization(telegram_id):
    city_name = ""
    sheet_name = "Права"
    values = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=sheet_name).execute()
    values_data = values['values']

    for row in values_data:
        if str(row[0]) == str(telegram_id):
            city_name = row[1]
    return city_name

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
