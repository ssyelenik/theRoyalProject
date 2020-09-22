import os

basedir = os.path.abspath(
     os.path.dirname(__file__)
)

class Config:
    pass

class DevConfig(Config):
    SECRET_KEY = "arandomsecretkey"
    SQLALCHEMY_DATABASE_URI= "sqlite:///" + os.path.join(basedir, "app.db")
    UPLOADED_VIDEOS_DEST = os.path.join(basedir, 'uploads')
    MAIL_SERVER     = "smtp.gmail.com"
    MAIL_PORT       = 587
    MAIL_USE_TLS    = True
    MAIL_USE_SSL    = False
    MAIL_USERNAME   = 'ssyelenik'
    MAIL_PASSWORD   = 'mnisghh2'

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = "1265ewqtfsdaxvgz9287ynx918u2nx8172m301u9"

config = {
    "development": DevConfig,
    "production": ProdConfig
}