import requests
import shutil

admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzExMjIyMzc0LCJpYXQiOjE3MDg2MzAzNzQsImp0aSI6ImRlNjRmOTU1MzExMTQ4ZmRiNDA1Yjg2MjBjMDFkZGI4IiwidXNlcl9pZCI6MX0.2P2W5RuZGw8rsm4tXI45cSrAZwPtXpoQAH5ZnRgK5FU"
emil = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4NjI5Njk3LCJpYXQiOjE3MDg2MjYwOTcsImp0aSI6IjJjNjQyOGYyYWNjYTRlZmRhMTBkNmIzNzI4ODNkNDQzIiwidXNlcl9pZCI6Mn0.5SlQNVMW216XrxKkKvRtm-ggUDAmi8jk_Bfdrv9y9KU"
emil2 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzExMjI4NjIwLCJpYXQiOjE3MDg2MzY2MjAsImp0aSI6ImJjNTlhNGIwODFkODRjNzdiMzhmYTQzMmIyZWYyZTdiIiwidXNlcl9pZCI6M30.iJ00D-qIwMXmKRINWT1ZQj8rwOqgv8CUp_m2eSfWvV0"
emil3 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzExMjIwMDczLCJpYXQiOjE3MDg2MjgwNzMsImp0aSI6ImRkYzRkZmY3MzhjMzRjMzY5MDVkZDZhZTFjZmIwNzEzIiwidXNlcl9pZCI6NH0.zd9cymuHPtv-K4eSyPM-j6ovpTZnLeTo1Fihl8Rmqqg"
emil5 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzExMjMxMDU0LCJpYXQiOjE3MDg2MzkwNTQsImp0aSI6IjQ5NWVlNjBlYWY1NzQ5ZGViMTU5YjA3ZGQzNGQ2NDZiIiwidXNlcl9pZCI6Nn0.jaB4NFYo9Br8OqnTqnrH0kTgEnJC3Fci9O13XDL8xwE"

# Admin pass = admin
# Emil and Emil2 pass = evetn1232
# print(dir(response))


def create_user():
    data = {
        'username': 'Emil5',
        'full_name': 'Emil5',
        'email': 'emil5@ya.ru',
        'password': 'evetn1232',
    }
    response = requests.post('http://127.0.0.1:8000/api/v1/users/', data=data)
    print(response.content)


def get_user_info_jwt():
    headers = {
        'Authorization': f'Bearer {admin_token}',
    }
    response = requests.get('http://127.0.0.1:8000/api/v1/users/1/', headers=headers)
    print(response.content)


def get_user_info_no_jwt():
    response = requests.get('http://127.0.0.1:8000/api/v1/users/2/')
    print(response.content)


def create_file():
    files = {'file_entity': open('testfile.txt', 'rb')}
    headers = {
        'Authorization': f'Bearer {emil2}',
    }
    response = requests.post('http://127.0.0.1:8000/api/v1/files/', files=files, headers=headers)
    print(response.content)


def change_file_description():
    data = {
        'description': '11111'
    }
    headers = {
        'Authorization': f'Bearer {emil2}',
    }
    response = requests.put('http://127.0.0.1:8000/api/v1/files/update/7/', data=data, headers=headers)
    print(response.content)


def change_file_freefile():
    data = {
        'free_file': False
    }
    headers = {
        'Authorization': f'Bearer {emil2}',
    }
    response = requests.put('http://127.0.0.1:8000/api/v1/files/update/7/', data=data, headers=headers)
    print(response.content)


def get_files_list():
    headers = {
        'Authorization': f'Bearer {emil3}',
    }
    response = requests.get('http://127.0.0.1:8000/api/v1/files/', headers=headers)
    print(response.content)


def delete_file():
    headers = {
        'Authorization': f'Bearer {emil3}',
    }
    response = requests.delete('http://127.0.0.1:8000/api/v1/files/delete/5/', headers=headers)
    print(response, response.content)


def download_file():
    headers = {
        'Authorization': f'Bearer {emil2}',
    }
    response = requests.get('http://127.0.0.1:8000/api/v1/download/7/', headers=headers, stream=True)
    with open('f.txt', 'wb') as new_f:
        shutil.copyfileobj(response.raw, new_f)
    print(response, response.content)


# def set_free_file():
#     headers = {
#         'Authorization': f'Bearer {emil3}',
#     }
#     data = {
#         'free_file': True
#     }
#     response = requests.put('http://127.0.0.1:8000/api/v1/freefile/3/', data=data, headers=headers)
#     print(response.content)


def delete_user():
    headers = {
        'Authorization': f'Bearer {admin_token}',
    }
    response = requests.delete('http://127.0.0.1:8000/api/v1/users/delete/5/', headers=headers)
    print(response.content)


def download_free_file():
    response = requests.get('http://127.0.0.1:8000/api/v1/files/freefile/7/', stream=True)
    with open('f.txt', 'wb') as new_f:
        shutil.copyfileobj(response.raw, new_f)
    print(response, response.content)



# create_user()
# get_user_info_jwt()
# get_user_info_no_jwt()
# create_file()
# change_file_description()
# change_file_freefile()
# get_files_list()
# delete_file()
download_file()
# set_free_file()
# delete_user()
download_free_file()