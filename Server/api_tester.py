from requests import post
from hashlib import sha512
from random import randint

login = sha512('user2'.encode('utf-8')).hexdigest()
password = '1234'
mail = 'bratezvova21@mail.ru'
email = sha512(mail.encode('utf-8')).hexdigest()



def start_reg():
    r = post('http://127.0.0.1:8080/api/initiate_registration', json={'email': mail})
    print(r.json())  


def complete_reg():
    token = input()
    register = post('http://127.0.0.1:8080/api/complete_registration', json={'hashed_email': email,
                                                                             'password': password,
                                                                             'public_key': str(randint(999999, 999999999)),
                                                                             'token': token,
                                                                             'hashed_login': login})
    print(register.json())

def create_chat(login, password, username):
    r = post('http://127.0.0.1:8080/api/create_chat', json={'login': login, 'password': password, 'user': username})
    print(r.json())


create_chat('user1', '1234', '@2ebcfb8953f75278')
#start_reg()
#complete_reg()
