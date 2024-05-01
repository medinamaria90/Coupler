from models import db, Couples, Labelcouple, Use_register, Chats, \
    Matches, Couples_prematching, Mensajes_html, Chat_html, Match_html
import os
from operator import attrgetter
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import not_, and_, or_, func, desc

couples_fieldnames = ["name1", "name2", "age1", "age2", "gender1", "gender2", "couple_description"]
photos_fieldnames = ["photo1","photo2","photo3","photo4","photo5","photo6"]
UPLOAD_DIRECTORY = f'user_uploads/profileimages'
class DatabaseManager:
    def __init__(self):
        pass  # Puedes inicializar cosas aquí si es necesario

    @classmethod
    def calculate_compatibility(cls, couple1id,couple2id):
        return 1

    @classmethod
    def is_there_a_match(cls, couple1id, couple2id):
        # Modificamos la consulta para utilizar exists()
        match_exists = db.session.query(
            db.session.query(Matches).filter(
                or_(
                    (Matches.fk_couple1_id == couple1id) & (Matches.fk_couple2_id == couple2id),
                    (Matches.fk_couple1_id == couple2id) & (Matches.fk_couple2_id == couple1id)
                )
            ).exists()
        ).scalar()
        return match_exists

    @classmethod
    def get_couples_prematching(cls, couple1_id):
        # Obtener todos los IDs de parejas mostradas anteriormente
        showed_couple_ids = db.session.query(Couples_prematching.couple2_id).filter(
            and_(
                Couples_prematching.couple1_id == couple1_id,
                Couples_prematching.showed > 0
            )
        ).all()

        # Extraer los IDs de las parejas mostradas
        showed_couple_ids = [couple.couple2_id for couple in showed_couple_ids]

        # Obtener nuevos candidatos que no se han mostrado anteriormente
        new_couples = db.session.query(Couples).filter(
            ~Couples.couple_id.in_(showed_couple_ids),
            Couples.couple_id != couple1_id
        ).limit(50).all()

        if new_couples:
            is_there_new_couples = False
            for couple in new_couples:
                couple2id = couple.couple_id
                if DatabaseManager.is_there_a_match(couple1id=couple1_id, couple2id=couple2id):
                    pass
                else:
                    compatibility = DatabaseManager.calculate_compatibility(couple1id=couple1_id, couple2id=couple2id)
                    prematching = Couples_prematching(couple1_id=couple1_id, couple2_id=couple2id, compatibility=compatibility, showed=0)
                    db.session.add(prematching)
                    db.session.commit()
                    is_there_new_couples = True
            if not is_there_new_couples:
                return None

        # Obtener la próxima pareja para mostrar
        couple_to_show = db.session.query(Couples_prematching.couple2_id).filter(
            Couples_prematching.couple1_id == couple1_id
        ).order_by(Couples_prematching.showed).first()
        if couple_to_show:
            couple = DatabaseManager.get_pareja_by_id(id=couple_to_show.couple2_id)
        return couple


    @classmethod
    def look_for_couple(cls, couple_id):
        couple = DatabaseManager.get_couples_prematching(couple1_id=couple_id)
        return couple

    @classmethod
    def look_for_conversation_by_couples_ids(cls, couple1_id, couple2_id):
        conversation = db.session.query(Conversations).filter(
            and_(Conversations.couple1_id_fk == couple1_id, Conversations.couple2_id_fk == couple2_id)).first()
        if conversation:
            pass
        else:
            conversation = db.session.query(Conversations).filter(
                and_(Conversations.couple1_id_fk == couple2_id, Conversations.couple2_id_fk == couple1_id)).first()
        return conversation

    @classmethod
    def look_for_prematches_by_couples_ids(cls, couple1_id, couple2_id):
        prematches=[]
        prematch = db.session.query(Couples_prematching).filter(
            and_(Couples_prematching.couple1_id == couple1_id, Couples_prematching.couple2_id == couple2_id)).first()
        if prematch:
            prematches.append(prematch)
        prematch = db.session.query(Couples_prematching).filter(
            and_(Couples_prematching.couple1_id == couple2_id, Couples_prematching.couple2_id == couple1_id)).first()
        if prematch:
            prematches.append(prematch)
        return prematches

    @classmethod
    def calculate_days(cls, first_date):
        last_date = datetime.now()
        diferencia = func.datediff(last_date, first_date)
        # Obtiene el número de días de diferencia
        dias = db.session.scalar(diferencia)
        if dias == 0:
            date_string = "hoy"
        elif dias == 1:
            date_string = "ayer"
        else:
            date_string = f"hace {dias} días"

        return date_string

    @classmethod
    def sql_date_to_datetime(cls, sql_date):
        datetime_date = sql_date.replace(tzinfo=None)
        return datetime_date

    @classmethod
    def get_the_other_couple(cls, couple_id,match=None):
        if match:
            if match.fk_couple1_id == couple_id:
                couple = DatabaseManager.get_pareja_by_id(id=match.fk_couple2_id)
            elif match.fk_couple2_id == couple_id:
                couple = DatabaseManager.get_pareja_by_id(id=match.fk_couple1_id)
        return couple

    @classmethod
    def chat_read(cls, chat_id=None, match_id=None):
        if chat_id:
            db.session.query(Chats).filter(Chats.chats_id == chat_id).update({Chats.read: True})
        if match_id:
            db.session.query(Chats).filter(Chats.match_id_fk == match_id).update({Chats.read: True})
        db.session.commit()

    @classmethod
    def retrieve_matches(cls, couple_id):
        # Filtro entre todos los matches, buscando que coincida el id de la pareja
        matches = db.session.query(Matches).filter(or_(Matches.fk_couple1_id == couple_id, Matches.fk_couple2_id == couple_id))
        if matches:
            couple_matches = []
            for match in matches:
                couple = DatabaseManager.get_the_other_couple(couple_id = couple_id, match=match)
                match_date_sent = DatabaseManager.sql_date_to_datetime(sql_date=match.date_match)
                if match.conversation_opened !=0:
                    last_msj = Chats.query.filter_by(match_id_fk=match.matches_id).order_by(Chats.date.desc()).first()
                    if last_msj:
                        match_date_string = None
                        last_msj_content = last_msj.message
                        last_msj_by = last_msj.couple_id_fk
                        if last_msj_by !=couple_id:
                            last_msj_read = last_msj.read
                        else:
                            last_msj_read = True
                        last_chat_id = last_msj.chats_id
                        last_msj_date_sent = DatabaseManager.sql_date_to_datetime(sql_date=last_msj.date)
                        date_string = DatabaseManager.calculate_days(last_msj_date_sent)
                else:
                    last_msj_content=None
                    last_msj_date_sent = None
                    match_date_string = DatabaseManager.calculate_days(match_date_sent)
                match = Match_html(last_msj_by= last_msj_by, last_chat_id= last_chat_id, last_msj_read= last_msj_read, match_date_string=match_date_string, last_msj_date_sent= last_msj_date_sent, last_msj_date_string=date_string,last_msj_content=last_msj_content,name1=couple.name1, name2=couple.name2, age1=couple.age1, age2=couple.age2, folder=DatabaseManager.get_couple_directory(couple.couple_id), conversation_opened=match.conversation_opened, match_date=match_date_sent, match_id=match.matches_id)
                couple_matches.append(match)

            def custom_sort_key(match):
                if match.last_msj_date_sent is not None:
                    return (match.last_msj_date_sent, match.match_date)
                else:
                    return (match.match_date,)
            couple_matches = sorted(couple_matches, key=custom_sort_key, reverse=True)
        return couple_matches

    @classmethod
    def retrieve_matches_ids(cls, couple_id):
        # Filtro entre todos los matches, buscando que coincida el id de la pareja
        matches = db.session.query(Matches.matches_id).filter(
            or_(Matches.fk_couple1_id == couple_id, Matches.fk_couple2_id == couple_id)
        ).all()
        # Inicializa una lista vacía para almacenar los IDs de los matches
        matches_list = []
        # Itera sobre los resultados y agrega los IDs a la lista
        for match_id, in matches:
            matches_list.append(match_id)

        return matches_list

    @classmethod
    def is_user_allowed_to_access_room(cls, couple_id, match_id):
        result = db.session.query(Matches).filter(
            (Matches.matches_id == match_id) &
            ((Matches.fk_couple1_id == couple_id) | (Matches.fk_couple2_id == couple_id))
        ).first()
        return result is not None

    @classmethod
    def retrieve_chat(cls, match_id, current_couple_id):
        # Todas las conversaciones del usuario
        chats =  db.session.query(Chats).filter_by(match_id_fk = match_id).order_by(Chats.date.asc()).all()
        match = DatabaseManager.get_match_by_match_id(match_id=match_id)
        couple2 = DatabaseManager.get_the_other_couple(couple_id=current_couple_id, match=match)
        chats_list=[]
        for chat in chats:
            if chat.couple_id_fk == current_couple_id:
                sent= True
            else:
                sent=False
            chat_html = Chat_html(date=chat.date, sent=sent,message=chat.message)
            chats_list.append(chat_html)
        return (chats_list, couple2.couple_id)

    @classmethod
    def like_couple(cls, couple1_id, couple2_id):
        couple_prematching_row = db.session.query(Couples_prematching).filter_by(couple1_id=couple1_id,
                                                                         couple2_id=couple2_id).first()
        if couple_prematching_row:
            couple_prematching_row.showed += 1
            couple_prematching_row.like = 1
            db.session.commit()
            # Did the couple like you back?
            couple_to_match = db.session.query(Couples_prematching).filter_by(couple1_id=couple2_id,
                                                                             couple2_id=couple1_id, like=1).first()
            if couple_to_match:
                match = DatabaseManager.is_there_a_match(couple1id=couple1_id, couple2id=couple2_id)
                # Esto es preventivo. No debería estar en couples prematching si hay ya match, pues se borra
                if match is None:
                    # No existing match found, so you can add a new match
                    match = Matches(fk_couple1_id=couple1_id, fk_couple2_id=couple2_id, date_match= datetime.now(), conversation_opened=0)
                    db.session.add(match)
                    db.session.commit()
                # borro los prematches
                prematches= db.session.query(Couples_prematching).filter(
                    or_(
                        (Couples_prematching.couple1_id==couple1_id) & (Couples_prematching.couple2_id==couple2_id),
                        (Couples_prematching.couple2_id==couple1_id) & (Couples_prematching.couple1_id==couple2_id)
                    )
                ).all()

                for prematch in prematches:
                    db.session.delete(prematch)
                    db.session.commit()
                return {"like":True, "match":True}
            else:
                return {"like": True, "match":False}
            
    @classmethod
    def dislike_couple(cls, couple1_id, couple2_id):
        couple_to_dislike = db.session.query(Couples_prematching).filter_by(couple1_id=couple1_id,
                                                                    couple2_id=couple2_id).first()
        if couple_to_dislike:
            couple_to_dislike.showed += 1
            couple_to_dislike.like = 0
            db.session.commit()
            return {"dislike": True}

    @classmethod
    def save_chat(cls, message, match_id, sender_id, first_message):
        print("In save chat")
        fecha_actual = datetime.now()
        new_chat = Chats(match_id_fk=match_id, couple_id_fk=sender_id, message=message,
                                         date=fecha_actual, read=False)
        db.session.add(new_chat)
        db.session.commit()
        if first_message == "true":
            match= DatabaseManager.get_match_by_match_id(match_id=match_id)
            match.conversation_opened=1
            db.session.commit()
            print("Message saved prob")
        return "correct"

    @classmethod
    def get_couple_directory(cls, couple_id):
        couple_directory = f'{UPLOAD_DIRECTORY}/{couple_id}'
        return couple_directory

    @classmethod
    def get_profile_photos(cls, couple_id):
        profile_photos = []
        couple_directory = DatabaseManager.get_couple_directory(couple_id)
        os.makedirs(couple_directory, exist_ok=True)  # Create the directory if it doesn't exist
        for image in sorted(os.listdir(couple_directory)):
            if image.lower().endswith(('.jpg', '.jpeg', '.png')):
                full_path = f"{couple_directory}/{image}"
                profile_photos.append(full_path)
        return profile_photos

    @classmethod
    def create_profile(cls, email):
        pareja = Couples(email=email)
        db.session.add(pareja)
        db.session.commit()

    @classmethod
    def upload_tag(cls, couple_id,labels):
        # Primero eliminamos todas las etiquetas
        Labelcouple.query.filter_by(couple_id_fk=couple_id).delete()
        db.session.commit()
        for label in labels:
            couple_tag = Labelcouple(couple_id_fk=couple_id, label=label )
            db.session.add(couple_tag)
            db.session.commit()\

    @classmethod
    def update_profile(cls, couple_id, **kwargs):
        # Busca la pareja
        pareja = db.session.query(Couples).filter_by(couple_id=couple_id).first()
        # Si hay kwargs, es porque hay tags
        if kwargs:
            for key, value in kwargs.items():
                if key == 'tags':
                    DatabaseManager.upload_tag(couple_id, labels=value)
                else:
                    setattr(pareja, key, value)

        number_of_photos = len(DatabaseManager.get_profile_photos(couple_id))
        pareja.number_of_photos=number_of_photos
        # POR AHORA EL DIRECTORIO LO CALCULO CON LA LOGICA INTERNA, pero esto puede cambiar en el futuro
        # pareja.folder=DatabaseManager.get_couple_directory(pareja.couple_id)
        db.session.commit()

    @classmethod
    def get_pareja_by_email(cls, email):
        couple =  Couples.query.filter_by(email=email).first()
        if couple == None:
            return None
        else:
            return couple

    @classmethod
    def get_pareja_by_id(cls, id):
        couple =  Couples.query.filter_by(couple_id=id).first()
        if couple == None:
            return None
        else:
            return couple
        
    @classmethod
    def get_testing_pareja_by_email(cls, email):
        testing_mails = ["testing@user.com", "testing2@user.com", "testing3@user.com"]
        couple = None
        if (email == testing_mails[0]):
            couple =  cls.get_pareja_by_id(1)
        elif (email == testing_mails[1]):
            couple =  cls.get_pareja_by_id(2)
        elif (email == testing_mails[2]):
            couple =  cls.get_pareja_by_id(3)
        if couple == None:
            return None
        else:
            return couple
  
    @classmethod
    def get_match_by_match_id(cls, match_id):
        match = db.session.query(Matches).filter_by(matches_id=match_id).first()
        return match
    @classmethod
    def get_tags_by_id(cls, couple_id):
        tags = Labelcouple.query.filter_by(couple_id_fk=couple_id).all()
        tags_list = []
        for tag in tags:
            tags_list.append(tag.label)
        if tags == None:
            return None
        else:
            return tags_list

    # Otras funciones para obtener información de las demás tablas

    @classmethod
    def update_registro_uso(cls):
        # Actualiza el registro de uso y realiza las operaciones necesarias
        pass
