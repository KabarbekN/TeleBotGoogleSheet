# # Подключаем библиотеки
#
# import googleapiclient.discovery
# import httplib2
# import telebot
# from googleapiclient import discovery
# from oauth2client.service_account import ServiceAccountCredentials
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#
# from authorization import authorization
# from read_remains_google import reading_from_remains_sheet
# from read_sales_google import reading_from_sells_sheet
# from telebot.async_telebot import AsyncTeleBot
# from telebot import types
# from telebot.types import Message
# from telebot.async_telebot import AsyncTeleBot
# from telebot import asyncio_filters
# from telebot.asyncio_storage import StateMemoryStorage
#
# # new feature for states.
# from telebot.asyncio_handler_backends import State, StatesGroup
#
# # default state storage is statememorystorage
#
#
# # from authorization import *
#
# telegram_support_acc = '@molodoi008'
# GMAIL_ACCOUNT = 'nkabarbek@gmail.com'
# BOT_TOKEN = '6045455125:AAHaNlRQOww3BHNe3rVms0BI9beuUiGD9d4'
# CREDENTIALS_FILE = r"C:\Users\Nurgissa\PycharmProjects\TeleBotSheet\key_for_google_cloud\speedy-toolbox-384010-87d27fc12adc.json"  # Имя файла с закрытым ключом, вы должны подставить свое
# spreadsheet_id = '1rZG1wfIw7oetjxISh-8Z7jrPT3KBvZJr-B8dExGU_uA'
#
# sheets_name_and_id = {696285621: "Пж",
#                       116876809: "Ост",
#                       1336947730: "Права"}  # dictionary with id of sheets
#
# bot = AsyncTeleBot(BOT_TOKEN, state_storage=StateMemoryStorage())
#
#
# class SellsStates(StatesGroup):
#     city = State()  # statesgroup should contain states
#     month = State()
#
#
# class RemainsStates(StatesGroup):
#     city = State()  #
#
#
# # Читаем ключи из файла
# credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
#                                                                ['https://www.googleapis.com/auth/spreadsheets',
#                                                                 'https://www.googleapis.com/auth/drive'])  # Пишем названия гугл апишек с которыми будем работать
#
# httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
# service = discovery.build('sheets', 'v4', http=httpAuth)  # Выбираем работу с таблицами и 4 версию API
#
# # THIS PART OF CODE IS NEEDED TO OPEN ACCESS FOR VIEW AND EDITING DATA
#
# driveService = googleapiclient.discovery.build('drive', 'v3',
#                                                http=httpAuth)  # Выбираем работу с Google Drive и 3 версию API
#
#
# # access = driveService.permissions().create(
# #     fileId = spreadsheet_id,
# #     body = {'type': 'user', 'role': 'writer', 'emailAddress': GMAIL_ACCOUNT},  # Открываем доступ на редактирование нужно заменить почту gmail на вашу
# #     fields = 'id',
# #     sendNotificationEmail=False
# # ).execute()
# # THIS PART OF CODE IS NEEDED TO OPEN ACCESS FOR VIEW AND EDITING DATA
#
#
#
#
# keyboard_sell_remain = InlineKeyboardMarkup()
# sells_button = InlineKeyboardButton('Продажи', callback_data='sell_button')
# remains_button = InlineKeyboardButton('Остатки', callback_data='remains_button')
# keyboard_sell_remain.add(sells_button, remains_button)
#
#
# @bot.message_handler(commands=['start', 'get'], content_types=['text'])
# async def send_hello_message(message):
#     username = message.from_user.username
#     print(username)
#     await bot.reply_to(message, "Добро пожаловать в бот", reply_markup=keyboard_sell_remain)
#
#
# # @bot.message_handler()
# # async def get_month_number(message):
# #     await bot.send_message(message.chat.id, "Такой команды нету, попробуйте еще раз /get")
# @bot.callback_query_handler(func=lambda call: True)
# async def handle_button_press(call):
#     if call.data == 'sell_button':
#         await bot.edit_message_reply_markup(call.message.chat.id,
#                                             call.message.message_id,
#                                             reply_markup=None)
#
#         city_user_name = authorization(call.message.chat.id)
#         if len(city_user_name[0]) == 0:
#             await bot.send_message(call.message.chat.id,
#                                    f"К сожалению, у вас нету доступа к данным свяжитесь с {telegram_support_acc}")
#         elif city_user_name[0] == 'Альфа':
#             await bot.send_message(call.message.chat.id, f"Добро пожаловать, {city_user_name[1]}")
#             await bot.send_message(call.message.chat.id,
#                                    "Введите название города,"
#                                    "по которому хотите получить данные")
#
#
#
#             bot.register_next_step_handler(call.message, get_city_name_from_sells)
#
#
#
#
#
#         else:
#             print("first check")
#             await bot.send_message(call.message.chat.id, f"Добро пожаловать, {city_user_name[1]}")
#             await bot.set_state(call.message.from_user.id, SellsStates.month, call.message.chat.id)
#             await bot.send_message(call.message.chat.id,
#                                    "Введите номер месяца, по которому вы хотите получить данные или же 0 если хотите получить все данные")
#
#             print("check")
#
#             # @bot.message_handler()
#             # async def get_month_number(message):
#             #     month_number = str(message.text)
#             #     if month_number.isdigit():
#             #         month_number = int(month_number)
#             #         if month_number == 0 or 1 <= month_number <= 12:
#             #             await bot.send_message(call.message.chat.id, "Ваш запрос обрабатывается, пожалуйста подождите")
#             #             await reading_from_sells_sheet(city_user_name[0], month_number, call.message.chat.id)
#             #         else:
#             #             await bot.send_message(message.chat.id, f"{month_number} месяца не существует")
#             #             await bot.send_message(message.chat.id, "Для возобновления работы нажмите /get ")
#             #     else:
#             #         await bot.send_message(message.chat.id, f"{message.text} не является месяцом")
#             #         await bot.send_message(message.chat.id, "Для возобновления работы нажмите /get ")
#
#     elif call.data == 'remains_button':
#         await bot.edit_message_reply_markup(call.message.chat.id,
#                                             call.message.message_id,
#                                             reply_markup=None)
#
#         city_user_name = authorization(call.message.chat.id)
#         if len(city_user_name[0]) == 0:
#             await bot.send_message(call.message.chat.id,
#                                    f"К сожалению, у вас нету доступа к данным свяжитесь с {telegram_support_acc}")
#             await bot.send_message(call.chat.id, "Для возобновления работы нажмите /get ")
#
#         elif city_user_name[0] == 'Альфа':
#             await bot.send_message(call.message.chat.id, f"Добро пожаловать, {city_user_name[1]}")
#             await bot.send_message(call.message.chat.id,
#                                    "Введите название города,"
#                                    "по которому хотите получить данные")
#
#             bot.register_next_step_handler(call.message, get_city_name_from_remains)
#
#
#
#
#
#
#         else:
#             await bot.send_message(call.message.chat.id, f"Добро пожаловать, {city_user_name[1]}")
#             await bot.send_message(call.message.chat.id, "Ваш запрос обрабатывается, пожалуйста подождите")
#             await reading_from_remains_sheet(city_user_name[0], call.message.chat.id)
#
# @bot.message_handler(state=SellsStates.month)
# async def month_get_sells_city_user(message):
#     print("fgdff")
#     await bot.send_message(message.chat.id, "Your month is ")
#     async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         data['month'] = message.text
#     await bot.send_message(message.chat.id, data['month'])
#
#
#
# async def get_city_name_from_remains(message):
#     city_name = str(message.text)
#     city_name = city_name.title()
#     if len(city_name) > 0:
#         await bot.send_message(message.chat.id, "Ваш запрос обрабатывается, пожалуйста подождите")
#         await reading_from_remains_sheet(city_name, message.chat.id)
#     else:
#         await bot.send_message(message.chat.id, f"Города {city_name} не существует")
#         await bot.send_message(message.chat.id, "Для возобновления работы нажмите /get ")
#
#
# async def get_city_name_from_sells(message):
#     city_name = str(message.text)
#     city_name = city_name.title()
#     if len(city_name) > 0:
#         print("checker oone")
#         await bot.send_message(message.chat.id,
#                                "Введите номер месяца, по которому вы хотите получить данные или же 0 если хотите получить все данные")
#
#         bot.register_next_step_handler(message, get_admin_month_of_city_from_sells, city_name)
#
#
#
#
#
#     else:
#         await bot.send_message(message.chat.id, f"Города {city_name} не существует")
#         await bot.send_message(message.chat.id, "Для возобновления работы нажмите /get ")
#
#
# async def get_admin_month_of_city_from_sells(message, city_name):
#     month_check = str(message.text)
#     if month_check.isdigit():
#         month_number = int(message.text)
#         if month_number == 0 or 1 <= month_number <= 12:
#             await bot.send_message(message.chat.id, "Ваш запрос обрабатывается, пожалуйста подождите")
#             await reading_from_sells_sheet(city_name, month_number, message.chat.id)
#         else:
#             await bot.send_message(message.chat.id, f"{month_number} месяца не существует")
#             await bot.send_message(message.chat.id, "Для возобновления работы нажмите /get ")
#     else:
#         await bot.send_message(message.chat.id, f"{message.text} не является месяцом")
#         await bot.send_message(message.chat.id, "Для возобновления работы нажмите /get ")
#
#
# @bot.message_handler()
# async def not_supported_command(message):
#     await bot.send_message(message.chat.id, "Данной команды не существует")
#     await bot.send_message(message.chat.id, "Для возобновления работы нажмите /get ")
#
#
# import asyncio
#
# asyncio.run(bot.polling(none_stop=True))
