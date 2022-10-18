import requests
import os
import random

from dotenv import load_dotenv
from pathlib import Path


def fetch_random_issue():

    comics_count_url = f'https://xkcd.com/info.0.json'
    comics_limit = requests.get(comics_count_url)
    comics_limit.raise_for_status()
    comics_limit = comics_limit.json()
    comics_random_number = random.randint(1, comics_limit['num'])

    return comics_random_number


def fetch_vk_server_link(comics_random_number, access_token, version):

    comics_url = f'https://xkcd.com/{comics_random_number}/info.0.json'
    comics_pic = requests.get(comics_url)
    comics_pic.raise_for_status()
    comics_pic = comics_pic.json()
    comics_pic_comment = comics_pic['alt']

    comics_download_link = comics_pic['img']
    comics_download = requests.get(comics_download_link)
    comics_download.raise_for_status()

    with open('comics.png', 'wb') as file:
        file.write(comics_download.content)

    server_upload_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'v': f"{version}",
        'access_token': f'{access_token}'
    }

    comics_upload = requests.get(server_upload_url, params=payload)
    comics_upload.raise_for_status()
    comics_upload = comics_upload.json()
    comics_upload_url = comics_upload['response']['upload_url']

    return comics_upload_url, comics_pic_comment


def make_wall_post(comics_upload_url, access_token, comics_pic_comment, group_id, user_id, version):

    with open('comics.png', 'rb') as file:
        files = {
            'v': f"{version}",
            'group_id ': f"{group_id}",
            'photo': file,
        }
        comics_server_upload = requests.post(comics_upload_url, files=files)
        comics_server_upload.raise_for_status()
        comics_server_upload = comics_server_upload.json()

    with open('comics.png', 'rb') as file:
        url = 'https://api.vk.com/method/photos.saveWallPhoto'
        params = {
        'access_token': f'{access_token}',
        'hash': f"{comics_server_upload['hash']}",
        'v': f"{version}",
        'photo':f"{comics_server_upload['photo']}",
        'group_id ': f"{group_id}",
        'user_id': f"{user_id}",
        'server': f"{comics_server_upload['server']}"
        }

        comics_server_save = requests.post(url, params=params)
        comics_server_save.raise_for_status()
        comics_server_save = comics_server_save.json()

    wall_post_url = 'https://api.vk.com/method/wall.post'
    params = {
    'v': f"{version}",
    'access_token': f'{access_token}',
    'owner_id': f"{comics_server_save['response'][0]['owner_id']}",
    'from_group': '1',
    'message': f"{comics_pic_comment}",
    'attachments': f"photo{comics_server_save['response'][0]['owner_id']}_{comics_server_save['response'][0]['id']}",
    }

    wall_post = requests.post(wall_post_url, params=params)
    wall_post.raise_for_status()

    os.remove('comics.png')


def main():

    load_dotenv()
    access_token = os.environ['ACCESS_TOKEN']
    group_id = os.environ['GROUP_ID']
    user_id = os.environ['USER_ID']
    version = os.environ['VERSION']

    comics_random_number = fetch_random_issue()
    comics_upload_url, comics_pic_comment = fetch_vk_server_link(comics_random_number, access_token, version)
    make_wall_post(comics_upload_url, access_token, comics_pic_comment, group_id, user_id, version)


if __name__ == '__main__':
    main()
