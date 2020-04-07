import flask
import time
import secrets
from data import db_session
from data.table import User, Token, UsedEmail, Chat
from flask import jsonify, request
from tokens import generate, send, check_token
from hashlib import sha512

blueprint = flask.Blueprint('main_api', __name__, 
                            template_folder='api_templates')


@blueprint.route('/api/complete_registration', methods=['POST'])
def create_user():
    '''Confirms registration by token'''
    if not request.json:
        return jsonify({'error': 'Empty reuqest'})
    
    elif not all(key in request.json for key in
                 ['hashed_email', 'password', 'public_key', 'token', 'hashed_login']):
        print(request.json)
        return jsonify({'error': 'Bad request'})

    params = request.json

    session = db_session.create_session()

    accept = check_token(params['token'], params['hashed_email'])
    if not accept:
        return jsonify({'error': 'Token error'})

    login = params['hashed_login']
    password_salt = secrets.token_hex(16)
    password = sha512(str(params['password'] + password_salt).encode('utf-8')).hexdigest()
    public_key = params['public_key']

    exist_login = session.query(User).filter(User.login==login).first()
    if exist_login:
        return jsonify({'error': 'Login already exist'})

    username = "@" + secrets.token_hex(8)
    username_exist = session.query(User).filter(User.username==username).first()
    start_time = time.time()
    while True:
        if time.time() - start_time > 5:
            return jsonify({'error': 'Username timeout'})
        if username_exist:
            username = "@" + secrets.token_hex(8)
            username_exist = session.query(User).filter(User.username==username).first()
        else:
            break
    
    temp_user = User(login=login, username=username, password=password, password_salt=password_salt, public_key=public_key)
    session.add(temp_user)
    
    temp_mail = UsedEmail(email=params['hashed_email'])
    session.add(temp_mail)
    
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/initiate_registration', methods=['POST'])
def start_register():
    '''Initiates registration, sends a token'''
    if not request.json:
        return jsonify({'error': 'Empty reuqest'})
    
    elif not all(key in request.json for key in
                 ['email']):
        return jsonify({'error': 'Bad request'})
    
    session = db_session.create_session()
    
    email = request.json['email']
    hashed_email = sha512(email.encode('utf-8')).hexdigest()
    exist_user_email = session.query(UsedEmail).filter(UsedEmail==hashed_email).first()
    if exist_user_email:
        return jsonify({'error': 'Email already exist'})
    
    exist_register_email = session.query(Token).filter(Token.email==hashed_email).first()
    if exist_register_email:
        return jsonify({'error': 'Email is already registered'})
    
    token = generate()
    exist_token = session.query(Token).filter(Token.token==token).first()
    start_time = time.time()
    while True:
        if time.time() - start_time > 5:
            return jsonify({'error': 'Token timeout'})
        if exist_token:
            token = generate()
            exist_token = session.query(Token).filter(Token.token==token).first()
        else:
            break
    try:
        suc = send(token, email)
        if not suc:
            raise Exception
    except Exception:
        return jsonify({'error': 'Send error'})
    
    time_send = time.time()
    temp_user = Token(email=hashed_email, token=token, unix_time=time_send)
    session.add(temp_user)
    session.commit()
    
    return jsonify({'success': 'OK'})


@blueprint.route('/api/create_chat', methods=['POST'])
def create_chat():
    '''Creates a chat with user {user}'''
    if not request.json:
        return jsonify({'error': 'Empty reuqest'})
    
    elif not all(key in request.json for key in
                 ['login', 'password', 'user']):
        return jsonify({'error': 'Bad request'})
    params = request.json
    
    session = db_session.create_session()

    hashed_login = sha512(params['login'].encode('utf-8')).hexdigest()
    exist_user = session.query(User).filter(User.login==hashed_login).first()
    if not exist_user:
        return jsonify({'error': 'login/password is incorrect'})
    
    password_salt = exist_user.password_salt
    password = sha512(str(params['password'] + password_salt).encode('utf-8')).hexdigest()
    if password != exist_user.password:
        return jsonify({'error': 'login/password is incorrect'})

    if exist_user.username == params['user']:
        return jsonify({'error': 'Incorrect username'})

    exist_user2 = session.query(User).filter(User.username==params['user']).first()
    if not exist_user2:
        return jsonify({'error': 'Incorrect username'})

    exist_chat = session.query(Chat).filter(Chat.user1==exist_user.username, Chat.user2==params['user']).first()
    if exist_chat:
        return jsonify({'error': 'Chat already exists'})

    chat_id = secrets.token_hex(16)
    chat_id_exist = session.query(Chat).filter(Chat.chat_id==chat_id).first()
    start_time = time.time()
    while True:
        if time.time() - start_time > 5:
            return jsonify({'error': 'Chat id timeout'})
        if chat_id_exist:
            chat_id = secrets.token_hex(16)
            chat_id_exist = session.query(Chat).filter(Chat.chat_id==chat_id).first()
        else:
            break
    
    temp_chat1 = Chat(user1=exist_user.username, user2=params['user'], chat_id=chat_id)
    temp_chat2 = Chat(user1=params['user'], user2=exist_user.username, chat_id=chat_id)
    session.add(temp_chat1)
    session.add(temp_chat2)
    session.commit()
    
    return jsonify({'success': 'OK'})


@blueprint.route('/api/get_user_chats', methods=['GET'])
def get_user_chats():
    '''Returns user chats'''
    if not request.json:
        return jsonify({'error': 'Empty reuqest'})
    
    elif not all(key in request.json for key in
                 ['login', 'password']):
        return jsonify({'error': 'Bad request'})
    params = request.json
    
    session = db_session.create_session()

    hashed_login = sha512(params['login'].encode('utf-8')).hexdigest()
    exist_user = session.query(User).filter(User.login==hashed_login).first()
    if not exist_user:
        return jsonify({'error': 'login/password is incorrect'})
    
    password_salt = exist_user.password_salt
    password = sha512(str(params['password'] + password_salt).encode('utf-8')).hexdigest()
    if password != exist_user.password:
        return jsonify({'error': 'login/password is incorrect'})

    chats = session.query(Chat).filter(Chat.user1==exist_user.username).all()
    out = []
    for chat in chats
        dic = {'username': chat.user2, 'chat_id': chat.chat_id}
        out.append(dic)
    return jsonify({'success': 'OK', 'chats': out})
