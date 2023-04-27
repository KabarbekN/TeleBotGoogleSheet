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
from download_send_file import download_file_from_google_sheet

CREDENTIALS_FILE = r"C:\Users\Nurgissa\PycharmProjects\TeleBotSheet\key_for_google_cloud\speedy-toolbox-384010-87d27fc12adc.json"  # Имя файла с закрытым ключом, вы должны подставить свое
spreadsheet_id = '1rZG1wfIw7oetjxISh-8Z7jrPT3KBvZJr-B8dExGU_uA'
GMAIL_ACCOUNT = 'nkabarbek@gmail.com'


credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])  # Пишем названия гугл апишек с которыми будем работать

httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
service = discovery.build('sheets', 'v4', http=httpAuth)  # Выбираем работу с таблицами и 4 версию API

# THIS PART OF CODE IS NEEDED TO OPEN ACCESS FOR VIEW AND EDITING DATA

driveService = googleapiclient.discovery.build('drive', 'v3',
                                               http=httpAuth)  # Выбираем работу с Google Drive и 3 версию API
BOT_TOKEN = '6045455125:AAHaNlRQOww3BHNe3rVms0BI9beuUiGD9d4'

bot = telebot.TeleBot(BOT_TOKEN)



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
            # result_style = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=[sheet_name],
            #                                           includeGridData=True).execute()
            # values_style = result_style['sheets'][0]['data'][0]['rowData']

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
            # batch_update_requests = {
            #     "requests": [
            #         {
            #             "updateCells": {
            #                 "rows":
            #                     [
            #                         values_style
            #                     ],
            #                 "start": {
            #                     "sheetId": 0
            #                 },
            #                 "fields": "userEnteredFormat"
            #             }
            #         },
            #         {
            #             'updateDimensionProperties': {
            #                 'range': {
            #                     'dimension': 'COLUMNS',
            #                     'startIndex': 1,
            #                     'endIndex': 2,  # update all columns
            #                     'sheetId': 0,
            #                 },
            #                 'properties': {
            #                     'pixelSize': 500,  # replace with the desired pixel size
            #                     'hiddenByUser': False,  # replace with the desired visibility setting
            #                 },
            #                 'fields': 'pixelSize,hiddenByUser'
            #             }
            #         }
            #     ]
            # }
            # try:
            #     request = service.spreadsheets().batchUpdate(spreadsheetId=city_spreadSheetId,
            #                                                  body=batch_update_requests)
            #     response = request.execute()
            # except googleapiclient.errors.HttpError as error:
            #     print(f'Произошла ошибка: {error}')
            document_name = "sells"
            download_file_from_google_sheet(city_spreadSheetId, title, chatId, document_name)
            print('https://docs.google.com/spreadsheets/d/' + city_spreadSheetId)
            driveService.files().delete(fileId=city_spreadSheetId).execute()
        else:
            print("Values data is null")
    else:
        bot.send_message(chatId, "Города с таким названием нету в базе данных")
