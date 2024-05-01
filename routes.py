import os
import pathlib
import socket
from PIL import Image
from werkzeug.utils import secure_filename
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from oauthlib.oauth2 import WebApplicationClient
import flask_login
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify, send_from_directory
from database import DatabaseManager
from forms import MyProfile
from flask_wtf.csrf import CSRFProtect
import traceback
from config import app, mail, production, current_year, GOOGLE_CLIENT_ID, redirect_uri
from flask_socketio import SocketIO, send, join_room, leave_room

ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}
UPLOAD_DIRECTORY = f'user_uploads/profileimages'

csrf = CSRFProtect()

client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri=redirect_uri
)
# Creating the login manager so Flask can handle login, and logout
login_manager_app = flask_login.LoginManager(app)
socketio = SocketIO(app, logger=True)

@login_manager_app.user_loader
def load_user(couple_id):
    return DatabaseManager.get_pareja_by_id(couple_id)

def resize_image(input_path, output_path, size):
    with Image.open(input_path) as img:
        img.thumbnail(size)
        img.save(output_path)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return function()
        else:
            return abort(401)  # Authorization required
    return wrapper

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def renamePhotos(folder_path):
    files = os.listdir(folder_path)
    files.sort()
    numero_foto = 1
    for file_name in files:
        if file_name.startswith("photo"):
            # Obtener la extensión del archivo (por ejemplo, ".jpg")
            ext = os.path.splitext(file_name)[-1]
            # Construir el nuevo nombre de archivo secuencial
            new_name = f"photo{numero_foto}{ext}"
            # Obtener la ruta completa del archivo original y del nuevo archivo
            old_path = os.path.join(folder_path, file_name)
            new_path = os.path.join(folder_path, new_name)
            # Renombrar el archivo
            os.rename(old_path, new_path)
            numero_foto += 1

@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    else:
        return render_template("login.html")

@app.route("/login_with_google", methods=["GET", "POST"])
def login_with_google():
    authorization_url, state = flow.authorization_url(prompt="select_account")
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)
    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session["google_id"] = id_info.get("sub")
    session["google_email"] = id_info.get("email")
    session["google_photo"] = id_info.get("picture")
    session["google_name"] = id_info.get("given_name")
    current_user = DatabaseManager.get_pareja_by_email(email=session["google_email"])
    if current_user is None:
        DatabaseManager.create_profile(email=session["google_email"])
        current_user = DatabaseManager.get_pareja_by_email(email=session["google_email"])
        flask_login.login_user(current_user)
        return redirect("/profile")
    else:
        flask_login.login_user(current_user)
        return redirect("/profile")

@app.route("/login_for_testing", methods=["GET", "POST"])
def login_for_testing():
    if request.method == "POST":
        email = request.form.get('email')
        current_user = DatabaseManager.get_testing_pareja_by_email(email)
        if current_user == None:
            flash("Usuario incorrecto", "error")
            return redirect("/login")
        flask_login.login_user(current_user)
        if current_user:
            return redirect("/profile")
        else:
            flash("Usuario incorrecto", "error")
            return redirect("/login")

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    logged_user = DatabaseManager.get_pareja_by_email(email=current_user.email)
    #testing only
    #current_user = DatabaseManager.get_pareja_by_id(id=1)
    #logged_user = DatabaseManager.get_pareja_by_id(id=30)
    tags_list = DatabaseManager.get_tags_by_id(couple_id=logged_user.couple_id)
    profile_form = MyProfile(
        gender1=logged_user.gender1, gender2=logged_user.gender2
    )
    profile_photos = DatabaseManager.get_profile_photos(logged_user.couple_id)
    photos_count = len(profile_photos)
    if photos_count == 0:
        message = "Sube al menos una foto"
    else:
        message = None
    if request.method == "POST" and profile_form.validate_on_submit():
        form_data = profile_form.data
        # Llama a la función update_profile con los datos del formulario
        try:
            DatabaseManager.update_profile(logged_user.couple_id, **form_data)
            flash("Cambios del perfil guardados exitosamente", "success")
        except Exception as e:
            flash(f"Error al guardar cambios en el perfil: {str(e)}", "error")
        return redirect(url_for("profile"))
    return render_template(
        "profile.html",
        form=profile_form,
        photos=profile_photos,
        photos_count=photos_count,
        couple_directory=DatabaseManager.get_couple_directory(logged_user.couple_id),
        user = logged_user,
        message=message,
        tags_list=tags_list,
        couple_id=str(logged_user.couple_id),
        name1=logged_user.name1,
        name2=logged_user.name2,
        age1=logged_user.age1,
        age2=logged_user.age2,
        couple_description=logged_user.couple_description,
    )

@app.route('/serve_upload/<path:filename>')
def serve_upload(filename):
    user_uploads_folder = os.path.join(os.path.dirname(__file__))
    return send_from_directory(user_uploads_folder, filename)

@app.route("/buscar", methods=["GET", "POST"])
@login_required
def buscar():
    should_reload = request.args.get("reload")
    if "pareja_activa_id" in session and session["pareja_activa_id"] != current_user.couple_id:
        pareja_activa_id = session["pareja_activa_id"]
        pareja_activa = DatabaseManager.get_pareja_by_id(pareja_activa_id)
    else:
        pareja_activa = DatabaseManager.look_for_couple(current_user.couple_id)
        if pareja_activa:
            pareja_activa_id = pareja_activa.couple_id
            session["pareja_activa_id"] = pareja_activa.couple_id
    if pareja_activa== None:
        return render_template(
            "scrolling.html",
            pareja=None,
            should_reload=should_reload
        )
    else:
        pareja_activa_tags = DatabaseManager.get_tags_by_id(pareja_activa_id)
        profile_photos = DatabaseManager.get_profile_photos(pareja_activa_id)
        return render_template(
            "scrolling.html",
            pareja=pareja_activa,
            profile_photos=profile_photos,
            pareja_tags=pareja_activa_tags,
            enumerate=enumerate,
            should_reload=should_reload
        )

@app.route("/like_couple", methods=["GET", "POST"])
@login_required
def like_couple():
    if request.method== "POST":
        response_dict = DatabaseManager.like_couple(couple1_id=current_user.couple_id, couple2_id=session["pareja_activa_id"])
        match = response_dict["match"]
        session.pop("pareja_activa_id")
        return jsonify({'message': 'liked couple', 'match':match}), 200  # Respuesta exitosa

@app.route("/last_chat_read", methods=["POST", "GET"])
@login_required
def last_chat_read():
    data = request.get_json()
    match_id = data.get('matchId')
    if match_id is not None:
        DatabaseManager.chat_read(match_id = match_id)
        return jsonify({'resultado': 'correcto'})
    else:
        return jsonify({'resultado': 'incorrecto', 'mensaje': 'chat_id missing'})

@app.route("/message_read", methods=["POST", "GET"])
@login_required
def message_read():
    data = request.get_json()
    chat_id = data.get('chat_id')
    if chat_id is not None:
        DatabaseManager.chat_read(chat_id)
        return jsonify({'resultado': 'correcto'})
    else:
        return jsonify({'resultado': 'incorrecto', 'mensaje': 'chat_id missing'})

@app.route("/send_message", methods=["POST", "GET"])
@login_required
def send_message():
    data = request.get_json()
    # Verifica si 'message' está presente en los datos
    if 'message' in data:
        # Obtiene el contenido del mensaje
        message = data['message']
        match_id = data['match_id']
        first_message = data['first_message']
        DatabaseManager.save_chat(message, match_id=match_id, sender_id=current_user.couple_id, first_message=first_message)
        return jsonify({'resultado': 'correcto',}), 200  # Respuesta exitosa

@app.route("/retrieve_chats", methods=['GET'])
@login_required
def retrieve_chats():
    print(current_user.couple_id)
    # all the conversations
    match_id = request.args.get('match_id')
    (chat_list, chat_couple_id) = DatabaseManager.retrieve_chat(match_id=match_id, current_couple_id=current_user.couple_id)
    chat_dicts = []
    for chat in chat_list:
        chat_dict = {
            'sent': chat.sent,
            'message': chat.message,
            'date': chat.date,
            # Agrega más atributos si es necesario
        }
        chat_dicts.append(chat_dict)
    pareja = DatabaseManager.get_pareja_by_id(chat_couple_id)
    pareja_dict={}
    pareja_dict["name1"] = pareja.name1
    pareja_dict["name2"] = pareja.name2
    pareja_dict["age1"] = pareja.age1
    pareja_dict["age2"] = pareja.age2
    pareja_dict["couple_description"] = pareja.couple_description
    profile_photos = DatabaseManager.get_profile_photos(chat_couple_id)
    # And the couple info
    pareja_activa_tags = DatabaseManager.get_tags_by_id(chat_couple_id)
    return jsonify({'resultado': 'correcto', "chats":chat_dicts, "profile_photos":profile_photos, "pareja":pareja_dict, "pareja_activa_tags":pareja_activa_tags}), 200  # Respuesta exitosa

@app.route("/chats", methods=["GET", "POST"])
@login_required
def chats():
    matches = DatabaseManager.retrieve_matches(couple_id=current_user.couple_id)
    return render_template("chats.html", matches=matches, user_id =current_user.couple_id )

@app.route("/get_updated_chat_data", methods=["GET", "POST"])
@login_required
def get_updated_chat_data():
    matches = DatabaseManager.retrieve_matches(couple_id=current_user.couple_id)
    return matches

@app.route("/micuenta", methods=["GET", "POST"])
@login_required
def micuenta():
    return render_template("micuenta.html")

@app.route("/dislike_couple", methods=["GET", "POST"])
@login_required
def dislike_couple():
    if request.method== "POST":
        DatabaseManager.dislike_couple(couple1_id=current_user.couple_id, couple2_id=session["pareja_activa_id"])
        session.pop("pareja_activa_id")
        return jsonify({'message': 'Disliked couple'}), 200  # Respuesta exitosa

@login_required
@app.route('/cerrar_sesion', methods=['GET', 'POST'])
def cerrar_sesion():
    flask_login.logout_user()
    return redirect("/")

@app.route('/deleteImg', methods=['POST'])
def deleteImg():
    data = request.form.to_dict()
    photo_url = data.get("photoUrl")
    user_uploads_folder = os.path.join(os.path.dirname(__file__), photo_url)
    try:
        # Check if the file exists before attempting to delete it
        if os.path.exists(user_uploads_folder):
            os.remove(user_uploads_folder)  # Delete the file
            renamePhotos(folder_path=f"{user_uploads_folder[:-10]}")
            DatabaseManager.update_profile(current_user.couple_id)
            return jsonify(message="Image deleted successfully"), 200
        else:
            return jsonify(message="The image doesnt exist"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/addImg', methods=['POST'])
def addImg():
    try:
        route = request.form['photo_data']
        user_uploads_folder = os.path.join(os.path.dirname(__file__), route)
        if not os.path.exists(user_uploads_folder):
            os.makedirs(user_uploads_folder)
        # Obtén la lista de archivos en el directorio
        existing_files = os.listdir(user_uploads_folder)
        # Calcula el número de fotos en el directorio
        photo_count = len([f for f in existing_files if f.startswith('photo')])
        new_filename = f'photo{photo_count + 1}.jpg'
        uploaded_file = request.files['photo']
        file_path = os.path.join(user_uploads_folder, new_filename)
        with Image.open(uploaded_file) as img:
            img = img.convert('RGB')
            # Obtiene las dimensiones originales de la imagen
            width, height = img.size
            # Calcula las nuevas dimensiones para hacer la imagen más alta que ancha (por ejemplo, 1.25:2)
            new_height = int(width * 1.25)
            if new_height > height:
                new_height = height
                new_width = int(height / 1.25)
            else:
                new_width = width
            # Calcula las coordenadas de recorte para centrar la imagen
            left = (width - new_width) / 2
            top = (height - new_height) / 2
            right = (width + new_width) / 2
            bottom = (height + new_height) / 2
            # Realiza el recorte
            img = img.crop((left, top, right, bottom))
            # Redimensiona la imagen a un tamaño máximo de 800x800
            img.thumbnail((800, 800))
            # Guarda la imagen
            img.save(file_path)
        DatabaseManager.update_profile(current_user.couple_id)
        return jsonify({"message": "Imagen subida exitosamente", "filename": new_filename})
    except Exception as e:
        return (f"Error uploading file {str(e)}")

# SocketIO handling server messages
def get_user_matches():
    matches = DatabaseManager.retrieve_matches_ids(couple_id=current_user.couple_id)
    return matches

# Mantener un diccionario para rastrear qué usuarios están en qué salas
@socketio.on('get_user_rooms')
def get_user_rooms():
    # Utiliza `socket.rooms` para obtener las salas a las que el usuario está unido
    user_rooms = list(socket.rooms)
    # Elimina la sala de conexión por defecto
    user_rooms.remove(request.sid)
    socketio.emit('user_rooms', user_rooms)

room_users = {}
@socketio.on('join_rooms')
def join_rooms():
    user_matches = get_user_matches()
    rooms = []  # Define una lista para almacenar las salas
    for match_id in user_matches:
        room = int(match_id)
        join_room(room)
        if match_id in room_users:
            room_users[match_id].add(current_user.couple_id)
        else:
            room_users[match_id] = {current_user.couple_id}
        rooms.append(match_id)  # Agrega el nombre de la sala a la lista 'rooms'
    for room, users in room_users.items():
        socketio.emit('get_rooms', rooms, room=request.sid)  # Emitir la lista de salas 'rooms'

@socketio.on('leave_rooms')
def leave_rooms():
    for room, users in room_users.items():
        if current_user.id in users:
            leave_room(room)
            users.remove(current_user.id)

@socketio.on('message')
def message(data):
    if 'message' in data:
        # Obtiene el contenido del mensaje
        message = data.get('message', '')  # Obtener el mensaje del objeto data
        match_id = data.get('match_id', '')
        first_message = data.get('first_message', '')
        if DatabaseManager.is_user_allowed_to_access_room(couple_id = current_user.couple_id, match_id = match_id):
            data["sender_id"] = current_user.couple_id
            DatabaseManager.save_chat(message, match_id=match_id, sender_id=data["sender_id"],
                                      first_message=first_message)
            room = int(match_id)
            socketio.emit('message', data, room=room)

if __name__ == '__main__':
    socketio.run(app)
    # host = "127.0.0.9"
