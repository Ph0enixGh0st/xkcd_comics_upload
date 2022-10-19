import requests
import os
import random

from dotenv import load_dotenv
from pathlib import Path


def download_random_comics():

    comics_count_url = f'https://xkcd.com/info.0.json'
    comics_limit = requests.get(comics_count_url)
    comics_limit.raise_for_status()
    comics_limit = comics_limit.json()
    comics_random_number = random.randint(1, comics_limit['num'])

    comics_url = f'https://xkcd.com/{comics_random_number}/info.0.json'
    comics_pic = requests.get(comics_url)
    comics_pic.raise_for_status()
    comics_pic = comics_pic.json()
    comics_pic_comment = comics_pic['alt']

    comics_download_link = comics_pic['img']
    comics_download_link = requests.get(comics_download_link)
    comics_download_link.raise_for_status()

    with open('comics.png', 'wb') as file:
        file.write(comics_download_link.content)

    return comics_pic_comment


def upload_comics_to_vk_server(vk_version, vk_access_token, vk_group_id):

    server_upload_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'v': f"{vk_version}",
        'access_token': f'{vk_access_token}'
    }

    comics_upload_vk_url = requests.get(server_upload_url, params=payload)
    comics_upload_vk_url.raise_for_status()
    comics_upload_vk_url = comics_upload_vk_url.json()
    comics_upload_vk_url = comics_upload_vk_url['response']['upload_url']

    with open('comics.png', 'rb') as file:
        files = {
            'v': f"{vk_version}",
            'group_id ': f"{vk_group_id}",
            'photo': file,
        }
        comics_server_upload = requests.post(comics_upload_vk_url, files=files)
        comics_server_upload.raise_for_status()
        comics_server_upload = comics_server_upload.json()

        return comics_server_upload


def save_and_post_on_vk_wall(vk_access_token, comics_server_upload, vk_version, vk_group_id, vk_user_id, comics_pic_comment):

    with open('comics.png', 'rb') as file:
        url = 'https://api.vk.com/method/photos.saveWallPhoto'
        params = {
        'access_token': f'{vk_access_token}',
        'hash': f"{comics_server_upload['hash']}",
        'v': f"{vk_version}",
        'photo':f"{comics_server_upload['photo']}",
        'group_id ': f"{vk_group_id}",
        'user_id': f"{vk_user_id}",
        'server': f"{comics_server_upload['server']}"
        }

        comics_server_save = requests.post(url, params=params)
        comics_server_save.raise_for_status()
        comics_server_save = comics_server_save.json()

    vk_wall_post_url = 'https://api.vk.com/method/wall.post'
    params = {
    'v': f"{vk_version}",
    'access_token': f'{vk_access_token}',
    'owner_id': f"{comics_server_save['response'][0]['owner_id']}",
    'from_group': '1',
    'message': f"{comics_pic_comment}",
    'attachments': f"photo{comics_server_save['response'][0]['owner_id']}_{comics_server_save['response'][0]['id']}",
    }

    vk_wall_post = requests.post(vk_wall_post_url, params=params)
    vk_wall_post.raise_for_status()

    os.remove('comics.png')


def main():

    load_dotenv()
    vk_access_token = os.environ['VK_ACCESS_TOKEN']
    vk_group_id = os.environ['VK_GROUP_ID']
    vk_user_id = os.environ['VK_USER_ID']
    vk_version = os.environ['VK_VERSION']

    comics_pic_comment = download_random_comics()
    comics_server_upload = upload_comics_to_vk_server(vk_version, vk_access_token, vk_group_id)

    save_and_post_on_vk_wall(vk_access_token, comics_server_upload, vk_version, vk_group_id, vk_user_id, comics_pic_comment)


if __name__ == '__main__':
    main()
