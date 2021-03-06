from .db_session import SqlAlchemyBase
import datetime
import sqlalchemy


class User(SqlAlchemyBase):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    password_salt = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    public_key = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)

    def __str__(self):
        return f"User({self.login}, {self.password})"


class Token(SqlAlchemyBase):
    __tablename__ = "tokens"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    token = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    unix_time = sqlalchemy.Column(sqlalchemy.Float, unique=False, nullable=False)


class UsedEmail(SqlAlchemyBase):
    __tablename__ = "used_emails"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)   


class Chat(SqlAlchemyBase):
    __tablename__ = "chats"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user1 = sqlalchemy.Column(sqlalchemy.String, unique=False, nullable=False)
    user2 = sqlalchemy.Column(sqlalchemy.String, unique=False, nullable=False)
    chat_id = sqlalchemy.Column(sqlalchemy.String, unique=False, nullable=False)


class Message(SqlAlchemyBase):
    __tablename__ = 'messages'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String, unique=False, nullable=False)
    data = sqlalchemy.Column(sqlalchemy.String, unique=False, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, unique=False, nullable=True)
    signature = sqlalchemy.Column(sqlalchemy.String, unique=False, nullable=False)
    unix_time = sqlalchemy.Column(sqlalchemy.Float, unique=False, nullable=False)
    chat_id = sqlalchemy.Column(sqlalchemy.String, unique=False, nullable=False)
    viewed = sqlalchemy.Column(sqlalchemy.Boolean, unique=False, nullable=False)
    sended_by = sqlalchemy.Column(sqlalchemy.String, unique=False, nullable=False)
    keys = sqlalchemy.Column(sqlalchemy.String, unique=False, nullable=False)
