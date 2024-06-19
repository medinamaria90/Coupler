from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv
import os
import datetime

from config_production import Config as Config_prod
from config_local import Config as Config_loc

load_dotenv()
production = os.getenv("PRODUCTION")

app = Flask(__name__)
if production == "False":
    config = Config_loc()
    app.config.from_object(Config_loc)
    redirect_uri = os.getenv("REDIRECT_URI_LOCAL")
if production == "True":
    config = Config_prod()
    app.config.from_object(Config_prod)
    redirect_uri = os.getenv("REDIRECT_URI_PROD")
app.secret_key = config.set_secret_key()
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
db = config.create_db_alchemy(app)
app.config.update(config.set_secret_key())
app.config.update(config.debug())

# Mail confif
app.config.update(config.mail_settings())
mail = Mail(app)
now = datetime.datetime.now()
current_date = now.date()
current_year = now.year
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
