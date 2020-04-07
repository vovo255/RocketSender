import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header
from random import randint
from data import db_session
from data.table import Token


def generate():
    token = randint(1000000, 9999999)
    return str(token)


def send(token, mail):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login('senderrocket@gmail.com','9TivPvXfjq8gAT9')
    msg = MIMEText(f'Ваш токен: {token}', 'plain', 'utf-8')
    msg['Subject'] = Header('Подтверждение регистрации', 'utf-8')
    msg['From'] = 'senderrocket@gmail.com'
    msg['To'] = mail
    try:
        smtpObj.sendmail(msg['From'], mail, msg.as_string())
    except Exception:
        smtpObj.quit()
        return False
    smtpObj.quit()
    return True


def check_token(token, hashed_email):
    session = db_session.create_session()
    token_obj = session.query(Token).filter(Token.token==token).first()
    if not token_obj:
        return False
    token_email = token_obj.email
    live_time = token_obj.unix_time
    if time.time() - live_time > 60:
        return False
    if token_email != hashed_email:
        return False
    return True
