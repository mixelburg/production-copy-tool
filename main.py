import json
import os.path
from os import getenv

from dotenv import load_dotenv

load_dotenv()

DATA_FOLDER_PATH = getenv('DATA_FOLDER_PATH')
PEM_FILE_PATH = getenv('PEM_FILE_PATH')
FILTER_PATTERN = getenv('FILTER_PATTERN')

REMOTE_HOST = getenv('REMOTE_HOST')
REMOTE_PATH = getenv('REMOTE_PATH')

BASTION_HOST = getenv('BASTION_HOST')
BASTION_PEM_FILE_PATH = getenv('BASTION_PEM_FILE_PATH')

SSH_COMMAND = f'ssh -i {PEM_FILE_PATH} -J dev'

with open(os.path.join(DATA_FOLDER_PATH, 'db.json')) as f:
    db = json.load(f)
    users_to_copy = filter(lambda x: FILTER_PATTERN in x['email'], db['users'])
    for user in users_to_copy:
        print(f'Copying {user["email"]}')
        user_id = user['defaultAccount']

        user_db_file = os.path.join(DATA_FOLDER_PATH, 'db', 'accounts', user_id, 'db.json')

        path = os.path.join(REMOTE_PATH, 'db', 'accounts', user_id)
        command = f'rsync --update --progress -aP -e "{SSH_COMMAND}" --rsync-path="mkdir -p {path} && rsync" {user_db_file} {REMOTE_HOST}:{path}'
        print(command)
        os.system(command)

        user_storage_folder = os.path.join(DATA_FOLDER_PATH, 'storage', f'account-{user_id}')
        path = os.path.join(REMOTE_PATH, 'storage')
        command = f'rsync --update --progress -aP "{SSH_COMMAND}" --rsync-path="mkdir -p {path} && rsync" {user_storage_folder} {REMOTE_HOST}:{path}'
        os.system(command)










