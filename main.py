import json
import os.path
from os import getenv

from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

DATA_FOLDER_PATH = getenv('DATA_FOLDER_PATH')
PEM_FILE_PATH = getenv('PEM_FILE_PATH')
FILTER_PATTERN = getenv('FILTER_PATTERN')

REMOTE_HOST = getenv('REMOTE_HOST')
REMOTE_PATH = getenv('REMOTE_PATH')

BASTION_HOST = getenv('BASTION_HOST')
BASTION_PEM_FILE_PATH = getenv('BASTION_PEM_FILE_PATH')

SSH_COMMAND = f'ssh -i {PEM_FILE_PATH} -J dev'
CHUNK_SIZE = 20

def copy_files(src, dst):
    command = f'rsync --progress -aP -e "{SSH_COMMAND}" --rsync-path="mkdir -p {dst} && rsync" {src} {REMOTE_HOST}:{dst}'
    os.system(command)


with open(os.path.join(DATA_FOLDER_PATH, 'db.json')) as f:
    db = json.load(f)
    users_to_copy = list(filter(lambda x: FILTER_PATTERN in x['email'], db['users']))

    cnt = 0

    for user in users_to_copy:
        print(f'Copying {user["email"]}')
        print(f'Progress: {cnt}/{len(users_to_copy)}')

        user_id = user['defaultAccount']
        copy_files(
            os.path.join(DATA_FOLDER_PATH, 'db', 'accounts', user_id, 'db.json'),
            os.path.join(REMOTE_PATH, 'db', 'accounts', user_id)
        )
        copy_files(
            os.path.join(DATA_FOLDER_PATH, 'storage', f'account-{user_id}'),
            os.path.join(REMOTE_PATH, 'storage')
        )

        print(f'\n[+] Copying {user["email"]} done\n')
        cnt += 1
