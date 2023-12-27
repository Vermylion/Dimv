import os
import pickle

from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request

import gdown
from gdown.download_folder import download_and_parse_google_drive_link, parse_google_drive_file
from gdown.download_folder import download as gdown_download


def create_service(client_secret_file, api_name, api_version, *scopes, quiet = True):
    if not quiet:
        print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        if not quiet:
            print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        if not quiet:
            print('Unable to connect.')
            print(e)
        return None


def extract_files_from_gdrive(file_list, extract_gdrive):
    for file in extract_gdrive:
        file_list.append({'id': file.id, 'type': file.type, 'name': file.name})
        if file.children != []:
            extract_files_from_gdrive(file_list, file.children)

    return file_list


def download_loop(files_to_download, folder_output, shared = True, quiet = True):
    
    for file in files_to_download:
        if file.type == 'application/vnd.google-apps.folder':
            try:
                os.makedirs(folder_output + '\\' + file.name)
            except:
                pass
            if folder_output != '':
                folder_output += '\\'
            download_loop(file.children, folder_output + file.name, quiet = quiet)
        else:
            if not ':' in folder_output:
                dir_path = os.path.dirname(os.path.realpath(__file__))
                print(dir_path + '\\' + folder_output + '\\' + file.name)
                file_name = download(file.id, output = dir_path + '\\' + folder_output + '\\' + file.name, quiet = quiet)
            else:
                file_name = download(file.id, output = folder_output + '\\' + file.name, quiet = quiet)


def find_files(folder, quiet = True):
    return download_and_parse_google_drive_link(folder, quiet)


def find_file(id, folder, quiet = True):
    id_and_name, file_list = [], []

    return_code, gdrive_file = find_files(folder)
    file_list = extract_files_from_gdrive(file_list, gdrive_file.children)

    [(id_and_name.append(e['id']), id_and_name.append(e['name'])) for e in file_list]
    id_and_name = [id, id_and_name[id_and_name.index(id) + 1]]

    if not quiet:
        print(f'File id: {id_and_name[0]} is named {id_and_name[1]}')

    return id_and_name


def download(id, output, shared = True, quiet = True):    
    if shared:
        filename = gdown_download('https://drive.google.com/uc?id=' + id, output, quiet = quiet)


def download_file(id, folder, output = '', quiet = True):

    id_and_name = find_file(id, folder, quiet = quiet)

    if not output == '':
        try:
            os.makedirs(output)
        except:
            pass

    download(id, output + '/' + id_and_name[1], shared = True, quiet = quiet)

def download_files(folder, output = '', shared = True, quiet = True):
    return_code, gdrive_file = find_files(folder, quiet)

    if shared:
        download_loop(gdrive_file.children, folder_output = output, shared = shared, quiet = quiet)