import os
from datetime import datetime

import googleapiclient.discovery
import httplib2
import telebot
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from telebot.async_telebot import AsyncTeleBot
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

bot = AsyncTeleBot(BOT_TOKEN)


async def download_file_from_google_sheet(spreadsheetId, city_name, chatId, document_name):
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
    await bot.send_document(chatId, document)
    document.close()
    await bot.send_message(chatId, "Для продолжения работы нажмите /get ")

    print(document_path)

    # try:
    #     os.rename(new_file_path_name, standard_file_path_name)
    #     print("File renamed successfully.")
    # except OSError as error:
    #     print(error)

    try:
        os.remove(new_file_path_name)
        print(f"File '{new_file_path_name}' has been deleted successfully!")
    except OSError as error:
        print(f"Error deleting file '{new_file_path_name}': {error}")
