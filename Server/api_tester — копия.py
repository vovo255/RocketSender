from requests import post, get
from hashlib import sha512
from random import randint

login = 'user1'
password = '9hwyOwYc'
email = 'bratezvova@mail.ru'




def start_reg():
    r = post('http://35.209.84.85:8080/api/initiate_registration', json={'email': email})
    print(r.json())
    print(r.status_code)


def complete_reg():
    token = input()
    register = post('http://35.209.84.85:8080/api/complete_registration', json={'email': email,
                                                                             'password': password,
                                                                             'public_key': str(randint(999999, 999999999)),
                                                                             'token': token,
                                                                             'login': login})
    print(register.json())

def create_chat(login, password, username):
    r = post('http://35.209.84.85:8080/api/create_chat', json={'login': login, 'password': password, 'user': username})
    print(r.json())
    print(r.status_code)


def get_user_data(login, password):
    r = get('http://35.209.84.85:8080/api/get_user_data', json={'login': login, 'password': password})
    print(r.json())
    print(r.status_code)

#create_chat('user1', '1234', '@2ebcfb8953f75278')
start_reg()
complete_reg()
#get_user_data(login, password)
