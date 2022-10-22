import requests
import os
import random

from dotenv import load_dotenv
from pathlib import Path


def download_random_comic():

    comic_count_url = f'https://xkcd.com/info.0.json'
    comic_limit = requests.get(comic_count_url)
    comic_limit.raise_for_status()
    comic_limit = comic_limit.json()
    comic_random_number = random.randint(1, comic_limit['num'])

    comic_url = f'https://xkcd.com/{comic_random_number}/info.0.json'
    comic_pic = requests.get(comic_url)
    comic_pic.raise_for_status()
    comic_pic = comic_pic.json()
    comic_pic_comment = comic_pic['alt']

    comic_download_link = comic_pic['img']
    comic_download_link = requests.get(comic_download_link)
    comic_download_link.raise_for_status()

    with open('comic.png', 'wb') as file:
        file.write(comic_download_link.content)

    return comic_pic_comment


def upload_comic_to_vk_server(vk_version, vk_access_token, vk_group_id):

    vk_server_upload_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'v': f"{vk_version}",
        'access_token': f'{vk_access_token}'
    }

    comic_upload_vk_url = requests.get(vk_server_upload_url, params=payload)
    comic_upload_vk_url.raise_for_status()
    comic_upload_vk_url = comic_upload_vk_url.json()
    comic_upload_vk_url = comic_upload_vk_url['response']['upload_url']

    with open('comic.png', 'rb') as file:
        files = {
            'v': f"{vk_version}",
            'group_id ': f"{vk_group_id}",
            'photo': file,
        }
        comic_vk_server_upload = requests.post(comic_upload_vk_url, files=files)

    comic_vk_server_upload.raise_for_status()
    comic_vk_server_upload = comic_vk_server_upload.json()

    vk_hash = comic_vk_server_upload['hash']
    vk_photo_id = comic_vk_server_upload['photo']
    vk_server_number = comic_vk_server_upload['server']

    return vk_hash, vk_photo_id, vk_server_number


def save_comic_to_vk_server(vk_access_token, vk_hash, vk_photo_id, vk_server_number, vk_version, vk_group_id, vk_user_id):

    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'v': f"{vk_version}",
        'access_token': f'{vk_access_token}',
        'hash': vk_hash,
        'photo': vk_photo_id,
        'group_id ': f"{vk_group_id}",
        'user_id': f"{vk_user_id}",
        'server': vk_server_number
    }

    comic_vk_server_save = requests.post(url, params=params)
    comic_vk_server_save.raise_for_status()
    comic_vk_server_save = comic_vk_server_save.json()

    vk_group_owner_id = comic_vk_server_save['response'][0]['owner_id']
    vk_save_id = comic_vk_server_save['response'][0]['id']

    return vk_group_owner_id, vk_save_id


def post_comic_to_vk_wall(vk_version, vk_access_token, vk_group_owner_id, vk_save_id, comic_pic_comment):

    vk_wall_post_url = 'https://api.vk.com/method/wall.post'
    params = {
        'v': f"{vk_version}",
        'access_token': f'{vk_access_token}',
        'owner_id': vk_group_owner_id,
        'from_group': '1',
        'message': f"{comic_pic_comment}",
        'attachments': f"photo{vk_group_owner_id}_{vk_save_id}",
    }

    vk_wall_post = requests.post(vk_wall_post_url, params=params)
    vk_wall_post.raise_for_status()


def main():

    try: 
        load_dotenv()
        vk_access_token = os.environ['VK_ACCESS_TOKEN']
        vk_group_id = os.environ['VK_GROUP_ID']
        vk_user_id = os.environ['VK_USER_ID']
        vk_version = os.environ['VK_VERSION']

        comic_pic_comment = download_random_comic()
        vk_hash, vk_photo_id, vk_server_number = upload_comic_to_vk_server(vk_version, vk_access_token, vk_group_id)
        vk_group_owner_id, vk_save_id = save_comic_to_vk_server(vk_access_token, vk_hash, vk_photo_id, vk_server_number, vk_version, vk_group_id, vk_user_id)

        post_comic_to_vk_wall(vk_version, vk_access_token, vk_group_owner_id, vk_save_id, comic_pic_comment)

    except ValueError: 
        print('Something went wrong, ValueError raised')

    finally:
        os.remove('comic.png')


if __name__ == '__main__':
    main()
