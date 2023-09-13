import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "This_must_be_changed"
    SQLALCHEMY_DATABASE_URI = os.getenv("ELEPHANTSQL_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False