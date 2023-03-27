import os
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(find_dotenv(), override=True)
ENV = os.environ

# Version
V1_API_PREFIX = '/api/v1'

ENVIROMENT = ENV.get('ENVIROMENT')
if ENVIROMENT == "TESTING":
    MYSQL_DATABASE = ENV.get("MYSQL_DATABASE_TEST")
else:
    MYSQL_DATABASE = ENV.get("MYSQL_DATABASE")

MYSQL_HOST = ENV.get("MYSQL_HOST")
MYSQL_PORT = ENV.get("MYSQL_PORT")
MYSQL_USER = ENV.get("MYSQL_USER")
MYSQL_PASSWORD = ENV.get("MYSQL_PASSWORD")
#JWT
JWT_EXPIRY_DAY=15

#SecretKey
SECRET_KEY=ENV.get("SECRET_KEY")

APP_URL = ENV.get('APP_URL')
API_KEY = ENV.get('API_KEY', '')