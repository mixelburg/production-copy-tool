import json
import os.path
from os import getenv

from dotenv import load_dotenv

load_dotenv()

DATA_FOLDER_PATH = getenv('DATA_FOLDER_PATH')
PEM_FILE_PATH = getenv('PEM_FILE_PATH')
FILTER_PATTERN = getenv('FILTER_PATTERN')
REMOTE_PATH = getenv('REMOTE_PATH')

BASTION_HOST = getenv('BASTION_HOST')
BASTION_PEM_FILE_PATH = getenv('BASTION_PEM_FILE_PATH')

SSH_COMMAND = f'ssh -i {PEM_FILE_PATH} -o ProxyCommand="ssh -i {BASTION_PEM_FILE_PATH} -W %h:%p"'

with open(os.path.join(DATA_FOLDER_PATH, 'db.json')) as f:
    db = json.load(f)
    users_to_copy = filter(lambda x: FILTER_PATTERN in x['email'], db['users'])
    for user in users_to_copy:
        print(f'Copying {user["email"]}')
        user_id = user['defaultAccount']

        user_db_folder = os.path.join(DATA_FOLDER_PATH, 'db', 'accounts', user_id)
        user_db_file = os.path.join(user_db_folder, 'db.json')
        command = f'rsync -aP "{SSH_COMMAND}" --rsync-path="mkdir -p {user_db_folder} && rsync" {user_db_file} {REMOTE_PATH}'
        print(command)
        os.system(command)

        # user_storage_folder = os.path.join(DATA_FOLDER_PATH, 'storage', f'account-{user_id}')
        # command = f'rsync -aP "{SSH_COMMAND}" --rsync-path="mkdir -p {user_storage_folder} && rsync" {user_db_file} {REMOTE_PATH}'
        # os.system(command)










