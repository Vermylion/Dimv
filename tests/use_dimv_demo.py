import Dimv as dimv

CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

folder = 'https://drive.google.com/drive/folders/1e0GsZ6_RbG8su43MfiOx4pURIoOqEqaE'
id = '1mJ-jfHNbXjjhCWIzaIW3ZvRaXw9VohpT'

service = dimv.create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES, quiet = False)

dimv.find_files(folder, quiet = True)

dimv.find_file(id, folder, quiet = False)

output = 'test/test.txt'
dimv.download(id, output = 'test/test.txt', shared = True, quiet = False)

dimv.download_file(id, folder, output = 'test/test', quiet = False)

dimv.download_files(folder, output = 'test/test', shared = True, quiet = False)