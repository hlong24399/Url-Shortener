import os



class Config(object):

    CONFIG_URL = os.environ.get("CONF_URL")
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CLIENT_ID= "9896625773-58htbba524eo6aoiqeec046ko9mohpok.apps.googleusercontent.com" or os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET= "MtbjjO4_QXgs1cSLqJ-B_hWP" or  os.environ.get("GOOGLE_CLIENT_SECRET")

    print(CONFIG_URL)
    print(SECRET_KEY)
    print(SQLALCHEMY_DATABASE_URI)
    print(SQLALCHEMY_TRACK_MODIFICATIONS)
    print(GOOGLE_CLIENT_ID)
    print(GOOGLE_CLIENT_SECRET)
