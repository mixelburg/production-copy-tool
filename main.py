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
CHUNK_SIZE = 2


def copy_files(src, dst):
    os.system(f'rsync --progress -aP -e "{SSH_COMMAND}" --rsync-path="mkdir -p {dst} && rsync" {src} {REMOTE_HOST}:{dst}')


def process_user(user):
    user_id = user['defaultAccount']
    print(f'Sending job {user["email"]}')
    copy_files(
        os.path.join(DATA_FOLDER_PATH, 'db', 'accounts', user_id, 'db.json'),
        os.path.join(REMOTE_PATH, 'db', 'accounts', user_id)
    )
    copy_files(
        os.path.join(REMOTE_PATH, 'db', 'accounts', user_id),
        os.path.join(REMOTE_PATH, 'storage')
    )


with open(os.path.join(DATA_FOLDER_PATH, 'db.json')) as f:
    db = json.load(f)
    users_to_copy = filter(lambda x: FILTER_PATTERN in x['email'], db['users'])

    with ThreadPoolExecutor(max_workers=CHUNK_SIZE) as exe:
        exe.map(process_user, users_to_copy)
