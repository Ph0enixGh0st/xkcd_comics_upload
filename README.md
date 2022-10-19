# XKCD Comics Upload
The script downloads random xkcd comics and posts it into VK wall.

### How to install
Using GitHub CLI:
```bash
gh repo clone Ph0enixGh0st/xkcd_comics_upload
```
Or download and unpack ZIP file from GIT Hub repository: https://github.com/Ph0enixGh0st/xkcd_comics_upload.git

# Prerequisites
Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

In order to start using the script .env file is to be created first.
Add the following lines to .env file:

```
VK_CLIENT_ID=[your client_id here]
VK_GROUP_ID=[your group_id here]
VK_ACCESS_TOKEN=[your access_token here]
VERSION=5.131
```

To get 'GROUP_ID' please create your group here (https://vk.com/groups?tab=admin), or use you existing VK group.
Also you can check your 'VK_GROUP_ID' here: (https://regvk.com/id/)

Next step is to create your app here: (https://vk.com/dev).
Please choose 'standalone' option.

After creating the app now it is time to fetch 'VK_CLIENT_ID'.
Please use this link (https://vk.com/apps?act=manage), then press 'Manage' button:
![image](https://user-images.githubusercontent.com/108229516/196530786-6699de2e-bb7f-41b3-8244-c5492803f164.png)
Your 'CLIENT_ID' will be shown in browser address field:
![image](https://user-images.githubusercontent.com/108229516/196531198-9e7bd806-a8b8-49cd-abea-cb9fa4b04280.png)


Next goes 'VK_ACCESS_TOKEN'. It can be obtained here:
(https://vk.com/dev/implicit_flow_user)
Please include the following access rights: 'scope=photos,groups,wall,offline'
Remove 'redirect_uri' from your access request.

You will see the following picture after sending a request:
![image](https://user-images.githubusercontent.com/108229516/196532350-3f30c890-d105-42ed-b947-5eeeb7d3c44d.png)
Press 'Allow' and your 'VK_ACCESS_TOKEN' will be displayed in browser address field after 'access_token='.

Please note that 'VK_ACCESS_TOKEN' provied full access to your VK account, therefore please pay attention to not share it with unwanted persons.


# comics_upload.py and how to run it
The script downloads random comics from https://xkcd.com/ and uploads it to VK group wall.
When running the script a .png file will be created in the script folder. After the comics pic is uploaded the script will delete it automatically.

```bash
python comics_upload.py
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).