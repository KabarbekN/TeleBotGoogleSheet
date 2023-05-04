import googleapiclient.discovery
import httplib2
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

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