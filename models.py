from flask_login import UserMixin
import datetime
from config import db


class Couples(db.Model, UserMixin):
    __tablename__ = 'couples'
    now = datetime.datetime.now()
    couple_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name1 = db.Column(db.String(105), unique=True, nullable=False)
    name2 = db.Column(db.String(105), unique=True, nullable=False)
    age1 = db.Column(db.Integer, unique=True, nullable=False)
    age2 = db.Column(db.Integer, unique=True, nullable=False)
    gender1 = db.Column(db.String(100), unique=True, nullable=False)
    gender2 = db.Column(db.String(100), unique=True, nullable=False)
    couple_description = db.Column(db.String(1500), unique=True, nullable=False)
    email = db.Column(db.Integer, unique=True, nullable=False)
    date_profile = db.Column(db.DateTime, default=now)
    folder = db.Column(db.String(105), unique=True, nullable=False)
    number_of_photos = db.Column(db.Integer, unique=True, nullable=False, default=0)

    def get_id(self):
        return self.couple_id
    def to_dict(self):
        attributes = [
            "couple_id",
            "name1",
            "name2",
            "age1",
            "age2",
            "gender1",
            "gender2",
            "couple_description",
            "email",
            "date_profile",
            # Add more attributes as needed
        ]

        data = {attr: getattr(self, attr) for attr in attributes}
        return data

class Chats(db.Model, UserMixin):
    __tablename__ = 'chats'
    chats_id = db.Column(db.Integer, primary_key=True)
    match_id_fk = db.Column(db.Integer)
    couple_id_fk= db.Column(db.Integer)
    message= db.Column(db.String(250))
    date= db.Column(db.DateTime)
    read= db.Column(db.Boolean)

class Labelcouple(db.Model, UserMixin):
    __tablename__ = 'labelcouple'
    labelcouple_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    couple_id_fk = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(45), unique=True, nullable=False)


class Matches(db.Model, UserMixin):
    __tablename__ = 'matches'
    now = datetime.datetime.now()
    matches_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fk_couple1_id = db.Column(db.Integer)
    fk_couple2_id = db.Column(db.Integer)
    date_match= db.Column(db.DateTime, default=now)
    conversation_opened= db.Column(db.Boolean)


class Couples_prematching(db.Model, UserMixin):
    __tablename__ = 'couples_prematching'
    couples_prematching_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    couple1_id = db.Column(db.Integer)
    couple2_id = db.Column(db.Integer)
    compatibility = db.Column(db.Float)
    showed = db.Column(db.Integer)
    like = db.Column(db.Boolean)


class Mensajes_html:
    def __init__(self, fecha, remitente, contenido, other_couple_names, folder, conversation_id, date_sent):
        self.fecha = fecha
        self.remitente = remitente
        self.contenido = contenido
        self.date_sent = date_sent
        self.other_couple_names = other_couple_names
        self.folder = folder
        self.conversation_id = conversation_id


class Chat_html:
    def __init__(self, date, sent, message):
        self.date = date
        self.sent = sent
        self.message = message
class Match_html:
    def __init__(self, name1, name2, age1, age2, conversation_opened,folder, match_id, match_date, match_date_string,
                 last_msj_content, last_msj_date_string, last_msj_date_sent, last_msj_read, last_chat_id,
                 last_msj_by):
        self.name1 = name1
        self.name2 = name2
        self.age1 = age1
        self.age2 = age2
        self.conversation_opened = conversation_opened
        self.folder = folder
        self.match_id = match_id
        self.match_date = match_date
        self.match_date_string = match_date_string
        self.last_msj_content = last_msj_content
        self.last_msj_date_string = last_msj_date_string
        self.last_msj_date_sent = last_msj_date_sent
        self.last_msj_read = last_msj_read
        self.last_msj_by = last_msj_by
        self.last_chat_id = last_chat_id


class Use_register(db.Model, UserMixin):
    __tablename__ = 'use_register'
    id = db.Column(db.Integer, primary_key=True)
    pass
    # Campos de la tabla Conexiones



