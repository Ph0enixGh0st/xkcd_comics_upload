import requests
import os
import random

from dotenv import load_dotenv
from pathlib import Path


def download_random_cartoon():

    cartoon_count_url = f'https://xkcd.com/info.0.json'
    cartoon_limit = requests.get(cartoon_count_url)
    cartoon_limit.raise_for_status()
    cartoon_limit = cartoon_limit.json()
    cartoon_random_number = random.randint(1, cartoon_limit['num'])

    cartoon_url = f'https://xkcd.com/{cartoon_random_number}/info.0.json'
    cartoon_pic = requests.get(cartoon_url)
    cartoon_pic.raise_for_status()
    cartoon_pic = cartoon_pic.json()
    cartoon_pic_comment = cartoon_pic['alt']

    cartoon_download_link = cartoon_pic['img']
    cartoon_download_link = requests.get(cartoon_download_link)
    cartoon_download_link.raise_for_status()

    with open('cartoon.png', 'wb') as file:
        file.write(cartoon_download_link.content)

    return cartoon_pic_comment


def upload_cartoon_to_vk_server(vk_version, vk_access_token, vk_group_id):

    server_upload_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'v': f"{vk_version}",
        'access_token': f'{vk_access_token}'
    }

    cartoon_upload_vk_url = requests.get(server_upload_url, params=payload)
    cartoon_upload_vk_url.raise_for_status()
    cartoon_upload_vk_url = cartoon_upload_vk_url.json()
    cartoon_upload_vk_url = cartoon_upload_vk_url['response']['upload_url']

    with open('cartoon.png', 'rb') as file:
        files = {
            'v': f"{vk_version}",
            'group_id ': f"{vk_group_id}",
            'photo': file,
        }
        cartoon_server_upload = requests.post(cartoon_upload_vk_url, files=files)
        cartoon_server_upload.raise_for_status()
        cartoon_server_upload = cartoon_server_upload.json()

        return cartoon_server_upload


def save_and_post_on_vk_wall(vk_access_token, cartoon_server_upload, vk_version, vk_group_id, vk_user_id, cartoon_pic_comment):

    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': f'{vk_access_token}',
        'hash': f"{cartoon_server_upload['hash']}",
        'v': f"{vk_version}",
        'photo':f"{cartoon_server_upload['photo']}",
        'group_id ': f"{vk_group_id}",
        'user_id': f"{vk_user_id}",
        'server': f"{cartoon_server_upload['server']}"
    }

    cartoon_server_save = requests.post(url, params=params)
    cartoon_server_save.raise_for_status()
    cartoon_server_save = cartoon_server_save.json()

    vk_wall_post_url = 'https://api.vk.com/method/wall.post'
    params = {
        'v': f"{vk_version}",
        'access_token': f'{vk_access_token}',
        'owner_id': f"{cartoon_server_save['response'][0]['owner_id']}",
        'from_group': '1',
        'message': f"{cartoon_pic_comment}",
        'attachments': f"photo{cartoon_server_save['response'][0]['owner_id']}_{cartoon_server_save['response'][0]['id']}",
    }

    vk_wall_post = requests.post(vk_wall_post_url, params=params)
    vk_wall_post.raise_for_status()

    os.remove('cartoon.png')


def main():

    load_dotenv()
    vk_access_token = os.environ['VK_ACCESS_TOKEN']
    vk_group_id = os.environ['VK_GROUP_ID']
    vk_user_id = os.environ['VK_USER_ID']
    vk_version = os.environ['VK_VERSION']

    cartoon_pic_comment = download_random_cartoon()
    cartoon_server_upload = upload_cartoon_to_vk_server(vk_version, vk_access_token, vk_group_id)

    save_and_post_on_vk_wall(vk_access_token, cartoon_server_upload, vk_version, vk_group_id, vk_user_id, cartoon_pic_comment)


if __name__ == '__main__':
    main()
