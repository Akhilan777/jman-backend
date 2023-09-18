import os
from dotenv import load_dotenv

load_dotenv()
base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "This_must_be_changed"
    SQLALCHEMY_DATABASE_URI = os.getenv("ELEPHANTSQL_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ML_MODEL_URI = os.path.join(base_dir, 'models\\accident_prediction_model.pkl')
    